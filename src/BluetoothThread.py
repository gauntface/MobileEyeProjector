from bluetooth import *
import threading, Queue, time, gobject

try:
    import gtk
    import gtk.glade
except:
    sys.exit(1)

class BluetoothThread(threading.Thread):

    def __init__(self, label_update_cb, inQueue, outQueue):
        threading.Thread.__init__(self)
        
        self.label_update_cb = label_update_cb
        self.inQueue = inQueue
        self.outQueue = outQueue
        self.killThread = False
        self.server_sock=BluetoothSocket(RFCOMM)
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
        
        try:
            while self.killThread == False:
                self.update_label("Waiting for connection on RFCOMM channel " + str(port))
                
                client_sock, client_info = self.server_sock.accept()
                
                self.update_label("Accepted Connection from " + client_info[0])
                
                try:
                    while self.killThread == False:
                        data = client_sock.recv(1024)
                        if len(data) == 0:
                            break
                        print "Received [%s]" % data
                except IOError:
                    pass
                
        except IOError:
            pass
        
        if self.run == False:
            self.server_sock.close()
        
    def update_label(self, msg):
        gobject.idle_add(self.label_update_cb, msg)
        #gtk.gdk.threads_enter()
        #self.msgLabel.set_text(msg)
        #gtk.gdk.threads_leave()
    
    def signal_kill_thread(self):
        self.killThread = True
