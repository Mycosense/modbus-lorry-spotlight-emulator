#!/usr/bin/env python3
import logging
import argparse
from pymodbus.server import StartSerialServer
from pymodbus.datastore import ModbusSparseDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

# Enable logging to see requests
logging.basicConfig(level=logging.CRITICAL)


# Config for modbus/serial com.
CONFIG_BAUDRATE = 115200
CONFIG_PARITY = "N",
CONFIG_STOPBITS = 1,
CONFIG_BYTESIZE = 8,
CONFIG_TIMEOUT = 1,

# Config modbus
CONFIG_SLAVE_ID = 0x12


class CustomDataBlock(ModbusSparseDataBlock):
    """ Custom Data Block to log and modify responses dynamically. """

    def __init__(self, values):
        super().__init__(values)

    def getValues(self, address, count=1):
        """ Hook into reads to modify responses dynamically. """
        values = super().getValues(address, count)
        print(f"Client Read -> Address: {address}, Count: {count}, Values: {values}")
        return values

    def setValues(self, address, values):
        """ Hook into writes to log and modify data dynamically. """
        print(f"Client Write -> Address: {address}, Values: {values}")
        super().setValues(address, values)


ir_data_block = CustomDataBlock({
    0: 0,
    1: 0xFFFF,
    2: 2000
})

hr_data_block = CustomDataBlock({i: 0 for i in range(100)})

store = ModbusSlaveContext(di=None,
                           co=None,
                           hr=hr_data_block,
                           ir=ir_data_block)
context = ModbusServerContext(slaves={CONFIG_SLAVE_ID: store}, single=False)


def main():

    parser = argparse.ArgumentParser(description="Emulate spotlight communication with the lorry")
    parser.add_argument("port", type=str, help="Serial port (e.g. /dev/tty.usbserial-AU051GIN, or COM3 on windows)")
    args = parser.parse_args()
    port = args.port

    print(f"Starting Modbus RTU Slave on {port} at {CONFIG_BAUDRATE} baud...")
    StartSerialServer(
        context,
        port=port,
        baudrate=CONFIG_BAUDRATE,
        parity=CONFIG_PARITY,
        stopbits=CONFIG_STOPBITS,
        bytesize=CONFIG_BYTESIZE,
        timeout=CONFIG_TIMEOUT,
    )


if __name__ == "__main__":
    main()
