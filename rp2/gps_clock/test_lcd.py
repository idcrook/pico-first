"""Implements a HD44780 character LCD connected via MCP23008 on I2C."""

# Adapted from https://github.com/dhylands/python_lcd/blob/master/lcd/pyb_i2c_adafruit_lcd_test.py

import utime
from machine import Pin, I2C
import lcd
from lcd.rp2_i2c_adafruit_lcd import I2cLcd

# The MCP23008 has a jumper selectable address: 0x20 - 0x27
LCD_I2C_ADDR = 0x20
LCD_DETECTED = False

I2C_BUS_NUMBER = 0
I2C_SDA = Pin(8)
I2C_SCL = Pin(9)
I2C_FREQUENCY = 400000

def test_lcd(i2c, lcd_addr):
    print("Running test_lcd")
    lcd = I2cLcd(i2c, lcd_addr, 2, 16)
    lcd.putstr("It Works!\nSecond Line")
    utime.sleep_ms(3000)
    lcd.clear()
    count = 0
    while count < 11:
        lcd.move_to(0, 0)
        lcd.putstr("%7d" % (utime.ticks_ms() // 1_000))
        utime.sleep_ms(1000)
        count += 1
        if count % 10 == 3:
            print("Turning backlight off")
            lcd.backlight_off()
        if count % 10 == 4:
            print("Turning backlight on")
            lcd.backlight_on()
        if count % 10 == 5:
            print("Turning display off")
            lcd.display_off()
        if count % 10 == 6:
            print("Turning display on")
            lcd.display_on()
        if count % 10 == 7:
            print("Turning display & backlight off")
            lcd.backlight_off()
            lcd.display_off()
        if count % 10 == 8:
            print("Turning display & backlight on")
            lcd.backlight_on()
            lcd.display_on()
    lcd.backlight_off()
    lcd.display_off()

def test_main():
    """Test function for verifying basic functionality."""
    global LCD_DETECTED
    print("Running test_main")
    i2c = I2C(I2C_BUS_NUMBER, sda=I2C_SDA, scl=I2C_SCL, freq=I2C_FREQUENCY)
    device_addresses = i2c.scan()
    if LCD_I2C_ADDR in device_addresses:
        LCD_DETECTED = True

    if LCD_DETECTED:
        test_lcd(i2c, LCD_I2C_ADDR)
    else:
        print("LCD device not found")
 

test_main()
