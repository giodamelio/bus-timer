from Adafruit_Seven_Segment_Backback import Adafruit_7Segment

# Init our display
display = Adafruit_7Segment.SevenSegment(address=0x70)

display.writeDigit(0, 0);
display.writeDigit(1, 0);
display.writeDigit(3, 0);
display.writeDigit(4, 0);

