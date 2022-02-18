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
        # normalizing the path from configs, given by the user,
        # parsing the given url, then getting filename-only string
        # joining normalized destination path and filename-only string
        # TODO: Do a proper URL parse to get the real filename+extension
        self.dest_path = os.path.join(os.path.normpath(GetValue(
            self._id, 'destination_folder')),
            os.path.basename(urlparse(self.url).path))
        #
        self.last_download_time = GetValue(self._id, 'last_download_time')
        self.event = event_manager.Event(str(_id))
        self.stopped = False
        self.download_percentage = 0
        # need this flag:
        ssl._create_default_https_context = ssl._create_unverified_context

    def StartThread(self):
        self.start()

    def StopThread(self):
        self.stopped = True

    def Handle_Progress(self, blocknum, blocksize, totalsize):
        readed_data = blocknum * blocksize
        if totalsize > 0:
            self.download_percentage = readed_data * 100 / totalsize
            # slow down the return of the percentages:
            if (int(self.download_percentage) % 5 == 0):
                self.event.SendMessage((self._id, self.download_percentage))

    def run(self):
        try:
            if (not self.stopped):
                self.event.SendMessage((self._id, self.download_percentage))
                if(self.dest_path != ''):
                    urllib.request.urlretrieve(
                        self.url, self.dest_path, self.Handle_Progress)
                else:
                    raise Exception('Destination is empty!')
                # end of main job
                self.event.SendMessage((self._id, self.download_percentage))
                print(self.dest_path)
            else:
                self.event.SendMessage((self._id, "Stopped"))
            if(not self.stopped):
                self.event.SendMessage((self._id, "Finished"))
        except Exception as e:
            print(e)
            self.event.SendMessage((self._id, "Error"))
