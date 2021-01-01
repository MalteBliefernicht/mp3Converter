from shutil import copyfile, rmtree
from unidecode import unidecode
from threading import Thread
import wx
import os
from pydub import AudioSegment
from time import sleep
import re



class FileDrop(wx.FileDropTarget):
    def __init__(self, parent):
        wx.FileDropTarget.__init__(self)
        self.parent = parent
        
    def OnDropFiles(self,x,y,filenames):
        extensions = ['mp4', 'ogg', 'flac', 'm4a', 'wav']
        
        self.parent.SetInsertionPointEnd()
        
        for name in filenames:
            res = re.search(r".*\.([a-z4]+)$", name)
            if res.group(1) in extensions:
                self.parent.update_dropbox(os.path.basename(name) + '\n')
                self.parent.path_list.append(name)
            else:
                pass
            

class MP3Converter(wx.Frame):
    def __init__(self):
        super(MP3Converter, self).__init__(parent=None, title='MP3Converter',
            size=(350,350))
        self.Centre()
        self.panel = wx.Panel(self)
        self.file_drop = FileDrop(self)
        self.quality_choice = ['128 kb/s', '192 kb/s', '256 kb/s', '320 kb/s']
        self.save_location = os.getcwd()
        self.path_list = []
        
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        text1 = wx.StaticText(self.panel, label='Drop Window')
        sizer1.Add(text1, flag=wx.TOP | wx.LEFT, border=10)
        main_sizer.Add(sizer1)
        
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.drop_box = wx.TextCtrl(self.panel,
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)
        sizer2.Add(self.drop_box,proportion=1,
            flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        main_sizer.Add(sizer2, proportion=1, flag=wx.EXPAND)
        
        sizer2b = wx.BoxSizer(wx.HORIZONTAL)
        button2b = wx.Button(self.panel, label='Clear')
        button2b.Bind(wx.EVT_BUTTON, self.clear_button)
        sizer2b.Add(button2b, flag=wx.LEFT, border=10)
        main_sizer.Add(sizer2b)
        
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        text3 = wx.StaticText(self.panel, label='Select Quality')
        sizer3.Add(text3, flag=wx.LEFT | wx.TOP, border=10)
        text3a = wx.StaticText(self.panel)
        sizer3.Add(text3a, flag=wx.LEFT, border=30)
        text3b = wx.StaticText(self.panel, label='Save MP3s to')
        sizer3.Add(text3b, flag=wx.LEFT | wx.TOP, border=10)
        main_sizer.Add(sizer3)
        
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        self.choice4 = wx.Choice(self.panel, choices=self.quality_choice)
        self.choice4.SetSelection(0)
        sizer4.Add(self.choice4, flag=wx.LEFT, border=10)
        text4 = wx.StaticText(self.panel)
        sizer4.Add(text4, flag=wx.LEFT, border=30)
        button4 = wx.Button(self.panel, label='Browse')
        button4.Bind(wx.EVT_BUTTON, self.browse_button)
        sizer4.Add(button4, flag=wx.LEFT, border=10)
        self.text_box = wx.TextCtrl(self.panel)
        self.text_box.SetValue(os.getcwd())
        sizer4.Add(self.text_box, flag=wx.LEFT, border=5)
        main_sizer.Add(sizer4)
        
        sizer_empty = wx.BoxSizer(wx.HORIZONTAL)
        text_empty = wx.StaticText(self.panel)
        sizer_empty.Add(text_empty)
        main_sizer.Add(sizer_empty)
        
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        button5 = wx.Button(self.panel, label='Convert')
        button5.Bind(wx.EVT_BUTTON, self.convert_thread)
        sizer5.Add(button5, flag=wx.ALL, border=10)
        self.gauge5 = wx.Gauge(self.panel, size=(150, 15), style=wx.GA_HORIZONTAL)
        sizer5.Add(self.gauge5, flag=wx.LEFT | wx.TOP, border=14)
        main_sizer.Add(sizer5)
        
        self.drop_box.SetDropTarget(self.file_drop)
        self.panel.SetSizer(main_sizer)
        self.Show()
        
    def SetInsertionPointEnd(self):
        self.drop_box.SetInsertionPointEnd()
        
    def update_dropbox(self, text):
        self.drop_box.WriteText(text)
        
    def clear_button(self, event):
        self.drop_box.Clear()
        for index in range(len(self.path_list)):
            del self.path_list[0]
        
    def browse_button(self, event):
        title = 'Select Save Folder'
        dialog = wx.DirDialog(self, title, style=wx.DD_DEFAULT_STYLE)
        if dialog.ShowModal() == wx.ID_OK:
            self.save_location = dialog.GetPath()
        dialog.Destroy()
        self.text_box.SetValue(self.save_location)
        
    def convert_thread(self, event):
        self.t = Thread(target=self.convert_button)
        self.t.start()
    
    def convert_quality(self):
        selection = self.choice4.GetString(self.choice4.GetSelection())
        if selection == '128 kb/s':
            return '128k'
        elif selection == '192 kb/s':
            return '192k'
        elif selection == '256 kb/s':
            return '256k'
        elif selection == '320 kb/s':
            return '320k'
        
    def convert_button(self):
        kbs_choice = self.convert_quality()
        self.gauge5.SetRange(range=len(self.path_list)*100)
        position = 0
        for input_path in self.path_list:
            position += 20
            self.gauge5.SetValue(position)
            os.makedirs(self.save_location+'\\Temp')
            new_path = self.save_location+'\\Temp\\'+unidecode(os.path.basename(input_path))
            copyfile(input_path, new_path)
            mp3_filename = re.search(r"^(.*)\.([a-z4]+)$", input_path)
            AudioSegment.from_file(new_path,
                mp3_filename.group(2)).export(self.save_location+'/'+os.path.basename(mp3_filename.group(1))+'.mp3',
                format="mp3", bitrate=kbs_choice)
            rmtree(self.save_location + '\\Temp')
            position += 80
            self.gauge5.SetValue(position)
        sleep(1)
        self.gauge5.SetValue(0)
        wx.MessageBox('All files have been converted.', 'Complete', wx.OK)

    
        
if __name__ == '__main__':
    app = wx.App()
    frame = MP3Converter()
    app.MainLoop()
