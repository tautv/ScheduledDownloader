# -*- coding: utf-8 -*-
import wx
import configs

class MainPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.SetBackgroundColour('#6f8089') # Test Purposes only
        self.createWidgets()
        self.bindWidgets()
        self.gridWidgets()
        self.createDynamicWidgets()

    def createWidgets(self):
        self.b_Temp = wx.Button(self, label="Test")

    def bindWidgets(self):
        self.b_Temp.Bind(wx.EVT_BUTTON, self.b_Temp_Command)

    def gridWidgets(self):
        pass

    def b_Temp_Command(self, evt):
        self.createDynamicWidgets()

    def createDynamicWidgets(self):
        print('----------------')


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None,
                         title="Scheduled Downloader",
                         size=(800,550))
        self.createWidgets()
        self.bindWidgets()
        self.gridWidgets()

    def createWidgets(self):
        self.panel = MainPanel(self)

    def bindWidgets(self):
        pass

    def gridWidgets(self):
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.panel, 1, wx.EXPAND|wx.ALL)

def LaunchGUI():
    APPLICATION = wx.App(False)
    _MainFrame = MainFrame()
    _MainFrame.Show()
    APPLICATION.MainLoop()
