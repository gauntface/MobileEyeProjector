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

#Currently on initialisation, run bluetooth thread to decide of UI

class MobileEyeUI:
    
    def __init__(self):
        self.gladefile = "./ui/MobileEyeProjectorUI.glade"
        self.wTree = gtk.glade.XML(self.gladefile)
        
        self.window = self.wTree.get_widget("RootWindow")
        
        self.window.fullscreen()
        self.isFullscreen = True
        self.window.connect('key_press_event', self.on_RootWindow_key_press_event)
        
        self.bluetoothLabel = self.wTree.get_widget("bluetoothLabel")
        self.bluetoothLabel.set_text("Initialising Program")
        
        self.window.show()
        
        self.bluetoothThread = BluetoothThread.BluetoothThread(self.update_bluetooth_label, self.show_markers)
        
        if self.window:
            self.window.connect("destroy", self.on_RootWindow_destroy)
        
    def on_RootWindow_destroy(self, widget):
        self.close_program()
	
    def on_RootWindow_key_press_event(self, widget, event):
        #keyname = gtk.gdk.keyval_name(event.keyval)
        #print "Key %s (%d) was pressed" % (keyname, event.keyval)
        
        if event.keyval == 65307:
            #Escape Key Pressed
            print "Escape Key Pressed"
            self.close_program()
        elif event.keyval == 102:
            if self.isFullscreen == True:
                self.window.unfullscreen()
                self.isFullscreen = False
            else:
                self.window.fullscreen()
                self.isFullscreen = True
    
    def close_program(self):
        self.bluetoothThread.signal_kill_thread()
        self.bluetoothLabel.set_text("Waiting for Bluetooth Socket to close")
        while gtk.events_pending():
            gtk.main_iteration(block=False)
        self.bluetoothThread.join()
        gtk.main_quit()
    
    def update_bluetooth_label(self, msg):
        self.bluetoothLabel.set_text(msg)
    
    def startBluetoothThread(self):
        self.bluetoothThread.start()
    
    def show_markers(self):
        print("Need to show markers");
        markerUI = MarkerUI(self)
        
    
if __name__ == "__main__":
    mobileEye = MobileEyeUI()
    mobileEye.startBluetoothThread()
    
    gtk.gdk.threads_init()
    
    gtk.gdk.threads_enter()
    gtk.main()
    gtk.gdk.threads_leave()
