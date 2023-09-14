import ffmpeg
import numpy as np
import time
import psutil

vid_info = ffmpeg.probe("input.mp4")['streams'][1]
frames = int(vid_info['nb_frames'])

process1 = (
    ffmpeg
    .input("input.mp4")
    .output('pipe:', format='rawvideo', pix_fmt='bgr24')
)
print(process1.compile())

process1 = process1.run_async(pipe_stdout=True)

start = time.perf_counter()
while True:
    in_bytes = process1.stdout.read(2160 * 3840 * 3)
    if not in_bytes:
        break
    frame = np.frombuffer(in_bytes, np.uint8).reshape([3840, 2160, 3])
end = time.perf_counter()

memory_usage = psutil.Process().memory_info().rss / (1024 ** 2)

print(f"{frames / (end - start):.1f} frames per second")
print(f"Memory usage: {memory_usage:.2f} MB")

process1.wait()
