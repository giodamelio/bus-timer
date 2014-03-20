import argparse
import time

import requests

class BusTimer():
    def __init__(self, options):
        self.options = options
        self.writeTime(self.getNextTime(2275, 8))
    
    def getNextTime(self, routeId, busId):
        data = requests.get("http://api.pugetsound.onebusaway.org/api/where/arrivals-and-departures-for-stop/1_%s.json" % routeId,
            params={
                "key": "TEST"
            }
        )

        # Get the predicted time until next bus
        nextBusTime = data.json()["data"]["arrivalsAndDepartures"][0]["predictedDepartureTime"]

        timeTillNextBus = nextBusTime - (int(time.time()) * 1000) 
        
        return (timeTillNextBus / 1000 / 60)

    def writeTime(self, time):
        if not self.options.noDisplay:
            # We have a hardware display
            from Adafruit_Seven_Segment_Backback import Adafruit_7Segment
            # Init our display
            display = Adafruit_7Segment.SevenSegment(address=0x70)
            display.writeDigit(0, str(time).zfill(4)[0])
            display.writeDigit(1, str(time).zfill(4)[1])
            display.writeDigit(3, str(time).zfill(4)[2])
            display.writeDigit(4, str(time).zfill(4)[3])
        else:
            # No hardware display
            print time
            print str(time).zfill(4)[0]


if __name__ == "__main__":
    # Parse our arguments
    parser = argparse.ArgumentParser()
    
    # Get the stop id 
    parser.add_argument("--stop-id", "-s", dest="id", help="Set the stop id")

    # Do we have a hardware diaplay
    parser.add_argument("--no-display", "-nd", dest="noDisplay", action="store_true", help="Do we have a hardware display")
    
    # Set our defautls 
    parser.set_defaults(noDisplay=False)

    # Parse our args
    args = parser.parse_args()

    # Start our timer
    timer = BusTimer(args)

