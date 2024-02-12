def Wifi():
    esp8266.init(SerialPin.P0, SerialPin.P1, BaudRate.BAUD_RATE115200)
    if esp8266.is_esp8266_initialized():
        esp8266.connect_wi_fi("HOAN VAN", "winthovanhoan")
        if esp8266.is_wifi_connected():
            Sensor_DHT22()
        else:
            OLED.write_string_new_line("Cannot connect to router. Please check and reboot sysstem")
            esp8266.connect_wi_fi("HOAN VAN", "winthovanhoan")
            basic.pause(500)
            control.reset()
    else:
        OLED.write_string_new_line("ESP8266 is not found. Please check and reboot sysstem")
        esp8266.init(SerialPin.P0, SerialPin.P1, BaudRate.BAUD_RATE115200)
        basic.pause(500)
        control.reset()
def Startup():
    basic.show_leds("""
        # . # . #
        . . . . .
        # . . . #
        . . . . .
        # . # . #
        """)
    basic.show_leds("""
        . . . . .
        . # # # .
        . # . # .
        . # # # .
        . . . . .
        """)
    basic.show_leds("""
        . . . . #
        . # # # .
        . # . # .
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
    music.play(music.string_playable("C E G B C5 A F D ", 300),
        music.PlaybackMode.UNTIL_DONE)
def Sensor_DHT22():
    dht11_dht22.query_data(DHTtype.DHT22, DigitalPin.P2, True, True, False)
    dht11_dht22.select_temp_type(tempType.CELSIUS)
    if dht11_dht22.sensorr_responding() and dht11_dht22.read_data_successful():
        dht11_dht22.select_temp_type(tempType.CELSIUS)
        Startup()
    elif not (dht11_dht22.sensorr_responding()) or not (dht11_dht22.read_data_successful()):
        OLED.write_string_new_line("Sensor DHT22 is not found. Please check and reboot system")
        dht11_dht22.query_data(DHTtype.DHT22, DigitalPin.P2, True, True, False)
        dht11_dht22.select_temp_type(tempType.CELSIUS)
        basic.pause(500)
        control.reset()
date = ""
time = ""
hour = 0
minute_text = ""
OLED.init(128, 64)
list2 = [0, 1]
music.play(music.create_sound_expression(WaveShape.SINE,
        1,
        5000,
        0,
        255,
        1000,
        SoundExpressionEffect.NONE,
        InterpolationCurve.LINEAR),
    music.PlaybackMode.UNTIL_DONE)
basic.pause(500)
music.play(music.create_sound_expression(WaveShape.SINE,
        5000,
        5000,
        255,
        255,
        100,
        SoundExpressionEffect.NONE,
        InterpolationCurve.LINEAR),
    music.PlaybackMode.UNTIL_DONE)
Wifi()

def on_forever():
    if esp8266.is_wifi_connected() and (esp8266.is_esp8266_initialized() and (dht11_dht22.read_data_successful() and dht11_dht22.sensorr_responding())):
        list2[0] = dht11_dht22.read_data(dataType.HUMIDITY)
        list2[1] = dht11_dht22.read_data(dataType.TEMPERATURE)
        esp8266.upload_thingspeak("2WWRE6MHVGBS1Q7S", list2[0], list2[1])
        if esp8266.is_thingspeak_uploaded():
            basic.show_icon(IconNames.YES)
            basic.clear_screen()
        else:
            basic.show_icon(IconNames.SAD)
            basic.clear_screen()
basic.forever(on_forever)

def on_forever2():
    global minute_text, hour, time, date
    esp8266.update_internet_time()
    if esp8266.is_internet_time_updated():
        if (0) < (10):
            minute_text = "0" + ("" + str(esp8266.get_minute()))
        else:
            minute_text = convert_to_text(esp8266.get_minute())
        if esp8266.get_hour() > 12:
            hour = esp8266.get_hour() - 12
        else:
            hour = esp8266.get_hour()
        time = "" + str(esp8266.get_hour()) + " / " + ("" + str(esp8266.get_minute())) + " / " + ("" + str(esp8266.get_second()))
        date = "" + str(esp8266.get_day()) + " / " + ("" + str(esp8266.get_month())) + " / " + ("" + str(esp8266.get_year()))
    else:
        esp8266.update_internet_time()
basic.forever(on_forever2)
