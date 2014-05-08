#!/bin/bash

question="..."
SUBDOMAINNAME="$(hostname)"

echo "$SUBDOMAINNAME"

if [ "$SUBDOMAINNAME" = "discourse8" ]; then
	question="My best feature is"
elif [ "$SUBDOMAINNAME" = "discourse10" ]; then
	question="I want to change"
elif [ "$SUBDOMAINNAME" = "discourse6" ]; then
	question="I want you to know"
elif [ "$SUBDOMAINNAME" = "discourse4" ]; then
	question="I am afraid of"
elif [ "$SUBDOMAINNAME" = "discourse0" ]; then
	question="I identify with"
elif [ "$SUBDOMAINNAME" = "discourse7" ]; then
	question="I am grateful for"
elif [ "$SUBDOMAINNAME" = "discourse5" ]; then
	question="I am happiest when"
elif [ "$SUBDOMAINNAME" = "discourse2" ]; then
	question="I depend on"
else
	question="...."
fi

/home/pi/ngrok -subdomain $SUBDOMAINNAME 5000 &
echo "opening tunnel at subdomain $SUBDOMAINNAME"
source /home/pi/printer_discourse/bin/activate
python /home/pi/printer_discourse/run.py "$question" &
echo "starting twilio service with question '$question'"
