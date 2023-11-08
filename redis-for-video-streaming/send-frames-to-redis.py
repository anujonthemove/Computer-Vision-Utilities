import cv2
import redis


def send_frames_to_redis(video_path, redis_host, redis_port):
    cap = cv2.VideoCapture(video_path)
    r = redis.Redis(host=redis_host, port=redis_port, password="")

    frame_counter = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        cv2.namedWindow("frame", cv2.WINDOW_KEEPRATIO)
        cv2.imshow("frame", frame)
        k = cv2.waitKey(1)
        if k == 27:
            cv2.destroyAllWindows()
            cap.release()
            break
        # Encode the frame as JPEG and convert to base64
        _, frame_encoded = cv2.imencode(".jpg", frame)
        # frame_base64 = base64.b64encode(frame_encoded.tobytes()).decode("utf-8")
        # frame_base64 = base64.b64encode(frame_encoded.tobytes())
        frame_bytes = frame_encoded.tobytes()

        # Send the frame and frame counter to Redis
        # r.set("frame_encoded", frame_base64)
        r.set("frame_bytes", frame_bytes)
        r.set("frame_counter", frame_counter)

        print(f"Sent frame {frame_counter}")
        frame_counter += 1

        # Adjust the sleep time to control the frame rate
        # time.sleep(0.1)  # Adjust as needed

    cap.release()
    r.close()


if __name__ == "__main__":
    video_path = "/home/acer/workspace/videos/Annealing_View_vid.mp4"
    redis_host = "localhost"
    redis_port = 6379

    send_frames_to_redis(video_path, redis_host, redis_port)
