""" Live-ECG monitor on ESP32 """

import machine, ssd1306, time

# Pins might differ depending on the board used
pin16 = machine.Pin(16, machine.Pin.OUT)
pin16.value(1)

i2c = machine.SoftI2C(scl=machine.Pin(15), sda=machine.Pin(4))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
oled.fill(0)
oled.show()


ecg_out = machine.ADC(machine.Pin(37, machine.Pin.IN))
ecg_out.atten(ecg_out.ATTN_11DB)
ecg_out.width(ecg_out.WIDTH_9BIT)

def rolling(x):
    for i in range(0,64):
        oled.pixel(x, i, 0)

def hr_monitor(x):
    x = x%128
    y = int(ecg_out.read()/8) # norm signal to range in -1,1
    oled.pixel(x, (-5+y), 1)
    time.sleep(1/128)

def main():
    while True:
        for x in range(0,128):
            hr_monitor(x)
            if x%21 == 0:
                oled.show()
        time.sleep(0.5)
        oled.fill(0)
        oled.show()

if __name__ = "__main__":
    main()
        
