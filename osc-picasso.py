import argparse
from cmath import pi
import random
import time

def fastsleep(duration):
    init_time = time.time()
    while True:
        if init_time + duration <= time.time():
            return

parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="127.0.0.1",
    help="The ip of the OSC server")
parser.add_argument("--port", type=int, default=9000,
    help="The port the OSC server is listening on")
parser.add_argument("--img", default="image.png",
    help="The image to draw")
args = parser.parse_args()


# Load image
from PIL import Image
img = Image.open(args.img)
img = img.convert('RGB') // Convert to RGB to ensure getPixel properly outputs 3 values

# Get aspect ratio
ratio = img.size[0] / img.size[1]
# Resize image
img = img.resize((int(512 * ratio), 128))
# Save resized image
img.save("thumbnail.png")

# Get image size
width, height = img.size

lastColorR = 0
lastColorG = 0
lastColorB = 0
lastColorA = 0

from pythonosc import udp_client
client = udp_client.SimpleUDPClient(args.ip, args.port)

time.sleep(1)

client.send_message("/avatar/parameters/PaintEnabled", False)

time.sleep(1)

client.send_message("/avatar/parameters/PaintEnabled", True)
client.send_message("/avatar/parameters/ColorR", 0.0)
client.send_message("/avatar/parameters/ColorG", 0.0)
client.send_message("/avatar/parameters/ColorB", 0.0)
client.send_message("/avatar/parameters/ColorA", 0.0)

while(True):
    for y in range(height):
        posY = 1 - (y / height)
        client.send_message("/avatar/parameters/PosY", posY)

        for x in range(width):
            posX = x / width
            client.send_message("/avatar/parameters/PosX", posX)

            # Get pixel
            pixel = img.getpixel((x, y))

            colorR = pixel[0] / 255
            colorG = pixel[1] / 255
            colorB = pixel[2] / 255
            colorA = 1.0
            if len(pixel) == 4:
                colorA = pixel[3] / 255

            if colorR != lastColorR:
                client.send_message("/avatar/parameters/ColorR", colorR)
                lastColorR = colorR

            if colorG != lastColorG:
                client.send_message("/avatar/parameters/ColorG", colorG)
                lastColorG = colorG
            
            if colorB != lastColorB:
                client.send_message("/avatar/parameters/ColorB", colorB)
                lastColorB = colorB
            
            if colorA != lastColorA:
                client.send_message("/avatar/parameters/ColorA", colorA)
                lastColorA = colorA

            # print x, y, and color as hex
            if len(pixel) == 4:
                print('X: {:04.2f} Y: {:04.2f} Color: #{:02x}{:02x}{:02x}{:02x}'.format(posX, posY, pixel[0], pixel[1], pixel[2], pixel[3]))
            else:
                print('X: {:04.2f} Y: {:04.2f} Color: #{:02x}{:02x}{:02x}'.format(posX, posY, pixel[0], pixel[1], pixel[2]))

            fastsleep(0.01)
