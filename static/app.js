
(function(){

	var UserState = function(manager, user_id) {
    this.manager = manager;
    this.user_id = user_id;
    this.cached = false;
    this.remote_loaded = false;
	};

	UserState.prototype = {
    can: function(metric) {

    },
    did: function(metric) {

    }
	};


	var StateManager = function(app_key, app_secrect) {
		this._users = {};
    this._app_key = app_key;
    this._app_secrect = app_secrect;
	};

	StateManager.prototype = {

		getUser: function(user_id){
			if (!this._users[user_id])
				this._users[user_id] = new UserState(manager, user_id);
      return this._users[user_id];
		}
	};

	if (window) {
		window.StateManager = StateManager;
	}

})();