import wx, wx.html
from taichi.artdirs import *
from wx import xrc
from taichi.wikipedia import Wikipedia
import threading
from taichi.base.htmlutils import stripHtml
from links import *

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
        page1 = generalPage(nb, [ Ezine, Dashboard, ABase])
        page1.arrangevbox()
        page2 = generalPage(nb, [ Wikipedia ])
        page2.arrangevbox()
        page3 = generalPage(nb, [ Wikipedia ])
        page3.arrangevbox()

        page4 = googlePage(nb, [Ezine])
        # add the pages to the notebook with the label to show on the tab
        nb.AddPage(page4, "Google")
        nb.AddPage(page1, "Yahoo!")
        nb.AddPage(page2, "Bing")
        nb.AddPage(page3, "Google Blog Search")


        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(nb, 10, wx.EXPAND)
        panel.SetSizer(sizer)
        return panel



class generalPage(wx.Panel):
    def __init__(self, parent, models):
        wx.Panel.__init__(self, parent)
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        #fp - Footprints stuff
        self.fphbox = wx.BoxSizer(wx.HORIZONTAL)        
        self.fplabel = wx.StaticText(self, -1, "Enter Footprint Here:")
        self.fpText = wx.TextCtrl(self, -1 )
        self.fphbox.Add(self.fplabel, 2)
        self.fphbox.Add(self.fpText , 4)
        self.fphbox.Add((-1, 25), 3)

        #kw - keywords stuff
        self.kwhbox = wx.BoxSizer(wx.HORIZONTAL)
        self.kwlabel = wx.StaticText(self, -1, "Enter Keywords Here:")
        self.kwText = wx.TextCtrl(self, -1 , style = wx.TE_MULTILINE)
        self.kwhbox.Add(self.kwlabel, 2)
        self.kwhbox.Add(self.kwText , 4)
        self.kwhbox.Add((-1, 25), 3)

        #proxy stuff
        self.proxyhbox = wx.BoxSizer(wx.HORIZONTAL)
        self.proxylabel = wx.StaticText(self, -1, "Proxy(Optional):")
        self.proxychbox = wx.CheckBox(self, -1, "Use Proxy")
        self.proxyText = wx.TextCtrl(self, -1)
        self.proxyhbox.Add(self.proxylabel, 2)
        self.proxyhbox.Add(self.proxychbox , 1)
        self.proxyhbox.Add((15, 5), 0)
        self.proxyhbox.Add(self.proxyText , 3 )
        self.proxyhbox.Add((15, 5), 3)

        #these are the buttons a
        self.resultshbox = wx.BoxSizer(wx.HORIZONTAL)        
        self.resultsBox = wx.TextCtrl(self, -1, style = wx.TE_MULTILINE)
        self.resultshbox.Add(self.resultsBox, 10, wx.EXPAND | wx.ALL, 15)

        self.remduphbox = wx.BoxSizer(wx.HORIZONTAL)        
        self.remdupButton = wx.Button(self, -1 , "Remove Duplicates")
        self.exportButton = wx.Button(self, -1 , "Export")
        self.startButton = wx.Button(self, -1 , "Start")
        self.pauseButton = wx.Button(self, -1 , "Pause")
        self.resumeButton = wx.Button(self, -1 , "Resume")
        self.stopButton = wx.Button(self, -1 , "Stop")


        self.remduphbox.Add(self.startButton, 2)
        self.remduphbox.Add(self.pauseButton, 2)
        self.remduphbox.Add(self.resumeButton, 2)
        self.remduphbox.Add(self.stopButton, 2)
        self.remduphbox.Add((15, 5), 5)
        self.remduphbox.Add(self.remdupButton, 4)
        self.remduphbox.Add(self.exportButton, 2)
        self.remduphbox.Add((15, 5), 3)


        self.SetSizer(self.vbox)
        self.models = models
        #self.Bind(wx.EVT_BUTTON,  self.OnClicked, id = self.button.GetId())


    def arrangevbox(self):
        self.vbox.Add(self.fphbox, 0, wx.EXPAND | wx.TOP | wx.LEFT, 15)
        self.vbox.Add(self.kwhbox, 0, wx.EXPAND | wx.TOP | wx. LEFT, 15)
        self.vbox.Add(self.proxyhbox,0, wx.EXPAND | wx.TOP | wx.LEFT, 15)
        self.vbox.Add(self.resultshbox, 2, wx.EXPAND | wx.TOP | wx.LEFT , 15)
        self.vbox.Add(self.remduphbox, 0, wx.EXPAND | wx.ALL, 15)
       


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



class googlePage(generalPage):
    
    def __init__(self, parent, models):

        generalPage.__init__(self, parent, models)
        self.countryhbox = wx.BoxSizer(wx.HORIZONTAL)
        self.countryCombo = wx.Choice(self, -1, choices = GOOGLE_URLS)
        self.countryLabel = wx.StaticText(self, -1 , "Country")
        self.countryhbox.Add(self.countryLabel, 2, wx.EXPAND | wx.ALL, 5)
        self.countryhbox.Add((-1, 25), 2)
        self.countryhbox.Add(self.countryCombo, 10, wx.EXPAND | wx.ALL, 5)
        self.countryhbox.Add((-1, 25), 6)
        self.arrangevbox()


    def arrangevbox(self):
        self.vbox.Add(self.fphbox, 0, wx.EXPAND | wx.TOP | wx.LEFT, 15)
        self.vbox.Add(self.kwhbox, 0, wx.EXPAND | wx.TOP | wx. LEFT, 15)
        self.vbox.Add(self.proxyhbox,0, wx.EXPAND | wx.TOP | wx.LEFT, 15)
        self.vbox.Add(self.countryhbox, 0, wx.EXPAND| wx.TOP | wx.LEFT , 15)
        self.vbox.Add(self.resultshbox, 2, wx.EXPAND | wx.TOP | wx.LEFT , 15)
        self.vbox.Add(self.remduphbox, 0, wx.EXPAND | wx.ALL, 15)

        

if __name__ == '__main__':
    app = wx.App(False)
    LinkMonster(None, -1, "Article Domination")
    app.MainLoop()
