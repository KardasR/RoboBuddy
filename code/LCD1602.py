from rpi_lcd import LCD

class LCD1602:
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.lcdClear()

    def __init__(self):
        try:
            self.lcd = LCD
        except Exception as e:
            print(f"Error initializing LCD: {e}")

    def lcdPrint(self, line1, line2):
        self.lcd.text(line1, 1)
        self.lcd.text(line2, 2)
        
    def lcdClear(self):
        self.lcd.clear()