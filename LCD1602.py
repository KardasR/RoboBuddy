from rpi_lcd import LCD
from time import sleep

lcd = LCD()

try:
    lcd.text("Papa, are", 1)
    lcd.text("you there?", 2)

    sleep(5)

finally:
    lcd.clear()