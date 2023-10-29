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
