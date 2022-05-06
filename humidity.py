#   Read ADC/DAC i2c module, with PCF8591.
#   Capacitive humidity sensor connected to adc channel 2.
#   Humidity sensor voltage at 100% humidity - 1.1V,
#   voltage at room humidity - 2.9V.

from smbus2 import SMBus, i2c_msg
import time

SECONDS = 240
CHANNELS_ADC = 4

i2c = SMBus(1) # open i2c bus

adc = [0, 0, 0, 0]
adc_f = [0, 0, 0, 0]

for s in range(SECONDS):
    string = ""
    string_f = ""

    register_control = 0b01000000 # PCF8591 control register value. ADC enabled, four single ended channels.

    for ch in range(CHANNELS_ADC):
        msg_tx = i2c_msg.write(0x48, [register_control])
        i2c.i2c_rdwr(msg_tx)

        msg_rx = i2c_msg.read(0x48, 1)
        i2c.i2c_rdwr(msg_rx)
        i2c.i2c_rdwr(msg_rx) #  Sample is ready only on second read

        adc[ch] = msg_rx.buf[0]
        adc_f[ch] = round(int.from_bytes(adc[ch], byteorder='little') / 256 * 100, 0)

        string = string + "ch" + str(ch) + " = " + str(adc[ch]) + "; "
        string_f = string_f + "ch" + str(ch) + " = " + str(adc_f[ch]) + "; "

        register_control += 1

    # print(string)
    # print(string_f)
    result = round(100 - (adc_f[2] * 1.8 - 68), 0) #    Humidity in %
    print(str(result))
    
    time.sleep(1)
