# Single Color RGB565 Blob Tracking Example
#
# This example shows off single color RGB565 tracking using the OpenMV Cam using the FLIR LEPTON.

# FLIR Lepton Shutter Note: FLIR Leptons with radiometry and a shutter will pause the video often
# as they heatup to re-calibrate. This will happen less and less often as the sensor temperature
# stablizes. You can force the re-calibration to not happen if you need to via the lepton API.
# However, it is not recommended because the image will degrade overtime.

import sensor, image, time, math, lcd

# Cool looking color palette
image.set_rainbow_lut(image.IRONBOW_LUT)

# Color Tracking Thresholds (L Min, L Max, A Min, A Max, B Min, B Max)
thresholds = [( 70, 100,  -30,   40,   20,  100)]

print("Resetting Lepton...")
sensor.reset()
print("Lepton Res (%dx%d)" % (sensor.lepton_width(), sensor.lepton_height()))
print("Radiometry Available: " + ("Yes" if sensor.lepton_type() else "No"))

sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time=5000)
clock = time.clock()
lcd.init()

# Only blobs that with more pixels than "pixel_threshold" and more area than "area_threshold" are
# returned by "find_blobs" below. Change "pixels_threshold" and "area_threshold" if you change the
# camera resolution. "merge=True" merges all overlapping blobs in the image.

while(True):
    clock.tick()
    img = sensor.snapshot()
    for blob in img.find_blobs(thresholds, pixels_threshold=200, area_threshold=200, merge=True):
        img.draw_rectangle(blob.rect())
        img.draw_cross(blob.cx(), blob.cy())
    lcd.display(img)
    print(clock.fps())
