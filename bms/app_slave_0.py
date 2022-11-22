from pyModbusTCP.server import ModbusServer, DataBank
from time import sleep
from random import uniform
from pyModbusTCP import utils


import tkinter as tk
master = tk.Tk()





# TK Parameters /////////////////////////////////////////////////////////////////////////////////

# Display Parameters
text_width  = 50
text_height = 1.5
text_bg     = "#9BC2E6"     # Background Colour

# Entry Parameters
entry_width = 30

#//////////////////////////////////////////////////////////////////////////////////////////////






# Entry and Diplay Cells /////////////////////////////////////////////////////////////////////////////////

# Signal 1
tk.Label(master, text="Signal 1 (BMS Status in BMS -> NAS REQ Pack)").grid(row=0, column=0)
o1 = tk.Text(master, width=text_width, height=text_height, bg = text_bg)
o1.grid(row=0, column=1, padx=20, pady=5)

# tk.Label(master, text="Signal 1 (RESP: NAS -> BMS):").grid(row=0, column=2)
# e1 = tk.Entry(master, width=entry_width)
# e1.grid(row=0, column=3, padx=20, pady=5)       





# Signal 2
tk.Label(master, text="Signal 2 (RPM Set Pt in BMS -> NAS REQ Pack):").grid(row=1, column=0)
o2 = tk.Text(master, width=text_width, height=text_height, bg = text_bg)
o2.grid(row=1, column=1, padx=20, pady=5)

# tk.Label(master, text="Signal 2 (RESP: NAS -> BMS):").grid(row=1, column=2)
# e2 = tk.Entry(master, width=entry_width)
# e2.grid(row=1, column=3, padx=20, pady=5)  





# Signal 3
tk.Label(master, text="Signal 3 (RPM Actual in BMS -> NAS REQ Pack):", anchor="w").grid(row=2, column=0)
o3 = tk.Text(master, width=text_width, height=text_height, bg = text_bg)
o3.grid(row=2, column=1, padx=20, pady=5)

# tk.Label(master, text="Signal 3 (RESP: NAS -> BMS):").grid(row=2, column=2)
# e3 = tk.Entry(master, width=entry_width)
# e3.grid(row=2, column=3, padx=20, pady=5)  




# Signal 4
# Label
tk.Label(master, text="Signal 4 (NAS Status to be included in NAS -> BMS RESP Pack):", anchor="w").grid(row=3, column=0)
e4 = tk.Entry(master, width=entry_width)       
e4.grid(row=3, column=1, padx=20, pady=5)


tk.Label(master, text="[NAS-ABNORMAL, NAS-AUTO-ACT, NAS-AUTO-RDY] (Default: 001)", anchor="w").grid(row=3, column=2)
# tk.Label(master, text="Signal 4 (RESP: BMS -> NAS):").grid(row=3, column=2)
# o4 = tk.Text(master, width=text_width, height=text_height, bg = text_bg)
# o4.grid(row=3, column=3, padx=20, pady=5)





# Signal 5
tk.Label(master, text="Signal 5 (RESP: NAS -> BMS):", anchor="w").grid(row=4, column=0)
e5 = tk.Entry(master, width=entry_width)
e5.grid(row=4, column=1, padx=20, pady=5)

# tk.Label(master, text="Signal 5 (RESP: BMS -> NAS):").grid(row=4, column=2)
# o5 = tk.Text(master, width=text_width, height=text_height, bg = text_bg)
# o5.grid(row=4, column=3, padx=20, pady=5)






# Server = Slave
server = ModbusServer("192.168.0.200", port=502, no_block=True)

# Cliet = Master is "192.168.0.99" (Test Condition)







# Slave Server ------------------------------------------------------

# Open a Slave Server
def open_slave_server():
    # server = ModbusServer("192.168.0.200", port=502, no_block=True)
    print("Start server")
    server.start()
    print("Server is online")


# STOP a Slave Server
def stop_slave_server():
    # server = ModbusServer("192.168.0.200", port=502, no_block=True)
    print("Shutdown server")
    server.stop()
    print("Server is offline")

# -------------------------------------------------------------------






# --------------------------------------------------------------------------------------------------------------
# - Get Data from REQ Signal from BMS


# BMS Status (Function Code 0x0F (15:Write Multiple Coils))
# - pyModbusTCP automatically sends response to the master
def get_bms_status():
    # Address = 00, Bits: 2bits
    bms_status = server.data_bank.get_coils(0, 2)

    # Display to the GUI
    o1.insert(tk.INSERT,"BMS_AUTO_MODE_RDY:" + str(bms_status[0]) + " / BMS_AUTO_MODE_ACT:" + str(bms_status[1]))
    

    # Display to the terminal
    print("BMS_AUTO_MODE_RDY:", bms_status[0], "BMS_AUTO_MODE_ACT:", bms_status[1])



# (Function Code 0x10(16: Multiple Registers) )
def get_bms_set_rpm():
    # Address = 00, Bits: 4bits ('1' get 4bits)
    bms_set_rpm = server.data_bank.get_holding_registers(0,1)

    # Display to the GUI
    o2.insert(tk.INSERT,"RPM Setting:" + str(int(bms_set_rpm[0] / 10)))
    
    # Display to the terminal
    print("RPM Setting:", int(bms_set_rpm[0]/10))




