import wx  # 导入wxPython
import os
import re
from handler import Handler
from window import Window

def findImageFile(dir):
    filenames = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            if re.search('.(jpe?g|png)$', file, re.M | re.I):
                filenames.append(file)
    return filenames


def process_img(event):
    path = path_text.GetValue()
    files = findImageFile(path)
    handler = Handler(files, path, './temp')
    handler.run()


def on_select(event):
    path = ''
    dlg = wx.DirDialog(frame, u"选择文件夹", style=wx.DD_DEFAULT_STYLE)
    if dlg.ShowModal() == wx.ID_OK:
        path = dlg.GetPath()  # 文件夹路径

    dlg.Destroy()

    path_text.SetValue(path)

    return path


file_dir = '/home/moment/PycharmProjects/first/static'
# print(findImageFile(file_dir))
# exit(0)

app = wx.App()
frame = wx.Frame(parent=None, title='图片处理', size=(500, 300))  # 创建顶级窗口

path_text = wx.TextCtrl(frame, pos=(5, 5), size=(350, 36), value=file_dir)
select_path = wx.Button(frame, label="浏览...", pos=(360, 5), size=(70, 36))
select_path.Bind(wx.EVT_BUTTON, on_select)

start_button = wx.Button(frame, label="开始", pos=(225, 200), size=(50, 36))
start_button.Bind(wx.EVT_BUTTON, process_img)
frame.Show()  # 显示窗口
app.MainLoop()  # 调用App类的MainLoop()主循环方法
