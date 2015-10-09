# Authors: Liam Harwood, Graham Burek, Max Vitkin

from Tkinter import * 
from tkSimpleDialog import askstring
from tkFileDialog   import asksaveasfilename
from tkMessageBox import askokcancel          
import requests
import time
#from SimpleCV import Image, Camera

url="http://api.idolondemand.com/1/api/sync/{}/v1"
apikey="ed67fc7b-9d91-4d31-a320-3d726afe74d5"

class Quitter(Frame):                        
    def __init__(self, parent=None):          
        Frame.__init__(self, parent)
        self.pack()
        widget = Button(self, text='Quit', command=self.quit)
        widget.pack(expand=YES, fill=BOTH, side=LEFT)
    def quit(self):
        ans = askokcancel('Quit', 'Are you sure?')
        if ans: Frame.quit(self)     


class ScrolledText(Frame):
    def __init__(self, parent=None, text='', file=None):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)               
        self.makewidgets()
        self.settext(text, file)
    def makewidgets(self):
        sbar = Scrollbar(self)
        text = Text(self, relief=SUNKEN)
        sbar.config(command=text.yview)                  
        text.config(yscrollcommand=sbar.set)           
        sbar.pack(side=RIGHT, fill=Y)                   
        text.pack(side=LEFT, expand=YES, fill=BOTH)     
        self.text = text
    def settext(self, text='', file=None):
        if file: 
            text = open(file, 'r').read()
        self.text.delete('1.0', END)                   
        self.text.insert('1.0', text)                  
        self.text.mark_set(INSERT, '1.0')              
        self.text.focus()                                
    def gettext(self):                               
        return self.text.get('1.0', END+'-1c')         



class SimpleEditor(ScrolledText):                        
    def __init__(self, parent=None, file=None): 
        frm = Frame(parent)
        frm.pack(fill=X)
        Button(frm, text='Save',  command=self.onSave).pack(side=LEFT)
        Button(frm, text='Paste', command=self.onPaste).pack(side=LEFT)
        Button(frm, text='Clear', command=self.onClear).pack(side=LEFT)
        Button(frm, text='tl;dr', command=self.onTLDR).pack(side=RIGHT)
        Button(frm, text='Find Articles', command=self.onFind).pack(side=RIGHT)
        Button(frm, text='Take Picture', command=self.onPicture).pack(side=RIGHT)
        
        Quitter(frm).pack(side=LEFT)
        ScrolledText.__init__(self, parent, file=file) 
        self.text.config(font=('courier', 9, 'normal'))
        self.text.insert(INSERT, 'Copy and paste a big block of text that you want to find more information about! Or you can take a picture of some text using the webcam!')
    def onSave(self):
        filename = asksaveasfilename()
        if filename:
            alltext = self.gettext()                      
            open(filename, 'w').write(alltext)          
    def onPaste(self):                                    
        try:
            text = self.selection_get(selection='CLIPBOARD')
            self.text.insert(INSERT, text)
        except TclError:
            pass
    def onClear(self):
        self.settext('')

        
            
# Request the API

    def postrequests(self,function,data={},files={}):
      data["apikey"]=apikey
      callurl=url.format(function)
      r=requests.post(callurl,data=data,files=files)
      return r.json()  
   
# Take user input find similar wiki pages                                      
    def onFind(self):
      userInput = self.gettext()     
      results = self.postrequests('findsimilar',{'text':userInput,'max_page_results' : 10,'absolute_max_results' : 10, 'indexes' : 'news_eng'})
      documents = results['documents']
      self.settext('')
      for document in documents:
          self.text.insert(END,document['reference'] + '\n' + '\n')

# Take picture and give text of picture. It doesn't work well. Reuquires SimpleCV.         
    def onPicture(self):
        self.settext('')
        #cam = Camera()
        #img = cam.getImage()
        #img.save('picture.jpg')
        #d = img.show()
        #time.sleep(1)
        #d.quit()
        #results = self.postrequests('ocrdocument',data={'mode':'photo'},files={'file': open('picture.jpg','rb')})
        #textblock = results['text_block']
        #text = textblock[0]['text']
        #self.text.insert(END, text)
        
    def onTLDR(self):
        userInput = self.gettext()     
        results = self.postrequests('extractconcepts',{'text':userInput})
        concepts = results['concepts']
        self.settext('')
        self.text.insert(END, 'This is about ' + concepts[0]['concept'] + '. ')
        self.text.insert(END, 'It contains information concerning ' + concepts[1]['concept'] + ' and ' + concepts[2]['concept'] + '. ')
        self.text.insert(END, 'It also includes some information on ' + concepts[3]['concept'] + ' and ' + concepts[4]['concept'] + ', and touches on ')
        self.text.insert(END, concepts[5]['concept'] + ' and ' + concepts[6]['concept'] + '.')
        
        
      
      
      
      
                  
     
                                       

if __name__ == '__main__':
    try:
        root = Tk()
        root.wm_title('Research Simulator 2014')
        SimpleEditor(parent=root,file=sys.argv[1]).mainloop()   
    except IndexError:
        SimpleEditor().mainloop()                  
