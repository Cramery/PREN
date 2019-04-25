# Benoetigte Module werden importiert und eingerichtet
import time

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# Hier wird der Ausgangs-Pin deklariert, an dem der Buzzer angeschlossen ist.
GPIO_PIN = 24
GPIO.setup(GPIO_PIN, GPIO.OUT)

# Das Software-PWM Modul wird initialisiert - hierbei wird die Frequenz 500Hz als Startwert genommen
Frequenz = 500  # In Hertz
pwm = GPIO.PWM(GPIO_PIN, Frequenz)


# Das Programm wartet auf die Eingabe einer neuen PWM-Frequenz vom Benutzer.
# Bis dahin wird der Buzzer mit der vorher eingegebenen Freuqenz betrieben (Startwert 500Hz)
try:
    while (True):
        print
        "----------------------------------------"
        print
        "Aktuelle Frequenz: %d" % Frequenz
        Frequenz = input("Bitte neue Frequenz eingeben (50-5000):")
        pwm.ChangeFrequency(Frequenz)

# Aufraeumarbeiten nachdem das Programm beendet wurde
except KeyboardInterrupt:
    GPIO.cleanup()