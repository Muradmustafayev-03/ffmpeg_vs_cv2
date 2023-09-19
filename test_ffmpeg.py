import ffmpeg
import numpy as np
import time
import psutil


def test_ffmpeg(input_video):
    probe = ffmpeg.probe(input_video)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)

    if video_stream is None:
        print("No video stream found in the input file.")
        return

    width = int(video_stream['width'])
    height = int(video_stream['height'])

    process1 = (
        ffmpeg.input(input_video).output('pipe:', format='rawvideo', pix_fmt='bgr24')
    )
    process1.compile()

    process1 = process1.run_async(pipe_stdout=True)

    start = time.perf_counter()
    while True:
        in_bytes = process1.stdout.read(width * height * 3)
        if not in_bytes:
            break
        frame = np.frombuffer(in_bytes, np.uint8).reshape([height, width, 3])
    end = time.perf_counter()

    memory_usage = psutil.Process().memory_info().rss / (1024 ** 2)

    fps = int(video_stream['nb_frames']) / (end - start)
    return fps, memory_usage


if __name__ == '__main__':
    for i in range(5):
        fps, mem = test_ffmpeg(f"input{i}.mp4")
        print(f"FPS: {fps:.1f}")
        print(f"Memory usage: {mem:.2f} MB")
