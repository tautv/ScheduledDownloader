# -*- coding: utf-8 -*-
from os import path
import wx
import configs
import download_manager
import event_manager
import time_helper


# Helper:
def isWidgetWithName(_widget, _instance, _name):
    if(isinstance(_widget, _instance)):
        if (_widget.GetName() == _name):
            return True
    return False


class MainPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.CreateWidgets()
        self.BindWidgets()
        self.GridWidgets()
        self.DynamicEvents = []  # holds tuple with (id, eventobject)
        self.gSizer = wx.FlexGridSizer(6, 10, 10)  # cols, gap, gap
        self.CreateDynamic(None)
        wx.CallAfter(self.UpdateTopTimer)

    def CreateWidgets(self):
        # Panels:
        self.Panel_Top = wx.Panel(self)
        self.Panel_Bottom = wx.Panel(self)
        # Sizers:
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer_Top = wx.BoxSizer(wx.HORIZONTAL)
        self.Sizer_Bottom = wx.BoxSizer(wx.VERTICAL)
        # Top Buttons:
        self.l_TimeNow = wx.StaticText(
            self.Panel_Top, label='1970/01/01 00:00:01')
        self.b_NewDownload = wx.Button(self.Panel_Top, label="Add New Download")

    def BindWidgets(self):
        self.b_NewDownload.Bind(wx.EVT_BUTTON, self.b_NewDownload_Command)

    def GridWidgets(self):
        # Grid Top Panel:
        self.Sizer_Top.Add(self.l_TimeNow)
        self.Sizer_Top.Add(self.b_NewDownload)
        # Grid Main Panels:
        self.Sizer.Add(self.Panel_Top, 0, wx.EXPAND | wx.ALL, border=5)
        self.Sizer.Add(self.Panel_Bottom, 1, wx.EXPAND | wx.ALL, border=5)
        # Set Sizers:
        self.Panel_Top.SetSizer(self.Sizer_Top)
        self.Panel_Bottom.SetSizer(self.Sizer_Bottom)
        self.SetSizer(self.Sizer)

    def CreateDynamic(self, evt):
        # If we created some dynamic widgets already, clear them:
        for _dWidget in self.gSizer.GetChildren():
            _dw = _dWidget.GetWindow()
            if (_dw):
                _dw.Destroy()
        self.gSizer = wx.FlexGridSizer(7, 10, 10)
        self.gSizer.AddGrowableCol(2, 1)
        # ----------------------------
        # Create Dynamic Widgets:
        for i in configs.GetAllSections():
            _d_l_ID = wx.StaticText(
                self.Panel_Bottom, name='ID_%s' % i, label="ID:%s" % i)
            _d_l_Name = wx.StaticText(self.Panel_Bottom, name='Name_%s' % i, label="Name: %s" % configs.GetValue(i, 'Name'))  # noqa
            _d_g_ProgressBar = wx.Gauge(self.Panel_Bottom, name='Gauge_%s' % i, range=100, size=(100, 20), style=wx.GA_HORIZONTAL)  # noqa
            _d_g_RemainingTime = wx.StaticText(
                self.Panel_Bottom, name="Remaining_%s" % i, label="Next Download: 00:00:00")  # noqa
            _d_b_Download = wx.Button(self.Panel_Bottom, name='%s' % i, label="Download Now")  # noqa
            _d_l_LastDownload = wx.StaticText(self.Panel_Bottom,
                                              name="LastDownload_%s" % i,
                                              label="Last Download: %s" %
                                              configs.GetValue(i, 'last_download_time'))  # noqa
            _d_b_Edit = wx.Button(
                self.Panel_Bottom, label="...", name="Edit_%s" % i)
            # Grid:
            self.gSizer.Add(_d_l_ID)
            self.gSizer.Add(_d_l_Name)
            self.gSizer.Add(_d_g_ProgressBar, 0, wx.EXPAND)
            self.gSizer.Add(_d_g_RemainingTime)
            self.gSizer.Add(_d_b_Download)
            self.gSizer.Add(_d_l_LastDownload)
            self.gSizer.Add(_d_b_Edit)
            # Bind Buttons:
            _d_b_Download.Bind(wx.EVT_BUTTON, self._d_b_Download_Command)
            _d_b_Edit.Bind(wx.EVT_BUTTON, self._d_b_Edit_Command)
            self.DynamicEvents.append((i, event_manager.Event(i)))
            self.DynamicEvents[-1][1].Subscribe(self.DynamicEvents_command)
            # Call Timer:
            self.UpdateTimeRemaining(str(i))
        # Add dynamic to bottom panel sizer:
        self.Sizer_Bottom.Add(
            self.gSizer, 1, flag=wx.ALL | wx.EXPAND, border=15)
        # Refresh GUI:
        self.Panel_Bottom.Layout()
        self.parent.Fit()

    def b_NewDownload_Command(self, evt):
        id = configs.GetNextSectionID()
        EditFrame(self, id).ShowModal()

    def _d_b_Download_Command(self, evt):
        id = evt.GetEventObject().GetName()
        dm_d = download_manager.Downloader(id)
        for _dWidget in self.gSizer.GetChildren():
            _dw = _dWidget.GetWindow()
            # Start download thread, disable the Download button
            if(isWidgetWithName(_dw, wx.Button, '%s' % id)):
                if (_dw.IsEnabled()):
                    dm_d.StartThread()
                    _dw.Disable()
            # Disable Edit button while downloading
            if(isWidgetWithName(_dw, wx.Button, 'Edit_%s' % id)):
                    _dw.Disable()

    def _d_b_Edit_Command(self, evt):
        id = evt.GetEventObject().GetName().replace('Edit_', '')
        EditFrame(self, id).ShowModal()

    def DynamicEvents_command(self, msg):
        _id = msg[0]
        _msg = msg[1]
        for _dWidget in self.gSizer.GetChildren():
            _dw = _dWidget.GetWindow()
            # Update Gauge part
            if(isWidgetWithName(_dw, wx.Gauge, 'Gauge_%s' % _id)):
                if(isinstance(_msg, str)):
                    if (_msg == 'Finished'):
                        _dw.SetValue(0)
                    if (_msg == 'Error'):
                        _dw.SetValue(0)
                    if (_msg == 'NoTotalSize'):
                        _dw.Pulse()
                if(isinstance(_msg, float)):
                    wx.CallAfter(_dw.SetValue, _msg)
            # Update StaticText part
            if(isWidgetWithName(_dw, wx.StaticText, 'LastDownload_%s' % _id)):  # noqa
                if(isinstance(_msg, str)):
                    if (_msg == 'Finished'):
                        _time_stamp = time_helper.GetTimestamp()
                        _dw.SetLabel('Last Download: %s' % _time_stamp)  # noqa
                        configs.SetValue(_id, 'last_download_time', _time_stamp)  # noqa
                    if (_msg == 'Error'):
                        _dw.SetLabel('Last Download: %s' % 'Error!')
            # Update Download Button part
            if(isWidgetWithName(_dw, wx.Button, '%s' % _id)):
                if(isinstance(_msg, str)):
                    if (_msg == 'Finished'):
                        _dw.Enable()
                    if (_msg == 'Error'):
                        _dw.Enable()
            # Update Edit Button part
            if(isWidgetWithName(_dw, wx.Button, 'Edit_%s' % _id)):
                if(isinstance(_msg, str)):
                    if (_msg == 'Finished'):
                        _dw.Enable()
                    if (_msg == 'Error'):
                        _dw.Enable()

    def UpdateTopTimer(self):
        self.l_TimeNow.SetLabel(time_helper.GetTimestamp())
        wx.CallLater(1000, self.UpdateTopTimer)

    def UpdateTimeRemaining(self, _id):
        for _dWidget in self.gSizer.GetChildren():
            _dw = _dWidget.GetWindow()
            if(isWidgetWithName(_dw, wx.StaticText, 'Remaining_%s' % _id)):
                _ldt = configs.GetValue(_id, "last_download_time")
                _freq = configs.GetValue(_id, "frequency")
                _rem = time_helper.TimeUntilNextDownload(_ldt, _freq)
                _dw.SetLabel('Next Download: %s' % _rem)
            if(isWidgetWithName(_dw, wx.Button, '%s' % _id)):
                if(time_helper.ShouldDownload(_ldt, _freq)):
                    if(_dw.IsEnabled()):
                        evt = wx.CommandEvent(wx.EVT_BUTTON.typeId)
                        evt.SetId(_dw.GetId())
                        evt.SetEventObject(_dw)
                        wx.PostEvent(_dw, evt)
        wx.CallLater(1000, self.UpdateTimeRemaining, _id)


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None,
                         title="Scheduled Downloader",
                         size=(900, 550))
        self.CreateWidgets()
        self.GridWidgets()

    def CreateWidgets(self):
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        panel = MainPanel(self)
        self.Sizer.Add(panel, 1, wx.EXPAND)

    def GridWidgets(self):
        self.SetSizerAndFit(self.Sizer)


