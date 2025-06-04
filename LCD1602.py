from rpi_lcd import LCD

lcd = LCD()

try:
    lcd.text("Papa, are", 1)
    lcd.text("you there?", 2)

except KeyboardInterrupt:
    pass

finally:
    lcd.clear()