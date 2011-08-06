/**
 * Utility functions.
 */

(function() {

    CMSUtils = function()
    {
    }

    CMSUtils.prototype =
    {

        /**
         * Returns a function binded to an object - useful in case
         * we need to send callback that needs to access to the
         * "this" object.
         *
         * Example:
         * var f = this.utils.bind_func(this, this.cb);
         * function_that_needs_a_cb(function(data) { f(data); });
         *
         * object (object): the object to bind to
         * method (function): the function to bind
         * returns (function): the binded function
         */
        bind_func: function(object, method)
        {
            return function()
            {
                return method.apply(object, arguments);
            };
        },

        /**
         * Perform an AJAX request.
         *
         * url (string): the url of the resource
         * par (string): the GET arguments already encoded
         * cb (function): the function to call with the response
         */
        ajax_request: function(url, par, cb)
        {
            var xmlhttp;
            if (window.XMLHttpRequest)
                xmlhttp=new XMLHttpRequest();
            else if (window.ActiveXObject)
                xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
            else
                alert("Your browser does not support XMLHTTP!");
            xmlhttp.onreadystatechange = function()
            {
                if (xmlhttp.readyState == 4)
                {
                    cb(xmlhttp.responseText);
                }
            }
            xmlhttp.open("GET", url + "?" + par, true);
            xmlhttp.send();
        },

        /**
         * Returns a random string of letters of specified length,
         * useful for generating ids.
         *
         * length (int): the length of the string to generate
         * returns (string): a random string of letters
         */
        random_string: function(length)
        {
            var string = "";
            var letters =
                "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
            for(var i = 0; i < length; i++)
            {
                var idx = Math.floor(Math.random() * letters.length);
                string += letters.charAt(idx);
            }
            return string;
        },

    };
}());