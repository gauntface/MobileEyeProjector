# -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import sys
import os
import gtk

from mobileeyeprojectorui.mobileeyeprojectoruiconfig import getdatapath

class AboutMobileeyeprojectoruiDialog(gtk.AboutDialog):
    __gtype_name__ = "AboutMobileeyeprojectoruiDialog"

    def __init__(self):
        """__init__ - This function is typically not called directly.
        Creation of a AboutMobileeyeprojectoruiDialog requires redeading the associated ui
        file and parsing the ui definition extrenally, 
        and then calling AboutMobileeyeprojectoruiDialog.finish_initializing().
    
        Use the convenience function NewAboutMobileeyeprojectoruiDialog to create 
        NewAboutMobileeyeprojectoruiDialog objects.
    
        """
        pass

    def finish_initializing(self, builder):
        """finish_initalizing should be called after parsing the ui definition
        and creating a AboutMobileeyeprojectoruiDialog object with it in order to finish
        initializing the start of the new AboutMobileeyeprojectoruiDialog instance.
    
        """
        #get a reference to the builder and set up the signals
        self.builder = builder
        self.builder.connect_signals(self)

        #code for other initialization actions should be added here

def NewAboutMobileeyeprojectoruiDialog():
    """NewAboutMobileeyeprojectoruiDialog - returns a fully instantiated
    AboutMobileeyeprojectoruiDialog object. Use this function rather than
    creating a AboutMobileeyeprojectoruiDialog instance directly.
    
    """

    #look for the ui file that describes the ui
    ui_filename = os.path.join(getdatapath(), 'ui', 'AboutMobileeyeprojectoruiDialog.ui')
    if not os.path.exists(ui_filename):
        ui_filename = None

    builder = gtk.Builder()
    builder.add_from_file(ui_filename)    
    dialog = builder.get_object("about_mobileeyeprojectorui_dialog")
    dialog.finish_initializing(builder)
    return dialog

if __name__ == "__main__":
    dialog = NewAboutMobileeyeprojectoruiDialog()
    dialog.show()
    gtk.main()

