#!/bin/bash

question="..."
SUBDOMAINNAME="$(hostname)"

if [ "$SUBDOMAINNAME" = "discourse8" ]; then
    question="My best feature is"
else if [ "$SUBDOMAINNAME" = "discourse10" ]; then
    question="I want to change"
else if [ "$SUBDOMAINNAME" = "discourse6" ]; then
    question="I want you to know"
else if [ "$SUBDOMAINNAME" = "discourse4" ]; then
    question="I am afraid of"
else if [ "$SUBDOMAINNAME" = "discourse0" ]; then
    question="I identify with"
else if [ "$SUBDOMAINNAME" = "discourse7" ]; then
    question="I am grateful for"
else if [ "$SUBDOMAINNAME" = "discourse5" ]; then
    question="I am happiest when"
else if [ "$SUBDOMAINNAME" = "discourse2" ]; then
    question="I depend on"
else
    question="...."
fi

/home/pi/ngrok -subdomain $SUBDOMAINNAME 5000 &
echo "opening tunnel at subdomain $SUBDOMAINNAME"
source /home/pi/printer_discourse/bin/activate
python /home/pi/printer_discourse/run.py "$question" &
echo "starting twilio service with question '$question'"