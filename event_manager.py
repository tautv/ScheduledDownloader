# -*- coding: utf-8 -*-
from pubsub import pub

class Event():
    def __init__(self, name):
        self.name = name

    def SendMessage(self, msg=''):
        pub.sendMessage(self.name, msg=msg)

    def Subscribe(self, func):
        pub.subscribe(func, self.name)
