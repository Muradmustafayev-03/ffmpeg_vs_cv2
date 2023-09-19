import cv2
import time
import psutil


def test_cv2(input_video):
    cap = cv2.VideoCapture(input_video, apiPreference=cv2.CAP_FFMPEG)
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    start = time.perf_counter()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
    end = time.perf_counter()

    memory_usage = psutil.Process().memory_info().rss / (1024 ** 2)
    fps = frames / (end - start)

    cap.release()

    return fps, memory_usage


if __name__ == '__main__':
    for i in range(5):
        fps, mem = test_cv2(f"input{i}.mp4")
        print(f"FPS: {fps:.1f}")
        print(f"Memory usage: {mem:.2f} MB")
