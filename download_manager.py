# -*- coding: utf-8 -*-
import time
import os
from threading import Thread
import urllib.request
import ssl
from urllib.parse import urlparse
import event_manager
from configs import GetValue
# from configs import SetValue
# import time_helper


class Downloader(Thread):
    def __init__(self, _id):
        super().__init__()
        self.daemon = True  # kills the thread when application quits
        self._id = _id
        self.url = GetValue(self._id, 'url')
        self.event = event_manager.Event(str(_id))
        self.stopped = False
        self._last_message_timer = time.time()
        # need this flag
        ssl._create_default_https_context = ssl._create_unverified_context
        # parse the URL; if it can't find the extension, try HTTP Head:
        _fname = os.path.basename(urlparse(self.url).path)
        if '.' not in _fname[-6:]:
            try:
                req = urllib.request.Request(self.url, method='HEAD')
                r = urllib.request.urlopen(req)
                _fname = r.info().get_filename()
            except Exception as e:
                self.StopThread()
                self.event.SendMessage((self._id, "Error"))
                print(e)
        # normalizing the path from configs, given by the user,
        # parsing the given url, then getting filename-only string
        # joining normalized destination path and filename-only string
        self.dest_path = os.path.join(os.path.normpath(GetValue(
            self._id, 'destination_folder')),
            os.path.basename(_fname))
        self.download_percentage = 0.00

    def StartThread(self):
        self.start()

    def StopThread(self):
        self.stopped = True

    def Handle_Progress(self, blocknum, blocksize, totalsize):
        if self.stopped:
            raise
        time_now = time.time()
        if totalsize <= 0:
            if time_now - self._last_message_timer > 0.1:
                self.event.SendMessage((self._id, "NoTotalSize"))
        read_data = blocknum * blocksize
        if totalsize > 0:
            self.download_percentage = read_data * 100 / totalsize
            if time_now-self._last_message_timer > 0.1:
                self.event.SendMessage((self._id, self.download_percentage))
                self._last_message_timer = time.time()

    def run(self):
        if not self.stopped:
            self.event.SendMessage((self._id, self.download_percentage))
            if self.dest_path == '':
                raise Exception("Destination path is empty")
            try:
                urllib.request.urlretrieve(
                    self.url, self.dest_path, self.Handle_Progress)
                self.event.SendMessage((self._id, self.download_percentage))
                self.event.SendMessage((self._id, "Finished"))
            except Exception as e:
                print(e)
                self.event.SendMessage((self._id, "Error"))
        else:
            self.event.SendMessage((self._id, "Stopped"))
