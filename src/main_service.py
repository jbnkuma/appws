#!/usr/bin/env python3
import json
import sys
import random

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import options, define

from src.utils import utilities


__docfomat_= "restructuredtext"

"""
    :author: Jesus Becerril Navarrete
    :organization: uknow
    :contact: jesusbn5@gmail.com
    :requires: python >= 3

"""

define("port", default=8000, help="run the give port", type=int)

class Service:

    def __init__(self):
       pass

class AddUser(tornado.web.RequestHandler):
    def post(self):
        try:
            files_data = utilities.UploadConfig().get_config()
            if len(files_data) > 0 :
                logs = utilities.Logs(files_data[0])
            else:
                raise utilities.nodata
            user = self.get_argument('user')
            password = self.get_argument('password')
            db = utilities.DataBase(files_data[0], files_data[1])
            table = "auth_data"
            statements = "*"
            provisory = " WHERE user_name == " + "\"" + user + "\""
            data = ""
            result = db.dataSearch(statements, table, provisory, data)
            data_user = result[0].fetchall()
            if len(data_user) > 0:
                self.write(json.dumps(['message:', {'state': ("300", "User Name exists")}]))
            else:

                statements = "  "
                provisory = ("(?, ?, ?)")
                data = (random.randrange(100), user, password)
                result = db.insertion(table, statements, provisory, data)
                if result == "ok":
                    self.write(json.dumps(['message:', {'state': ("200", "User successfully registered")}]))
                else:
                    self.write(json.dumps(['message:', {'state': ("300",
                                                                  "An unexpected error has occurred try again")}]))

        except IOError:
            self.write(json.dumps(['session:', {'id': (None)},
                                           'message:', {'state': ("500",
                                                                  "An unexpected error happened")}]))
            self.logs.error_log("An unexpected error happened:  {1}\n" \
                "Error: {0}".format(str(sys.exc_info()[0])))

class LoginUser(tornado.web.RequestHandler):
    def post(self):
        try:
            files_data = utilities.UploadConfig().get_config()
            if len(files_data) > 0 :
                logs = utilities.Logs(files_data[0])
            else:
                raise utilities.nodata

            user = self.get_argument('user')
            password = self.get_argument('password')
            logs.info_log("search user")
            db = utilities.DataBase(files_data[0], files_data[1])
            table = "auth_data"
            statements = "id, user_name, password"
            provisory = " WHERE user_name == " + "\"" + user + "\""
            data = ""
            result = db.dataSearch(statements, table, provisory, data)
            data_user = result[0].fetchall()
            if len(data_user) > 0:
                if password == data_user[0][2]:
                    logs.info_log("User login ok")
                    session = utilities.SessionGenerator().get_session()
                    self.write(json.dumps(['session:', {'id': (str(session))},
                                           'message:', {'state': ("200")},
                                           {"userid": (str(data_user[0][0]))}]))
                else:
                    logs.info_log("User don`t exist")
                    self.write(json.dumps(['session:', {'id': (None)},
                                           'message:', {'state': ("404")}]))
                    result[1].close()
            else:
                    logs.info_log("User don`t exist")
                    self.write(json.dumps(['session:', {'id': (None)},
                                           'message:', {'state': ("404")}]))
                    result[1].close()

        except IOError:
            self.write(json.dumps(['session:', {'id': (None)},
                                           'message:', {'state': ("500",
                                                                  "An unexpected error happened")}]))
            self.logs.error_log("An unexpected error happened:  {1}\n" \
                "Error: {0}".format(str(sys.exc_info()[0])))



class AddInfo(tornado.web.RequestHandler):
    def post(self):
        try:
            files_data = utilities.UploadConfig().get_config()
            if len(files_data) > 0 :
                logs = utilities.Logs(files_data[0])
            else:
                raise utilities.nodata

            user_id =  self.get_argument("user_id")
            build_size = self.get_argument("size_build")
            build_age = self.get_argument("age")
            bedrooms = self.get_argument("bedrooms")
            toilets = self.get_argument("toilets")
            parking = self.get_argument("parking")
            floors = self.get_argument("floors")
            maintenance = self.get_argument("maintenance")
            condition = self.get_argument("condition")
            location = self.get_argument("location")
            photo = self.get_argument("photo")

            db = utilities.DataBase(files_data[0], files_data[1])
            table = "depatament_income"
            statements =""
            provisory =""

            db.insertion()


        except IOError:
            self.write(json.dumps(['session:', {'id': (None)},
                                           'message:', {'state': ("500",
                                                                  "An unexpected error happened")}]))
            self.logs.error_log("An unexpected error happened:  {1}\n" \
                "Error: {0}".format(str(sys.exc_info()[0])))


class TestServer(tornado.web.RequestHandler):
    def get(self):
        greeting = self.get_argument('', json.dumps(['session:', {'id': (None)},
                                           'message:', {'state': ("0",
                                                        'Its works :) ')}]))
        self.write(greeting)

if __name__ == "__main__":

    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/login/", LoginUser), (r"/add_user/", AddUser),
        (r"/addinfo/", AddInfo),(r"/", TestServer)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()