# (Function Code 0x10(16: Multiple Registers) )
def get_bms_actual_set_rpm():
    # Address = 100
    bms_set_actual_rpm = server.data_bank.get_holding_registers(100, 2)
    # (Old, Deprecated)
    # bms_actual_rpm = server.data_bank.get_holding_registers(0,2)


    # Display to the GUI (Non-complementary Number)
    # o2.insert(tk.INSERT,"RPM Setting:" + str(int(bms_set_actual_rpm[0] / 10)))
    # o3.insert(tk.INSERT,"RPM Actual:"  + str(int(bms_set_actual_rpm[1] / 10)))


    # Display to the GUI (Two's complementary Number)
    o2.insert(tk.INSERT,"RPM Setting:" + str(_to_int(hex2complement(bms_set_actual_rpm[0]),16)))
    o3.insert(tk.INSERT,"RPM Actual:"  + str(_to_int(hex2complement(bms_set_actual_rpm[1]),16)))
    
    # Display to the terminal
    print("10 X RPM Setting:", str(_to_int(hex2complement(bms_set_actual_rpm[0]), 16)))
    print("10 X RPM Actual :", str(_to_int(hex2complement(bms_set_actual_rpm[1]), 16)))
    # print("RPM Setting:", int(bms_set_actual_rpm[0] / 10))
    # print("RPM Actual :", int(bms_set_actual_rpm[1] / 10))

    # Print for Two's complement of Hex Number
    # print("Setting Point RPM:", bin(bms_set_actual_rpm[0]), "Hex:", bin(int(65535)), "Two's complementary:", hex2complement(bms_set_actual_rpm[0]), "Comp-Hex-to-int:", _to_int(hex2complement(bms_set_actual_rpm[0]),16))
# --------------------------------------------------------------------






# ---------------------------------------------------------------------------------------------------
# - Bits, HEX Manipulation, Utils
# - References
#  -> https://www.codegrepper.com/code-examples/python/how+to+convert+integer+to+hex+signed+2%27s+complement+in+python
def to_hex(val, nbits):
  return hex((val + (1 << nbits)) % (1 << nbits)).lstrip('0x')

def hex2complement(number):
    hexadecimal_result = format(number, "03X")
    return hexadecimal_result.zfill(4) # .zfill(n) adds leading 0's if the integer has less digits than n

def _to_int(val, nbits):
    i = int(val, 16)
    if i >= 2 ** (nbits - 1):
        i -= 2 ** nbits
    return i
#----------------------------------------------------------------------------------------------------





# ---------------------------------------------------------------------------------------------------
# - Input Data to be sent to BMS as a RESPONSE

# (Function Code 0x02 (Master Setting is "02: Read Discrete Inputs(1X)") )
def resp_nas_status():

    # Default (001)
    #- bit2: HiNAS Abnormal = 0
    #- bit1: Auto Mode Act  = 0
    #- bit0: Auto Mode RDY  = 1
    default_input = "001"
    
    # Dealing with an exceptional input decided by length of the input 
    if (len(e4.get()) == 0) or (len(e4.get()) == 1) or (len(e4.get()) == 2):
        gui_input = default_input
    else:
        gui_input = e4.get()

    # Get bits from the entry
    nas_auto_mode_ready = int(gui_input[2]) # bit 0
    nas_auto_mode_act   = int(gui_input[1]) # bit 1
    nas_abnormal        = int(gui_input[0]) # bit 2
    nas_status = server.data_bank.set_discrete_inputs(0, [nas_auto_mode_ready, nas_auto_mode_act, nas_abnormal])
    
    print("Input From GUI:", e4.get())
    print("NAS_STATUS(Bin):", nas_abnormal, nas_auto_mode_act, nas_auto_mode_ready)



# (Function Code 0x04 (Mater Setting is "04 Read Input Registers(3x)"))
def resp_nas_rpm_cmd():
    default_input = "80"

    if (len(e5.get())==0) or (len(e5.get())==1):
        gui_input = default_input
    else:
        gui_input = e5.get()
    
  
    num_bits =16
    rpm_set_hex2c = hex2complement(int(gui_input))
    rpm_set_int2c = _to_int(rpm_set_hex2c,num_bits)
    server.data_bank.set_input_registers(0,[rpm_set_int2c])

    print("RPM SET PT hex2c:", rpm_set_hex2c, "int2c:", rpm_set_int2c)


    # (Deprecated)----------------------------------------------------------------
    # nas_set_rpm = server.data_bank.set_input_registers(0,[int(10*int(rpm_set_int2cgui_input))])
    # print("NAS_RPM_SET(Dec):", int(10*int(gui_input)))
    # ----------------------------------------------------------------------------

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////





def show():
    o1.delete('1.0', tk.END)
    o2.delete('1.0', tk.END)
    o3.delete('1.0', tk.END)

    # print("Work: %s" % e4.get())
    # print("author:%s" % e5.get())

    # o1.insert(tk.INSERT,"dd")

    # e4.delete(0, "end")
    # e5.delete(0, "end")

    #-------------
    get_bms_status()
    get_bms_actual_set_rpm()
    #-------------

    #-------------
    resp_nas_status()
    resp_nas_rpm_cmd()
    #-------------
   

    master.after(ms=1000, func=show)





# Button ------------------------------------------------------------------------------------------------------------------------------
tk.Button(master, text="Start Slave(Server)", width=10, command=open_slave_server).grid(row=5, column=0, sticky= "w", padx=10, pady=5)
tk.Button(master, text="Stop Slave(Server)", width=10, command=stop_slave_server).grid(row=5, column=1, sticky= "w", padx=10, pady=5)
tk.Button(master, text="Start Test", width=10, command=show).grid(row=5, column=2, sticky= "w", padx=10, pady=5)
# tk.Button(master, text="GET BMS STATUS", width=10, command=get_bms_set_rpm).grid(row=5, column=3, sticky= "w", padx=10, pady=5)
tk.Button(master, text="Exit", width=10, command=master.quit).grid(row=5, column=3, sticky="e", padx=10, pady=5)
#--------------------------------------------------------------------------------------------------------------------------------------



master.wm_title("BMS Interface Tester")
master.mainloop()