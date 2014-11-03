"""
Statement:
    Create the base handler where sub handlers to extend
Author:
    Will
Date:
    2014.11.03
"""

# -*- coding: utf-8 -*-
import tornado.web

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        user_id = self.get_secure_cookie("uid")
        if not user_id:
            return None
        return self.db.get("SELECT * FROM users WHERE id=%s", int(user_id))

    def write_error(self, status_code, **kwargs):
        """Write out the error message in json:
        {
            "request" : "/api/requesturl",
            "error_code" : "403",
            "error" : "error message"
        }  
        """
        response = {"request" : self.request.uri,
                    "error_code" : status_code}
        if "error" in kwargs:
            response["error"] = kwargs["error"]
            del kwargs["error"]
        elif "reason" in kwargs:
            response["error"] = kwargs["reason"]
            del kwargs["reason"]
        else:
            response["error"] = "Unknown internal error"
        #for k, v in kwargs.iteritems():
        #        response[k] = v
        # default 'Content-Type' is 'application/json' when self.write()
        #self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(response)

