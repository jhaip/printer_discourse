#!/bin/bash
SUBDOMAINNAME = "discourse$1"
/home/pi/ngrok -subdomain $SUBDOMAINNAME 5000 &
echo "opening tunnel at subdomain $SUBDOMAINNAME"
source /home/pi/printer_discourse/bin/activate
python /home/pi/printer_discourse/run.py &
echo "starting twilio service"