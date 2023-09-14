import cv2
import time
import numpy as np
import psutil

cap = cv2.VideoCapture("input.mp4", apiPreference=cv2.CAP_FFMPEG)
frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

start = time.perf_counter()
while True:
    ret, frame = cap.read()
    if ret is False:
        break
    assert frame.shape == (2160, 3840, 3)
    assert frame.dtype == np.uint8
end = time.perf_counter()

memory_usage = psutil.Process().memory_info().rss / (1024 ** 2)

print(f"{frames / (end - start):.1f} frames per second")
print(f"Memory usage: {memory_usage:.2f} MB")

cap.release()
