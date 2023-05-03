# HVAC Over Cloud

## About
HVAC-over-cloud is software running on an embedded sensor network. This repo was designed using the Orange Pi 5 hardware (OP5). The OP5 is connected to the sensor network and samples the data. After formatting, the data is sent to an AWS Cloud DB

## How to Use
1. Flash OS onto OP5 [link](http://www.orangepi.org/html/hardWare/computerAndMicrocontrollers/service-and-support/Orange-pi-5.html)
> Project uses Ubunutu 20.0.3
2. Log into OP5 GUI and connect to internet
3. Install Pycharm or equivalent IDE (Python 3.8 < x)
3. Install git bash 
4. Open terminal, run cmd (with [repo-https-link](https://github.com/caleanunoah/HVAC-over-cloud))
    ```commandline
    git clone [repo-https-link]
    cd hvac-over-cloud
   ```

## Examples
Connecting the Orange Pi 5 to the BACnet module of the Honeywell 301C. Then run 'main.py' In the terminal you will see a dictionary of info printed with information from the 301C
