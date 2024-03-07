// get time for NTP server
function read_time_set () {
    if (esp8266.isWifiConnected() && esp8266.isESP8266Initialized()) {
        esp8266.updateInternetTime()
        if (esp8266.isInternetTimeUpdated()) {
            Time_and_date = ["" + esp8266.getHour() + " / " + esp8266.getMinute(), "" + esp8266.getDay() + " / " + esp8266.getMonth()]
        } else {
            esp8266.updateInternetTime()
        }
    }
}
bluetooth.onBluetoothConnected(function () {
    basic.showIcon(IconNames.Yes)
    basic.clearScreen()
    connection = true
    while (connection) {
        data = bluetooth.uartReadUntil(serial.delimiters(Delimiters.Hash))
        living_room_code()
        kitchen_code()
    }
})
function Wifi () {
    esp8266.init(SerialPin.P0, SerialPin.P1, BaudRate.BaudRate115200)
    if (esp8266.isESP8266Initialized()) {
        esp8266.connectWiFi(ssid, password)
        if (esp8266.isWifiConnected()) {
            Sensor_DHT22()
        } else {
            OLED12864_I2C.clear()
            OLED12864_I2C.showString(
            0,
            0,
            "Cannot connect to router. Please check and reboot sysstem",
            1
            )
            OLED12864_I2C.clear()
            basic.pause(2000)
            esp8266.connectWiFi(ssid, password)
            basic.pause(500)
            esp8266.sendTelegramMessage("", "", "Cannot connect to router. Please check and reboot sysstem")
            if (esp8266.isTelegramMessageSent()) {
                basic.showIcon(IconNames.Yes)
                basic.clearScreen()
            } else {
                basic.showIcon(IconNames.No)
                basic.clearScreen()
            }
            control.reset()
        }
    } else {
        OLED12864_I2C.clear()
        OLED12864_I2C.showString(
        0,
        0,
        "ESP8266 is not found. Please check and reboot sysstem",
        1
        )
        OLED12864_I2C.clear()
        basic.pause(2000)
        esp8266.init(SerialPin.P0, SerialPin.P1, BaudRate.BaudRate115200)
        esp8266.connectWiFi(ssid, password)
        basic.pause(500)
        esp8266.sendTelegramMessage("", "", "ESP8266 is not found. Please check and reboot sysstem")
        if (esp8266.isTelegramMessageSent()) {
            basic.showIcon(IconNames.Yes)
            basic.clearScreen()
        } else {
            basic.showIcon(IconNames.No)
            basic.clearScreen()
        }
        control.reset()
    }
}
function kitchen_code () {
    if (true) {
    	
    } else if (data == "") {
    	
    }
}
function sensor_door () {
    if (pins.digitalReadPin(DigitalPin.P4) == 1 && door_status) {
        music.ringTone(988)
        esp8266.sendTelegramMessage("", "", "emergency warning !!! Stranger detected")
        basic.pause(2000)
        door_status = false
    } else {
        music.stopAllSounds()
    }
}
function Startup () {
    basic.showLeds(`
        # . # . #
        . . . . .
        # . . . #
        . . . . .
        # . # . #
        `)
    basic.showLeds(`
        . . . . .
        . # # # .
        . # . # .
        . # # # .
        . . . . .
        `)
    basic.showLeds(`
        . . . . #
        . # # # .
        . # . # .
        . # # # .
        # . . . .
        `)
    basic.showLeds(`
        . . . . #
        . # # # .
        # # # # #
        . # # # .
        # . . . .
        `)
    basic.showLeds(`
        # . . . #
        . # # # .
        # # # # #
        . # # # .
        # . . . #
        `)
    basic.showLeds(`
        # . # . #
        . # # # .
        # # # # #
        . # # # .
        # . # . #
        `)
    basic.clearScreen()
    music.play(music.stringPlayable("C E G B C5 A F D ", 325), music.PlaybackMode.UntilDone)
    music.stopAllSounds()
}
function living_room_code () {
    if (data == "air_conditioner_turned_on") {
        status1[0] = true
    } else if (data == "air_conditioner_turned_off") {
        status1[0] = false
    } else if (data == "living_room_light _turned_on") {
        status1[1] = true
    } else if (data == "living_room_light _turned_off") {
        status1[1] = false
    } else if (data == "TV_turned _on") {
        status1[2] = true
    } else if (data == "TV_turned _off") {
        status1[2] = false
    } else if (data == "movie_mode_enabled") {
        status1[0] = true
        status1[1] = false
        status1[2] = true
        status1[3] = false
    } else if (data == "movie_mode_disabled") {
        status1[0] = false
        status1[1] = true
        status1[2] = false
        status1[3] = true
    } else if (data == "window_blinds_open") {
        status1[3] = true
    } else if (data == "window_blinds_close") {
        status1[3] = false
    }
}
function temperature_show () {
    if (dht11_dht22.readDataSuccessful() && dht11_dht22.sensorrResponding()) {
        OLED12864_I2C.showString(
        3,
        3,
        "Temperate outside",
        1
        )
        OLED12864_I2C.showNumber(
        3,
        4,
        dht11_dht22.readData(dataType.temperature),
        1
        )
    }
}
function send_info_from_sensor () {
    if (esp8266.isWifiConnected() && (esp8266.isESP8266Initialized() && (dht11_dht22.readDataSuccessful() && dht11_dht22.sensorrResponding()))) {
        list2[0] = dht11_dht22.readData(dataType.humidity)
        list2[1] = dht11_dht22.readData(dataType.temperature)
        esp8266.uploadThingspeak(
        "2WWRE6MHVGBS1Q7S",
        list2[0],
        list2[1]
        )
        if (esp8266.isThingspeakUploaded()) {
            basic.showIcon(IconNames.Yes)
            basic.clearScreen()
        } else {
            basic.showIcon(IconNames.No)
            basic.clearScreen()
        }
    }
}
function Sensor_DHT22 () {
    dht11_dht22.queryData(
    DHTtype.DHT22,
    DigitalPin.P2,
    true,
    true,
    false
    )
    dht11_dht22.selectTempType(tempType.celsius)
    if (dht11_dht22.sensorrResponding() && dht11_dht22.readDataSuccessful()) {
        dht11_dht22.selectTempType(tempType.celsius)
        OLED12864_I2C.rect(
        1,
        1,
        60,
        30,
        3
        )
        for (let index = 0; index < randint(1, 5); index++) {
            OLED12864_I2C.showString(
            70,
            70,
            "Starting up.",
            1
            )
            OLED12864_I2C.showString(
            70,
            70,
            "Starting up..",
            1
            )
            OLED12864_I2C.showString(
            70,
            70,
            "Starting up...",
            1
            )
        }
        OLED12864_I2C.clear()
        Startup()
    } else if (!(dht11_dht22.sensorrResponding()) || !(dht11_dht22.readDataSuccessful())) {
        OLED12864_I2C.clear()
        OLED12864_I2C.showString(
        0,
        0,
        "Hello!",
        1
        )
        OLED12864_I2C.clear()
        basic.pause(2000)
        dht11_dht22.queryData(
        DHTtype.DHT22,
        DigitalPin.P2,
        true,
        true,
        false
        )
        dht11_dht22.selectTempType(tempType.celsius)
        esp8266.sendTelegramMessage("", "", "Sensor DHT22 is not found. Please check and reboot system")
        if (esp8266.isTelegramMessageSent()) {
            basic.showIcon(IconNames.Yes)
            basic.clearScreen()
        } else {
            basic.showIcon(IconNames.No)
            basic.clearScreen()
        }
        control.reset()
    }
}
NFC.nfcEvent(function () {
    // có hai module thẻ RFID ở hai vị trí bao gồm: 
    // 1. Cổng, lối vào đầu tiên
    // 2.Cửa chính, sẽ bao gồm mật khẩu và thẻ RFID để mở khóa
    if (NFC.getUID() == "2991AAA3") {
        pins.analogWritePin(AnalogPin.P6, 511)
        basic.pause(1500)
        pins.analogWritePin(AnalogPin.P6, 0)
    } else if (NFC.getUID() == "5547562A") {
        OLED12864_I2C.showString(
        0,
        0,
        "RFID card is detected!",
        1
        )
        OLED12864_I2C.clear()
        OLED12864_I2C.showString(
        0,
        0,
        "Next you need to enter the password you set to enter the house",
        1
        )
        OLED12864_I2C.clear()
        OLED12864_I2C.showString(
        0,
        0,
        keypad.getKeyString(),
        1
        )
        if (keypad.getKeyString() == password_door) {
            pins.servoWritePin(AnalogPin.P5, 140)
            OLED12864_I2C.clear()
            OLED12864_I2C.showString(
            0,
            0,
            "Type # to close",
            1
            )
            if (keypad.getKeyString() == "#") {
                pins.servoWritePin(AnalogPin.P5, 90)
                OLED12864_I2C.clear()
            } else {
                pins.servoWritePin(AnalogPin.P5, 140)
            }
        } else {
            pins.servoWritePin(AnalogPin.P5, 90)
        }
    }
})
let temp_air = 0
let data = ""
let Time_and_date: string[] = []
let ssid = ""
let password = ""
let door_status = false
let connection = false
let status1: boolean[] = []
let list2: number[] = []
let password_door = ""
bluetooth.startAccelerometerService()
bluetooth.startButtonService()
bluetooth.startIOPinService()
bluetooth.startLEDService()
bluetooth.startTemperatureService()
bluetooth.startMagnetometerService()
bluetooth.startUartService()
NFC.NFC_setSerial(SerialPin.P2, SerialPin.P8)
OLED12864_I2C.init(60)
password_door = "A312465BDC"
list2 = [1, 1]
// tạo 1 mảng chứa trạng thái các đồ điện tử lần lượt từ trên xuống dưới là:
// -điều hòa
// -đèn phòng khách
// -TV
// -Rèm cửa
status1 = [
false,
false,
false,
false
]
// tạo 1 mảng chứa trạng thái các đồ điện tử lần lượt từ trên xuống dưới là:
// -điều hòa
// -đèn phòng khách
// -TV
// -Rèm cửa
let status_kitchen = [false, false]
connection = false
pins.analogWritePin(AnalogPin.P6, 0)
door_status = false
password = "Winthovanhoan"
ssid = "HOAN VAN"
keypad.setKeyPad4(
DigitalPin.P9,
DigitalPin.P10,
DigitalPin.P11,
DigitalPin.P12,
DigitalPin.P13,
DigitalPin.P14,
DigitalPin.P15,
DigitalPin.P16
)
music.play(music.createSoundExpression(WaveShape.Sine, 1, 5000, 0, 255, 1000, SoundExpressionEffect.None, InterpolationCurve.Linear), music.PlaybackMode.UntilDone)
basic.pause(500)
music.play(music.createSoundExpression(WaveShape.Sine, 5000, 5000, 255, 255, 100, SoundExpressionEffect.None, InterpolationCurve.Linear), music.PlaybackMode.UntilDone)
Wifi()
OLED12864_I2C.showString(
0,
0,
"6.1.5",
1
)
OLED12864_I2C.showString(
0,
0,
"Device serial number: " + control.deviceSerialNumber(),
1
)
basic.forever(function () {
    temperature_show()
    send_info_from_sensor()
    read_time_set()
    sensor_door()
    if (data.includes("#331")) {
        temp_air = parseFloat("" + data.charAt(0) + data.charAt(1))
    } else if (data.includes("#415")) {
        ssid = ssid
    } else if (data.includes("#416")) {
    	
    } else if (data.includes("#417")) {
        ssid = ssid
    }
})
