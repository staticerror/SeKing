
import wx, wx.html
from taichi.artdirs import *
from wx import xrc
from taichi.wikipedia import Wikipedia
import threading
from taichi.base.htmlutils import stripHtml

class LinkMonster(wx.Frame):
    
    def __init__(self, parent , id,  title):
        wx.Frame.__init__(self, parent, id, title, size=(550, 580))

        self.MenuBar()
        self.MainArea()
        self.StatusBar()

        self.Centre()
        self.Maximize()
        self.Show()

        
    def MenuBar(self):
        
        menubar = wx.MenuBar()
        file = wx.Menu()
        edit = wx.Menu()
        help = wx.Menu()

        menubar.Append(file , "&File")
        menubar.Append(edit , "&Edit")
        menubar.Append(help , "&Help")
        
        self.SetMenuBar(menubar)
        
    
    def MainArea(self):
        # Master Blaster container, the main guy in the app responsible for every thing
        vbox = wx.BoxSizer(wx.VERTICAL)
        editortoolbar = self.EditorToolbar() #Editor actions, below menubar
        verticaltoolbar = self.VerticalToolbar() # the three main research, edit etc
        
        #vbox.Add(editortoolbar, 0, wx.EXPAND) # editor, below menubar
        vbox.Add(verticaltoolbar, 1, wx.EXPAND | wx.RIGHT| wx.TOP | wx.BOTTOM, 20) 



        self.SetSizer(vbox)


        
    def VerticalToolbar(self):
        
        MainContainer = wx.BoxSizer(wx.HORIZONTAL)

        MainContainer.Add((20, -1))
        
        notebook = self.ResearchNoteBook()
        MainContainer.Add(notebook, 7,  wx.EXPAND | wx.ALL, 10)
        

        return MainContainer


    def EditorToolbar(self):

        editortoolbar = wx.ToolBar(self, -1 )
        editortoolbar.AddLabelTool(wx.ID_EXIT, '', wx.Bitmap('/home/desktop/Desktop/crystal_project/24x24/actions/save_all.png'))
        editortoolbar.AddLabelTool(wx.ID_EXIT, '', wx.Bitmap('/home/desktop/Desktop/crystal_project/24x24/actions/fileclose.png'))
        editortoolbar.Realize()
        return editortoolbar


    def StatusBar(self):
        self.statusbar = self.CreateStatusBar()
    

    def ResearchNoteBook(self):
        
        panel = wx.Panel(self)
        nb = wx.Notebook(panel)

        # create the page windows as children of the notebook
        page1 = ResearchPage(nb, [ Ezine, Dashboard, ABase])
        page2 = ResearchPage(nb, [ Wikipedia ])
        # add the pages to the notebook with the label to show on the tab
        nb.AddPage(page1, "Google")
        nb.AddPage(page2, "Yahoo!")
        nb.AddPage(page2, "Bing")
        nb.AddPage(page2, "Google Blog Search")


        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(nb, 10, wx.EXPAND)
        panel.SetSizer(sizer)

        return panel





class ResearchPage(wx.Panel):
    def __init__(self, parent, models):
        wx.Panel.__init__(self, parent)
        self.vbox = wx.BoxSizer(wx.VERTICAL)




        
        self.fphbox = wx.BoxSizer(wx.HORIZONTAL)        
        self.fplabel = wx.StaticText(self, -1, "Enter Footprint Here")
        self.fpText = wx.TextCtrl(self, -1 )
        self.fphbox.Add(self.fplabel, 2)
        self.fphbox.Add(self.fpText , 4)
        self.fphbox.Add((-1, 25), 3)

        self.kwhbox = wx.BoxSizer(wx.HORIZONTAL)
        self.kwlabel = wx.StaticText(self, -1, "Enter Keywords Here")
        self.kwText = wx.TextCtrl(self, -1 , style = wx.TE_MULTILINE)
        self.kwhbox.Add(self.kwlabel, 2)
        self.kwhbox.Add(self.kwText , 4)
        self.kwhbox.Add((-1, 25), 3)

        self.proxyhbox = wx.BoxSizer(wx.HORIZONTAL)
        self.proxylabel = wx.StaticText(self, -1, "Proxy(Optional)")
        self.proxychbox = wx.CheckBox(self, -1, "Use Proxy")
        self.proxyText = wx.TextCtrl(self, -1)
        self.proxyhbox.Add(self.proxylabel, 2)
        self.proxyhbox.Add(self.proxychbox , 2)
        self.proxyhbox.Add(self.proxyText , 2 )
        self.proxyhbox.Add((-1, 25), 3)

        self.resultshbox = wx.BoxSizer(wx.HORIZONTAL)        
        self.resultsBox = wx.TextCtrl(self, -1, style = wx.TE_MULTILINE)
        self.resultshbox.Add(self.resultsBox, 10, wx.EXPAND | wx.ALL, 15)

        self.remduphbox = wx.BoxSizer(wx.HORIZONTAL)        
        self.remdupButton = wx.Button(self, -1 , "Remove Duplicates")
        self.exportButton = wx.Button(self, -1 , "Export")
        self.remduphbox.Add(self.remdupButton, 4)
        self.remduphbox.Add((-1, 5), 2)
        self.remduphbox.Add(self.exportButton, 4)
        self.remduphbox.Add((-1, 5), 2)

        self.vbox.Add(self.fphbox, 0, wx.EXPAND | wx.TOP | wx.LEFT, 15)
        self.vbox.Add(self.kwhbox, 0, wx.EXPAND | wx.TOP | wx. LEFT, 15)
        self.vbox.Add(self.proxyhbox,0, wx.EXPAND | wx.TOP | wx.LEFT, 15)
        self.vbox.Add(self.resultshbox, 2, wx.EXPAND | wx.TOP | wx.LEFT , 15)
        self.vbox.Add(self.remduphbox, 0, wx.EXPAND | wx.TOP | wx.LEFT | wx.BOTTOM, 15)


        self.SetSizer(self.vbox)
        self.models = models
        

        #self.Bind(wx.EVT_BUTTON,  self.OnClicked, id = self.button.GetId())


    def fetchArticleThread(self):
        self.resultbox.Disable()
        for model in self.models:
            n = model()
            n.fetchArticle(self.keyword)
            for result in n.article:
                self.resultbox.AppendText(stripHtml(str(result)))
        self.resultbox.AppendText("\n\n\n")

    def OnClicked(self, event):
        
        self.keyword = str(self.textbox.GetValue())
#        self.keyword = str(self.keyword.replace(' ', "+"))

        self.resultbox.Clear()
        threading.Thread(target = self.fetchArticleThread).start()

        
if __name__ == '__main__':
    app = wx.App(False)
    LinkMonster(None, -1, "Article Domination")
    app.MainLoop()
