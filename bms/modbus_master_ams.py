from pyModbusTCP.client import ModbusClient
import time
import os
# client = ModbusClient(host="192.168.0.200", port=502, debug=True)
client = ModbusClient(host=os.getenv("HOST"), port=int(os.getenv("AMS_PORT")))
i = 10
try:
    client.open()
    while True:
        data = list(range(i, i + 13))
        print(client.write_multiple_registers(0,data))
        i = (i + 13) % 60000
        time.sleep(0.1)
    client.close()
except Exception as e:
    print(e)
    print("Shut Down Client")
    client.close()