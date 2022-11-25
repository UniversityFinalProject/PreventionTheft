import serial

MYPORT = "COM5"
distance_list = []

def funct(event):
    arduino = serial.Serial(port = MYPORT, baudrate=9600)

    while True:
        try:
            msg = arduino.readline()
            result = msg.decode('utf-8')
            result = str(result).strip()
            distance = int(float(result))
            distance_list.append(distance)
       
        except Exception:
            pass

        if event.is_set():
            return
