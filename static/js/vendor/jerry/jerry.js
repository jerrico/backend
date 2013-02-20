(function() {

  /* mnified json2 from https://raw.github.com/douglascrockford/JSON-js/master/json2.js */
  if(typeof JSON!=="object"){JSON={}}(function(){"use strict";function f(e){return e<10?"0"+e:e}function quote(e){escapable.lastIndex=0;return escapable.test(e)?'"'+e.replace(escapable,function(e){var t=meta[e];return typeof t==="string"?t:"\\u"+("0000"+e.charCodeAt(0).toString(16)).slice(-4)})+'"':'"'+e+'"'}function str(e,t){var n,r,i,s,o=gap,u,a=t[e];if(a&&typeof a==="object"&&typeof a.toJSON==="function"){a=a.toJSON(e)}if(typeof rep==="function"){a=rep.call(t,e,a)}switch(typeof a){case"string":return quote(a);case"number":return isFinite(a)?String(a):"null";case"boolean":case"null":return String(a);case"object":if(!a){return"null"}gap+=indent;u=[];if(Object.prototype.toString.apply(a)==="[object Array]"){s=a.length;for(n=0;n<s;n+=1){u[n]=str(n,a)||"null"}i=u.length===0?"[]":gap?"[\n"+gap+u.join(",\n"+gap)+"\n"+o+"]":"["+u.join(",")+"]";gap=o;return i}if(rep&&typeof rep==="object"){s=rep.length;for(n=0;n<s;n+=1){if(typeof rep[n]==="string"){r=rep[n];i=str(r,a);if(i){u.push(quote(r)+(gap?": ":":")+i)}}}}else{for(r in a){if(Object.prototype.hasOwnProperty.call(a,r)){i=str(r,a);if(i){u.push(quote(r)+(gap?": ":":")+i)}}}}i=u.length===0?"{}":gap?"{\n"+gap+u.join(",\n"+gap)+"\n"+o+"}":"{"+u.join(",")+"}";gap=o;return i}}if(typeof Date.prototype.toJSON!=="function"){Date.prototype.toJSON=function(e){return isFinite(this.valueOf())?this.getUTCFullYear()+"-"+f(this.getUTCMonth()+1)+"-"+f(this.getUTCDate())+"T"+f(this.getUTCHours())+":"+f(this.getUTCMinutes())+":"+f(this.getUTCSeconds())+"Z":null};String.prototype.toJSON=Number.prototype.toJSON=Boolean.prototype.toJSON=function(e){return this.valueOf()}}var cx=/[\u0000\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g,escapable=/[\\\"\x00-\x1f\x7f-\x9f\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g,gap,indent,meta={"\b":"\\b"," ":"\\t","\n":"\\n","\f":"\\f","\r":"\\r",'"':'\\"',"\\":"\\\\"},rep;if(typeof JSON.stringify!=="function"){JSON.stringify=function(e,t,n){var r;gap="";indent="";if(typeof n==="number"){for(r=0;r<n;r+=1){indent+=" "}}else if(typeof n==="string"){indent=n}rep=t;if(t&&typeof t!=="function"&&(typeof t!=="object"||typeof t.length!=="number")){throw new Error("JSON.stringify")}return str("",{"":e})}}if(typeof JSON.parse!=="function"){JSON.parse=function(text,reviver){function walk(e,t){var n,r,i=e[t];if(i&&typeof i==="object"){for(n in i){if(Object.prototype.hasOwnProperty.call(i,n)){r=walk(i,n);if(r!==undefined){i[n]=r}else{delete i[n]}}}}return reviver.call(e,t,i)}var j;text=String(text);cx.lastIndex=0;if(cx.test(text)){text=text.replace(cx,function(e){return"\\u"+("0000"+e.charCodeAt(0).toString(16)).slice(-4)})}if(/^[\],:{}\s]*$/.test(text.replace(/\\(?:["\\\/bfnrt]|u[0-9a-fA-F]{4})/g,"@").replace(/"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g,"]").replace(/(?:^|:|,)(?:\s*\[)+/g,""))){j=eval("("+text+")");return typeof reviver==="function"?walk({"":j},""):j}throw new SyntaxError("JSON.parse")}}})();

  /* RSVP.js for async handling from https://github.com/tildeio/rsvp.js */
  (function(e){"use strict";function v(e,n){t.async(function(){e.trigger("promise:resolved",{detail:n}),e.isResolved=!0,e.resolvedValue=n})}function m(e,n){t.async(function(){e.trigger("promise:failed",{detail:n}),e.isRejected=!0,e.rejectedValue=n})}function g(e){var t,n=[],r=new h,i=e.length;i===0&&r.resolve([]);var s=function(e){return function(t){o(e,t)}},o=function(e,t){n[e]=t,--i===0&&r.resolve(n)},u=function(e){r.reject(e)};for(t=0;t<i;t++)e[t].then(s(t),u);return r}function y(e,n){t[e]=n}var t={},n=typeof window!="undefined"?window:{},r=n.MutationObserver||n.WebKitMutationObserver,i;if(typeof process!="undefined"&&{}.toString.call(process)==="[object process]")t.async=function(e,t){process.nextTick(function(){e.call(t)})};else if(r){var s=[],o=new r(function(){var e=s.slice();s=[],e.forEach(function(e){var t=e[0],n=e[1];t.call(n)})}),u=document.createElement("div");o.observe(u,{attributes:!0}),window.addEventListener("unload",function(){o.disconnect(),o=null}),t.async=function(e,t){s.push([e,t]),u.setAttribute("drainQueue","drainQueue")}}else t.async=function(e,t){setTimeout(function(){e.call(t)},1)};var a=function(e,t){this.type=e;for(var n in t){if(!t.hasOwnProperty(n))continue;this[n]=t[n]}},f=function(e,t){for(var n=0,r=e.length;n<r;n++)if(e[n][0]===t)return n;return-1},l=function(e){var t=e._promiseCallbacks;return t||(t=e._promiseCallbacks={}),t},c={mixin:function(e){return e.on=this.on,e.off=this.off,e.trigger=this.trigger,e},on:function(e,t,n){var r=l(this),i,s;e=e.split(/\s+/),n=n||this;while(s=e.shift())i=r[s],i||(i=r[s]=[]),f(i,t)===-1&&i.push([t,n])},off:function(e,t){var n=l(this),r,i,s;e=e.split(/\s+/);while(i=e.shift()){if(!t){n[i]=[];continue}r=n[i],s=f(r,t),s!==-1&&r.splice(s,1)}},trigger:function(e,t){var n=l(this),r,i,s,o,u;if(r=n[e])for(var f=0;f<r.length;f++)i=r[f],s=i[0],o=i[1],typeof t!="object"&&(t={detail:t}),u=new a(e,t),s.call(o,u)}},h=function(){this.on("promise:resolved",function(e){this.trigger("success",{detail:e.detail})},this),this.on("promise:failed",function(e){this.trigger("error",{detail:e.detail})},this)},p=function(){},d=function(e,t,n,r){var i=typeof n=="function",s,o,u,a;if(i)try{s=n(r.detail),u=!0}catch(f){a=!0,o=f}else s=r.detail,u=!0;s&&typeof s.then=="function"?s.then(function(e){t.resolve(e)},function(e){t.reject(e)}):i&&u?t.resolve(s):a?t.reject(o):t[e](s)};h.prototype={then:function(e,n){var r=new h;return this.isResolved&&t.async(function(){d("resolve",r,e,{detail:this.resolvedValue})},this),this.isRejected&&t.async(function(){d("reject",r,n,{detail:this.rejectedValue})},this),this.on("promise:resolved",function(t){d("resolve",r,e,t)}),this.on("promise:failed",function(e){d("reject",r,n,e)}),r},resolve:function(e){v(this,e),this.resolve=p,this.reject=p},reject:function(e){m(this,e),this.resolve=p,this.reject=p}},c.mixin(h.prototype),e.Promise=h,e.Event=a,e.EventTarget=c,e.all=g,e.configure=y})(window.RSVP={});


  /*
  CryptoJS v3.0.2
  code.google.com/p/crypto-js
  (c) 2009-2012 by Jeff Mott. All rights reserved.
  code.google.com/p/crypto-js/wiki/License
  from http://crypto-js.googlecode.com/svn/tags/3.0.2/build/rollups/hmac-sha256.js
  // */
  // var CryptoJS=CryptoJS||function(h,i){var e={},f=e.lib={},l=f.Base=function(){function a(){}return{extend:function(j){a.prototype=this;var d=new a;j&&d.mixIn(j);d.$super=this;return d},create:function(){var a=this.extend();a.init.apply(a,arguments);return a},init:function(){},mixIn:function(a){for(var d in a)a.hasOwnProperty(d)&&(this[d]=a[d]);a.hasOwnProperty("toString")&&(this.toString=a.toString)},clone:function(){return this.$super.extend(this)}}}(),k=f.WordArray=l.extend({init:function(a,j){a=
  // this.words=a||[];this.sigBytes=j!=i?j:4*a.length},toString:function(a){return(a||m).stringify(this)},concat:function(a){var j=this.words,d=a.words,c=this.sigBytes,a=a.sigBytes;this.clamp();if(c%4)for(var b=0;b<a;b++)j[c+b>>>2]|=(d[b>>>2]>>>24-8*(b%4)&255)<<24-8*((c+b)%4);else if(65535<d.length)for(b=0;b<a;b+=4)j[c+b>>>2]=d[b>>>2];else j.push.apply(j,d);this.sigBytes+=a;return this},clamp:function(){var a=this.words,b=this.sigBytes;a[b>>>2]&=4294967295<<32-8*(b%4);a.length=h.ceil(b/4)},clone:function(){var a=
  // l.clone.call(this);a.words=this.words.slice(0);return a},random:function(a){for(var b=[],d=0;d<a;d+=4)b.push(4294967296*h.random()|0);return k.create(b,a)}}),o=e.enc={},m=o.Hex={stringify:function(a){for(var b=a.words,a=a.sigBytes,d=[],c=0;c<a;c++){var e=b[c>>>2]>>>24-8*(c%4)&255;d.push((e>>>4).toString(16));d.push((e&15).toString(16))}return d.join("")},parse:function(a){for(var b=a.length,d=[],c=0;c<b;c+=2)d[c>>>3]|=parseInt(a.substr(c,2),16)<<24-4*(c%8);return k.create(d,b/2)}},q=o.Latin1={stringify:function(a){for(var b=
  // a.words,a=a.sigBytes,d=[],c=0;c<a;c++)d.push(String.fromCharCode(b[c>>>2]>>>24-8*(c%4)&255));return d.join("")},parse:function(a){for(var b=a.length,d=[],c=0;c<b;c++)d[c>>>2]|=(a.charCodeAt(c)&255)<<24-8*(c%4);return k.create(d,b)}},r=o.Utf8={stringify:function(a){try{return decodeURIComponent(escape(q.stringify(a)))}catch(b){throw Error("Malformed UTF-8 data");}},parse:function(a){return q.parse(unescape(encodeURIComponent(a)))}},b=f.BufferedBlockAlgorithm=l.extend({reset:function(){this._data=k.create();
  // this._nDataBytes=0},_append:function(a){"string"==typeof a&&(a=r.parse(a));this._data.concat(a);this._nDataBytes+=a.sigBytes},_process:function(a){var b=this._data,d=b.words,c=b.sigBytes,e=this.blockSize,g=c/(4*e),g=a?h.ceil(g):h.max((g|0)-this._minBufferSize,0),a=g*e,c=h.min(4*a,c);if(a){for(var f=0;f<a;f+=e)this._doProcessBlock(d,f);f=d.splice(0,a);b.sigBytes-=c}return k.create(f,c)},clone:function(){var a=l.clone.call(this);a._data=this._data.clone();return a},_minBufferSize:0});f.Hasher=b.extend({init:function(){this.reset()},
  // reset:function(){b.reset.call(this);this._doReset()},update:function(a){this._append(a);this._process();return this},finalize:function(a){a&&this._append(a);this._doFinalize();return this._hash},clone:function(){var a=b.clone.call(this);a._hash=this._hash.clone();return a},blockSize:16,_createHelper:function(a){return function(b,d){return a.create(d).finalize(b)}},_createHmacHelper:function(a){return function(b,d){return g.HMAC.create(a,d).finalize(b)}}});var g=e.algo={};return e}(Math);
  // (function(h){var i=CryptoJS,e=i.lib,f=e.WordArray,e=e.Hasher,l=i.algo,k=[],o=[];(function(){function e(a){for(var b=h.sqrt(a),d=2;d<=b;d++)if(!(a%d))return!1;return!0}function f(a){return 4294967296*(a-(a|0))|0}for(var b=2,g=0;64>g;)e(b)&&(8>g&&(k[g]=f(h.pow(b,0.5))),o[g]=f(h.pow(b,1/3)),g++),b++})();var m=[],l=l.SHA256=e.extend({_doReset:function(){this._hash=f.create(k.slice(0))},_doProcessBlock:function(e,f){for(var b=this._hash.words,g=b[0],a=b[1],j=b[2],d=b[3],c=b[4],h=b[5],l=b[6],k=b[7],n=0;64>
  // n;n++){if(16>n)m[n]=e[f+n]|0;else{var i=m[n-15],p=m[n-2];m[n]=((i<<25|i>>>7)^(i<<14|i>>>18)^i>>>3)+m[n-7]+((p<<15|p>>>17)^(p<<13|p>>>19)^p>>>10)+m[n-16]}i=k+((c<<26|c>>>6)^(c<<21|c>>>11)^(c<<7|c>>>25))+(c&h^~c&l)+o[n]+m[n];p=((g<<30|g>>>2)^(g<<19|g>>>13)^(g<<10|g>>>22))+(g&a^g&j^a&j);k=l;l=h;h=c;c=d+i|0;d=j;j=a;a=g;g=i+p|0}b[0]=b[0]+g|0;b[1]=b[1]+a|0;b[2]=b[2]+j|0;b[3]=b[3]+d|0;b[4]=b[4]+c|0;b[5]=b[5]+h|0;b[6]=b[6]+l|0;b[7]=b[7]+k|0},_doFinalize:function(){var e=this._data,f=e.words,b=8*this._nDataBytes,
  // g=8*e.sigBytes;f[g>>>5]|=128<<24-g%32;f[(g+64>>>9<<4)+15]=b;e.sigBytes=4*f.length;this._process()}});i.SHA256=e._createHelper(l);i.HmacSHA256=e._createHmacHelper(l)})(Math);
  // (function(){var h=CryptoJS,i=h.enc.Utf8;h.algo.HMAC=h.lib.Base.extend({init:function(e,f){e=this._hasher=e.create();"string"==typeof f&&(f=i.parse(f));var h=e.blockSize,k=4*h;f.sigBytes>k&&(f=e.finalize(f));for(var o=this._oKey=f.clone(),m=this._iKey=f.clone(),q=o.words,r=m.words,b=0;b<h;b++)q[b]^=1549556828,r[b]^=909522486;o.sigBytes=m.sigBytes=k;this.reset()},reset:function(){var e=this._hasher;e.reset();e.update(this._iKey)},update:function(e){this._hasher.update(e);return this},finalize:function(e){var f=
  // this._hasher,e=f.finalize(e);f.reset();return f.finalize(this._oKey.clone().concat(e))}})})();

  /*
  CryptoJS v3.0.2
  code.google.com/p/crypto-js
  (c) 2009-2012 by Jeff Mott. All rights reserved.
  code.google.com/p/crypto-js/wiki/License
  from http://crypto-js.googlecode.com/svn/tags/3.0.2/build/components/enc-base64-min.js
  */
  // (function(){var h=CryptoJS,i=h.lib.WordArray;h.enc.Base64={stringify:function(b){var e=b.words,f=b.sigBytes,c=this._map;b.clamp();for(var b=[],a=0;a<f;a+=3)for(var d=(e[a>>>2]>>>24-8*(a%4)&255)<<16|(e[a+1>>>2]>>>24-8*((a+1)%4)&255)<<8|e[a+2>>>2]>>>24-8*((a+2)%4)&255,g=0;4>g&&a+0.75*g<f;g++)b.push(c.charAt(d>>>6*(3-g)&63));if(e=c.charAt(64))for(;b.length%4;)b.push(e);return b.join("")},parse:function(b){var b=b.replace(/\s/g,""),e=b.length,f=this._map,c=f.charAt(64);c&&(c=b.indexOf(c),-1!=c&&(e=c));
  // for(var c=[],a=0,d=0;d<e;d++)if(d%4){var g=f.indexOf(b.charAt(d-1))<<2*(d%4),h=f.indexOf(b.charAt(d))>>>6-2*(d%4);c[a>>>2]|=(g|h)<<24-8*(a%4);a++}return i.create(c,a)},_map:"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="}})();


  function make_params(obj) {
    var s = [];
    for (key in obj) {
      s.push(encodeURIComponent( key ) + "=" + encodeURIComponent( obj[key] || '' ))
    }
    // Return the resulting serialization
    return s.join( "&" ).replace( /%20/g, "+" );
  };

  var Restrictions = {
    "BinaryRestriction": {
      "allows": function(restriction, user, attr, change) {
        return restriction.allow;
      },
      "did": function(restriction, user, attr, change){

      }
    },
    "TotalAmountRestriction": {
      "allows": function(restriction, user, attr, change){
        if (!restriction.left) return false;
        return restriction.left - change >= 0;
      },
      "did": function(restriction, user, attr, change){
        return restriction.left -= change;
      }
    },

    "PerTimeRestriction": {
      "allows": function(restriction, user, attr, change){
        if (!restriction.left) return false;
        return restriction.left - change >= 0;
      },
      "did": function(restriction, user, attr, change){
        return restriction.left -= change;
      }
    },

    "AccountAmountRestriction": {
      "allows": function(restriction, user, attr, change){
        if (!user[restriction.account_item]) return false;
        return user.account[restriction.account_item] - ((restriction.quantity_change || 1) * change) > 0;
      },
      "did": function(restriction, user, attr, change){
        return user.account[restriction.account_item] -= ((restriction.quantity_change || 1) * change) > 0;
      }
    }
  };


var getJSON = function(url, meth, data) {
  var method = meth? meth.toUpperCase(): "GET",
      promise = new RSVP.Promise(),
      client = new XMLHttpRequest();

  client.open(method, url);

  client.onreadystatechange = function() {
    if (this.readyState === 4) { // done
      if (this.status === 200) {
        try {
          this.json = JSON.parse(this.responseText);
        }
        catch (err) {
          promise.reject({"error": err, res: this});
          return;
        }

        if (this.json.status != "success") {
          promise.reject({"error": "ServerSaysNo", res: this});
          return;
        }
        promise.resolve(this.json.result);
        return true;
      }

      // haven't returned yet. reject then.
      promise.reject(this);

    }
  };

  // client.responseType = "json";
  client.setRequestHeader("Accept", "application/json");
  client.send(data);

  return promise;
};

  var JerryUser = function(user_id, device_id, provider, profile_state) {
    this.loaded = false;
    this.provider = provider;
    this.user_id = user_id;
    this.device_id = device_id;
    this.profile_name = "";
    this.default_mode = false;
    this.restrictions = {};
    this.profile_state = {};

    if (profile_state) this.loadState(profile_state);
  };


  JerryUser.prototype = {

    decorateParams: function(params) {
      if (this.user_id) params["user_id"] = this.user_id;
      if (this.device_id) params["device_id"] = this.device_id;
      return params;
    },

    getCans: function() {
      var res = {},
          key;
      for (key in this.restrictions) {
        res[key] = this.can(key);
      };
      return res;
    },

    loadState: function(profile_state) {
      this.profile_state = profile_state;
      this.profile_name = profile_state.profile;
      this.default_mode = profile_state['default'] === 'allow';
      this.restrictions = profile_state.states;
      this.account = profile_state.account;
      this.loaded = true;
      this.trigger("loaded");
    },

    can: function(attr, action, change_amount) {
      var change = change_amount || 1,
          restrictions = this.restrictions[action];
      if (!restrictions || restrictions.length === 0) return this.default_mode;

      for (var idx=0; idx < restrictions.length; idx++) {
        var restriction = restrictions[idx];
        if (!Restrictions[restriction._class].allows(
              restriction, this, action, change
          )) return false;
      }

      return !this.default_mode;
    },

    did: function(attr, change_amount) {
      var change = change_amount || 1,
          restrictions = this.restrictions[action];

      if (restrictions && restrictions.length > 0) {
        for (var idx=0; idx < restrictions.length; idx++) {
          var restriction = restrictions[idx];
          Restrictions[restriction._class].did(
                restriction, this, action, change
            );
        }
      }

      var res = this.provider.did(this, action, change);
      this.trigger("did", {user: this, action: action, change: change});
      return res;
    }
  };

  RSVP.EventTarget.mixin(JerryUser.prototype);


  var Jerry = function () {
    this.key = null;
    this.endpoint = "http://api.jerri.co/api/v1/";
    this.customMethods = {};
    return this;
  };

  Jerry.prototype = {
    userClass: JerryUser,

    init: function(key, endpoint){
      this.key = key;
      if (endpoint) this.endpoint = endpoint;
      return this;
    },

    _request: function(method, end, params, data) {
      var url = this.customMethods[end] ? this.customMethods[end] : this.endpoint + end;
      params["_key"] = this.key;
      return getJSON(url + "?" + make_params(params), method, data)
    },

   did: function(user, action, quantity) {
    return this.log(user, action, quantity);
   },

   log: function(user, action, quantity, unit){
      var entry = {'action': action},
          url = this.end_point + "logger";

      if (quantity) entry.quantity = quantity;
      if (unit) entry.unit = unit;


      this.trigger("log", {entries: [entry]});

      return this._request("POST", "logger", {},
            make_params(user.decorateParams({'entries': JSON.stringify([entry])})));
    },

    signin: function(user_id, device_id){
        var user = new this.userClass(user_id, device_id, this)
        user.promise = this._request("GET", "permission_state", user.decorateParams({})
            ).then(function(json) {
              console.log(json);
              user.loadState(json);
              this.trigger("userSignedIn", {user: user});
            }, function(err) {
              console.log(err);
            });
        return user
    }

  };

  RSVP.EventTarget.mixin(Jerry.prototype);

  window.jerry = new Jerry();
  if (window.on_jerry_loaded) window.on_jerry_loaded(window.jerry);
})(); 