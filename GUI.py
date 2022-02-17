# -*- coding: utf-8 -*-
import wx
import configs

class MainPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.SetBackgroundColour('#6f8089')
        self.CreateWidgets()
        self.BindWidgets()
        self.GridWidgets()
        self.DynamicSizers = []
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
        self.Sizer.Add(self.Panel_Top, 0, wx.EXPAND|wx.ALL)
        self.Sizer.Add(self.Panel_Bottom, 1, wx.EXPAND|wx.ALL)
        # Set Sizers:
        self.Panel_Top.SetSizer(self.Sizer_Top)
        self.Panel_Bottom.SetSizer(self.Sizer_Bottom)
        self.SetSizer(self.Sizer)

    def CreateDynamic(self, evt):
        # If we created some dynamic widgets already, clear them:
        if(len(self.DynamicSizers)>0):
            for _dSizer in self.DynamicSizers:
                for _dWidget in _dSizer.GetChildren():
                    _dw = _dWidget.GetWindow()
                    if(_dw!= None):
                        _dw.Destroy()
            self.DynamicSizers = []
        # ----------------------------
        # Create Dynamic Widgets:
        for i in configs.GetAllSections():
            _dSizer = wx.BoxSizer(wx.HORIZONTAL)
            _d_l_ID = wx.StaticText(self.Panel_Bottom, label="ID:%s" %i)
            _d_l_Name = wx.StaticText(self.Panel_Bottom, label="Supplier Name: %s" % configs.GetValue(i, 'Name'))
            _d_g_ProgressBar = wx.Gauge(self.Panel_Bottom, range=100, style=wx.GA_HORIZONTAL)
            _d_b_Download = wx.Button(self.Panel_Bottom, label="Download Now", name="%s" %i)
            _d_l_LastDownload = wx.StaticText(self.Panel_Bottom, label="Last Download Time: %s" % configs.GetValue(i, 'last_download_time'))
            _d_b_Edit = wx.Button(self.Panel_Bottom, label="...", name="%s" %i)
            # Grid:
            _dSizer.AddSpacer(10)
            _dSizer.Add(_d_l_ID, 0, wx.LEFT)
            _dSizer.AddSpacer(10)
            _dSizer.Add(_d_l_Name, 0, wx.LEFT)
            _dSizer.AddSpacer(10)
            _dSizer.Add(_d_g_ProgressBar, 1, wx.CENTER|wx.EXPAND)
            _dSizer.AddSpacer(10)
            _dSizer.Add(_d_b_Download, 0, wx.CENTER)
            _dSizer.AddSpacer(10)
            _dSizer.Add(_d_l_LastDownload, 0, wx.CENTER|wx.EXPAND)
            _dSizer.AddSpacer(10)
            _dSizer.Add(_d_b_Edit, 0, wx.RIGHT)
            _dSizer.AddSpacer(10)
            # Bind Buttons:
            _d_b_Download.Bind(wx.EVT_BUTTON, self._d_b_Download_Command)
            _d_b_Edit.Bind(wx.EVT_BUTTON, self._d_b_Edit_Command)
            # Add dynamic sizer to bottom panel
            self.Sizer_Bottom.Add(_dSizer)
            # Add this new sizer to a list for later use:
            self.DynamicSizers.append(_dSizer)
            # layout it all:
            self.Panel_Bottom.Layout()

    def _d_b_Download_Command(self, evt):
        id = evt.GetEventObject().GetName()
        print("Event for ID: %s" %id)

    def _d_b_Edit_Command(self, evt):
        id = evt.GetEventObject().GetName()
        print("Event for ID: %s" %id)
        EditFrame(self, id).ShowModal()

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None,
                         title="Scheduled Downloader",
                         size=(800,550))
        self.CreateWidgets()
        self.GridWidgets()

    def CreateWidgets(self):
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        panel = MainPanel(self)
        self.Sizer.Add(panel, 1, wx.EXPAND)

    def GridWidgets(self):
        self.SetSizer(self.Sizer)
        #self.Fit()

class EditFrame(wx.Dialog):
    def __init__(self, parent, _id):
        self._id = _id
        self.title = "Edit %s" %_id
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
