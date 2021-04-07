
#!/usr/bin/env python

import colorsys
import time
from sys import exit
import os

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    exit('This script requires the pillow module\nInstall with: sudo pip install pillow')

try:
    import unicornhathd
except ImportError:
    pi = False
    from unicorn_hat_sim import unicornhathd
    print("Running on simulator")
    unicornhathd.set_layout(unicornhathd.AUTO)
    unicornhathd.rotation(0)
    unicornhathd.brightness(0.5)

class splashScreen():
    def __init__(self, text=None, rainbow=True, rotation=0):
        if text==None:
            self.text = 'Splash screen! Informing you that the program has started!'
        else:
            self.text = text
        self.font_size = 12
        linuxFont = "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"
        macFont = "/Library/Fonts/GillSans.ttc"
        if os.path.isfile(linuxFont):
            self.font = linuxFont
        else:
            self.font = macFont
        self.rainbow = rainbow
        unicornhathd.rotation(rotation)
        
        self.prepareImage()
        self.show()
        #unicornhathd.off()

    def prepareImage(self):
        self.width, self.height = unicornhathd.get_shape()
        unicornhathd.brightness(0.5)
        text_x = 1
        text_y = 2
        # Load the font using PIL's ImageFont
        font = ImageFont.truetype(self.font, self.font_size)
        # Ask the loaded font how big our text will be
        self.text_width, self.text_height = font.getsize(self.text)
        # Make sure we accommodate enough width to account for our text_x left offset
        self.text_width += self.width + text_x
        # Now let's create a blank canvas wide enough to accomodate our text
        self.image = Image.new('RGB', (self.text_width, max(self.height, self.text_height)), (0, 0, 0))
        # To draw on our image, we must use PIL's ImageDraw
        draw = ImageDraw.Draw(self.image)
        # And now we can draw text at our desited (text_x, text_y) offset, using our loaded font
        draw.text((text_x, text_y), self.text, fill=(255, 255, 255), font=font)

    def show(self):
        # To give an appearance of scrolling text, we move a 16x16 "window" across the image we generated above
        # The value "scroll" denotes how far this window is from the left of the image.
        # Since the window is "width" pixels wide (16 for UHHD) and we don't want it to run off the end of the,
        # image, we subtract "width".
        for scroll in range(self.text_width - self.width):
            for x in range(self.width):

                # Figure out what hue value we want at this point.
                # "x" is the position of the pixel on Unicorn HAT HD from 0 to 15
                # "scroll" is how far offset from the left of our text image we are
                # We want the text to be a complete cycle around the hue in the HSV colour space
                # so we divide the pixel's position (x + scroll) by the total width of the text
                # If this pixel were half way through the text, it would result in the number 0.5 (180 degrees)
                hue = (x + scroll) / float(self.text_width)

                # Now we need to convert our "hue" value into r,g,b since that's what colour space our
                # image is in, and also what Unicorn HAT HD understands.
                # This list comprehension is just a tidy way of converting the range 0.0 to 1.0
                # that hsv_to_rgb returns into integers in the range 0-255.
                # hsv_to_rgb returns a tuple of (r, g, b)
                br, bg, bb = [int(n * 255) for n in colorsys.hsv_to_rgb(hue, 1.0, 1.0)]

                # Since our rainbow runs from left to right along the x axis, we can calculate it once
                # for every vertical line on the display, and then re-use that value 16 times below:

                for y in range(self.height):
                    # Get the r, g, b colour triplet from pixel x,y of our text image
                    # Our text is white on a black background, so these will all be shades of black/grey/white
                    # ie 255,255,255 or 0,0,0 or 128,128,128
                    pixel = self.image.getpixel((x + scroll, y))

                    # Now we want to turn the colour of our text - shades of grey remember - into a mask for our rainbow.
                    # We do this by dividing it by 255, which converts it to the range 0.0 to 1.0
                    r, g, b = [float(n / 255.0) for n in pixel]

                    # We can now use our 0.0 to 1.0 range to scale our three colour values, controlling the amount
                    # of rainbow that gets blended in.
                    # 0.0 would blend no rainbow
                    # 1.0 would blend 100% rainbow
                    # and anything in between would copy the anti-aliased edges from our text
                    r = int(br * r)
                    g = int(bg * g)
                    b = int(bb * b)

                    # Finally we colour in our finished pixel on Unicorn HAT HD
                    if self.rainbow:
                        unicornhathd.set_pixel(self.width - 1 - x, y, r, g, b)
                    else:
                        unicornhathd.set_pixel(self.width - 1 - x, y, pixel[0], pixel[1], pixel[2])

            # Finally, for each step in our scroll, we show the result on Unicorn HAT HD
            unicornhathd.show()
            # And sleep for a little bit, so it doesn't scroll too quickly!
            time.sleep(0.1)
