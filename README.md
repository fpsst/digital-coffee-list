# digital-coffee-list
## Description
Digital replacement for paper-based coffee lists using NFC reader (RC522), a Pi Zero W, rotary encoder (KY-040) and OLED in a 3D printed case.
Still work in progress.

## Requirements
This project is written for Python 3. The Pi Zero needs to be configured to use SPI (cardd reader) and I2C (OLED). 
I used [this library for KY-040](https://github.com/martinohanlon/KY040) and
[this one for the RC522 reader](https://github.com/pimylifeup/MFRC522-python).

The adafruit OLED lib comes with adafruit-blinka, which - as all other libs - can be installed using pip.

## Usage
The aim of this project is to provide a digital list in which the number of consumed and paid coffees is tracked. 
The use case is a shared coffee machine as used in e.g. offices.

Users authenticate with 13.45 MHz RFID chips or cards. The Pi Zero creates an MD5-hash from the chip ID and translates it into a Base58 uppercase short hash string (Probability for collision is considered low enough for medium sized offices up to 50 people), which is shown on the OLED display.
In the target application (not fully implemented yet), the user can then log into the Pi Zero's WiFi AP, visit a website (URL provided by e.g. QR-Code) and enter the pair of hash string and user name. Once this data is entered, the OLED can display the user name with each consumed coffee, along with the coffee count.

The sqlite DB contains the hash string, user name, #coffees, #paid coffees. As long as users are not registered, the coffee count can still be incremented and be assigned to the user lateron.
