module.exports = class
    # Define some constents
    HT16K33_REGISTER_DISPLAY_SETUP = 0x80

    constructor: (@address = 0x70) ->
        # Hacky way to determine if we are on the raspberry pi
        os = require "os"
        if os.arch() isnt "arm"
            console.log "You must be on a raspberry pi for this to work"
            process.exit 1
        else
            i2c = require "i2c"

        wire = new i2c(address, {device: "/dev/i2c-1"})
        wire.scan (err, data) ->
            console.log data

