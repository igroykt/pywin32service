# PyWIN32Service
Install Python script as Windows Service

### Requirements:
Python 3.x

Windows Resource Kits: https://www.microsoft.com/en-us/download/details.aspx?id=17657

Administrator rights to get access to system registry

### Basic usage:
install - install script as service

uninstall - remove service

help - print usage info

### Class usage:
**Basic initialization:** myapp = pywin32service.PyWIN32Service("test", "d:\\pywin32service\\test.py", "Python Test Script")

Parameter 1 is a name of service (type: string).

Parameter 2 is a path to python script (type: string).

Parameter 3 is a name of service that will be displayed in list of services (type: string).
