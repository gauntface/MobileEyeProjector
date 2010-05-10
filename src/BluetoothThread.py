from bluetooth import *
import threading, Queue, time, gobject

try:
    import gtk
    import gtk.glade
    from xml.dom import minidom
except:
    sys.exit(1)

class BluetoothThread(threading.Thread):

    def __init__(self, label_update_cb, show_blankscreen_cb, show_marker_cb):
        threading.Thread.__init__(self)
        
        self.label_update_cb = label_update_cb
        self.show_blankscreen_cb = show_blankscreen_cb
        self.show_marker_cb = show_marker_cb
        self.killThread = False
        self.server_sock=BluetoothSocket(RFCOMM)
        self.client_sock=BluetoothSocket(RFCOMM)
        print("Bluetooth init complete")
    
    # On run we try to connect to bluetooth and set up UI
    def run(self):
        
        self.update_label("Opening Bluetooth Connection")
        
        # Set the Server Timeout to 0.5 Secounds (Means Waiting to Accept a
        # connection doesn't block
        self.server_sock.settimeout(10)
        # Bind local adapter and port
        self.server_sock.bind(("",PORT_ANY))
        # The number of connections to be made
        self.server_sock.listen(1)
        
        port = self.server_sock.getsockname()[1]
        
        uuid = "00001101-0000-1000-8000-00805F9B34FB"
        
        self.update_label("Server Socket Set-Up")
        
        advertise_service(
                self.server_sock,
                "GauntFaceServer",
                service_id = uuid,
                service_classes = [uuid, SERIAL_PORT_CLASS],
                profiles = [SERIAL_PORT_PROFILE]
            )
        
        connectionOnPrevLoop = True
        
        while self.killThread == False:
            try:
                if(connectionOnPrevLoop == True):
                    self.update_label("Waiting for connection on RFCOMM channel " + str(port))
                    print("Waiting for connection")
                    connectionOnPrevLoop = False
                
                self.client_sock, client_info = self.server_sock.accept()
                
                self.update_label("Accepted Connection from " + client_info[0])
                print("Accepted Connection")
                connectionOnPrevLoop = True
                
                try:
                    while self.killThread == False:
                        data = self.client_sock.recv(1024)
                        print "Received [%s]" % data
                        
                        if len(data) == 0:
                            break
                        elif(data == "<ConnectionConfirm></ConnectionConfirm>"):
                            self.client_sock.send("<ConnectionConfirm></ConnectionConfirm>")
                            print("Connection Confirmed")
                            self.show_blankscreen_ui(True)
                        else:
                            xmldoc = minidom.parseString(data)
                            for e in xmldoc.childNodes:
                                if e.nodeType == e.ELEMENT_NODE:
                                    if e.localName == "ShowMarkers":
                                        projectorAngleString = self.getText(e.childNodes)
                                        projectorAngle = float(projectorAngleString)
                                        self.show_marker_ui(True, projectorAngle)
                                        break
                                    elif e.localName == "HideMarkers":
                                        self.show_marker_ui(False, 0)
                                    
                            #firstnode = xmldoc.firstChild
                            #if firstnode == "<ShowMarkers>"
                            
                except IOError:
                    print("Connection broke")
                    self.show_blankscreen_ui(False)
                    self.show_marker_ui(False, 0)
                    pass
                
            except IOError:
                pass
        
        if self.run == False:
            self.server_sock.close()
    
    def getText(self, nodeList):
        text = ""
        for node in nodeList:
            if node.nodeType == node.TEXT_NODE:
                text = text + node.data
        return text
    
    def update_label(self, msg):
        gobject.idle_add(self.label_update_cb, msg)
        #gtk.gdk.threads_enter()
        #self.msgLabel.set_text(msg)
        #gtk.gdk.threads_leave()
    
    def signal_kill_thread(self):
        self.killThread = True
        self.client_sock.shutdown(2)
    
    def show_blankscreen_ui(self, shouldDisplay):
        gobject.idle_add(self.show_blankscreen_cb, shouldDisplay)
    
    def show_marker_ui(self, shouldDisplay, rotationAngle):
        gobject.idle_add(self.show_marker_cb, shouldDisplay, rotationAngle)
