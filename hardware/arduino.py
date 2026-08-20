import serial

try:
    arduino = serial.Serial(
        "COM3",
        9600,
        timeout=0.1
    )
except Exception:
    print("Arduino Error")

def leer_tarjeta():
    if arduino.in_waiting > 0:

        uid = arduino.readline().decode().strip()

        if uid:
            return uid

    return None