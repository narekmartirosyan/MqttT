from __future__ import print_function

import time
from mraa import getGpioLookup
from upm import pyupm_buzzer as upmBuzzer

def main():
    from grove import helper
    from grove.helper import helper
    helper.root_check()

    print("Insert Grove-Buzzer to Grove-Base-Hat slot PWM[12 13 VCC GND]")

    # Grove Base Hat for Raspberry Pi
    #   PWM JST SLOT - PWM[12 13 VCC GND]
    pin = 12
    #
    # Create the buzzer object using RaspberryPi GPIO12
    mraa_pin = getGpioLookup("GPIO%02d" % pin)
    buzzer = upmBuzzer.Buzzer(mraa_pin)

    #chords = [upmBuzzer.BUZZER_DO, upmBuzzer.BUZZER_RE, upmBuzzer.BUZZER_MI,
    #          upmBuzzer.BUZZER_FA, upmBuzzer.BUZZER_SOL, upmBuzzer.BUZZER_LA,
    #          upmBuzzer.BUZZER_SI];

    chords = [upmBuzzer.BUZZER_DO]
    # Print sensor name
    print(buzzer.name())

    # Play sound (DO, RE, MI, etc.), pausing for 0.1 seconds between notes
    for chord_ind in range (0,1):
        # play each note for a half second
        print(buzzer.playSound(chords[chord_ind], 500000))
        time.sleep(1)

    print("exiting application")

    # Delete the buzzer object
    del buzzer

if __name__ == '__main__':
    main()
