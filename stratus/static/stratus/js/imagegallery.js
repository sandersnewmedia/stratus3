(function(Backbone, _, $) {

    var Image = Backbone.Model.extend({
        url: function() {
            var url = Backbone.Model.prototype.url.call(this);
            return (_.last(url) != '/') ? url + '/' : url;
        }
    });

    var ImageList = Backbone.Collection.extend({
        model: Image,

        initialize: function(options) {
            this.url = options.baseUrl;
        },

        bulkUpdate: function() {
            return Backbone.sync('update', this, {
                success: _.bind(function(model, resp, xhr) {
                    this.reset(resp);
                }, this)
            });
        }
    });

    var ImageView = Backbone.View.extend({
        attributes: {
            'class': 'thumbnail span2 inline-related',
        },

        events: {
            'click .delete': 'deleteModel',
        },

        initialize: function(options) {
            this.template = _.template($('#image-template').html());
            this.listenTo(this.model, 'change', this.render);
            this.listenTo(this.model, 'destroy', this.remove);
        },

        render: function() {
            this.$el.html(this.template(this.model.toJSON()));
            this.$el.attr('id', 'image-' + this.model.id);
            return this;
        },

        deleteModel: function() {
            this.model.destroy({success: _.bind(function() {;
                this.trigger('deleteModel');
            }, this)});
        }
    });

    window.ImageInline = Backbone.View.extend({
        events: {
            'click .add-row a': 'openSelector',
        },

        initialize: function() {
            _.bindAll(this, 'openSelector', 'uploadSuccess', 'updateAll', 'updateMaxReached');

            this.images = new ImageList({baseUrl: this.options.baseUrl});

            this.addRowEl = this.$('.add-row');
            this.imageListEl = this.$('.images-list');
            this.fileInputEl = this.$el.find('.image-file-input');

            this.listenTo(this.images, 'add', this.addOne);
            this.listenTo(this.images, 'reset', this.addAll);
            this.listenTo(this.images, 'add', this.updateMaxReached);
            this.listenTo(this.images, 'reset', this.updateMaxReached);

            this.fileInputEl.fileupload({
                url: this.images.url,
                dataType: 'json',
                autoUpload: true,
                success: this.uploadSuccess
            });

            this.imageListEl.sortable({
                containment: this.$el,
                helper: _.bind(function(event, el) {
                    return el.removeClass('thumbnail').addClass('dragging');
                }),
                deactivate: _.bind(function(event, ui) {
                    $(ui.item).addClass('thumbnail').removeClass('dragging');
                    this.updateAll();
                }, this)
            });

            this.images.fetch();
        },

        addOne: function(image) {
            var view = new ImageView({model: image});
            this.listenTo(view, 'deleteModel', this.updateAll)
            this.listenTo(view, 'deleteModel', this.updateMaxReached)
            this.imageListEl.append(view.render().el);
        },

        addAll: function() {
            this.imageListEl.html('');
            this.images.each(this.addOne, this);
        },

        openSelector: function(event) {
            this.fileInputEl.click();
            return false;
        },

        uploadSuccess: function(data) {
            this.images.add(data);
            return false;
        },

        updateAll: function() {
            var ids = this.imageListEl.sortable('toArray');
            if (ids.length) {
                _.each(ids, this.updateOne, this);
                this.images.bulkUpdate();
            }
        },

        updateOne: function(id, order) {
            var id = id.replace('image-', '');
            var model = this.images.get(id);

            if (model) {
                model.set({order: order});
            }
        },

        updateMaxReached: function() {
            if (this.images.length >= this.options.max) {
                this.addRowEl.hide();
                this.fileInputEl.fileupload('disable');
            } else {
                this.addRowEl.show();
                this.fileInputEl.fileupload('enable');
            }
        }
    });

})(Backbone, _, jQuery);
