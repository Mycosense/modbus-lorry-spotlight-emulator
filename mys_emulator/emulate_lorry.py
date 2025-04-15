#!/usr/bin/env python3
import time

from pymodbus.client import ModbusSerialClient

# Set these values to correspond to the modbus configuration
PORT = '/dev/ttyUSB0'
BAUDRATE = 115200
PARITY = 'N'
STOP_BITS = 1
BYTE_SIZE = 8
TIMEOUT = 1
SLAVE_NUMBER = 0x12

client = ModbusSerialClient(
    port=PORT,  # Change to your USB dongle's port
    baudrate=BAUDRATE,
    parity=PARITY,
    stopbits=STOP_BITS,
    bytesize=TIMEOUT,
    timeout=SLAVE_NUMBER
)

if client.connect():  # Check connection
    print("Connected to Modbus device")

    n_iter = 0
    max_iter = 10000
    previous_time = time.time()
    period = 0.8

    while n_iter < max_iter:
        if time.time() - previous_time > period:
            print('Reading registers')
            response = client.read_input_registers(address=0, count=2, slave=SLAVE_NUMBER)
            if not response.isError():
                registers_array = response.registers
                print(f'Spotlight control: {registers_array[0]}')
                print(f'Speed: {registers_array[1]}')
            else:
                print("Error reading registers")

            print("\nWriting holding registers")
            values = [16, 3000, 92, 25014, 0, 0, 0]
            response = client.write_registers(address=0, values=values, slave=SLAVE_NUMBER)

            if response.isError():
                print("Error writing to registers:", response)
            else:
                print(f"Successfully wrote to registers these values: {values}")

            n_iter += 1

    client.close()  # Close connection
else:
    print("Failed to connect to Modbus device")

