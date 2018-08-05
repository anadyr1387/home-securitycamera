'''
Created on Jun 11, 2018

@author: Andy
'''

import tkinter as tk
from tkinter import ttk
import client1_basic
import streamingcapture1
import queue
import threading
from PIL import Image, ImageTk


class NotebookDemo (ttk.Frame):
    
    def __init__(self, isapp=True, name='gui'):
        ttk.Frame.__init__(self, name=name)
        self.pack()
        self.master.title('GUI')
    
        #self.isapp = isapp
        self._create_widgets()
        
    def _create_widgets(self):
        #comboboxfont = tkFont.Font(family='Helvetica', size=40)
        #self.option_add("*TCombobox*Listbox*Font", comboboxfont)
        #self._create_demo_panel()
        self.senttext='empty'
        
        btnframe = ttk.Frame()
        btnframe.pack()
        
        txbutton = ttk.Button(btnframe, text='TX Server', command=lambda: self._getinputtext())
        txbutton.pack()
        
        disconnectbutton = ttk.Button(btnframe, text='disconnect', command=lambda: self._endclient())
        disconnectbutton.pack()
        
        self.inputtext1 = ttk.Combobox(btnframe, width=15, 
                                  textvariable=self.senttext)
        self.inputtext1.pack()
        
        
        
            
        self.img = ImageTk.PhotoImage(Image.open('G411.png'))
        print('using default image')      
        self.videopanel = ttk.Label(btnframe, image = self.img)
        self.videopanel.pack(side = "bottom", fill = "both", expand = "yes")
        
        #if server_requests.checkqueue(self, self.senttext, imagequeue):
        #    self.img = imagequeue.get()
        #    print('getting image from queue') 


        #frame for image viewing
        #self.videopanel = ttk.Label(btnframe, image = self.img)
        #self.videopanel.pack(side = "bottom", fill = "both", expand = "yes")
        
        
        
        
        
    def _getinputtext(self):
        self.senttext = self.inputtext1.get()
        server_requests.requestimage(self, self.senttext, self.videopanel)
            
    def _endclient(self):
        server_requests.requestimage(self, 'end')
    
    
    
    
    
    
class server_requests:
    
    def requestimage(self, inputtext1, frameobject):
        #print('request received of:' +str(inputtext1))
        #client1_basic.clientcode(inputtext1)
        
        worker = threading.Thread(target=streamingcapture1.streamcapture, args = (client1_basic.connectserver(), imagequeue))
        worker.setDaemon(True)
        worker.start()
        
        while True:
            print('in true loop')
            if imagequeue.qsize() > 5:
                print('should update image now')
                #self.after(10, server_requests.updateimage(self, frameobject))
                self.image = ImageTk.PhotoImage(imagequeue.get())
                frameobject.configure(image=self.image)
                frameobject.update()
            else:
                pass
            
            #check status of thread, will be inactive once connection broken
            status = worker.isAlive()
            #print('status of thread' + str(status))
            if status == False:
                break
            
            
        #    self.after(300)
        #    #while inputtext1 is not 'end':
        #    length = imagequeue.qsize()
        #    print('queue size = ' + str(length))
    
    
    #loop to indicate when mainloop should be updating GUI
    def checkqueue(self, inputtext1, activequeue):
        length = activequeue.qsize()
        
        print('length queue = ' + str(length))
        #if queue less than 5 objects, assume empty
        if length < 5:
            print('nawt ok')
            #return False
        
        #if greater than five objects, assume not empty
        else:
            print('ok')
            #return True
            
    def updateimage(self, frameobject):
        #self.img = ImageTk.PhotoImage(Image.open('G411.png'))
        #self.imageobject = ImageTk.PhotoImage(Image.open(imagequeue.get()))
        
        self.image = ImageTk.PhotoImage(imagequeue.get())
        frameobject.configure(image=self.image)
        frameobject.pack()
        
        #print('image converted to imagetk format')
        
        #image.show()
        
        #print('getting image from queue') 
        
        #self.videopanel = ttk.Label(btnframe, image = self.img)
        #self.videopanel.pack(side = "bottom", fill = "both", expand = "yes")
        
        


if __name__ == '__main__':
    
    imagequeue = queue.LifoQueue()
    
    
    
    NotebookDemo().mainloop()     
    #server_requests.requestimage('',' text')