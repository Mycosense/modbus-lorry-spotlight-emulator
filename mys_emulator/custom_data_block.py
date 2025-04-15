from pymodbus.datastore import ModbusSparseDataBlock

from mys_emulator.utils import uint16_to_bit_array, bit_array_to_uint16


# Input registers
REG_30001_ADDR = 0x00  # Spotlight control FIXME in datasheet it's 0x00
REG_30002_ADDR = 0x01  # Spotlight speed FIXME in datasheet it's 0x01

SL_CTL_ENABLE = 1  # b0: Spotlight control enable
REG_30001_VAL = bit_array_to_uint16([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, SL_CTL_ENABLE])
REG_30002_VAL = 2000  # unit16 spotlight speed mm/min


# Holding registers
REG_40001_ADDR = 0x01  # Lorry status FIXME in datasheet it's 0x00
REG_40002_ADDR = 0x02  # Lorry speed FIXME in datasheet it's 0x01
REG_40003_ADDR = 0x03  # Lorry battery level FIXME in datasheet it's 0x02
REG_40004_ADDR = 0x04  # Lorry battery voltage FIXME in datasheet it's 0x03
REG_40005_ADDR = 0x05  # Lorry weight 1 FIXME in datasheet it's 0x04
REG_40006_ADDR = 0x06  # Lorry weight 2 FIXME in datasheet it's 0x05
REG_40007_ADDR = 0x07  # Lorry weight 3 FIXME in datasheet it's 0x06
REG_40001_VAL = 0
REG_40002_VAL = 0
REG_40003_VAL = 0
REG_40004_VAL = 0
REG_40005_VAL = 0
REG_40006_VAL = 0
REG_40007_VAL = 0


class SpotlightInputRegistersDataBlock(ModbusSparseDataBlock):
    """ Custom Data Block to log and modify responses dynamically. """

    def __init__(self, values):
        super().__init__(values)

    def getValues(self, address, count=1):
        """ Hook into reads to modify responses dynamically. """
        values = super().getValues(address, count)
        print(f"Client Read -> Address: {address}, Count: {count}, Values: {values}")
        return values


class SpotlightHoldingRegisterDataBlock(ModbusSparseDataBlock):
    """ Custom Data Block to log and modify responses dynamically. """

    def __init__(self, values):
        super().__init__(values)

    def setValues(self, address, values):
        """ Hook into writes to log and modify data dynamically. """
        print(f"Client Write -> Address: {address}, Values: {values}")
        super().setValues(address, values)
        self.decode_registers()

    def decode_registers(self):
        # Decoding value received from the lorry for debug
        values = super().getValues(REG_40001_ADDR, 7)
        reg_40001 = list(reversed(uint16_to_bit_array(values[0])))
        print('Received value from lorry:')
        print(f'- lorry status, error: {reg_40001[0]}')
        print(f'- lorry status, horizontal limit right: {reg_40001[1]}')
        print(f'- lorry status, horizontal limit left: {reg_40001[2]}')
        print(f'- lorry status, emergency stop active: {reg_40001[3]}')
        print(f'- lorry status, spotlight suggestion mode active: {reg_40001[4]}')
        print(f'- lorry status, error code: {reg_40001[5:]}')
        print(f'- lorry speed: {values[1]}')
        print(f'- lorry battery level: {values[2]}%')
        print(f'- lorry battery voltage: {values[3]}mV')
        print(f'- lorry weight 1: {values[4]}g')
        print(f'- lorry weight 2: {values[5]}g')
        print(f'- lorry weight 3: {values[6]}g')


def create_spotlight_input_register_block(speed: int) -> SpotlightInputRegistersDataBlock:
    REG_30002_VAL = speed
    return SpotlightInputRegistersDataBlock({
        REG_30001_ADDR: REG_30001_VAL,
        REG_30002_ADDR: REG_30002_VAL
    })


def create_spotlight_holding_register_block() -> SpotlightHoldingRegisterDataBlock:
    return SpotlightHoldingRegisterDataBlock({
        REG_40001_ADDR: REG_40001_VAL,
        REG_40002_ADDR: REG_40002_VAL,
        REG_40003_ADDR: REG_40003_VAL,
        REG_40004_ADDR: REG_40004_VAL,
        REG_40005_ADDR: REG_40005_VAL,
        REG_40006_ADDR: REG_40006_VAL,
        REG_40007_ADDR: REG_40007_VAL,
    })
