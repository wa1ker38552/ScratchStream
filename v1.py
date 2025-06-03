import scratchattach as scratch3
from PIL import Image
import requests
import dxcam
import math
import time

project_id = 'PROJECT_ID_HERE'
ssid = 'YOUR_SSID_HERE'

session = scratch3.Session(ssid, username="YOUR_USERNAME_HERE")
conn = session.connect_cloud(project_id)

# 10 cloud variables / project
# 256 chars per cloud variable
# 1 needed for an indicator/toggle leaving 9 cloud variables
# 9 * 256 = 2304 chars
# each pixel requires 9 chars to represent with rgb and 12 to represent with hex (after encoding) so we're going with rgb
# 2304 / 9 = 256 pixels
# √256 = 16
# final image can be a max of 16x16 in resolution

def format_zeroes(value: int, amount: int) -> str:
    v = str(value)
    return f'{"0"*(amount-len(v))}{v}'

def send_to_scratch(data: str):
    chunks = [data[i:i + 256] for i in range(0, len(data), 256)]
    for i, chunk in enumerate(chunks):
        conn.set_var(f'chunk_{i+1}', chunks[i])
    for i in range(ALOTTED_VARIABLES-len(chunks)):
        conn.set_var(f'chunk_{ALOTTED_VARIABLES-i}', '0')

ALOTTED_VARIABLES = 10 # amount of avaliable cloud variables
aval_chars = ALOTTED_VARIABLES*256
res = math.floor(math.sqrt(aval_chars/9))

# dxcam is benchmarked as being fasther than other open source capturing software (at least for windows)
camera = dxcam.create()
camera.start()

while True:
    im = Image.fromarray(camera.get_latest_frame())
    im = im.resize((res, res))
    pix = im.load()


    pixels = []

    for i in range(res):
        data = []
        for j in range(res):
            try:
                r, g, b = pix[j, i]
            except ValueError:
                # goofy or transparent pixel
                r, g, b = 255, 255, 255
            except TypeError:
                # goofy or transparent pixel
                r, g, b = 255, 255, 255
            r = format_zeroes(r, 3)
            g = format_zeroes(g, 3)
            b = format_zeroes(b, 3)
            data.append(f'{r}{g}{b}')
        pixels.append(data)

    data = ''.join([''.join(ln) for ln in pixels])
    send_to_scratch(data)
