import serial.tools.list_ports

class SerialCtrl():
    def __init__(self):
      self.com_list = []

    def getCOMList(self):
       ports= serial.tools.list_ports
       

if __name__=="__main__":
    SerialCtrl()