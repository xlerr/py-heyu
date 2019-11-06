import wx  # 导入wxPython
import os
import re
from handler import Handler


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


file_dir = '/home/moment/PycharmProjects/first/static'
# print(findImageFile(file_dir))
# exit(0)

app = wx.App()
frame = wx.Frame(parent=None, title='第一个窗口程序')  # 创建顶级窗口
path_text = wx.TextCtrl(frame, pos=(5, 5), size=(350, 24), value=file_dir)
start_button = wx.Button(frame, label="打开", pos=(370, 5), size=(50, 24))
start_button.Bind(wx.EVT_BUTTON, process_img)
frame.Show()  # 显示窗口
app.MainLoop()  # 调用App类的MainLoop()主循环方法
