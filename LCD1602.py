from rpi_lcd import LCD

lcd = LCD()

class LCD1602:
    def lcdPrint(line1, line2):
        lcd.text(line1, 1)
        lcd.text(line2, 2)
        
    def lcdClear():
        lcd.clear()