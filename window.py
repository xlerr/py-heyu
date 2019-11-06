import wx


class Window(wx.Frame):

    def __init__(self, *args, **kw):
        super(Window, self).__init__(*args, **kw)

        self.pnl = wx.Panel(self)

        wx.StaticText(self.pnl, label='源图:', style=wx.ALIGN_CENTRE, pos=(10, 10))
        self.source_path = wx.TextCtrl(self.pnl, pos=(10, 36), size=(350, 36))

        select_path = wx.Button(self.pnl, label="浏览...", pos=(370, 36), size=(70, 36))
        select_path.Bind(wx.EVT_BUTTON, self.on_select_source_path)

        wx.StaticText(self.pnl, label='保存目录:', style=wx.ALIGN_CENTRE, pos=(10, 82))
        self.save_path = wx.TextCtrl(self.pnl, pos=(10, 108), size=(350, 36))

        select_path = wx.Button(self.pnl, label="浏览...", pos=(370, 108), size=(70, 36))
        select_path.Bind(wx.EVT_BUTTON, self.on_select_save_path)

        self.SetSize((450, 300))
        self.SetTitle('图片处理工具')
        self.Centre()
        self.Show(True)

    def on_select_source_path(self, event):
        dlg = wx.DirDialog(self.pnl, u"选择文件夹", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.source_path.SetValue(dlg.GetPath())
        dlg.Destroy()

    def on_select_save_path(self, event):
        dlg = wx.DirDialog(self.pnl, u"选择文件夹", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.save_path.SetValue(dlg.GetPath())
        dlg.Destroy()



def main():
    ex = wx.App()
    Window(None)
    ex.MainLoop()


if __name__ == '__main__':
    main()
