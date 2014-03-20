# Hacky way to determine if we are on the raspberry pi
os = require "os"
if os.arch() isnt "arm"
    i2c = require "i2c"
    console.log "I2C disabled"

module.exports = class
    constructor: ->
        HT16K33_REGISTER_DISPLAY_SETUP = 0x80
        #wire = new i2c(address, {device: "/dev/i2c-1", debug: true})
