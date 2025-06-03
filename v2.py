import scratchattach as sa
from PIL import Image
import time
import math

def format_zeroes(value: int, amount: int) -> str:
    v = str(value)
    return f'{"0"*(amount-len(v))}{v}'


packets = 20
res = math.floor(math.sqrt((packets * 9 * 256)/9))
print(f'Resolution: {res}x{res}')

im = Image.open('test1.png')
im = im.resize((res, res))
pix = im.load()

project_id = 'PROJECT ID'
ssid = "SSID"
session = sa.login_by_id(ssid, username="USERNAME")
conn = session.connect_cloud(project_id)

s = ''
for row in range(res):
    for col in range(res):
        r, g, b = pix[col, row]
        r = format_zeroes(r, 3)
        g = format_zeroes(g, 3)
        b = format_zeroes(b, 3)
        s += f'{r}{g}{b}'


chunks = [s[i:i + 256] for i in range(0, len(s), 256)]
packets = [chunks[i:i + 9] for i in range(0, len(chunks), 9)]
print(f'Total chunks: {len(chunks)} - Total packets: {len(packets)} - Total characters: {len(s)}')
cn = 0
for p in packets:
    for i, c in enumerate(p):
        conn.set_var(f'chunk_{i+2}', c)
    for i in range(9-len(p)):
        print(9-i+1)
        conn.set_var(f'chunk_{9-i+1}', '0')

    conn.set_var('chunk_1', f'{format_zeroes(cn+1, 2)}{format_zeroes(len(packets), 2)}')
    cn += 1
    time.sleep(.2)
    print('Sending packet:', cn)
