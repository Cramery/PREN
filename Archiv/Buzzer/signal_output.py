# Benoetigte Module werden importiert und eingerichtet
import time

import RPi.GPIO as GPIO

# detected number
number = 5

GPIO.setmode(GPIO.BCM)
# Hier wird der Ausgangs-Pin deklariert, an dem der Buzzer angeschlossen ist.
GPIO_PIN = 24
GPIO.setup(GPIO_PIN, GPIO.OUT)

# Das Software-PWM Modul wird initialisiert - hierbei wird die Frequenz 500Hz als Startwert genommen
Frequenz = 10  # In Hertz
pwm = GPIO.PWM(GPIO_PIN, Frequenz)
pwm.start(1)

while (number > -1):
    time.sleep(1)
    pwm.ChangeFrequency(1500)
    time.sleep(1)
    pwm.ChangeFrequency(10)
    number -= 1
    print(number)


# Aufraeumarbeiten nachdem das Programm beendet wurde
GPIO.cleanup()