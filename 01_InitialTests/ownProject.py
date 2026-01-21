import numpy as np
from PIL import Image

# ==========================
# CONFIG
# ==========================
RESOLUTION = 2048
CLOUD_SCALE = 4.0
CLOUD_COVERAGE = 0.45
CLOUD_SOFTNESS = 0.18
SKY_BRIGHTNESS = 30
CLOUD_BRIGHTNESS = 220
OCTAVES = 6
SEED = 123

np.random.seed(SEED)

# ==========================
# VALUE NOISE
# ==========================
def smoothstep(t):
    return t * t * (3 - 2 * t)

def value_noise(width, height, scale):
    grid_x = int(width / scale) + 2
    grid_y = int(height / scale) + 2
    grid = np.random.rand(grid_y, grid_x)

    img = np.zeros((height, width), dtype=np.float32)

    for y in range(height):
        for x in range(width):
            gx = x / scale
            gy = y / scale

            x0 = int(gx)
            y0 = int(gy)

            sx = smoothstep(gx - x0)
            sy = smoothstep(gy - y0)

            n0 = grid[y0, x0]
            n1 = grid[y0, x0 + 1]
            ix0 = n0 + sx * (n1 - n0)

            n0 = grid[y0 + 1, x0]
            n1 = grid[y0 + 1, x0 + 1]
            ix1 = n0 + sx * (n1 - n0)

            img[y, x] = ix0 + sy * (ix1 - ix0)

    return img

def fractal_noise(width, height, octaves):
    noise = np.zeros((height, width), dtype=np.float32)
    amplitude = 1.0
    frequency = 1.0
    max_amp = 0

    for _ in range(octaves):
        layer = value_noise(width, height, RESOLUTION / (CLOUD_SCALE * frequency))
        noise += layer * amplitude
        max_amp += amplitude
        amplitude *= 0.5
        frequency *= 2.0

    return noise / max_amp

# ==========================
# GENERATE CLOUD FIELD
# ==========================
noise = fractal_noise(RESOLUTION, RESOLUTION, OCTAVES)

cx = cy = RESOLUTION // 2
radius = RESOLUTION // 2

img = np.zeros((RESOLUTION, RESOLUTION), dtype=np.float32)

for y in range(RESOLUTION):
    for x in range(RESOLUTION):
        dx = (x - cx) / radius
        dy = (y - cy) / radius
        r = np.sqrt(dx*dx + dy*dy)

        if r <= 1.0:
            horizon_weight = r ** 1.4

            cloud = noise[y, x] - CLOUD_COVERAGE
            cloud = np.clip(cloud / CLOUD_SOFTNESS, 0, 1)

            cloud *= horizon_weight

            img[y, x] = SKY_BRIGHTNESS + cloud * CLOUD_BRIGHTNESS

# ==========================
# FINAL IMAGE
# ==========================
img = np.clip(img, 0, 255).astype(np.uint8)
rgb = np.stack([img, img, img], axis=2)

# Mask outside horizon
yy, xx = np.mgrid[:RESOLUTION, :RESOLUTION]
mask = (xx - cx)**2 + (yy - cy)**2 <= radius**2
rgb[~mask] = 0

Image.fromarray(rgb).save("allsky_clouds.png")
print("Saved allsky_clouds.png")
