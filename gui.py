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


    
    def StatusBar(self):
        self.statusbar = self.CreateStatusBar()
    

    def ResearchNoteBook(self):
        
        panel = wx.Panel(self)
        nb = wx.Notebook(panel)

        # create the page windows as children of the notebook
        page1 = generalPage(nb, [ Yahoo])
        page1.arrangevbox()
        page2 = generalPage(nb, [ Bing ])
        page2.arrangevbox()
        page3 = generalPage(nb, [ GoogleBlog  ])
        page3.arrangevbox()

        page4 = googlePage(nb, [Google ])
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
        self.noScrapedLabel = wx.StaticText(self, -1, "Links Scraped:")
        self.noLabel = wx.StaticText(self, -1, " ")




        self.remduphbox.Add(self.noScrapedLabel, 0)
        self.remduphbox.Add(self.noLabel, 0)
        self.remduphbox.Add((-1, -1),1)
        self.remduphbox.Add(self.startButton, 0)
        self.remduphbox.Add(self.pauseButton, 0)
        self.remduphbox.Add(self.resumeButton, 0)
        self.remduphbox.Add(self.stopButton, 0)
        self.remduphbox.Add((-1, -1),1)
        self.remduphbox.Add(self.remdupButton, 2)
        self.remduphbox.Add(self.exportButton, 1)

        
#        self.remduphbox.Add((15, 5), 1)


        self.SetSizer(self.vbox)
        self.models = models
        self.Bind(wx.EVT_BUTTON,  self.OnStart, id = self.startButton.GetId())
        self.Bind(wx.EVT_BUTTON,  self.OnPause, id = self.pauseButton.GetId())
        self.Bind(wx.EVT_BUTTON,  self.OnRemDup, id = self.remdupButton.GetId())


    def arrangevbox(self):
        self.vbox.Add(self.fphbox, 0, wx.EXPAND | wx.TOP | wx.LEFT, 15)
        self.vbox.Add(self.kwhbox, 0, wx.EXPAND | wx.TOP | wx. LEFT, 15)
        self.vbox.Add(self.proxyhbox,0, wx.EXPAND | wx.TOP | wx.LEFT, 15)
        self.vbox.Add(self.resultshbox, 2, wx.EXPAND | wx.TOP | wx.LEFT , 15)
        self.vbox.Add(self.remduphbox, 0, wx.EXPAND | wx.ALL, 15)
       


    def fetchLinksThread(self):
        self.resultsBox.Disable()

        for model in self.models:
            n = model()
            if (model == Google):
                base_urlno = self.countryCombo.GetSelection()
                base_url = self.countryCombo.GetString(base_urlno)
                base_url = str(base_url)
            else:
                base_url = None
#            self.kwText.AppendText(base_url) #debugging purposes
            for no in range(1, 100):
                result = n.getLinks(KEYWORD,  no, base_url)
                for res in result:
                        self.resultsBox.AppendText(str(res) + "\n")
                        self.contents = self.resultsBox.GetValue()
                        self.total = self.contents.split("\n")
                        self.length = str(len(self.total))
                        previousVal = self.noScrapedLabel.GetLabel()
                        self.noLabel.SetLabel(self.length)
                


    def OnStart(self, event):
        self.keyword = str(self.kwText.GetValue())
        self.keyword = str(self.keyword.replace(' ', "+"))

        self.resultsBox.Clear()
#        self.t = thread_looper (0.1, self.fetchLinksThread)
#        self.t.start()

        self.t = threading.Thread(target = self.fetchLinksThread).start()

    def OnPause(self, event):
        self.t.stop()


    def OnRemDup(self, event):
        
        self.contents = self.resultsBox.GetValue()

        self.resultsBox.Clear() # order is important, always should be after self.contents!
        self.listoflinks = self.contents.split("\n")
        self.unique = uniquer(self.listoflinks)
        self.length = str(len(self.unique))
	for lin in self.unique:
		self.resultsBox.AppendText(str(lin) + "\n")
	self.listoflinks = self.contents.split("\n")
	self.length = str(len(self.listoflinks))
	self.noLabel.SetLabel(self.length)


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

        self.countryCombo.SetSelection(0) #useful for accessing items
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
