# HVAC Over Cloud

## About
HVAC-over-cloud is software running as an embedded device within a sensor network. The OP5 monitors HVAC environments which involve an array of wired sensors. This repo was designed using the Orange Pi 5 hardware (OP5). The OP5 is connected to the sensor network and samples the data. After formatting, the data is sent to an AWS Cloud DB

## Navigating Repo

**./lib > __init__.py**  holds many network connection paramers
**main.py**  Program entry point

## How to Use
1. Flash OS onto OP5 [link](http://www.orangepi.org/html/hardWare/computerAndMicrocontrollers/service-and-support/Orange-pi-5.html)
   > Project uses Ubuntu 20.0.3
2. Log into OP5 GUI and connect to internet
   > Ethernet connection (Can do wireless if you have a wireless adapter or the Orange Pi 5B.)
3. Install Pycharm or equivalent IDE
   > Python 3.8 or higher
4. Install git bash 
5. Open git bash & run cmd (with [repo-link](https://github.com/caleanunoah/HVAC-over-cloud))
    ```commandline
    git clone repo-link
    cd hvac-over-cloud
   ```
6. Open shell and run cmd
   ```commandline
   pip install -r requirements.txt 
   ```
7. Run cmd and note down static ipv4 address for Orange Pi 5
    ```commandline
    ifconfig 
    ```
8. Adjust lib.__init__ if needed 
9. Run 'main.py' & if BACnet do next step
10. (If BACnet) Run 'main.py' and note down the Honeywell 301C IPv4 address and adjust)

## Examples
Some example applications of the HVAC over Cloud embedded system 

## Example 1: Refrigerant Leak Detection System
Connecting the Orange Pi 5 to the BACnet network for monitoring of a Refrigerant Leak Detection system

Sensor Network ---> BACnet Module ---> Orange Pi 5 ---> Cloud DB



