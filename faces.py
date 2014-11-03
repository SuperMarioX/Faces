"""
Statement:
    This file is used to init the app, including the following:
    1.Define the database info
    2.Define the handler to route
    3.Build up the server

Author:
    Will

Date:
    2014.11.02
"""
#---------------------------------------------------------------------------
#-*- coding: utf-8 -*-
import os
import uuid
import base64

import tornado.options
from tornado.options import define, options
import tornado.web
import tornado.httpserver
import tornado.ioloop

from app import torndb
import app.user

#---------------------Database info--------------------------------------------
define("port", default=8888, help="Run it on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="Database host")
define("mysql_database", default="pluto2", help="Database name")
define("mysql_user", default="pluto", help="Database user")
define("mysql_password", default="pluto", help="Database password, should be encrypted")

class FacesApplication(tornado.web.Application):
    def __init__(self):
        # Handler to route
        handlers = [
            (r"/faces/user/register", app.user.RegisterHandler),
            (r"/faces/user/login", app.user.LoginHandler),
            (r"/faces/user/logout", app.user.LogoutHandler)
        ]
        # Settings for this app
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,
            # Use UUID to generate cookie secret
            cookie_secret=base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes),
            login_url="/faces/user/login",
            debug=True,
        )

        # Call the parent init function
        tornado.web.Application.__init__(self, handlers, **settings)

        # Have one global db connection across all handlers
        self.db = torndb.Connection(
            host=options.mysql_host,
            database=options.mysql_database,
            user=options.mysql_user,
            password=options.mysql_password
        )


def startserver():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(FacesApplication())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
    http_server.close_all_connections()


if __name__ == "__main__":
    startserver()