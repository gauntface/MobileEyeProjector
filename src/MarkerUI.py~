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
except:
    sys.exit(1)

class MarkerUI:
    
    def __init__(self, connection_window):
        self.gladefile = "./ui/MobileEyeMarkerUI.glade"
        self.wTree = gtk.glade.XML(self.gladefile)
        
        self.window = self.wTree.get_widget("RootWindow")
        
        #self.window.fullscreen()
        self.isFullscreen = False
        self.window.connect('key_press_event', self.on_RootWindow_key_press_event)
        
        self.window.show()
        
        self.connection_window = connection_window
        
        if self.window:
            self.window.connect("destroy", self.on_RootWindow_destroy)
        
    def on_RootWindow_destroy(self, widget):
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
    
    def close_program(self):
        self.window.hide()
        self.connection_window.close_program()
    
if __name__ == "__main__":
    mobileEye = MarkerUI()
    
    gtk.gdk.threads_init()
    
    gtk.gdk.threads_enter()
    gtk.main()
    gtk.gdk.threads_leave()
