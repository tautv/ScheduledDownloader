# -*- coding: utf-8 -*-
from threading import Thread
import urllib.request
import ssl
from urllib.parse import urlparse
import os
import event_manager
from configs import GetValue


class Downloader(Thread):
    def __init__(self, _id):
        super().__init__()
        self._id = _id
        self.url = GetValue(self._id, 'url')
        self.event = event_manager.Event(str(_id))
        self.stopped = False
        # need this flag
        ssl._create_default_https_context = ssl._create_unverified_context
        # parse the URL; if it can't find the extension, try HTTP Head:
        _fname = os.path.basename(urlparse(self.url).path)
        if '.' not in _fname:
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
        if not self.stopped:
            if totalsize < 0:
                self.event.SendMessage((self._id, "NoTotalSize"))
            read_data = blocknum * blocksize
            if totalsize > 0:
                self.download_percentage = read_data * 100 / totalsize
                # slow down the return of the percentages:
                if int(self.download_percentage) % 5 == 0:
                    self.event.SendMessage(
                        (self._id, self.download_percentage))

    def run(self):
        if not self.stopped:
            self.event.SendMessage((self._id, self.download_percentage))
            if self.dest_path != '':
                try:
                    urllib.request.urlretrieve(
                        self.url, self.dest_path, self.Handle_Progress)
                except Exception as e:
                    print(e)
                    self.event.SendMessage((self._id, "Error"))
                    self.StopThread()
            else:
                self.event.SendMessage((self._id, "Error"))
                raise Exception('Destination is empty!')
            # end of main job
            self.event.SendMessage((self._id, self.download_percentage))
            self.event.SendMessage((self._id, "Finished"))
        else:
            self.event.SendMessage((self._id, "Stopped"))
