#-*- coding:utf-8 -*-
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
from Controller import SendMessage

from google.appengine.api import taskqueue
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import xmpp


class Gtalk(webapp.RequestHandler):
    def post(self):
        self.GetMessage()
    
    def GetMessage(self):
        aMessage = xmpp.Message(self.request.POST)
        sMessageFrom = aMessage.sender[:aMessage.sender.find('/')].lower()
        sMessage = aMessage.body

        lAdmin = ('litrin@gmail.com', 'hanyuxia@gmail.com')

        #FriendList().add(sMessageFrom)       
        if sMessageFrom in lAdmin:
            sMessageRely = self.sendMessage(sMessage)
        else:
            FriendList().add(sMessageFrom)
            sMessageRely = self.userSetting(sMessage, sMessageFrom)
            
        aMessage.reply(sMessageRely)
        
    def sendMessage(self, sMessage):
        lUser = FriendList().getAllUniq()
        lStatus = []

        iMessageCount = len(lUser)
        xmppHandle = SendMessage()
        xmppHandle.setMessage(sMessage)
        
        if iMessageCount < 300:
            
            lStatus = xmppHandle.sendMulit(lUser)
            sMessageRely = u"%s个用户将会收到消息!" % (iMessageCount)

        else:
            xmppHandle.backGroundTask(lUser)
            logging.info("total %s message add to queue!" % iMessageCount )
            
            sMessageRely = u"%s个用户将会收到消息，在%s秒之内请不要发送消息！" % (
                    iMessageCount, int(iMessageCount / 500)+5)
        
        
        return sMessageRely


    def userSetting(self, sCommand, sMessageFrom):
        message = u'不支持输入的命令"%s",请输入on或off!' % sCommand
        if sCommand.lower() in ("off", "/off"):
            FriendList().delete(sMessageFrom)
            message = u'静默模式已被激活！'

        if sCommand.lower() in ("on", "/on"):    
            FriendList().add(sMessageFrom)
            message = u'收听模式已被激活！'

        return message
        

app = webapp.WSGIApplication([ 
                               ('/_ah/xmpp/message/chat/', Gtalk )
                              ],
                              debug=True)

run_wsgi_app(app)

