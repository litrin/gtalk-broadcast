#!/usr/bin/env python
#
# Copyright 2012 Litrin J.
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

import logging
from Model import FriendList
from Model import CacheUserList
from Comtroller import SendMessage

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class BGSend(webapp.RequestHandler):
    def post(self):
        sGroup = self.request.get('group')
        sMessage = self.request.get('message')

        if sMessage != '':
            xmppHandle = SendMessage(sMessage=sMessage)
            lStatus = xmppHandle.sendMulit(CacheUserList(sGroup))
            
            logging.info(",".join(lStatus))

        self.finish("ok!")

app = webapp.WSGIApplication([ 
                                ('/background', BGSend),
                              ],
                              debug=True)

run_wsgi_app(app)