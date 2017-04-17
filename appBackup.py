# This is a backup of our main.py file

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

form = """
    <form method="post">
        what is your birthday?
        <br>

        <label> Month
            <input type="text" name="month" value="%(month)s">
        </label>

        <label> Day
            <input type="text" name="day" value="%(day)s">
        </label>

        <label> Year
            <input type="text" name="year" value="%(year)s">
        </label>

        <div>%(error)s</div>

        <br>
        <br>
        <input type="submit">
    </form>
"""

months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']


# Make a mapping of the first 3 letters to lower case for Months array
month_abbvs = dict((m[:3].lower(),m) for m in months)

# Validity Check Functions
def valid_month(month):
    if month:
        short_month = month[:3].lower()
        return month_abbvs.get(short_month)

def valid_day(day):
    if day and day.isdigit():
        day = int(day)
        if day > 0 and day <= 31:
            return day

def valid_year(year):
    if year and year.isdigit():
        year = int(year)
        if year > 1900 and year < 2020:
            return year

# Implementing HTML Escaping via Python
def escape_html(s):
    return cgi.escape(s, quote=True)


class MainHandler(webapp2.RequestHandler):
    def write_form(self, error="", month="", day="", year=""):
        self.response.out.write(form % {"error": error,
                                        "month": escape_html(month),
                                        "day": escape_html(day),
                                        "year": escape_html(year)})

    def get(self):
        # Hello
        self.write_form()

    def post(self):
        #what the user adds into the fields
        user_month = self.request.get('month')
        user_day = self.request.get('day')
        user_year = self.request.get('year')

        month = valid_month(self.request.get('month'))
        day = valid_day(self.request.get('day'))
        year = valid_year(self.request.get('year'))

        if not (month and day and year):
            # render error div but leave what user typed in
            self.write_form("That doesn't look valid",
                            user_month, user_day, user_year)
            # else if all true
        else:
            self.redirect("/thanks")

class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Thanks! Das a Valid Form")


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/thanks', ThanksHandler)
], debug=True)
