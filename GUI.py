# -*- coding: utf-8 -*-
import wx
import configs
import download_manager
import event_manager


class MainPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.SetBackgroundColour('#6f8089')
        self.CreateWidgets()
        self.BindWidgets()
        self.GridWidgets()
        self.DynamicEvents = []  # holds tuple with (id, eventobject)
        self.gSizer = wx.FlexGridSizer(6, 10, 10)  # cols, gap, gap
        self.CreateDynamic(None)

    def CreateWidgets(self):
        # Panels:
        self.Panel_Top = wx.Panel(self)
        self.Panel_Top.SetBackgroundColour('#551111')
        self.Panel_Bottom = wx.Panel(self)
        self.Panel_Bottom.SetBackgroundColour('#115511')
        # Sizers:
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer_Top = wx.BoxSizer(wx.HORIZONTAL)
        self.Sizer_Bottom = wx.BoxSizer(wx.VERTICAL)
        # Top Buttons:
        self.b_Button1 = wx.Button(self.Panel_Top, label="Button 1")
        self.b_Button2 = wx.Button(self.Panel_Top, label="Button 2")

    def BindWidgets(self):
        self.b_Button1.Bind(wx.EVT_BUTTON, self.CreateDynamic)

    def GridWidgets(self):
        # Grid Top Panel:
        self.Sizer_Top.Add(self.b_Button1)
        self.Sizer_Top.Add(self.b_Button2)
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
        self.gSizer = wx.FlexGridSizer(6, 10, 10)
        self.gSizer.AddGrowableCol(2, 1)
        # ----------------------------
        # Create Dynamic Widgets:
        for i in configs.GetAllSections():
            _d_l_ID = wx.StaticText(
                self.Panel_Bottom, name='ID_%s' % i, label="ID:%s" % i)
            _d_l_Name = wx.StaticText(self.Panel_Bottom, name='Name_%s' % i,
                                      label="Download Name: %s" % configs.GetValue(i, 'Name'))
            _d_g_ProgressBar = wx.Gauge(
                self.Panel_Bottom, name='Gauge_%s' % i, range=100, style=wx.GA_HORIZONTAL)
            _d_b_Download = wx.Button(
                self.Panel_Bottom, name='%s' % i, label="Download Now")
            _d_l_LastDownload = wx.StaticText(self.Panel_Bottom,
                                              name="LastDownload_%s" % i,
                                              label="Last Download Time: %s" %
                                              configs.GetValue(i, 'last_download_time'))
            _d_b_Edit = wx.Button(
                self.Panel_Bottom, label="...", name="%s" % i)
            # Grid:
            self.gSizer.Add(_d_l_ID)
            self.gSizer.Add(_d_l_Name)
            self.gSizer.Add(_d_g_ProgressBar, 0, wx.EXPAND)
            self.gSizer.Add(_d_b_Download)
            self.gSizer.Add(_d_l_LastDownload)
            self.gSizer.Add(_d_b_Edit)
            # Bind Buttons:
            _d_b_Download.Bind(wx.EVT_BUTTON, self._d_b_Download_Command)
            _d_b_Edit.Bind(wx.EVT_BUTTON, self._d_b_Edit_Command)
            self.DynamicEvents.append((i, event_manager.Event(i)))
            self.DynamicEvents[-1][1].Subscribe(self.DynamicEvents_command)
        # Add dynamic to bottom panel sizer:
        self.Sizer_Bottom.Add(
            self.gSizer, 1, flag=wx.ALL | wx.EXPAND, border=15)
        # Refresh GUI:
        self.Panel_Bottom.Layout()
        self.parent.Fit()

    def _d_b_Download_Command(self, evt):
        id = evt.GetEventObject().GetName()
        download_manager.Downloader(id).StartThread()
        for _dWidget in self.gSizer.GetChildren():
            _dw = _dWidget.GetWindow()
            if(isinstance(_dw, wx.Button)):
                if (_dw.GetName() == '%s' % id):
                    _dw.Disable()

    def _d_b_Edit_Command(self, evt):
        id = evt.GetEventObject().GetName()
        EditFrame(self, id).ShowModal()

    def DynamicEvents_command(self, msg):
        _id = msg[0]
        _msg = msg[1]
        if(isinstance(_msg, float)):
            for _dWidget in self.gSizer.GetChildren():
                _dw = _dWidget.GetWindow()
                if(isinstance(_dw, wx.Gauge)):
                    if (_dw.GetName() == 'Gauge_%s' % _id):
                        wx.CallAfter(_dw.SetValue, _msg)
        if(isinstance(_msg, str)):
            if (_msg == 'Finished'):
                for _dWidget in self.gSizer.GetChildren():
                    _dw = _dWidget.GetWindow()
                    if(isinstance(_dw, wx.Gauge)):
                        if (_dw.GetName() == 'Gauge_%s' % _id):
                            _dw.SetValue(0)
                    if(isinstance(_dw, wx.StaticText)):
                        if (_dw.GetName() == 'LastDownload_%s' % _id):
                            _dw.SetLabel('Last Download Time: %s' % 'Now')
                    if(isinstance(_dw, wx.Button)):
                        if (_dw.GetName() == '%s' % _id):
                            _dw.Enable()


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None,
                         title="Scheduled Downloader",
                         size=(850, 550))
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
        self.title = "Edit %s" % _id
        super().__init__(parent, title=self.title)
        self.CreateWidgets()
        self.GridWidgets()

    def CreateWidgets(self):
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.l_Test = wx.StaticText(self, label=self.title)

    def GridWidgets(self):
        self.Sizer.Add(self.l_Test)


def LaunchGUI():
    APPLICATION = wx.App(False)
    _MainFrame = MainFrame()
    _MainFrame.Show()
    APPLICATION.MainLoop()
