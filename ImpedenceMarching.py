from PIL import Image, ImageDraw, ImageFilter
import math

# linear interpolation function
def lerp(x, y, blend):
    return x + blend * (y - x)

# normalize for color ranges
def normalize01(input):
    return input/255
def normalize255(input):
    normalizedOutput = int(input*255)
    if (normalizedOutput > 255):
        normalizedOutput = 255
    return int(normalizedOutput)

im = Image.open("Heightmap.png")
imR = im.convert("L")
imG = im.convert("L")
imB = im.convert("L")
imA = im.convert("L")
imRGBA = im.convert("RGBA")

uSteps = im.size[0]
vSteps = im.size[1]
status = False
flowColor = (0,0,255)
stepLossRate = 1
materialDensity = .75
rSteps = 150

# START TIMING
import time
startTime = time.time()

def impede(im_in, rotation = 0):
    # we need to generate a list of U,V tuples to pass to the drawing board
    #draw = ImageDraw.Draw(im_in)
    im_temp = im_in.rotate(rotation)

    for column in range(0,uSteps):
        startUV = (int(uSteps/2),1)

        # init prevHeight
        prevHeight = 0

        # init density
        flowDensity = 1

        # init coordinate positions
        uPos = column
        vPos = 0

        if status:
            print("Step: " + str(column+1) + "/" + str(uSteps))

        # draw flowColor over the current pixel
        # if heightColor is less than prevHeight, flowDensity is unchanged - if it's MORE than prevHeight, deltaHeight is subtracted from flowDensity

        # loop through every vertical pixel in this U column
        for row in range(0,vSteps):
            # reduce flowDensity by loss rate
            flowDensity = flowDensity * stepLossRate

            # only do if valid UV in range
            if (vPos <= vSteps):
                # get height at current pixel
                height = im_temp.getpixel((uPos,vPos))

                # get deltaHeight
                deltaHeight = normalize01(height - prevHeight) * materialDensity

                # if deltaHeight is positive, lower density
                if (deltaHeight > 0):
                    newDensity = flowDensity - deltaHeight

                    # prevent negative flowDensity
                    if (newDensity > 0):
                        flowDensity = newDensity
                    else:
                        flowDensity = 0

                # draw newColor onto current pixel
                im_temp.putpixel((uPos,vPos),normalize255(flowDensity))
                #print(newColor)

                prevHeight = height

            # increment the v position if in range
            newVPos = vPos + 1
            if (newVPos <= vSteps):
                vPos = newVPos

    return im_temp.rotate(-1 * rotation)

imR = impede(imR, 0)
imG = impede(imG, 90)
imB = impede(imB, 180)
imA = impede(imA, 270)

for u in range(uSteps):
    for v in range(vSteps):
        imRGBA.putpixel(
            (u, v),
            (
                imR.getpixel((u, v)),
                imG.getpixel((u, v)),
                imB.getpixel((u, v)),
                imA.getpixel((u, v))
            )
        )

print("Flowmarch Completed!")
endTime = time.time()

print("Time elapsed: {} seconds".format('%.2f'%(endTime - startTime)))

# write to stdout
imR.save("Impedence_R.png")
imG.save("Impedence_G.png")
imB.save("Impedence_B.png")
imA.save("Impedence_A.png")
imRGBA.save("Impedence_RGBA.png")
#imRGBA.show()
