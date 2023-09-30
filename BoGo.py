import serial
import threading
import time

class BoGo:
    def __init__(self) -> None:
        self.arduino1 = Arduino("COM7")

        self.arduinos = [self.arduino1]

        self.cmdThread = threading.Thread(target=self.sendServoCmd)
        self.cmdThread.start()

        self.animThread = threading.Thread(target=self.animate)
        self.animThread.start()

        self.animation = "idle"


    def sendServoCmd(self):
        while True:
            for arduino in self.arduinos:
                arduino.sendServoCmd()

    def loopAnimation(self):
        multiplier = 1
        increment = 1
        while self.animation == "loop":
            for arduino in self.arduinos:
                for servo in arduino.servos:
                    if servo.value + (increment * multiplier) > servo.max or servo.value + (increment * multiplier) < servo.min:
                        multiplier *= -1
                        servo.set(max(servo.min, min(servo.max, servo.value + (increment * multiplier))))
                    else:
                        servo.set(servo.value + (increment * multiplier))
            time.sleep(0.0001)

    def angryAnimation(self):
        pass

    def animate(self):
        while True:
            if self.animation == "loop":
                self.loopAnimation()
            elif self.animation == "angry":
                self.angryAnimation()
            else:
                # Idle animation
                for arduino in self.arduinos:
                    for servo in arduino.servos:
                        servo.set(90)
            time.sleep(0.1)

    def __del__(self) -> None:
        # self.cmdThread.join()
        for arduino in self.arduinos:
            arduino.ser.close()



class Servo:
    def __init__(self) -> None:
        self.min = 10
        self.max = 170
        self.offset = 0
        self.value = self.min + self.offset


    def set(self, value) -> None:
        if value < self.min:
            value = self.min
        elif value > self.max:
            value = self.max
        self.value = value

class Arduino:
    def __init__(self, port, baud = 9600) -> None:
        self.ser = serial.Serial(port, baud)
        self.servos = [Servo(), Servo(), Servo(), Servo(), Servo(), Servo()]

    def sendServoCmd(self):
        # Send servo command with leading zeros
        cmd = f"{self.servos[0].value:03d},{self.servos[1].value:03d},{self.servos[2].value:03d},{self.servos[3].value:03d},{self.servos[4].value:03d},{self.servos[5].value:03d}\n"
        print("Sending: " + cmd)
        self.ser.write(cmd.encode())


if __name__ == "__main__":
    bogo = BoGo()
    bogo.animation = "loop"
    