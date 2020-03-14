def displayInky(output):
    from PIL import Image, ImageFont, ImageDraw
    from inky import InkyPHAT

    inky_display = InkyPHAT("red")
    inky_display.set_border(inky_display.RED)

    img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
    draw = ImageDraw.Draw(img)

    headerSize = 12
    headerFont = ImageFont.truetype("/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf", headerSize)
    messageFont = ImageFont.truetype("/usr/share/fonts/truetype/liberation2/LiberationMono-Regular.ttf", int(75 / (output['bodyLines'])))
    
    x = 0
    y = 0
    draw.text((x, y), output['header'] + ' - '+ output['subHeader'], inky_display.RED, headerFont)
    draw.text((x, y+headerSize), output['body'], inky_display.BLACK, messageFont)
    inky_display.set_image(img)
    inky_display.show()


def displayCmd(output):
    print('\n**************\n')
    print(output['header'])
    print(output['subHeader'])
    print('_______________')
    print(output['body'])
    print('**************\n')