import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
from app import app

class FlaskService(win32serviceutil.ServiceFramework):
    _svc_name_ = "<name you want it called>"
    _svc_display_name_ = "<display name>"
    _svc_description_ = "This service runs the ECSI web application."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        self.main()

    def main(self):
        app.run()

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(FlaskService)
