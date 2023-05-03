local_ipv4_addr = "192.168.1.70/24"                      # IPv4 Address - local machine's Wireless LAN
honeywell_301C_ipv4_addr = "192.168.1.254"               # IPv4 Address - Honeywell 301C Controller - IPv4 address
ethernet_ipv4_addr = "192.168.1.80/24"                   # IPv4 Address - Ethernet switch (type = managed)
yabe_room_sim_port = "55481"                             # YABE generates port for simulation (new # each time ROOM SIM is started)

# Socket ports on hardware
BAC0_port = "47808"                                      # This is a defined in BACnet as the port #
BAC0_alt = [i for i in range(1, 10)]

# Sensor IDs (Founding YABE)
OBJ_ID_PPM = [513]                                       # BACnet ID of PPM reading found using (YABE: https://sourceforge.net/projects/yetanotherbacnetexplorer/)
OBJ_ID_BUZZ = [46360]                                       # BACnet ID of PPM reading found using (YABE: https://sourceforge.net/projects/yetanotherbacnetexplorer/)


if __name__ == "__main__":
    print(BAC0_alt)