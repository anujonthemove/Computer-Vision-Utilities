import sys
import time

import cv2
from shapely.geometry import LineString

DIVIDING_FACTOR = 4


class ROIDefiner:
    def __init__(self):
        self.drawing_mode = False
        self.select_x, self.select_y = -1, -1
        self.boundary_points = []
        self.boundary_points_inner = []

    def parse_wkt_data(self, wkt_data):
        wkt_data_split = wkt_data.split()
        x = int(round(float(wkt_data_split[1].strip("("))))
        y = int(round(float(wkt_data_split[2].strip(")"))))
        return x, y

    def set_boundary_points_inner(self, pa, pb):
        line_distance = LineString([pa, pb])
        y_threshold = int(line_distance.length / DIVIDING_FACTOR)
        point_y_threshold = LineString([pa, pb]).interpolate(y_threshold)
        point_x, point_y = self.parse_wkt_data(point_y_threshold.wkt)
        return point_x, point_y

    def draw_line(self, image, p1, p2, color, thickness):
        cv2.line(image, p1, p2, color, thickness)

    def define_roi(self, frame, copy_frame):
        self.drawing_mode = True

        def draw_rectangle(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                if self.drawing_mode:
                    self.select_x, self.select_y = x, y
            elif event == cv2.EVENT_LBUTTONUP:
                if self.drawing_mode:
                    if len(self.boundary_points) < 4:
                        self.boundary_points.append((self.select_x, self.select_y))
                        if len(self.boundary_points) == 2:
                            self.draw_line(
                                frame,
                                self.boundary_points[0],
                                self.boundary_points[1],
                                (255, 255, 255),
                                2,
                            )
                        elif len(self.boundary_points) == 3:
                            self.draw_line(
                                frame,
                                self.boundary_points[1],
                                self.boundary_points[2],
                                (0, 255, 255),
                                2,
                            )
                        elif len(self.boundary_points) == 4:
                            self.draw_line(
                                frame,
                                self.boundary_points[2],
                                self.boundary_points[3],
                                (255, 255, 255),
                                2,
                            )
                            self.draw_line(
                                frame,
                                self.boundary_points[3],
                                self.boundary_points[0],
                                (0, 255, 255),
                                2,
                            )
                            print(
                                "---------------------------------------------------------------------"
                            )
                            # ...
                            print(
                                "---------------------------------------------------------------------"
                            )
                            print("Press: \n'c': Confirm\n'r': Reset\n'q': Quit")
                            print(
                                "---------------------------------------------------------------------\n"
                            )

        cv2.namedWindow("Define RoI", cv2.WINDOW_KEEPRATIO)
        cv2.setMouseCallback("Define RoI", draw_rectangle)
        print("\nImage resolution: ", frame.shape)
        print("--------------------------------------------------------------")
        print("Define roi, select Left->Top->Right->Bottom points on an image")
        print("Please follow the below order while selecting roi")
        print("--------------------------------------------------------------")
        print("Select --> lower_left_x, lower_left_y  point")
        print("Select --> upper_left_x, upper_left_y  point")
        print("Select --> upper_right_x, upper_right_y  point")
        print("Select --> lower_right_x, lower_right_y  point")

        while True:
            cv2.imshow("Define RoI", frame)
            key = cv2.waitKey(10) & 0xFF
            if key == ord("r"):
                frame = copy_frame.copy()
                self.boundary_points[:] = []
                self.boundary_points_inner[:] = []
            elif key == ord("c"):
                self.drawing_mode = False
                cv2.destroyWindow("Define RoI")
                cv2.waitKey(1)
                break
            elif key == ord("q"):
                self.drawing_mode = False
                cv2.destroyWindow("Define RoI")
                cv2.waitKey(1)
                print("\n*** ROI NOT SET: Operation cancelled by user ***")
                sys.exit(0)

        return self.boundary_points


if __name__ == "__main__":
    roi_definer = ROIDefiner()
    # Load your image here
    frame = cv2.imread("0.jpg")
    copy_frame = frame.copy()
    boundary_points = roi_definer.define_roi(frame, copy_frame)
    print("Selected Boundary Points:", boundary_points)