class EditFrame(wx.Dialog):
    def __init__(self, parent, _id):
        self._id = _id
        print(self._id)
        self.parent = parent
        self.isNew = False
        if(self._id not in configs.GetAllSections()):
            configs.AddSection(self._id)
            self.isNew = True
        self.title = "Edit %s" % configs.GetValue(_id, 'Name')
        super().__init__(parent, title=self.title)
        self.CreateWidgets()
        self.BindWidgets()
        self.GridWidgets()

    def CreateWidgets(self):
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer_Flex = wx.FlexGridSizer(2, 5, 5)
        self.Sizer_Flex.AddGrowableCol(1, 1)
        self.Sizer_Buttons = wx.BoxSizer(wx.HORIZONTAL)
        # Widgets
        self.l_ID = wx.StaticText(self, label="ID: %s" % self._id)
        self.l_Name = wx.StaticText(self, label="Name: ")
        self.e_Name = wx.TextCtrl(self, value="%s" % configs.GetValue(self._id, "Name"))  # noqa
        self.l_URL = wx.StaticText(self, label="URL: ")
        self.e_URL = wx.TextCtrl(self, value="%s" % configs.GetValue(self._id, "URL"))  # noqa
        self.l_DestFolder = wx.StaticText(self, label="Destination Path: ")
        self.e_DestFolder = wx.TextCtrl(self, value="%s" % configs.GetValue(self._id, "destination_folder"))  # noqa
        self.l_Frequency = wx.StaticText(self, label="Frequency\n(Days HH:MM:SS): ")
        self.e_Frequency = wx.TextCtrl(self, value="%s" % configs.GetValue(self._id, "frequency"))  # noqa
        # Widgets Buttons
        self.b_Save = wx.Button(self, label="Save")
        self.b_Reset = wx.Button(self, label="Reset")
        if (self.isNew):
            self.b_Reset.Disable()
        self.b_Delete = wx.Button(self, label="Delete")
        self.b_Cancel = wx.Button(self, label="Cancel")
        if (self.isNew):
            self.b_Cancel.Disable()

    def BindWidgets(self):
        self.b_Save.Bind(wx.EVT_BUTTON, self.b_Save_Command)
        self.b_Reset.Bind(wx.EVT_BUTTON, self.b_Reset_Command)
        self.b_Delete.Bind(wx.EVT_BUTTON, self.b_Delete_Command)
        self.b_Cancel.Bind(wx.EVT_BUTTON, self.b_Cancel_Command)

    def b_Save_Command(self, evt):
        # get values to check:
        _freq = self.e_Frequency.GetValue()
        _dest = self.e_DestFolder.GetValue()
        # check values:
        if not (time_helper.IsValidFrequency(_freq)):
            wx.MessageBox('''Frequency format not valid!
                            It has to be:
                            "DD HH:MM:SS"

                            Example: (0 23:59:59)
                            (0 days 23 hours:59 Minutes:59 Seconds)

                            Minimum download frequency is every minute''',
                          'ERROR', wx.OK | wx.ICON_INFORMATION)
            return
        if not (path.exists(_dest)):
            wx.MessageBox('''Destination path is not valid!
                             Please check the folder exists.''',
                          'ERROR', wx.OK | wx.ICON_INFORMATION)
            return
        # if validation passed - update:
        configs.SetValue(self._id, 'Frequency', _freq)  # noqa
        configs.SetValue(self._id, 'Destination_Folder', _dest)  # noqa
        configs.SetValue(self._id, 'URL', self.e_URL.GetValue())
        configs.SetValue(self._id, 'Name', self.e_Name.GetValue())
        wx.CallAfter(self.parent.CreateDynamic, None)
        wx.CallAfter(self.Close)

    def b_Reset_Command(self, evt):
        self.e_Name.SetValue(configs.GetValue(self._id, 'Name'))
        self.e_URL.SetValue(configs.GetValue(self._id, 'URL'))
        self.e_DestFolder.SetValue(configs.GetValue(self._id, 'Destination_Folder'))  # noqa
        self.e_Frequency.SetValue(configs.GetValue(self._id, 'Frequency'))  # noqa

    def b_Cancel_Command(self, evt):
        wx.CallAfter(self.Close)

    def b_Delete_Command(self, evt):
        configs.RemoveSection(self._id)
        wx.CallAfter(self.parent.CreateDynamic, None)
        wx.CallAfter(self.Close)

    def GridWidgets(self):
        self.Sizer.Add(self.l_ID, 0, wx.CENTER)
        #
        self.Sizer_Flex.Add(self.l_Name, border=5)
        self.Sizer_Flex.Add(self.e_Name, 0, wx.EXPAND)
        self.Sizer_Flex.Add(self.l_URL, border=5)
        self.Sizer_Flex.Add(self.e_URL, 0, wx.EXPAND)
        self.Sizer_Flex.Add(self.l_DestFolder, border=5)
        self.Sizer_Flex.Add(self.e_DestFolder, 0, wx.EXPAND)
        self.Sizer_Flex.Add(self.l_Frequency, border=5)
        self.Sizer_Flex.Add(self.e_Frequency, 0, wx.EXPAND)
        #
        self.Sizer_Buttons.Add(self.b_Save, border=5)
        self.Sizer_Buttons.Add(self.b_Reset, border=5)
        self.Sizer_Buttons.Add(self.b_Delete, border=5)
        self.Sizer_Buttons.Add(self.b_Cancel, border=5)
        #
        self.Sizer.Add(self.Sizer_Flex, 1, flag=wx.ALL | wx.EXPAND, border=15)
        self.Sizer.Add(self.Sizer_Buttons, 0, wx.CENTER, border=15)
        self.Layout()


def LaunchGUI():
    APPLICATION = wx.App(False)
    _MainFrame = MainFrame()
    _MainFrame.Show()
    APPLICATION.MainLoop()
