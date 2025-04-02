#!/usr/bin/env python3
import logging
import argparse
from pymodbus.server import StartSerialServer
from pymodbus.datastore import ModbusSparseDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification


# Config for modbus/serial com.
CONFIG_BAUDRATE = 115200
CONFIG_PARITY = "N",
CONFIG_STOPBITS = 1,
CONFIG_BYTESIZE = 8,
CONFIG_TIMEOUT = 1,

# Enable logging to see requests
logging.basicConfig(level=logging.CRITICAL)


class LiveDataBlock(ModbusSparseDataBlock):
    """ Custom Data Block to log and modify responses dynamically. """

    def __init__(self, values):
        super().__init__(values)

    def getValues(self, address, count=1):
        """ Hook into reads to modify responses dynamically. """
        values = super().getValues(address, count)
        logging.info(f"Client Read -> Address: {address}, Count: {count}, Values: {values}")
        print(f"Client Read -> Address: {address}, Count: {count}, Values: {values}")

        # Example: If the client reads register 10, return a dynamic value
        # if address == 1:
        #    return [42]  # Always return 42 at address 10

        return values

    def setValues(self, address, values):
        """ Hook into writes to log and modify data dynamically. """
        logging.info(f"Client Write -> Address: {address}, Values: {values}")
        print(f"Client Write -> Address: {address}, Values: {values}")
        super().setValues(address, values)
        # print(f"values: {super().getValues(0, 20)}")


# Initialize Data Store
# data_block = LiveDataBlock({i: 0 for i in range(100)})  # Registers 0-99
# store = ModbusSlaveContext(hr=data_block, di=None, co=None, ir=data_block)
# context = ModbusServerContext(slaves={18: store}, single=True)

# ✅ Corrected: Pass the dictionary inside `LiveDataBlock`
hr_data_block = LiveDataBlock({i: 0 for i in range(256)})  # Registers 0-99
ir_data_block = LiveDataBlock(
    {0: 0, 1: 0xFFFF, 2: 1000, 3: 0}
)  # Registers 0-99

# ✅ Corrected: Ensure `di`, `co`, `ir`, and `hr` all use a valid data block
store = ModbusSlaveContext(di=None, co=None, hr=hr_data_block, ir=ir_data_block)

# ✅ Corrected: Ensure `single=False` when using multiple slave IDs
context = ModbusServerContext(slaves={18: store}, single=False)


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
