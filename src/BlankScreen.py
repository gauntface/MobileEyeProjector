#!/usr/bin/env python
# Enter application, select UI To set-up and launch

import sys, BluetoothThread, gobject
from MarkerUI import MarkerUI
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

class BlankScreen:
    
    def __init__(self, connection_window):
        self.gladefile = "./ui/MobileEyeBlankScreen.glade"
        self.wTree = gtk.glade.XML(self.gladefile)
        
        self.window = self.wTree.get_widget("RootWindow")
        
        self.window.fullscreen()
        self.isFullscreen = True
        self.window.connect('key_press_event', self.on_RootWindow_key_press_event)
        
        self.window.show()
        
        self.connection_window = connection_window
        self.markerUI = None
        
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
        self.connection_window.close_program()
    
    def show_markers(self, shouldDisplay, rotationAngle):
        print("Showing Markers")
        if shouldDisplay:
            if self.markerUI:
                self.markerUI.hide()
            self.markerUI = MarkerUI(self, rotationAngle)
        elif self.markerUI:
            self.markerUI.hide()
    
    def change_marker(self, cornerCoords):
        print("Changing Markers")
        if self.markerUI:
            self.markerUI.change_marker(cornerCoords)
    
if __name__ == "__main__":
    mobileEye = BlankScreen()
    
    gtk.gdk.threads_init()
    
    gtk.gdk.threads_enter()
    gtk.main()
    gtk.gdk.threads_leave()
            
