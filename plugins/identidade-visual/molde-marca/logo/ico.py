# favicon.ico (16/32/48) a partir dos PNG gerados por png.js. Rode de dentro de <projeto>/identidade/logo.
from PIL import Image
imgs = [Image.open(f'favicon/favicon-{n}.png').convert('RGBA') for n in (48, 32, 16)]
imgs[0].save('favicon/favicon.ico', sizes=[(48, 48), (32, 32), (16, 16)], append_images=imgs[1:])
print('ico ok')
