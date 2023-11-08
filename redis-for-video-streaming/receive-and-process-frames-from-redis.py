import cv2
import numpy as np
import redis


def receive_and_process_frame(redis_host, redis_port):
    r = redis.Redis(host=redis_host, port=redis_port, password="")

    while True:
        try:
            frame_bytes = r.get("frame_bytes")
            frame_counter = r.get("frame_counter").decode("utf-8")

            if frame_bytes is not None:
                frame_bytes = np.frombuffer(frame_bytes, dtype=np.uint8)
                frame = cv2.imdecode(frame_bytes, cv2.IMREAD_COLOR)

                # Process the frame as needed

                # Show the frame in a window
                cv2.namedWindow("frame", cv2.WINDOW_KEEPRATIO)
                cv2.imshow("frame", frame)
                k = cv2.waitKey(1)
                if k == 27:
                    cv2.destroyAllWindows()
                    break

                print("Frame received - Counter:", frame_counter)
            else:
                print("No frame received")

        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    redis_host = "localhost"
    redis_port = 6379

    receive_and_process_frame(redis_host, redis_port)
