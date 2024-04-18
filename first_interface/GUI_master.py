from tkinter import *
from tkinter import messagebox
from tkinter import ttk

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
            self.conn= ConnGUI(self.root, self.serial)

         else:
            ErrorMsg = f"Failure to estabish UART connecting using {self.clicked_com.get()}"
            messagebox.showerror("showerror", ErrorMsg)
      else:
         self.conn.ConnGUIClose()
         self.serial.SerialClose()
         InfoMsg = f"UART connecting using {self.clicked_com.get()} is now closed"
         messagebox.showwarning("showinfo", InfoMsg)
         self.btn_connect["text"] = "Connect" 
         self.btn_refresh["state"] = "active" 
         self.drop_bd["state"] = "active" 
         self.drop_com["state"] = "active" 


class ConnGUI():
   def __init__(self, root, serial):
      self.root=root
      self.serial=serial
      self.frame=LabelFrame(
         root,text="Connection Manager", padx=5, pady=5, bg="white", width=60
      )
      self.sync_label =Label(
         self.frame, text="Sync Status: ", bg= "white", width=15, anchor= "w"
      )
      self.sync_satatus =Label(
         self.frame, text="...Sync... ", bg= "white", width=5, fg="orange"
      )

      self.ch_label= Label(
         self.frame, text="Active channels: ", bg= "white", width=15, anchor= "w"
      )

      self.ch_status= Label(
         self.frame, text=".... ", bg= "white", width=5, fg="orange"
      )

      self.btn_start_stream = Button(self.frame, text="Start", state="disabled",
                                       width=5, command=self.start_stream)     
      self.btn_stop_stream = Button(self.frame, text="Stop", state="disabled",
                                      width=5, command=self.stop_stream)
      self.btn_add_chart = Button(self.frame,text="+", state = "disabled", width=5, bg = "white", fg="#098577",command=self.new_chart )
      self.btn_kill_chart = Button(self.frame,text="-", state = "disabled", width=5, bg = "white", fg="#CC252C", command=self.kill_chart)
     
      self.save = False
      self.saveVar = IntVar()
      self.save_check = Checkbutton(self.frame, text = "Save data", variable=self.saveVar, onvalue=1, offvalue=0, bg="white", state="disabled", command=self.save_data)
     
      self.separator= ttk.Separator(self.frame, orient='vertical') 
      self.padx = 20
      self.pady = 15
      self.ConnGUIOpen()

     
   def ConnGUIOpen(self):
      self.root.geometry('800x120')
      self.frame.grid(row=0, column=4, rowspan=3, columnspan=5, padx=5, pady=5)
     
      self.sync_label.grid(column=1, row=1)
      self.sync_satatus.grid(column=2, row=1)
     
      self.ch_label.grid(column=1, row=2)
      self.ch_status.grid(column=2, row=2, pady=self.pady)

      self.btn_start_stream.grid(column=3, row= 1, padx= self.padx)
      self.btn_stop_stream.grid(column=3, row= 2, padx= self.padx)

      self.btn_add_chart.grid(column=4, row= 1, padx=self.padx)
      self.btn_kill_chart.grid(column=5, row= 1, padx=self.padx)

      self.save_check.grid(column=4, row=2, columnspan=2)

      self.separator.place(relx=0.58,rely=0, relwidth=0.001, relheight=1 )


   def ConnGUIClose(self):
      for widget in self.frame.winfo_children():
         widget.destroy()
      self.frame.destroy()
      self.root.geometry("360x120")

   def start_stream(self):
      pass

   def stop_stream(self):
      pass

   def new_chart(self):
      pass

   def kill_chart(self):
      pass

   def save_data(self):
      pass



if __name__=="__main__":
  RootGUI()
  ComGUI()
  ConnGUI()