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
from Model import FriendList
from Model import CacheUserList
from google.appengine.api import taskqueue
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

        lAdmin = ['litrin@gmail.com', 'hanyuxia@gmail.com']

        #FriendList().add(sMessageFrom)       
        if sMessageFrom in lAdmin:
            sMessageRely = self.sendMessage(sMessage)
        else:
            FriendList().add(sMessageFrom)
            sMessageRely = self.userSetting(sMessage)

        aMessage.reply(sMessageRely)

    def sendMessage(self, sMessage):
        lUser = FriendList().getAllUniq():
        lStatus = []

        iMessageCount = len(lUser)
        if  iMessageCount < 500:
            for sUser in lUser:
                bStatus = xmpp.send_message(sUser, sMessage)
                lStatus.append(sUser)

            logging.info(",".join(lStatus))

        else:
            self.bgSend(lUser)  
            logging.info("total %s message add to queue!" % iMessageCount )

        sMessageRely = "%s have already send message to %s users!" % (sMessageFrom, iMessageCount)
        
        return sMessageRely


    def userSetting(self, sCommand):

        if sCommand.lower() == "off":
            FriendList().delete(sMessageFrom)

        if sCommand.lower() == "on":    
            FriendList().add(sMessageFrom) 

        return "OK!"


    def bgSend(self, lUser):
        iGroup = 0 
        loop = 0
        lUserSplit = []

        for sUser in lUser:
            loop += 1
            lUserSplit.append(sUser)

            if loop % 100 == 0:
                oCacheHandle = CacheUserList(iGroup)
                oCacheHandle.add(lUserSplit)
                taskqueue.add(url='/background', params={'group': iGroup})

                lUserSplit = []
                iGroup += 1

        oCacheHandle = CacheUserList(iGroup)
        oCacheHandle.add(lUserSplit)
        taskqueue.add(url='/background', params={'group': iGroup})
        
        return True
        

class BGSend(webapp.RequestHandler):
    def post(self):
        sGroup = self.request.get('group')
        oCacheHandle = CacheUserList(sGroup)
        lUser = oCacheHandle.pop()
        lStatus = []
        for sUser in lUser:
            bStatus = xmpp.send_message(sUser, sMessage)
            lStatus.append(sUser)

        logging.info(",".join(lStatus))

        self.finish("ok!")

app = webapp.WSGIApplication([ ('/background', BGSend),
                               ('/_ah/xmpp/message/chat/', Gtalk )],
                              debug=True)

run_wsgi_app(app)

