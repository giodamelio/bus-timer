import argparse
import time
from threading import Timer

import requests

class BusTimer():
    def __init__(self, options):
        self.options = options
        self.refresh()
        
    def refresh(self):
        Timer(self.options.interval, self.refresh, ()).start()
        
        time = self.getNextTime(self.options.stopId, self.options.busId)
        
        print "Next {0} arives in {1} minutes".format(self.options.busId, time)

        self.writeTime(time)
    
    def getNextTime(self, routeId, busId):
        if self.options.testData:
            return int(self.options.testData)
        else:
            data = requests.get("http://api.pugetsound.onebusaway.org/api/where/arrivals-and-departures-for-stop/1_%s.json" % routeId,
                params={
                    "key": "TEST"
                }
            )

            # Get the predicted time until next bus
            if len(data.json()["data"]["arrivalsAndDepartures"]) > 0:
                nextBusTime = data.json()["data"]["arrivalsAndDepartures"][0]["predictedDepartureTime"]
            else:
                return -1

            timeTillNextBus = nextBusTime - (int(time.time()) * 1000)

            return (timeTillNextBus / 1000 / 60)

    def writeTime(self, time):
        if not self.options.noDisplay:
            # We have a hardware display
            from Adafruit_Seven_Segment_Backback import Adafruit_7Segment
            # Init our display
            display = Adafruit_7Segment.SevenSegment(address=0x70)
            
            # If there are no buses on the scedule do a line
            if time == -1:
                display.writeDigitRaw(0, 0x40)
                display.writeDigitRaw(1, 0x40)
                display.writeDigitRaw(3, 0x40)
                display.writeDigitRaw(4, 0x40)
                return

            # Check if our nunber is negitive
            negative = True if time < 0 else False

            # Remove the negitive value
            time = abs(time)

            # Convert the time to a string and fill extra digits
            time = str(time).zfill(4)

            display.writeDigit(0, int(time[0]))
            display.writeDigit(1, int(time[1]))
            display.setColon(True)
            display.writeDigit(3, int(time[2]))
            display.writeDigit(4, int(time[3]), negative)
        else:
            # No hardware display
            print time
            print str(time).zfill(4)[0]


if __name__ == "__main__":
    # Parse our arguments
    parser = argparse.ArgumentParser()
    
    # Get the stop id 
    parser.add_argument("--stop-id", "-s", dest="stopId", default=2275, help="Set the stop id")

    # Get the bus id 
    parser.add_argument("--bus-id", "-b", dest="busId", default=8, help="Set the bus id")

    # Get the refresh interval
    parser.add_argument("--refresh-interval", "-i", dest="interval", default=30, help="Set the refresh interval in seconds")

    # Do we have a hardware diaplay
    parser.add_argument("--no-display", "-nd", dest="noDisplay", action="store_true", help="Do we have a hardware display")

    # Use test data
    parser.add_argument("--test-data", "-d", dest="testData", help="Set the bus id")
    
    # Set our defautls 
    parser.set_defaults(noDisplay=False)

    # Parse our args
    args = parser.parse_args()

    # Start our timer
    timer = BusTimer(args)

