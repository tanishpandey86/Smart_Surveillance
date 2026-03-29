import cv2
import numpy as np

class KLTTracker:
    def __init__(self):
        self.lk_params = dict(
            winSize=(15, 15),
            maxLevel=3,
            criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,
                      10, 0.03)
        )
        self.feature_params = dict(
            maxCorners=100, qualityLevel=0.3,
            minDistance=7, blockSize=7
        )
        self.prev_gray = None
        self.prev_pts  = None

    def update(self, frame, mask):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if self.prev_gray is None:
            self.prev_gray = gray
            return []

        new_pts = cv2.goodFeaturesToTrack(gray, mask=mask,
                                          **self.feature_params)
        trails = []
        if self.prev_pts is not None and len(self.prev_pts) > 0:
            curr_pts, status, _ = cv2.calcOpticalFlowPyrLK(
                self.prev_gray, gray, self.prev_pts, None,
                **self.lk_params
            )
            good_new = curr_pts[status == 1]
            good_old = self.prev_pts[status == 1]
            trails = list(zip(good_new, good_old))

        self.prev_gray = gray
        self.prev_pts  = new_pts
        return trails