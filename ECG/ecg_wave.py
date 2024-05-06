import serial


serial_port = 'COM3'
baud_rate = 115200
data_to_send = b'\x55\xAA\x04\xFB\x01\xFF'

# data_to_send = b'\x55\xAA\x04\x02\x01\xF8'

ser = serial.Serial(serial_port, baud_rate, timeout=1)

try:
    print(f"Connected to {serial_port} at {baud_rate} baud.")

    ser.write(data_to_send)
    print("Sent data:", data_to_send)

 

except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
except KeyboardInterrupt:
    print("Keyboard interrupt. Exiting...")
finally:
    if ser.isOpen():
        ser.close()
        print("Serial port closed.")
