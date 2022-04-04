# WOL-Server
A lightweight webserver to run as a systemd service, eg on a raspberry pi, connected via eth cable to a main PC.
HTML Requests trigger the sending of the magic packet via ethernet to wake the PC.
The ethernet driver is unloaded in between requests, to save power.
To make the request, the client must have access to the local network, perhaps through a VPN (https://www.wireguard.com/).

## Usage
Create /lib/systemd/system/wol_server.service to point to wol_server.py, eg:
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

### Start the server
```
sudo systemctl start wol_server.service
```

### Load on startup 
```
sudo systemctl enable wol_server.service
```

### Stop the server
```
sudo systemctl stop wol_server.service
```

