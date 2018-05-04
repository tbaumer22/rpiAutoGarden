import os
import time
import schedule
from threading import Timer
from weather import Weather, Unit

weather = Weather(unit=Unit.CELSIUS)
lookup = weather.lookup(2487365)
condition = lookup.condition

needToWaterMore = False


def initialization():
    schedule.every().day.at("11:30").do(startWatering, [0, 1])
    updateWeather()
    schedule.every().hour.do(updateWeather)


def updateWeather():
    lookup = weather.lookup(2487365)
    condition = lookup.condition
    print(condition.text)
    if condition != "Showers" & condition != "Thundershowers" & condition != "scattered showers":
        needToWaterMore = True
    else:
        needToWaterMore = False
    if condition == "cloudy":
        print("THIS WORKS REGARDLESS OF CASE")


def startWatering(stack, relayNum):
    os.system("megaio " + str(stack) + " rwrite " + str(relayNum) + " on")
    print("NOW WATERING THE PLANTS")
    # SHOULD BE 12 SECS
    needToStop = Timer(12.0, stopWatering, [stack,relayNum])
    needToStop.start()
    if needToWaterMore == True:
        waterMore = Timer(20.0, startWatering, [0, 1])
        waterMore.start()


def stopWatering(stack, relayNum):
    os.system("megaio " + str(stack) + " rwrite " + str(relayNum) + " off")
    print("FINISHED WATERING THE PLANTS")
    initialization()


initialization()
while True:
    schedule.run_pending()
    time.sleep(1)