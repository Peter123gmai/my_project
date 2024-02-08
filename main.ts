function sensor_temperature () {
    if (dht11_dht22.readDataSuccessful() && dht11_dht22.sensorrResponding()) {
        OLED.drawLoading(30)
        Wifi_setup()
    } else if (!(dht11_dht22.sensorrResponding()) || !(dht11_dht22.readDataSuccessful())) {
        OLED.clear()
        OLED.writeStringNewLine("Sensor temperature is not found. please check and reboot into system ")
        OLED.clear()
        OLED.writeStringNewLine("Rebooting...")
        OLED.clear()
        dht11_dht22.queryData(
        DHTtype.DHT22,
        DigitalPin.P9,
        true,
        true,
        false
        )
        basic.pause(5000)
        control.reset()
    }
}
function startup () {
    music.play(music.createSoundExpression(WaveShape.Sine, 1, 5000, 0, 255, 1000, SoundExpressionEffect.None, InterpolationCurve.Linear), music.PlaybackMode.UntilDone)
    basic.pause(500)
    music.play(music.createSoundExpression(WaveShape.Sine, 5000, 5000, 255, 255, 100, SoundExpressionEffect.None, InterpolationCurve.Linear), music.PlaybackMode.UntilDone)
    OLED.init(128, 64)
    OLED.writeStringNewLine("Smart Home Iot project. OS version v5.6.5")
    OLED.writeStringNewLine("Device name: " + control.deviceName())
    OLED.writeStringNewLine("Device serial number: " + ("" + control.deviceSerialNumber()))
    OLED.clear()
    OLED.drawLoading(0)
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
    dht11_dht22.queryData(
    DHTtype.DHT22,
    DigitalPin.P8,
    true,
    true,
    false
    )
    dht11_dht22.selectTempType(tempType.celsius)
    OLED.drawLoading(5)
    sensor_temperature()
}
function startup2 () {
    basic.showLeds(`
        # . # . #
        . . . . .
        # . # . #
        . . . . .
        # . # . #
        `)
    basic.showLeds(`
        . . . . .
        . # # # .
        . # # # .
        . # # # .
        . . . . .
        `)
    basic.showLeds(`
        . . . . #
        . # # # .
        . # # # .
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
    OLED.clear()
    OLED.writeStringNewLine("Type Password:")
    music.play(music.stringPlayable("C E G B C5 A F D ", 300), music.PlaybackMode.UntilDone)
}
function Wifi_setup () {
    esp8266.init(SerialPin.USB_TX, SerialPin.USB_RX, BaudRate.BaudRate115200)
    if (esp8266.isESP8266Initialized()) {
        OLED.drawLoading(50)
        esp8266.connectWiFi("VAN HOAN", "Winthovanhoan")
        if (esp8266.isWifiConnected()) {
            OLED.drawLoading(100)
            OLED.clear()
            for (let index = 0; index < 4; index++) {
                OLED.writeStringNewLine("starting up.")
                basic.pause(100)
                OLED.writeStringNewLine("starting up..")
                basic.pause(100)
                OLED.writeStringNewLine("starting up...")
                basic.pause(100)
            }
            OLED.clear()
            basic.clearScreen()
            startup2()
        } else {
            OLED.clear()
            OLED.writeStringNewLine("cannot connect to router wifi. Please check and reboot into system")
            esp8266.connectWiFi("VAN HOAN", "Winthovanhoan")
            OLED.clear()
            OLED.writeStringNewLine("Rebooting...")
            OLED.clear()
            basic.pause(5000)
            control.reset()
        }
    } else {
        OLED.clear()
        OLED.writeStringNewLine("cannot initialize module wifi ESP8266 - Cytron. Please check and reboot into system")
        OLED.clear()
        OLED.writeStringNewLine("Rebooting...")
        OLED.clear()
        basic.pause(5000)
        control.reset()
    }
}
let gate_door_is_close = false
DS1307.DateTime(
2024,
2,
8,
4,
15,
30,
30
)
let list2 = [0, 1]
startup()
basic.forever(function () {
    if (gate_door_is_close == true) {
        OLED.writeStringNewLine(keypad.getKeyString())
        if (keypad.getKeyString() == "A03745BCD83") {
            gate_door_is_close = false
            OLED.writeStringNewLine("Type # to close")
        }
    } else if (gate_door_is_close == false) {
        if (keypad.getKeyString() == "#") {
            gate_door_is_close = true
            OLED.writeStringNewLine("Type password: ")
        }
    }
})
basic.forever(function () {
    if (dht11_dht22.readDataSuccessful() && (esp8266.isESP8266Initialized() && esp8266.isWifiConnected() && dht11_dht22.readDataSuccessful())) {
        list2[0] = dht11_dht22.readData(dataType.humidity)
        list2[1] = dht11_dht22.readData(dataType.temperature)
        radio.sendValue("RTC-82734568", list2[0])
        radio.sendValue("RTC-53456725", list2[1])
        esp8266.uploadThingspeak(
        "2WWRE6MHVGBS1Q7S",
        list2[0],
        list2[1]
        )
        if (esp8266.isThingspeakUploaded()) {
            basic.showIcon(IconNames.Yes)
            basic.clearScreen()
        } else {
            basic.showNumber(593)
        }
    }
})
