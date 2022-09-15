from time import sleep
import sys
import json
from eurotherm.eurotherm_2404 import Eurotherm_2404


# Import the necessary packages
from consolemenu import *
from consolemenu.items import *


def createMenu(oven_controller=Eurotherm_2404):

    # Create the menu
    menu = ConsoleMenu("Title", "Subtitle")

    # Create some items

    # MenuItem is the base class for all items, it doesn't do anything when selected
    menu_item = MenuItem("Menu Item")

    # A FunctionItem runs a Python function when selected
    updateSPTo50_item = FunctionItem("Update Oven SP1 to 50", oven_controller.update_temperature_sp, [50])
    updateSPTo75_item = FunctionItem("Update Oven SP1 to 75", oven_controller.update_temperature_sp, [75])
    updateSPTo100_item = FunctionItem("Update Oven SP1 to 100", oven_controller.update_temperature_sp, [100])
    updateSPTo150_item = FunctionItem("Update Oven SP1 to 150", oven_controller.update_temperature_sp, [150])
    putInAutoMode_item = FunctionItem("Put Oven in Auto Mode", oven_controller.set_in_auto_working_mode)
    putInManualMode_item = FunctionItem("Put Oven in Manual Mode", oven_controller.set_in_manual_working_mode)

    # Once we're done creating them, we just add the items to the menu
    menu.append_item(menu_item)
    menu.append_item(updateSPTo50_item)
    menu.append_item(updateSPTo75_item)
    menu.append_item(updateSPTo100_item)
    menu.append_item(updateSPTo150_item)
    menu.append_item(putInAutoMode_item)
    menu.append_item(putInManualMode_item)

    # Finally, we call show to show the menu and allow the user to interact
    menu.show()

def create_interument(config_file_path):

    # read JSON file with temperature calibration params
    with open(config_file_path, 'r') as f:
        config_params = json.load(f)

    connection_string = config_params["instruments"]["oven"]["controller"]["connection_string"].split(":")
    #print(connection_string)

    communication_protocol=connection_string[0]
    communication_id=connection_string[1]
    transport_protocol=connection_string[2]
    method=connection_string[3]
    port=connection_string[4]
    baudrate=connection_string[5]
    bytesize=int(connection_string[6])
    parity=connection_string[7]
    stopbits=int(connection_string[8])
    timeout=int(connection_string[9])

    addresses = config_params["instruments"]["oven"]["controller"]["addresses"]
    oven_controller = Eurotherm_2404(communication_protocol,communication_id,transport_protocol, method, port, baudrate,
                                     bytesize, parity, stopbits, timeout, addresses)
    return oven_controller

def main():

    oven_controller = create_interument('eurotherm\\config.json')
    createMenu(oven_controller)


if __name__ == '__main__':
    sys.exit(main())  # next section explains the use of sys.exit