from rpi_lcd import LCD

lcd = LCD()

class LCD1602:
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.lcdClear()

    def lcdPrint(line1, line2):
        lcd.text(line1, 1)
        lcd.text(line2, 2)
        
    def lcdClear():
        lcd.clear()