# PyWIN32Service
Install Python script as Windows Service. This is a wrapper for srvany and compatible with ConfigParser or any other libraries. You can use srvany and create registry keys manually each time or you can use this wrapper that will handle the rest. To use it you have to change the entry point of your program so that it pays respect to the wrapper (see test.py for example).

### Requirements:
Python 3.x

Windows Resource Kits: https://www.microsoft.com/en-us/download/details.aspx?id=17657

Administrator rights to get access to system registry

Make sure that path to Windows Resource Kits and Python exists in %PATH%

### Class usage:
**Initialization:** myapp = pywin32service.PyWIN32Service("test", "d:\\\pywin32service\\\test.py", "Python Test Script")

Parameter 1 is a name of service (type: string).

Parameter 2 is a path to python script (type: string).

Parameter 3 is a name of service that will be displayed in list of services (type: string).

**Install:** myapp.install()

**Uninstall:** myapp.uninstall()

**Print help:** myapp.usage()

### CLI usage:
```
D:\pywin32service>python test.py install
Service installed successfully

D:\pywin32service>net start test
Служба "Python Test Script" запускается.
Служба "Python Test Script" успешно запущена.

D:\pywin32service>sc query test
Имя_службы: test
        Тип                : 10  WIN32_OWN_PROCESS
        Состояние          : 4  RUNNING
                                (STOPPABLE, PAUSABLE, ACCEPTS_SHUTDOWN)
        Код_выхода_Win32   : 0  (0x0)
        Код_выхода_службы  : 0  (0x0)
        Контрольная_точка  : 0x0
        Ожидание           : 0x0

D:\pywin32service>net stop test
Служба "Python Test Script" успешно остановлена.

D:\pywin32service>python test.py uninstall
Service uninstalled successfully
```
