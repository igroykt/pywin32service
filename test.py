import pywin32service
import logging
import time
import datetime
import sys

# @params:  string  "script name for manage from cli"
# @params:  string  "path to script"
# @params:  string  "name that will be displayed in services list"
myapp = pywin32service.PyWIN32Service("test", "d:\\pywin32service\\test.py", "Python Test Script")

logging.basicConfig(filename='test.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def main():
    try:
        logging.info("Program started.")
        print("Program started")
        while True:
            logging.info(datetime.datetime.now())
            print(datetime.datetime.now())
            time.sleep(5)
    except KeyboardInterrupt:
        logging.info("Program terminated.")
        print("Program terminated")

if(len(sys.argv) ==2):
    if sys.argv[1] == "install":
        myapp.install()
    if sys.argv[1] == "uninstall":
        myapp.uninstall()
    if sys.argv[1] == "help":
        myapp.usage()
else:
    main()