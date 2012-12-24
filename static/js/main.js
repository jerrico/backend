
$(function() {

  // Util
  var TmplView = Backbone.View.extend({

    default_context: {},

    extend_context: function() {
      return {};
    },

    render:function () {
      var context = _.extend({},
          this.default_context,
          this.model ? this.model.toJSON() : {},
          this.extend_context());

      $(this.el).html(this.template(context));
      return this;
    }
  });

  var HomeView = TmplView.extend({
     template: _.template($('#tmpl-main').html())
  });

  var AppState = Backbone.Model.extend({
    defaults: {

    }
  });


  var Router = Backbone.Router.extend({

    routes: {
        // home
        "": "home"
    },

    el: $("body"),

    initialize: function() {
      var app = this;
      app.state = new AppState({});
      app.main = $('#main');
      app.progress = 10;

    },

    show_modal: function(title, content) {
      var $el = $(this.el).find("#generalModal");
      $el.find(".close").show();
      $el.find(".modal-header h3").html(title);
      $el.find(".content-wrapper").html(content);
      $el.modal('show');
      return $el;
    },

    close_modal: function() {
      $(this.el).find("#generalModal").modal("hide");
    },

    _update_loading_progress: function(additional) {
      this.progress += additional;
      this.main.find("#progress-bar").css({"width": this.progress + "%"});
    },

    start: function() {
      var me = this;
      me._update_loading_progress(99);
      Backbone.history.start();
      /*
      function next() {
        me._update_loading_progress(20);
      }
      return $.when(this.profiles.fetch().then(next),
            this.books.fetch().then(next),
            this.videos.fetch().then(next),
            this.recommendations.fetch().then(next)
          ).then(function() {
            Backbone.history.start();
          });
      */
    },


    home: function () {
        // Since the home view never changes, we instantiate it and render it only once
        if (!this.homeView) {
            this.homeView = new HomeView({app: this});
            this.homeView.render();
        } else {
            this.homeView.delegateEvents(); // delegate events when the view is recycled
        }
        this.main.html(this.homeView.el);
        this.trigger("pageLoaded", "home");
    },

  });

  
  var app = new Router();
  app.start();
  window.app = app;

});