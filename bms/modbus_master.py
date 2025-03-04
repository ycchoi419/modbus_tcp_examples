from pyModbusTCP.client import ModbusClient
from time import sleep

client = ModbusClient(host="10.0.100.20", port=502)


try:
    client.open()
    while True:
        # print(client.read_holding_registers(0))
        # print(client.read_holding_registers(0, 4))
        client.write_multiple_registers(3,[22,2,3])
        sleep(0.1)
        # client.close()
except:
    print("Shut Down Client")
    client.close()