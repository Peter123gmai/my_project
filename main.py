def Starting_up():
    global list2
    bluetooth.start_accelerometer_service()
    bluetooth.start_button_service()
    bluetooth.start_io_pin_service()
    bluetooth.start_led_service()
    bluetooth.start_temperature_service()
    bluetooth.start_magnetometer_service()
    bluetooth.start_uart_service()
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
    OLED12864_I2C.show_string(0, 0, "Smarthome Iot version 5.8.4", 1)
    OLED12864_I2C.show_string(0,
        0,
        "Device serial number: " + str(control.device_serial_number()),
        1)
def read_time_set():
    global minute_text, hour, time, date
    if esp8266.is_wifi_connected() and esp8266.is_esp8266_initialized():
        esp8266.update_internet_time()
        if esp8266.is_internet_time_updated():
            if (0) < (10):
                minute_text = "0" + str(esp8266.get_minute())
            else:
                minute_text = convert_to_text(esp8266.get_minute())
            if esp8266.get_hour() > 12:
                hour = esp8266.get_hour() - 12
            else:
                hour = esp8266.get_hour()
            time = "" + str(esp8266.get_hour()) + " / " + str(esp8266.get_minute()) + " / " + str(esp8266.get_second())
            date = "" + str(esp8266.get_day()) + " / " + str(esp8266.get_month()) + " / " + str(esp8266.get_year())
        else:
            esp8266.update_internet_time()

def on_bluetooth_connected():
    basic.show_icon(IconNames.YES)
    basic.clear_screen()
bluetooth.on_bluetooth_connected(on_bluetooth_connected)

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
        esp8266.connect_wi_fi("HOAN VAN", "Winthovanhoan")
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
def sensor_door():
    global user_leaved
    if pins.digital_read_pin(DigitalPin.P4) == 1 and user_leaved:
        music.ring_tone(988)
        esp8266.send_telegram_message("", "", "emergency warning !!! Stranger detected")
        basic.pause(2000)
        user_leaved = False
    else:
        music.stop_all_sounds()
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
    music.play(music.string_playable("C E G B C5 A F D ", 325),
        music.PlaybackMode.UNTIL_DONE)
    music.stop_all_sounds()
def temperature_show():
    if dht11_dht22.read_data_successful() and dht11_dht22.sensorr_responding():
        OLED12864_I2C.show_string(3, 3, "Temperate outside", 1)
        OLED12864_I2C.show_number(3, 4, dht11_dht22.read_data(dataType.TEMPERATURE), 1)
def send_info_from_sensor():
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
        OLED12864_I2C.clear()
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

def my_function():
    # có hai module thẻ RFID ở hai vị trí bao gồm: 
    # 1. Cổng, lối vào đầu tiên
    # 2.Cửa chính, sẽ bao gồm mật khẩu và thẻ RFID để mở khóa
    if NFC.get_uid() == "2991AAA3":
        pins.analog_write_pin(AnalogPin.P6, 511)
        basic.pause(1500)
        pins.analog_write_pin(AnalogPin.P6, 0)
    elif NFC.get_uid() == "5547562A":
        bluetooth.uart_write_string("Gate opened")
        OLED12864_I2C.show_string(0, 0, "RFID card is detected!", 1)
        OLED12864_I2C.clear()
        OLED12864_I2C.show_string(0, 0, "Next, Type your password", 1)
        OLED12864_I2C.clear()
        OLED12864_I2C.show_string(0, 0, keypad.get_key_string(), 1)
        if keypad.get_key_string() == "A312465BDC":
            pins.servo_write_pin(AnalogPin.P5, 140)
            OLED12864_I2C.clear()
            OLED12864_I2C.show_string(0, 0, "Type # to close", 1)
            if keypad.get_key_string() == "#":
                bluetooth.uart_write_string("Gate closed")
                pins.servo_write_pin(AnalogPin.P5, 90)
                OLED12864_I2C.clear()
            else:
                pins.servo_write_pin(AnalogPin.P5, 140)
        else:
            pins.servo_write_pin(AnalogPin.P5, 90)
NFC.nfc_event(my_function)

date = ""
time = ""
hour = 0
minute_text = ""
list2: List[number] = []
user_leaved = False
pins.analog_write_pin(AnalogPin.P6, 0)
user_leaved = False
Starting_up()

def on_forever():
    temperature_show()
    send_info_from_sensor()
    read_time_set()
    sensor_door()
basic.forever(on_forever)
