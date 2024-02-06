def sensor_temperature():
    if dht11_dht22.read_data_successful() and dht11_dht22.sensorr_responding():
        OLED.draw_loading(30)
        Wifi_setup()
    elif not (dht11_dht22.sensorr_responding()) or not (dht11_dht22.read_data_successful()):
        OLED.write_string_new_line("Sensor temperature is not found. please check and reboot into system ")
        OLED.clear()
        OLED.write_string_new_line("Rebooting...")
        OLED.clear()
        dht11_dht22.query_data(DHTtype.DHT22, DigitalPin.P9, True, True, False)
        basic.pause(5000)
        control.reset()
def startup():
    OLED.init(128, 64)
    OLED.write_string_new_line("Personal smart home project system. OS version v12.5.7")
    OLED.write_string_new_line("Device name: " + control.device_name())
    OLED.write_string_new_line("Device serial number: " + ("" + str(control.device_serial_number())))
    OLED.clear()
    OLED.draw_loading(0)
    keypad.set_key_pad4(DigitalPin.P9,
        DigitalPin.P10,
        DigitalPin.P11,
        DigitalPin.P12,
        DigitalPin.P13,
        DigitalPin.P14,
        DigitalPin.P15,
        DigitalPin.P16)
    dht11_dht22.query_data(DHTtype.DHT22, DigitalPin.P8, True, True, False)
    dht11_dht22.select_temp_type(tempType.CELSIUS)
    OLED.draw_loading(5)
    sensor_temperature()
def startup2():
    basic.show_leds("""
        # . # . #
        . . . . .
        # . # . #
        . . . . .
        # . # . #
        """)
    basic.show_leds("""
        . . . . .
        . # # # .
        . # # # .
        . # # # .
        . . . . .
        """)
    basic.show_leds("""
        . . . . #
        . # # # .
        . # # # .
        . # # # .
        # . . . .
        """)
    basic.show_leds("""
        . . . . #
        . # # # .
        # # # # #
        . # # # .
        # . . . .
        """)
    basic.show_leds("""
        # . . . #
        . # # # .
        # # # # #
        . # # # .
        # . . . #
        """)
    basic.show_leds("""
        # . # . #
        . # # # .
        # # # # #
        . # # # .
        # . # . #
        """)
    basic.clear_screen()
    OLED.clear()
    OLED.write_string_new_line("Type Password:")
    music.play(music.string_playable("C E G B C5 A F D ", 300),
        music.PlaybackMode.UNTIL_DONE)
def Wifi_setup():
    esp8266.init(SerialPin.USB_TX, SerialPin.USB_RX, BaudRate.BAUD_RATE115200)
    if esp8266.is_esp8266_initialized():
        OLED.draw_loading(50)
        esp8266.connect_wi_fi("VAN HOAN", "Winthovanhoan")
        if esp8266.is_wifi_connected():
            OLED.draw_loading(100)
            OLED.clear()
            for index in range(4):
                OLED.write_string_new_line("starting up.")
                basic.pause(100)
                OLED.write_string_new_line("starting up..")
                basic.pause(100)
                OLED.write_string_new_line("starting up...")
                basic.pause(100)
            OLED.clear()
            basic.clear_screen()
            startup2()
        else:
            OLED.write_string_new_line("cannot connect to router wifi. Please check and reboot into system")
            esp8266.connect_wi_fi("VAN HOAN", "Winthovanhoan")
            OLED.clear()
            OLED.write_string_new_line("Rebooting...")
            OLED.clear()
            basic.pause(5000)
            control.reset()
    else:
        OLED.write_string_new_line("cannot initialize module wifi esp8266. Please check and reboot into system")
        OLED.clear()
        OLED.write_string_new_line("Rebooting...")
        OLED.clear()
        basic.pause(5000)
        control.reset()
gate_door_is_close = False
list2 = [0, 1]
startup()

def on_forever():
    global gate_door_is_close
    if gate_door_is_close == True:
        OLED.write_string_new_line(keypad.get_key_string())
        if keypad.get_key_string() == "A03745BCD83":
            gate_door_is_close = False
            OLED.write_string_new_line("Type # to close")
    elif gate_door_is_close == False:
        if keypad.get_key_string() == "#":
            gate_door_is_close = True
            OLED.write_string_new_line("Type password: ")
basic.forever(on_forever)

def on_forever2():
    if dht11_dht22.read_data_successful() and (esp8266.is_esp8266_initialized() and esp8266.is_wifi_connected() and dht11_dht22.read_data_successful()):
        list2[0] = dht11_dht22.read_data(dataType.HUMIDITY)
        list2[1] = dht11_dht22.read_data(dataType.TEMPERATURE)
        esp8266.upload_thingspeak("2WWRE6MHVGBS1Q7S", list2[0], list2[1])
        if esp8266.is_thingspeak_uploaded():
            basic.show_icon(IconNames.YES)
            basic.clear_screen()
        else:
            basic.show_number(593)
basic.forever(on_forever2)
