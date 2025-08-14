import sys
sys.path.insert(0, './env/Lib/site-packages')

from pymodbus.exceptions import ModbusException
from pymodbus.pdu import ExceptionResponse
from pymodbus.client import ModbusTcpClient

SLAVE = 0x01


def read_coil_call(client, coil):
    """Show complete modbus call, sync version."""
    try:
        rr = client.read_coils(coil, 1, slave=SLAVE)
    except ModbusException as exc:
        txt = f"ERROR: exception in pymodbus {exc}"
        raise exc
    if rr.isError():
        txt = "ERROR: pymodbus returned an error!"
        raise ModbusException(txt)
    if isinstance(rr, ExceptionResponse):
        txt = "ERROR: received exception from device {rr}!"
        # THIS IS NOT A PYTHON EXCEPTION, but a valid modbus message
        raise ModbusException(txt)

    # Validate data
    txt = f" Coil response: {rr.bits[0]}"
    #print(rr.bits[0])
    #print(txt)
    # test = int.from_bytes(rr.encode(), "little")
    # print(test)

    ##print(txt)
    return rr.bits[0]

def write_coil_call(client, coil, state):
    """Show complete modbus call, sync version."""
    try:
        #rr = client.read_coils(coil, 1, slave=SLAVE)
        rr = client.write_coil(coil,state,slave=SLAVE)
    except ModbusException as exc:
        txt = f"ERROR: exception in pymodbus {exc}"
        raise exc
    if rr.isError():
        txt = "ERROR: pymodbus returned an error!"
        raise ModbusException(txt)
    if isinstance(rr, ExceptionResponse):
        txt = "ERROR: received exception from device {rr}!"
        # THIS IS NOT A PYTHON EXCEPTION, but a valid modbus message
        raise ModbusException(txt)

def read_memory_word_call(client, address):
    """Leitura de registrador (holding register - 16 bits)"""
    try:
        rr = client.read_holding_registers(address, 1, slave=SLAVE)
    except ModbusException as exc:
        raise ModbusException(f"ERROR: exception in pymodbus {exc}")
    if rr.isError() or isinstance(rr, ExceptionResponse):
        raise ModbusException("ERROR: Modbus register read failed.")
    return rr

def write_memory_word_call(client, address, value):
    """Escrita de registrador (holding register - 16 bits)"""
    try:
        rr = client.write_register(address, value, slave=SLAVE)
    except ModbusException as exc:
        raise ModbusException(f"ERROR: exception in pymodbus {exc}")
    if rr.isError() or isinstance(rr, ExceptionResponse):
        raise ModbusException("ERROR: Modbus register write failed.")
