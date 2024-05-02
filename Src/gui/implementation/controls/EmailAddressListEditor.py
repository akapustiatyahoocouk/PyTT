#   Dependencies on other PyTT components
from awt.interface.api import *

##########
#   Piblic entities
class EmailAddressListEditor(Panel):
    
    ##########
    #   Construction
    def __init__(self, parent: tk.BaseWidget):
        Panel.__init__(self, parent)
        
        #   Create controls
        self.__email_addresses_list_box = ListBox(self, height=3)
        self.__actions_panel = Panel(self)
        
        self.__add_email_address_button = Button(self.__actions_panel, text="Add")
        self.__modify_email_address_button = Button(self.__actions_panel, text="Modify")
        self.__remove_email_address_button = Button(self.__actions_panel, text="Remove")
        
        #   Adjust controls
        
        #   Set up control structure
        self.__actions_panel.pack(side=tk.RIGHT, padx=0, pady=0, fill=tk.Y)
        self.__email_addresses_list_box.pack(padx=2, pady=2, fill=tk.BOTH, expand=True)

        self.__add_email_address_button.grid(row=0, column=0, padx=0, pady=2, sticky="WE")
        self.__modify_email_address_button.grid(row=1, column=0, padx=0, pady=2, sticky="WE")
        self.__remove_email_address_button.grid(row=2, column=0, padx=0, pady=2, sticky="WE")
