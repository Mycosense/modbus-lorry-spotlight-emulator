#!/usr/bin/env python3
import logging
import argparse
from pymodbus.server import StartSerialServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

from mys_emulator.custom_data_block import create_spotlight_holding_register_block
from mys_emulator.custom_data_block import create_spotlight_input_register_block

# Enable logging to see requests
logging.basicConfig(level=logging.CRITICAL)


# Config for modbus/serial com.
CONFIG_BAUDRATE = 115200
CONFIG_PARITY = "N"
CONFIG_STOPBITS = 1
CONFIG_BYTESIZE = 8
CONFIG_TIMEOUT = 1

# Config modbus
CONFIG_SLAVE_ID = 0x12


def main():

    parser = argparse.ArgumentParser(description="Emulate spotlight communication with the lorry")
    parser.add_argument("port", type=str, help="Serial port (e.g. /dev/tty.usbserial-AU051GIN, or COM3 on windows)")
    parser.add_argument("speed", type=int, help="Spotlight speed mm/min (0 to 10000")
    args = parser.parse_args()
    port = args.port
    speed = args.speed
    if 10000 < speed or speed < 0:
        exit(1)

    store = ModbusSlaveContext(di=None,
                               co=None,
                               hr=create_spotlight_holding_register_block(),
                               ir=create_spotlight_input_register_block(speed))
    context = ModbusServerContext(slaves={CONFIG_SLAVE_ID: store}, single=False)

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
