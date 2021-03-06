from flask import Flask, request, redirect
from Adafruit_Thermal import *
import twilio.twiml
import logging, socket, sys

printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)

question = str(sys.argv[1])
 
app = Flask(__name__)

printer.setSize('S')
printer.println("listening for messages!")

def thermalPrintMessage(message):
    printer.setSize('S')
    # printer.feed(1)
    printer.println(question)
    printer.setSize('M')
    printer.println(message)
    printer.setSize('S')
    printer.feed(1)
    printer.println('________________________________')

def logMessage(from_number,message):
    logging.warn(from_number+"\t"+message)
 
@app.route("/", methods=['GET', 'POST'])
def hello_monkey():

    message = "Thanks for participating!\n- The Printer Discourse"
 
    from_number = request.values.get('From', None)
    in_message = request.values.get('Body', None)

    if in_message == "give me the ip":
        print "Attempting to print IP"
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 0))
            in_message = s.getsockname()[0]
        except:
            in_message = 'Network is unreachable.'
        message = in_message

    logging.basicConfig(filename='log.log',level=logging.WARN,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logMessage(from_number,in_message)

    print "Message from:", from_number
    print in_message
    print "---"

    thermalPrintMessage(in_message)

    resp = twilio.twiml.Response()
    resp.message(message)
 
    return str(resp)
 
if __name__ == "__main__":
    app.run(debug=True)
