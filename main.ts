function Wifi () {
    esp8266.init(SerialPin.P0, SerialPin.P1, BaudRate.BaudRate115200)
    if (esp8266.isESP8266Initialized()) {
        esp8266.connectWiFi("HOAN VAN", "winthovanhoan")
        if (esp8266.isWifiConnected()) {
            Sensor_DHT22()
        } else {
            OLED.writeStringNewLine("Cannot connect to router. Please check and reboot sysstem")
            esp8266.connectWiFi("HOAN VAN", "winthovanhoan")
            basic.pause(500)
            control.reset()
        }
    } else {
        OLED.writeStringNewLine("ESP8266 is not found. Please check and reboot sysstem")
        esp8266.init(SerialPin.P0, SerialPin.P1, BaudRate.BaudRate115200)
        basic.pause(500)
        control.reset()
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
    music.play(music.stringPlayable("C E G B C5 A F D ", 300), music.PlaybackMode.UntilDone)
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
        Startup()
    } else if (!(dht11_dht22.sensorrResponding()) || !(dht11_dht22.readDataSuccessful())) {
        OLED.writeStringNewLine("Sensor DHT22 is not found. Please check and reboot system")
        dht11_dht22.queryData(
        DHTtype.DHT22,
        DigitalPin.P2,
        true,
        true,
        false
        )
        dht11_dht22.selectTempType(tempType.celsius)
        basic.pause(500)
        control.reset()
    }
}
let date = ""
let time = ""
let hour = 0
let minute_text = ""
OLED.init(128, 64)
let list2 = [0, 1]
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
basic.forever(function () {
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
            basic.showIcon(IconNames.Sad)
            basic.clearScreen()
        }
    }
})
basic.forever(function () {
    esp8266.updateInternetTime()
    if (esp8266.isInternetTimeUpdated()) {
        if ((0 as any) < (10 as any)) {
            minute_text = "0" + ("" + esp8266.getMinute())
        } else {
            minute_text = convertToText(esp8266.getMinute())
        }
        if (esp8266.getHour() > 12) {
            hour = esp8266.getHour() - 12
        } else {
            hour = esp8266.getHour()
        }
        time = "" + esp8266.getHour() + " / " + ("" + esp8266.getMinute()) + " / " + ("" + esp8266.getSecond())
        date = "" + esp8266.getDay() + " / " + ("" + esp8266.getMonth()) + " / " + ("" + esp8266.getYear())
    } else {
        esp8266.updateInternetTime()
    }
})
