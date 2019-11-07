from handler import Handler
import wx
import json


class Window(wx.Frame):

    def __init__(self, *args, **kw):
        super(Window, self).__init__(*args, **kw)

        self.pnl = wx.Panel(self)

        wx.StaticText(self.pnl, label='源图:', pos=(10, 10))
        self.source_path = wx.TextCtrl(self.pnl, pos=(10, 36), size=(350, 36))
        self.source_path.Bind(wx.EVT_LEFT_UP, self.on_select_source_path)

        wx.StaticText(self.pnl, label='保存目录:', pos=(10, 82))
        self.save_path = wx.TextCtrl(self.pnl, pos=(10, 108), size=(350, 36))
        self.save_path.Bind(wx.EVT_LEFT_UP, self.on_select_save_path)

        wx.StaticText(self.pnl, label='颜色:', pos=(10, 154))
        self.signature_color = wx.StaticText(self.pnl, pos=(10, 180), size=(150, 36))
        self.signature_color.SetBackgroundColour('black')
        self.signature_color.Bind(wx.EVT_LEFT_UP, self.OnSignatureColorClick)

        wx.StaticText(self.pnl, label='标题:', pos=(10, 226))
        self.title = wx.TextCtrl(self.pnl, pos=(10, 252), size=(350, 36))

        self.loadConfig()

        wx.Button(self.pnl, label="开始", pos=(10, 520), size=(70, 36)).Bind(wx.EVT_BUTTON, self.ProcessImages)
        wx.Button(self.pnl, label="保存配置", pos=(290, 520), size=(70, 36)).Bind(wx.EVT_BUTTON, self.SaveConfig)

        self.SetSize((370, 600))
        self.SetTitle('图片处理工具')
        self.Centre()
        self.Show(True)

    def SaveConfig(self, event):
        config = self.readConfig()
        config.update(self.getConfig())
        with open('config.json', 'w') as f:
            f.write(json.dumps(config, ensure_ascii=False, indent=True))

    def getConfig(self):
        config = {
            'sourcePath': self.source_path.GetValue(),
            'savePath': self.save_path.GetValue(),
            'signatureColor': list(self.signature_color.GetBackgroundColour()),
            'title': self.title.GetValue(),
        }
        return config

    def readConfig(self):
        f = open('config.json', encoding='utf-8')
        config = {
            'sourcePath': '',
            'savePath': '',
            'signatureColor': 'black',
            'title': '',
            'titleColor': ''
        }
        config.update(json.load(f))
        return config

    def loadConfig(self):
        config = self.readConfig()
        self.source_path.SetValue(config['sourcePath'])
        self.save_path.SetValue(config['savePath'])
        self.signature_color.SetBackgroundColour(config['signatureColor'])
        self.title.SetValue(config['title'])

    def OnSignatureColorClick(self, event):
        dlg = wx.ColourDialog(self)
        dlg.GetColourData().SetChooseFull(True)  # 创建颜色对象数据
        if dlg.ShowModal() == wx.ID_OK:
            self.signature_color.SetBackgroundColour(dlg.GetColourData().GetColour())  # 根据选择设置画笔颜色
        dlg.Destroy()

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

    def ProcessImages(self, event):
        config = self.readConfig()
        config.update(self.getConfig())
        Handler(config).run()


def main():
    ex = wx.App()
    Window(None)
    ex.MainLoop()


if __name__ == '__main__':
    main()
