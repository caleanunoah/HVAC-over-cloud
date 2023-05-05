local_ipv4_addr = "192.168.1.70/24"                      # IPv4 Address - local machine's Wireless LAN
honeywell_301C_ipv4_addr = "192.168.1.72"               # IPv4 Address - Honeywell 301C Controller
ethernet_ipv4_addr = "192.168.1.80/24"                   # IPv4 Address - Ethernet switch

ipv4_pc = "192.168.1.70/24"
ipv4_orangepi = "192.168.1.75/24"

# Socket ports on hardware
BAC0_port = "47808"                                      # This is a defined in BACnet as the port #

# Sensor IDs (Founding YABE)
OBJ_ID_PPM = ["513"]                                       # BACnet ID of PPM reading found using (YABE: https://sourceforge.net/projects/yetanotherbacnetexplorer/)
OBJ_ID_BUZZ = ["46360"]                                    # BACnet ID of PPM reading found using (YABE: https://sourceforge.net/projects/yetanotherbacnetexplorer/)
