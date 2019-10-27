from PIL import Image, ImageFont, ImageDraw
from font_hanken_grotesk import HankenGroteskBold, HankenGroteskMedium
from font_intuitive import Intuitive
from inky import InkyPHAT

inky_display = InkyPHAT("red")
inky_display.set_border(inky_display.RED)
scale_size = 1
img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)

font = ImageFont.truetype(HankenGroteskBold, int(20 * scale_size))

message = "Hello, World! \n Ben"
x = (inky_display.WIDTH / 2)
#Display at top
y = 0

draw.text((x, y), message, inky_display.RED, font)
inky_display.set_image(img)
inky_display.show()