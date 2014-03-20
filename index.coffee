request = require("request")

SevenSegment = require("./7Segment")

class BusTimer
    constructor: (@stopId, @busId, @updateFrequency) ->
        @getStopData()

    getStopData: ->
        request(
            url: "http://api.pugetsound.onebusaway.org/api/where/arrivals-and-departures-for-stop/1_#{@stopId}.json"
            qs:
                key: "TEST"
        , (error, response, body) =>
            # Get relevent data for response
            data = JSON.parse(body).data.arrivalsAndDepartures

            # Filter out bus's with the right id
            data = data.filter (x) =>
                x.routeId == "1_#{@busId}"

            # Pick out the bus that will arrive the soonest
            data = data[0]
            
            # Find time until next bus
            console.log Math.floor((data.predictedDepartureTime - (new Date).getTime()) / 1000 / 60)
        )

timer = new BusTimer(2275, 8, 30)

