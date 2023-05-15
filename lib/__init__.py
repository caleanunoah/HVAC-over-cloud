#local_ipv4_addr = "192.168.1.70/24"                      # (Initial) IPv4 Address - local machine
honeywell_301C_ipv4_addr = "192.168.137.253"               # IPv4 Address - Honeywell 301C Controller
ethernet_ipv4_addr = "192.168.1.80/24"                   # IPv4 Address - Ethernet switch

ipv4_pc = "192.168.137.1/24"                            # Laptop Ethernet addr.
ipv4_orangepi = "192.168.1.75/24"

# Socket ports on hardware
BAC0_port = "47808"                                      # This is a defined in BACnet as the port #

# Sensor IDs (Founding YABE)
# NEU RLDS IDs
#             [Adr 2, Adr. 1, Adr 3, Adr 4]
#OBJ_ID_PPM = ["513", "257", "769", "1025"]                                       # BACnet ID of PPM reading found using (YABE: https://sourceforge.net/projects/yetanotherbacnetexplorer/)
OBJ_ID_PPM = ["513"]                                       # BACnet ID of PPM reading found using (YABE: https://sourceforge.net/projects/yetanotherbacnetexplorer/)
OBJ_ID_BUZZ = ["46360"]                                    # BACnet ID of PPM reading found using (YABE: https://sourceforge.net/projects/yetanotherbacnetexplorer/)
