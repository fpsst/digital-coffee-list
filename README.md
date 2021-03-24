# digital-coffee-list
## Description
Digital replacement for paper-based coffee lists using NFC reader (RC522), a Pi Zero W, rotary encoder (KY-040) and OLED in a 3D printed case.
Still work in progress.

## Requirements
This project is written for Python 3. The Pi Zero needs to be configured to use SPI (cardd reader) and I2C (OLED). 
I used [this library for KY-040](https://github.com/martinohanlon/KY040) and
[this one for the RC522 reader](https://github.com/pimylifeup/MFRC522-python).

The adafruit OLED lib comes with adfruit-blinka, which - as all other libs - can be found using pip.


