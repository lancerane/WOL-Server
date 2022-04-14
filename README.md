# WOL-Server
A lightweight Bottle webserver to run as a systemd service, eg on a raspberry pi, connected via eth cable to a main PC.

HTTP requests trigger the sending of the magic packet via ethernet to wake the PC.
The ethernet driver is unloaded in between requests, to save power.
To make the request, the client must have access to the local network, perhaps through a VPN (https://www.wireguard.com/).

## On the server
### Install dependencies
```
pip install -r requirements.txt
sudo apt-get update && sudo apt-get install etherwake
```
### Set up the environment 
Create a local .env file:
```
PORT=...
MAC_ADDRESS=...[of the receiving PC]
INTERFACE=...[eg, eth0]
ROOT_DIR=...[abs path to the favicon enclosing dir]
ENTRYPOINT=...
ETH_DRIVER=...[as listed on lsmod]
```

### Create the service
/lib/systemd/system/wol_server.service to point to wol_server.py, eg:
```
[Unit]
Description=WOL bottle webserver 
After=network-online.target
 
[Service]
ExecStart=python3 <PATH>/wol_server.py
WorkingDirectory=<PATH>
StandardOutput=inherit
StandardError=inherit
Restart=always
User=<USER>
 
[Install]
WantedBy=multi-user.target
```

### Start the service and enable load on startup
```
sudo systemctl start wol_server.service
sudo systemctl enable wol_server.service
```

### Stop the server
```
sudo systemctl stop wol_server.service
```

## On the receiving PC 
- Enable WOL in the BIOS. May also need to disable fast boot and ErP
- Enable magic packet reception - on Ubuntu:
```
sudo ethtool -s <NIC> wol g
```
Note that this may need to be run at every boot.
- May additionally need to update ethernet drivers

## On the client
Go to http://192.x.x.x:PORT/ENTRYPOINT to send the packet.
