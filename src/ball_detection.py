import cv2 as cv

from cv_mat import CVMat


class BallDetector(CVMat):

    def __init__(self, frame):
        CVMat.__init__(self, frame=frame)

    def extract_ball(self, thresh_lb, thresh_ub):
        self.extract_object(thresh_lb=thresh_lb, thresh_ub=thresh_ub, field=None, kernel_size=3)

    def approx_poly_dp(self, min_area=20, max_area=4000):
        # Find contours
        _, contours, hierarchy = cv.findContours(self.frame, mode=cv.RETR_EXTERNAL, method=cv.CHAIN_APPROX_SIMPLE)

        center = None
        radius = None
        _max_area = -1

        # Extract the best contour that fits the min/max conditions
        # Find circle using Approx Poly DP
        if contours:
            best_contour = max(contours, key=cv.contourArea)

            if best_contour is not None and min_area <= cv.contourArea(best_contour) <= max_area:
                approx = cv.approxPolyDP(best_contour, 0.005 * cv.arcLength(best_contour, True), True)
                center, radius = self.minimum_enclosing_circle(approx)

        return center, radius, _max_area

    @staticmethod
    def minimum_enclosing_circle(contour):
        # Find the smallest circle in a given contour
        (x, y), radius = cv.minEnclosingCircle(contour)

        return (int(round(x)), int(round(y))), int(round(radius))

