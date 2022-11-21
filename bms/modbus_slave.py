from pyModbusTCP.server import ModbusServer, DataBank
from time import sleep
from random import uniform
from pyModbusTCP import utils

# Create an instance of ModbusServer
#- if port=502, this code should be run as superuser
# server = ModbusServer("localhost", port=502, no_block=True)
server = ModbusServer("192.168.0.200", port=502, no_block=True)



try:
    print(server.port)
    print("Start server")
    server.start()

    print("Server is online")
    state = [0]
    

    while True:
        # dummy = [int(100)]
        # print("Dummy message:", dummy)

        # DataBank.set_words(0, [int(uniform(0,100))])
        # DataBank.set_words(1, [int(uniform(0,100))])

        # DataBank.set_words(0, [int(1)])
        # DataBank.set_words(1, [int(2)])
        # DataBank.set_words(2, [int(3)])
        # DataBank.set_words(3, [int(4)])
        # DataBank.set_words(4, [int(5)])
        # DataBank.set_bits(0,[2])
        # server.data_bank.set_coils(0,[0])

        print("From addr:0 Get 2bits:", server.data_bank.get_coils(0,2))
    
        # print("2:", server.data_bank.get_coils(2))
        # print("3:", server.data_bank.get_coils(3))
        # print("4:", server.data_bank.get_coils(4))
        # print("0:", hex(DataBank.get_bits(0)[0]))



   


        # print("0:", hex(DataBank.get_words(0)[0]), "1:", hex(DataBank.get_words(1)[0]), "2:", hex(DataBank.get_words(2)[0]), "3:", hex(DataBank.get_words(3)[0]),"4:", hex(DataBank.get_words(4)[0]))

        
        sleep(0.1)

        # if state != DataBank.get_words(1):
        #     state = DataBank.get_words(1)
        #     print("Value of Register 1 has changed to " + str(state))
        #     sleep(0.1)

            
except ValueError:
    print("Shutdown server")
    server.stop()
    print("Server is offline")