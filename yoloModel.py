from torch import hub, cuda
import numpy as np
from cv2 import cv2


def load_model(mod='yolov5m6'):
    """Loads Yolo5 model."""
    model = hub.load('yolov5', mod, source='local')
    model.conf = 0.25  # NMS confidence threshold
    model.iou = 0.45  # NMS IoU threshold
    model.agnostic = False  # NMS class-agnostic
    model.multi_label = False  # NMS multiple labels per box
    model.max_det = 1000  # maximum number of detections per image
    model.amp = False  # Automatic Mixed Precision (AMP) inference
    return model


class YoloModel:
    """Class implements Yolo5 model to make inferences on an image, video or YouTube video."""

    def __init__(self):
        """Initializes the class with youtube url and output file.
        :param path: Has to be as youtube URL,on which prediction is made.
        :param out_file: A valid output file name."""

        self.device = 'cuda' if cuda.is_available() else 'cpu'
        self.model = load_model()
        self.classes = self.model.names
        self.colors = np.random.randint(0, 255, size=(len(self.classes), 3), dtype="uint8")

    def score_frame(self, frame):
        """Takes a single frame as input, and scores the frame using yolo5 model.
        :param frame: input frame in numpy/list/tuple format.
        :return: Labels and Coordinates of objects detected by model in the frame."""
        self.model.to(self.device)
        frame = [frame]
        results = self.model(frame)

        labels, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
        return labels, cord

    def class_to_label(self, x):
        """For a given label value, return corresponding string label.
        :param x: numeric label
        :return: corresponding string label"""
        return self.classes[int(x)]

    def plot_boxes(self, results, frame):
        """Takes a frame and its results as input, and plots the bounding boxes and label on to the frame.
        :param results: contains labels and coordinates predicted by model on the given frame.
        :param frame: Frame which has been scored.
        :return: Frame with bounding boxes and labels ploted on it."""

        labels, cord = results
        n = len(labels)
        x_shape, y_shape = frame.shape[1], frame.shape[0]
        for i in range(n):
            row = cord[i]
            if row[4] >= 0.2:
                label = self.class_to_label(labels[i])
                x1, y1, x2, y2 = int(row[0] * x_shape), int(row[1] * y_shape), int(row[2] * x_shape), int(
                    row[3] * y_shape)
                color = [int(c) for c in self.colors[self.classes.index(label)]]
                cv2.rectangle(frame, (x1, y1), (x2, y2), color=color, thickness=1)
                cv2.putText(frame, label, (x1, y1), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=color, thickness=1)

        return frame

    def __call__(self, frame):
        """This function is called when class is executed, it runs the loop to read the video frame by frame,
        and write the output into a new file.
        :return: void"""

        results = self.score_frame(frame)
        frame = self.plot_boxes(results, frame)

        return frame
