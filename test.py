import d3dshot
from PIL import Image

cam = d3dshot.create()
image = cam.screenshot()

data = image.tobytes()
print(image.mode, image.size, len(data))
new_image = Image.frombytes(image.mode, image.size, data)
new_image.show()