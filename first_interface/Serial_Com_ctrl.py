import serial.tools.list_ports

class SerialCtrl():
    def __init__(self):
      self.com_list = []

    def getCOMList(self):
       ports= serial.tools.list_ports.comports()
       self.com_list = [com[0] for com in ports]
       self.com_list.insert(0, "-")

if __name__=="__main__":
    SerialCtrl()