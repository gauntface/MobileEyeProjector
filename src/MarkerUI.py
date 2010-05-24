#!/usr/bin/env python
# Enter application, select UI To set-up and launch

import sys, BluetoothThread, gobject
try:
    import pygtk
    pygtk.require("2.0")
except:
    pass

try:
    import gtk
    import gtk.glade
    import Image
    import StringIO
except:
    sys.exit(1)

class MarkerUI:
    
    def __init__(self, blank_window, rotationAmount):
        self.gladefile = "./ui/MobileEyeMarkerUI.glade"
        self.wTree = gtk.glade.XML(self.gladefile)
        
        self.window = self.wTree.get_widget("RootWindow")
        self.markerImg = self.wTree.get_widget("MarkerImg")
        
        pilImg = Image.open("./ui/res/images/markers.png")
        
        # Reset rotation amount to as not using hardware
        rotationAmount = 0;
        
        pilImg = pilImg.rotate(rotationAmount, Image.NEAREST, True)
        pixbufImg = self.image2pixbuf(pilImg)
        
        self.markerImg.set_from_pixbuf(pixbufImg)
        
        self.window.fullscreen()
        self.isFullscreen = True
        self.window.connect('key_press_event', self.on_RootWindow_key_press_event)
        
        self.window.show()
        
        self.blank_window = blank_window
        
        if self.window:
            self.window.connect("destroy", self.window_destroy)
        
    def hide(self):
        self.window.hide()
    
    def on_RootWindow_key_press_event(self, widget, event):
        
        if event.keyval == 65307:
            #Escape Key Pressed
            print "MarkerUI: Escape Key Pressed"
            self.close_program()
        elif event.keyval == 102:
            if self.isFullscreen == True:
                self.window.unfullscreen()
                self.isFullscreen = False
            else:
                self.window.fullscreen()
                self.isFullscreen = True
    
    def window_destroy(self, widget):
        self.close_program()
    
    def close_program(self):
        self.window.hide()
        self.blank_window.close_program()
    
    def image2pixbuf(self, img):
        fileOut = StringIO.StringIO()
        img.save(fileOut, "png")
        contents = fileOut.getvalue()
        fileOut.close()
        loader = gtk.gdk.PixbufLoader("png")
        loader.write(contents, len(contents))
        pixbuf = loader.get_pixbuf()
        loader.close()
        return pixbuf
    
    def change_marker(self, cornerCoords):
        
        imageID = int(cornerCoords[0])
        
        if(imageID == -1):
            pilImg = Image.open("./ui/res/images/products/-1.png")
        elif(imageID == 0):
            pilImg = Image.open("./ui/res/images/products/0.png")
        elif(imageID == 1):
            pilImg = Image.open("./ui/res/images/products/1.png")
        elif(imageID == 2):
            pilImg = Image.open("./ui/res/images/products/2.png")
        elif(imageID == 3):
            pilImg = Image.open("./ui/res/images/products/3.png")
        elif(imageID == 4):
            pilImg = Image.open("./ui/res/images/products/4.png")
            
        pixbufImg = self.image2pixbuf(pilImg)
        self.markerImg.set_from_pixbuf(pixbufImg)
        
        self.blank_window.send_bluetooth_msg("<MarkersDisplayed></MarkersDisplayed>")
    
if __name__ == "__main__":
    mobileEye = MarkerUI()
    
    gtk.gdk.threads_init()
    
    gtk.gdk.threads_enter()
    gtk.main()
    gtk.gdk.threads_leave()
