#!/usr/bin/env python
#
# Copyright 2013 Litrin J.
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
from google.appengine.api import taskqueue
from Model import CacheUserList
from google.appengine.api import xmpp

class SendMessage:
    
    Message = None
    User = None
    
    def __init__(self, sUser=None, sMessage=None):
        if sUser is not None:
            self.setUser(sUser)
        if sMessage is not None:
            self.setMessage(sMessage)
    
            
    def setUser(self, sUser):
        self.User = sUser
    
        
    def setMessage(self, sMessage):
        self.Message = sMessage
    
    
    def send(self):
        if self.User is not None and self.Message is not None:
            return xmpp.send_message(self.User, self.Message) == xmpp.NO_ERROR
            
        return False
            
    def sendMulit(self, lUser):
        if self.Message is None:
            return []
        
        lStatus =[]
        for sUser in lUser:
            if xmpp.send_message(sUser, self.Message) == xmpp.NO_ERROR:
                lStatus.append(sUser)
                
        return lStatus
        
    def backGroundTask(self, lUser, sTaskUrl='/background'):

        iGroup = 0 
        loop = 0
        lUserSplit = []

        for sUser in lUser:
            loop += 1
            lUserSplit.append(sUser)

            if loop & 0x7F == 0:
                oCacheHandle = CacheUserList(iGroup)
                oCacheHandle.add(lUserSplit)
                
                params={
                        'group': iGroup, 
                        'message': self.Message
                        }
                        
                taskqueue.add(url=sTaskUrl, params=params)

                lUserSplit = []
                iGroup += 1

        oCacheHandle = CacheUserList(iGroup)
        oCacheHandle.add(lUserSplit)
        params = {
                'group': iGroup, 
                'message': self.Message
                }
        taskqueue.add(url=sTaskUrl, params=params)
        
        return True