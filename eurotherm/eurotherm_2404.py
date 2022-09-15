"""
==============
py2404.py
==============

"""
from interfaces.temperature_controller_i import Temperature_Controller_I
from pymodbus.client.sync import ModbusSerialClient as ModbusClient, ModbusSerialClient

# --------------------------------------------------------------------------- #
# configure the client logging
# --------------------------------------------------------------------------- #
import logging

from pymodbus.register_read_message import ReadHoldingRegistersResponse

FORMAT = ('%(asctime)-15s %(threadName)-15s '
          '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)

not_implemented_transport_protocol = Exception("Not implemented transport protocol. ")
not_implemented_communication_protocol = Exception("Not implemented communication protocol")
not_connected_instrument = Exception("Not connected instrument")


class Eurotherm_2404(Temperature_Controller_I):
    """The :class:`py2404` class serves as an interface for the Eurotherm 2404 temperature controller - programmer.

    It starts a pymodbus client with the given **kwargs

    The methods to connect are::

          - ascii
          - rtu
          - binary

        :param method: The method to use for connection
        :param port: The serial port to attach to
        :param stopbits: The number of stop bits to use
        :param bytesize: The bytesize of the serial messages
        :param parity: Which kind of parity to use
        :param baudrate: The baud rate to use for the serial device
        :param timeout: The timeout between serial requests (default 3s)
        :param strict:  Use Inter char timeout for baudrates <= 19200 (adhere
        to modbus standards)
        :param handle_local_echo: Handle local echo of the USB-to-RS485 adaptor

    Raises
    ------
        invalid_unit_exception = Exception("Invalid Unit Type - Please Use 'C', 'K', or 'F'")
        not_set_up_exception = Exception("Multimeter not set up properly")
        no_channels_exception = Exception("No channels have been defined to set up")
    """

    def __init__(self, communication_protocol, communication_id, transport_protocol="RS232", method='rtu', port="COM1",
                 baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=3, addresses=dict()):

        """
        Initialize the :class:`py2404` object.

        :param method:
                The methods to connect are::
              - ascii
              - rtu
              - binary
        :param kwargs:
            port: The serial port to attach to
            stopbits: The number of stop bits to use
            bytesize: The bytesize of the serial messages
            parity: Which kind of parity to use
            baudrate: The baud rate to use for the serial device
            timeout: The timeout between serial requests (default 3s)
            strict:  Use Inter char timeout for baudrates <= 19200 (adhere
            to modbus standards)
            handle_local_echo: Handle local echo of the USB-to-RS485 adaptor
        :return: None
        """

        self.client = None
        self.device_id = -1
        self.connected = False
        self.addresses = dict()

        if transport_protocol == "RS232":
            if communication_protocol == "MODBUS":
                self.connect(communication_id, method, port, baudrate, bytesize, parity, stopbits, timeout)
                self.addresses = addresses
            else:
                raise not_implemented_communication_protocol
        else:
            raise not_implemented_transport_protocol

    def connect(self, communication_id, method, port, baudrate, bytesize, parity, stopbits, timeout):
        self.client = ModbusSerialClient(method=method, port=port, baudrate=baudrate, bytesize=bytesize,
                                         parity=parity, stopbits=stopbits, timeout=timeout)
        if self.client.connect():
            self.device_id = communication_id
            self.connected = True

    def disconnect(self):
        self.client.close()
        self.connected = False
        self.device_id = -1

    def update_temperature_sp(self, temperature=0):
        """Updates the temperature controller setpoint"""
        if not self.connected:
            raise not_connected_instrument
        else:
            self.client.write_register(self.addresses["set_temperature_sp1"], temperature, unit=self.device_id)

    def get_temperature_sp(self):
        """Gets the temperature controller setpoint"""
        if not self.connected:
            raise not_connected_instrument
        else:
            return self.client.read_input_registers(self.addresses["read_temperature_sp1"], count=1, unit=self.device_id)

    def get_actual_temperature(self):
        """Gets the actual temperature of the process"""
        if not self.connected:
            raise not_connected_instrument
        else:
            return self.client.read_input_registers(self.addresses["read_temperature"], count=1, unit=self.device_id)

    def get_actual_output_power(self):
        """Gets the actual output power"""
        if not self.connected:
            raise not_connected_instrument
        else:
            return self.client.read_input_registers(self.addresses["read_output_power"], count=1, unit=self.device_id)

    def set_in_manual_working_mode(self):
        """Sets the temperature controller in manual mode"""
        if not self.connected:
            raise not_connected_instrument
        else:
            return self.client.write_register(self.addresses["set_working_mode"], 1, unit=self.device_id)

    def set_in_auto_working_mode(self):
        """Sets the temperature controller in auto mode"""
        if not self.connected:
            raise not_connected_instrument
        else:
            return self.client.write_register(self.addresses["set_working_mode"], 0, unit=self.device_id)

    def __str__(self):
        if self.connected:
            return "Connected to device " + str(self.client.__str__()) + "\n"
        else:
            return "Device is not yet connected"
