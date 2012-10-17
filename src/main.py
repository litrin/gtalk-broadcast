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

import logging
from DBModel import FriendList
from WebPage import WebPage

from google.appengine.api import xmpp
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class Gtalk(webapp.RequestHandler):
    def post(self):
        self.GetMessage()
    
    def GetMessage(self):
        aMessage = xmpp.Message(self.request.POST)
        sMessageFrom = aMessage.sender[:aMessage.sender.find('/')].lower()
        sMessage = aMessage.body
        
        #this is the admin account list
        lAdmin = []

        #FriendList().add(sMessageFrom)       
        if sMessageFrom in lAdmin:
            sMessageRely = self.sendMessage(sMessage)
        else:
            FriendList().add(sMessageFrom)
            sMessageRely = self.userSetting(sMessage)

        aMessage.reply(sMessageRely)

    def sendMessage(self, sMessage):
        lStatus = []
        for sUser in FriendList().getAll():
            if sUser not in dStatus.keys():
                bStatus = xmpp.send_message(sUser, sMessage)
                if bStatus : lStatus.append(sUser)

        iMessageCount = len(lStatus)
        if  iMessageCount < 500:
            logging.info(",".join(lStatus))
        else:
            logging.info("total %s message sent!" % iMessageCount )

        sMessageRely = "%s have already send message to %s users!" % (sMessageFrom, iMessageCount)
        
        return sMessageRely

    def userSetting(self, sCommand):

        if sCommand.lower() == ":off":
            FriendList().delete(sMessageFrom)

        if sCommand.lower() == ":on":    
            FriendList().add(sMessageFrom) 

        return "OK!"

app = webapp.WSGIApplication([
                               ('/_ah/xmpp/message/chat/', Gtalk )],
                              debug=True)

run_wsgi_app(app)

