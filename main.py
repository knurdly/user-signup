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
import cgi
import re


# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
    <html>
        <head>
            <title>User Sign-Up</title>

            <style type="text/css">
                .error {
                    color: red;
                    }
            </style>
        </head>

        <body>

        <h1> Sign-Up </h1>
"""
form="""
            <form method="post" name="form">
                <table>
                    <tr>
                        <td><label for="username">Username</label></td>
                        <td>
                            <input name="username" type="text" value="%(username)s" >
                            <span class="error">%(username_error)s</span>

                        </td>
                    </tr>

                    <tr>
                        <td><label for="password">Password</label></td>
                        <td>
                            <input name="password" type="password">
                            <span class="error">%(password_error)s</span>
                        </td>
                    </tr>


                    <tr>
                        <td><label for="verification">Verify Password</label></td>
                        <td>
                            <input name="verification" type="password">
                            <span class="error">%(verification_error)s</span>
                        </td>
                    </tr>

                    <tr>
                        <td><label for="email">Email (optional)</label></td>
                        <td>
                            <input name="email" type="email" value="%(email)s">
                            <span class="error">%(email_error)s</span>
                        </td>
                    </tr>
                </table>

                <input type="submit">

            </form>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

class MainHandler(webapp2.RequestHandler):

    def get(self,username=None,username_error=None,password_error=None,verification_error=None,email=None, email_error=None ):
        content = page_header + form + page_footer
        self.response.write(content % {"username":"",
                                    "username_error":"",
                                    "password_error":"",
                                    "verification_error":"",
                                    "email":"",
                                    "email_error":""})

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verification = self.request.get("verification")
        email = self.request.get("email")

        username_error = self.validate_username(username)
        password_error = self.validate_password(password)
        verification_error = self.validate_verification(verification,password)
        email_error = self.validate_email(email)

        #you must pass through all the variables before this will work
        if username_error == password_error == verification_error == "" and email_error == "Thanks for giving us your email. >:)":
            self.response.write("<h1>Thank you for signing up, " + username + "!</h1><br><h2> -<em>and thanks for the email</em> >:)")
        elif username_error == password_error == verification_error == email_error == "":
            self.response.write("<h1>Thank you for signing up, " + username + "!</h1>")
        else:
            self.response.write(page_header +
                                form % {"username":username,
                                        "username_error":username_error,
                                        "password_error":password_error,
                                        "verification_error":verification_error,
                                        "email":email,
                                        "email_error":email_error} +
                                page_footer)


    def validate_username(self,username):

        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")

        if not username:
            username_error = "Username is blank!".format(username)
            return username_error
        elif username and USER_RE.match(username):
            return ""
        else:
            username_error = "Invalid username."
            return username_error


    def validate_password(self,password):
        USER_RE = re.compile(r".{3,20}$")
        if not password:
            password_error = "Password is blank!".format(password)
            return password_error
        elif password and USER_RE.match(password):
            return ""
        else:
            password_error = "Invalid password."
            return password_error


    def validate_verification(self,verification,password):

        if password != verification:
            verification_error = "Passwords don't match".format(verification)
            return verification_error + " password: " + password + " verification: " + verification
        else:
            return ""


    def validate_email(self,email):

        USER_RE = re.compile(r'[\S]+@[\S]+.[\S]+$')

        if not email:
            return ""
        elif email and USER_RE.match(email):
            return "Thanks for giving us your email. >:)"
        else:
            email_error = "Invalid email."
            return email_error


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
