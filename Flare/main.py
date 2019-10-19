#!/usr/bin/env python

# Copyright 2015 Google Inc.
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

"""
Sample Google App Engine application that lists the objects in a Google Cloud
Storage bucket.

For more information about Cloud Storage, see README.md in /storage.
For more information about Google App Engine, see README.md in /appengine.
"""

import json
import StringIO
import os
import googleapiclient.discovery
import googleapiclient.http
import cloudstorage as gcs
import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)



# The bucket that will be used to list objects.
BUCKET_NAME = 'user_fire_images'

class MainPage(webapp2.RequestHandler):

    def post(self):
        uploaded_file = self.request.POST.get("file")
        uploaded_file_content = uploaded_file.file.read()
        uploaded_file_filename = uploaded_file.filename
        uploaded_file_type = uploaded_file.type

        # This write_retry_params params bit isn't essential, but Google's examples recommend it
        write_retry_params = gcs.RetryParams(backoff_factor=1.1)
        gcs_file = gcs.open(
            "/" + BUCKET_NAME + "/" + uploaded_file_filename,
            "w",
            content_type=uploaded_file_type,
            retry_params=write_retry_params
        )
        gcs_file.write(uploaded_file_content)
        gcs_file.close()

app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)
