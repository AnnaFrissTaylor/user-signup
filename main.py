#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re

form="""
<!DOCTYPE html>
<html>
<head>
    <title> user-signup </title>
    <style type="text/css">
        .error {
            color: red;
            }
    </style>
</head>
<body>
<table>
<form method="post">
    <h1>Username</h1>
    <tr>
    <td>
    <label>
        Username
    </td>
        <td>
            <input type ="text" name="username" value="%(username)s"
        </td>
        <td>
            <div class="error"> %(user_error)s</div>
        </td>
        </tr>
    </label>
    <br>
    <tr>
    <td>
    <label>
            Password
    </td>
    <td>
            <input type="password" name="password" value="">
        </td>
        <td>
            <div class="error"> %(error)s</div>
         </td>
    </label>
    </tr>
    <br>
    <tr>
    <td>
    <label>
            Verify Password
        </td>
        <td>
            <input type="password" name="verify_password" value="">
        </td>
        <td>
            <div class="error"> %(error)s</div>
         </td>
         </tr>
    </label>
    <br>
    <tr>
    <td>
    <label>
            Email (Optional)
        </td>
        <td>
            <input type="text" name="email" value= "%(email)s">
        </td>
        <td>
        <div class="error"> %(email_error)s</div>
        </td>
        </tr>
    </label>
    <tr>
    <td>
    <br>
    <input type="submit">
    </td>
    </tr>
</form>
</table>
</body>
"""

def user_check(users_username):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return USER_RE.match(users_username)

def valid_password(password, verify_password):
    if password == verify_password:
        return True
    else:
        return False

def user_password(password):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return USER_RE.match(password)


def valid_email(users_email):
    if users_email == "":
        return True
    else:
        USER_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
        return USER_RE.match(users_email)


class MainHandler(webapp2.RequestHandler):
    def write_form(self, user_error, error, email_error, username="", email=""):
        self.response.out.write(form % {"user_error": user_error,
                                        "error": error,
                                        "email_error": email_error,
                                        "username": username,
                                        "email": email})

    def get(self):
        self.write_form("", "", "",)


    def post(self):

        users_username = self.request.get('username')
        users_email = self.request.get('email')
        users_password = self.request.get('password')
        users_verify_password = self.request.get('verify_password')

        Final_username = user_check(users_username)
        Final_email = valid_email(users_email)
        Final_password = valid_password(users_password, users_verify_password)
        Final_password2 = user_password(users_password)
        error = ""
        user_error = ""
        email_error = ""

        if not user_check(users_username):
            user_error = "That is not a valid user name"


        if not Final_password or not Final_password2:
            error = "That is not a valid password"

        if not valid_email(users_email):
            email_error = "That is not a valid email"


        if Final_username and Final_email and Final_password and Final_password2:
            self.redirect("/muchosGracias?username=%s" % users_username)
        else:
            self.write_form(user_error, error, email_error, users_username, users_email)

class muchosGracias(webapp2.RequestHandler):
    def get(self):
        users_username = self.request.get('username')
        self.response.out.write("Welcome " + users_username)

app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/muchosGracias', muchosGracias)
], debug=True)
