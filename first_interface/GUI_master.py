from tkinter import *
from tkinter import messagebox

class RootGUI:
    def __init__(self):
        self.root=Tk()
        self.root.title("Serial communication")
        self.root.geometry("800x500")
        self.root.config(bg="Cornsilk")


class ComGUI():
   def __init__(self,root, serial):
      self.root = root
      self.serial = serial
      self.frame = LabelFrame(root, text="Com manager", padx=5, pady=5, bg="white")
      self.label_com = Label( 
         self.frame, text="Available port(s): ", bg="white", width=15, anchor="w")
      self.label_bd = Label(
         self.frame, text="Baude Rate: ", bg="white", width=15, anchor="w")
      self.btn_refresh = Button(
         self.frame, text="Refresh", width= 10, command=self.com_refresh)
      self.btn_connect = Button(
         self.frame, text="Connect", width= 10, state="disabled" , command=self.serial_connect)
      self.BaudOptionMenu()
      self.ComOptionMenu()
      self.publish()


   def ComOptionMenu(self):
      self.serial.getCOMList()      
      self.clicked_com = StringVar()
      self.clicked_com.set(self.serial.com_list[0])
      self.drop_com = OptionMenu(
         self.frame, self.clicked_com, *self.serial.com_list, command=self.Connect_ctrl)
      self.drop_com.config(width=10)


   def BaudOptionMenu(self):
      bds = ["-", "110", "300", "600", "1200", "2400", "4800", "9600", "14400", "19200", "38400", "57600", "115200"]
      self.clicked_bd=StringVar()
      self.clicked_bd.set(bds[0])
      self.drop_bd = OptionMenu(
         self.frame, self.clicked_bd, *bds, command=self.Connect_ctrl)
      self.drop_bd.config(width=10)
 
   
   def publish(self):
      self.frame.grid(row=0, column=0, rowspan=3, columnspan=3, padx=5, pady=5)
      self.label_com.grid(column=1, row=2)
      self.drop_com.grid(column=2, row=2)
      self.label_bd.grid(column=1, row=3)
      self.drop_bd.grid(column=2, row=3)
      self.btn_refresh.grid(column=3, row=2)
      self.btn_connect.grid(column=3, row=3)
   
   def Connect_ctrl(self, other):
      if "-" in self.clicked_com.get() or "-" in self.clicked_bd.get():
          self.btn_connect["state"]= "disable"
      else:
         self.btn_connect["state"]= "active"

   
   def com_refresh(self):
      self.drop_com.destroy()
      self.ComOptionMenu()
      self.drop_com.grid(column=2, row=2)
      logic = []
      self.Connect_ctrl(logic)

   def serial_connect(self):
      if self.btn_connect ["text"] in "Connect":
         self.serial.SerialOpen(self)
         if self.serial.ser.status:
            self.btn_connect["text"] = "Disconnect" 
            self.btn_refresh["state"] = "disable" 
            self.drop_bd["state"] = "disable" 
            self.drop_com["state"] = "disable" 
            InfoMsg = f"Successful UART connecting using {self.clicked_com.get()}"
            messagebox.showinfo("showinfo", InfoMsg)

         else:
            ErrorMsg = f"Failure to estabish UART connecting using {self.clicked_com.get()}"
            messagebox.showerror("showerror", ErrorMsg)
      else:
         self.btn_connect["text"] = "Connect" 
         self.btn_refresh["state"] = "active" 
         self.drop_bd["state"] = "active" 
         self.drop_com["state"] = "active" 

if __name__=="__main__":
  RootGUI()
  ComGUI()