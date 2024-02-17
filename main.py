# #define BLYNK_TEMPLATE_ID "TMPL6mDQdY-HU"
# 
# #define BLYNK_TEMPLATE_NAME "Quickstart Template"
# 
# #define BLYNK_AUTH_TOKEN "xSgmbQg-83OPJxGfZk6upXthH15t0-9t"
def Wifi():
    esp8266.init(SerialPin.P0, SerialPin.P1, BaudRate.BAUD_RATE115200)
    if esp8266.is_esp8266_initialized():
        esp8266.connect_wi_fi("HOAN VAN", "winthovanhoan")
        if esp8266.is_wifi_connected():
            Sensor_DHT22()
        else:
            OLED12864_I2C.clear()
            OLED12864_I2C.show_string(0,
                0,
                "Cannot connect to router. Please check and reboot sysstem",
                1)
            OLED12864_I2C.clear()
            basic.pause(2000)
            esp8266.connect_wi_fi("HOAN VAN", "winthovanhoan")
            basic.pause(500)
            esp8266.send_telegram_message("",
                "",
                "Cannot connect to router. Please check and reboot sysstem")
            if esp8266.is_telegram_message_sent():
                basic.show_icon(IconNames.YES)
                basic.clear_screen()
            else:
                basic.show_icon(IconNames.NO)
                basic.clear_screen()
            control.reset()
    else:
        OLED12864_I2C.clear()
        OLED12864_I2C.show_string(0,
            0,
            "ESP8266 is not found. Please check and reboot sysstem",
            1)
        OLED12864_I2C.clear()
        basic.pause(2000)
        esp8266.init(SerialPin.P0, SerialPin.P1, BaudRate.BAUD_RATE115200)
        basic.pause(500)
        esp8266.send_telegram_message("",
            "",
            "ESP8266 is not found. Please check and reboot sysstem")
        if esp8266.is_telegram_message_sent():
            basic.show_icon(IconNames.YES)
            basic.clear_screen()
        else:
            basic.show_icon(IconNames.NO)
            basic.clear_screen()
        control.reset()
def Starting_up():
    global list2
    NFC.NFC_setSerial(SerialPin.P2, SerialPin.P8)
    OLED12864_I2C.init(60)
    list2 = [1, 1]
    keypad.set_key_pad4(DigitalPin.P9,
        DigitalPin.P10,
        DigitalPin.P11,
        DigitalPin.P12,
        DigitalPin.P13,
        DigitalPin.P14,
        DigitalPin.P15,
        DigitalPin.P16)
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
        OLED12864_I2C.rect(1, 1, 60, 30, 3)
        for index in range(randint(1, 5)):
            OLED12864_I2C.show_string(70, 70, "Starting up.", 1)
            OLED12864_I2C.show_string(70, 70, "Starting up..", 1)
            OLED12864_I2C.show_string(70, 70, "Starting up...", 1)
        Startup()
    elif not (dht11_dht22.sensorr_responding()) or not (dht11_dht22.read_data_successful()):
        OLED12864_I2C.clear()
        OLED12864_I2C.show_string(0, 0, "Hello!", 1)
        OLED12864_I2C.clear()
        basic.pause(2000)
        dht11_dht22.query_data(DHTtype.DHT22, DigitalPin.P2, True, True, False)
        dht11_dht22.select_temp_type(tempType.CELSIUS)
        esp8266.send_telegram_message("",
            "",
            "Sensor DHT22 is not found. Please check and reboot system")
        if esp8266.is_telegram_message_sent():
            basic.show_icon(IconNames.YES)
            basic.clear_screen()
        else:
            basic.show_icon(IconNames.NO)
            basic.clear_screen()
        control.reset()
date = ""
time = ""
hour = 0
minute_text = ""
list2: List[number] = []
Starting_up()

def on_forever():
    if NFC.detected_rfi_dcard():
        OLED12864_I2C.show_string(0, 0, "RFID card is detected!", 1)
        OLED12864_I2C.clear()
        OLED12864_I2C.show_string(0, 0, "Next, Type your password", 1)
        OLED12864_I2C.clear()
        OLED12864_I2C.show_string(0, 0, keypad.get_key_string(), 1)
        if keypad.get_key_string() == "A312465BDC":
            pins.servo_write_pin(AnalogPin.P5, 140)
            OLED12864_I2C.clear()
        else:
            pins.servo_write_pin(AnalogPin.P5, 90)
basic.forever(on_forever)

def on_forever2():
    if dht11_dht22.read_data_successful() and dht11_dht22.sensorr_responding():
        OLED12864_I2C.show_string(3, 3, "Temperate outside", 1)
        OLED12864_I2C.show_number(3, 4, dht11_dht22.read_data(dataType.TEMPERATURE), 1)
basic.forever(on_forever2)

def on_forever3():
    global minute_text, hour, time, date
    if esp8266.is_wifi_connected() and esp8266.is_esp8266_initialized():
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
basic.forever(on_forever3)

def on_forever4():
    if esp8266.is_wifi_connected() and (esp8266.is_esp8266_initialized() and (dht11_dht22.read_data_successful() and dht11_dht22.sensorr_responding())):
        list2[0] = dht11_dht22.read_data(dataType.HUMIDITY)
        list2[1] = dht11_dht22.read_data(dataType.TEMPERATURE)
        esp8266.upload_thingspeak("2WWRE6MHVGBS1Q7S", list2[0], list2[1])
        if esp8266.is_thingspeak_uploaded():
            basic.show_icon(IconNames.YES)
            basic.clear_screen()
        else:
            basic.show_icon(IconNames.NO)
            basic.clear_screen()
basic.forever(on_forever4)
