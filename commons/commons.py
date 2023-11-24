def is_jupyter():
    try:
        import IPython

        if IPython.get_ipython() is not None:
            # print("Running in Jupyter Notebook")
            return True
        else:
            return False
            # print("Running as a standalone .py file")
    except NameError:
        return False


def display(text, image):
    if is_jupyter():
        print("Running in Jupyter Notebook")
        import matplotlib as mpl
        import matplotlib.pyplot as plt

        mpl.rcParams["figure.dpi"] = 300

        plt.title(text)
        plt.axis("off")
        plt.imshow(image)
        plt.show()
    else:
        print("Running as a standalone .py file")
        import cv2

        cv2.imshow(text, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def generate_output_string():
    from datetime import datetime

    now = datetime.now()
    output_str = now.strftime("%d_%m_%Y_%H_%M_%S") + "_output"
    return output_str


# Taken from: https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class TextStyle:
    start = "\033[1m"
    end = "\033[0;0m"


def recreate_directory(path):
    import shutil

    # Remove the existing output directory and its contents if it exists
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
            print("Removed existing directory:", path)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))

    # Create the output directory
    os.makedirs(path)


class CustomVideoCapture:
    @staticmethod
    def get_video_capture_object(path):
        cap = None
        num_frames = 0
        fps = 0
        try:
            cap = cv2.VideoCapture(path)

            if cap.isOpened():
                num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                fps = int(cap.get(cv2.CAP_PROP_FPS))

                if num_frames > 0:
                    print("==================")
                    print(f"#Frames: {num_frames}")
                    print(f"Video FPS: {fps}")
                    print("==================")
                    print()
                else:
                    print(
                        "The video file is empty or there was an issue reading the frame count."
                    )
                    sys.exit(0)
            else:
                print("The video could not be opened.")

        except cv2.error as e:
            print(f"OpenCV error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
        # finally:
        # video.release()
        return cap, num_frames, fps

    def load_image(image_path):
        import cv2

        """
        Read an image.

        Parameters:
        - image_path (str): The path to the image file.

        Returns:
        - Image
        """
        try:
            # Read the image
            image = cv2.imread(image_path)

            if image is None:
                raise FileNotFoundError(
                    f"Error: Unable to read the image at '{image_path}'."
                )
        except Exception as e:
            print(f"Error: {e}")

        return image
