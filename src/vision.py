import cv2 as cv

from ball_detection import BallDetector
from cv_mat import CVMat
from field_objects import Ball, Lines, Field
from line_segment_detection import LineSegmentDetector
import opencv_gui as gui
from configuration import Configuration


def get_region_colour_space_values_cb(event, x, y, _frame):
    global colour_space_roi, configuration, selected_object

    # Retrieve average values for colourspace
    if event == cv.EVENT_LBUTTONDOWN:
        colour_space_roi = (x, y)
    elif event == cv.EVENT_LBUTTONUP:
        roi_mean = cv.mean(_frame[colour_space_roi[1]:y, colour_space_roi[0]:x])
        selected_object.set_colour_space_value(roi_mean[:-1])
        configuration.update(selected_object.name, selected_object.export_configuration())
        colour_space_roi = None


def set_colour_space_threshold_cb(threshold):
    global selected_object, configuration

    # Change colourspace threshold for selected object
    selected_object.set_colour_space_threshold(threshold=threshold)
    configuration.update(selected_object.name, selected_object.export_configuration())


def switch_selected_object_cb(value):
    global selected_object, field_objects_list

    # Switch the tuning object
    selected_object = field_objects_list.values()[value]
    colour_space_threshold = selected_object.threshold
    gui.set_colour_space_threshold_trackbar_position(colour_space_threshold)


def track_ball():
    global ball, ball_mat, output

    # Find the ball using Approx Poly DP
    ball_center, ball_radius, ball_area = ball_mat.approx_poly_dp(min_area=ball.min_area, max_area=ball.max_area)

    # Draw ball if found
    if ball_center and ball_radius and ball_area:
        cv.circle(output.frame, center=ball_center, radius=ball_radius, color=ball.output_colour, thickness=2)


def draw_field():
    global lines, lines_mat, output

    # Find the lines and corners, classify each line
    lines_mat.lsd(max_distance_apart=lines.max_distance_apart, min_length=lines.min_length)
    lines_mat.find_corners(max_distance_apart=lines.corner_max_distance_apart)
    field_lines = lines_mat.classify_lines()

    # Draw lines if found
    if field_lines:
        for line_type in field_lines.keys():
            if line_type == 'boundary':
                colour = lines.output_boundary_colour
            elif line_type == 'goal_area':
                colour = lines.output_goal_area_colour
            elif line_type == 'center':
                colour = lines.output_center_colour
            else:
                colour = lines.output_undefined_colour

            for line in field_lines[line_type]:
                pt1, pt2 = line.to_cv_line()
                cv.line(output.frame, pt1=pt1, pt2=pt2, color=colour, thickness=3)


if __name__ == '__main__':
    # Load configurations
    configuration = Configuration()
    configuration.load()
    colour_space_roi = None

    # Initialize objects and load configurations
    field = Field(configuration=configuration.config['field'])
    lines = Lines(configuration=configuration.config['lines'])
    ball = Ball(configuration=configuration.config['ball'])
    field_objects_list = {'field': field, 'lines': lines, 'ball': ball}
    selected_object = field

    # Create GUI and set callbacks
    gui.set_mouse_cb('camera', lambda event, x, y, flags, params:
                     get_region_colour_space_values_cb(event, x, y, original.colour_space_frame))
    gui.create_trackbar(gui.DEBUG_WINDOW_NAME, trackbar_name='Object', default_value=0,
                        max_value=len(field_objects_list.values()) - 1, callback=switch_selected_object_cb)
    gui.create_colour_space_threshold_trackbar(selected_object.threshold, set_colour_space_threshold_cb)

    # Open camera device
    cap = cv.VideoCapture(configuration.config['camera_index'])
    FRAME_HEIGHT = configuration.config['resized_frame_height']

    while cv.waitKey(1) != 27:
        ret_code, raw_image = cap.read()
        if raw_image.data:
            original = CVMat(raw_image, height=FRAME_HEIGHT)

            # Create an output frame from a clone of the original
            output = original.clone()

            # Extract background from soccer field
            field_mat = original.clone()
            field_mat.background_mask(thresh_lb=field.lower_bound, thresh_ub=field.upper_bound,
                                      min_area=field.min_area, line_width=lines.max_width)
            if selected_object == field_objects_list['field']:
                gui.show_debug_window(field_mat.frame, field.name)
            output.frame = cv.bitwise_and(output.frame, output.frame, mask=field_mat.frame)

            # Extract lines from soccer field and detect lines using LSD
            lines_mat = LineSegmentDetector(frame=original.frame)
            lines_mat.extract_lines(thresh_lb=lines.lower_bound, thresh_ub=lines.upper_bound, field=field_mat.frame)
            if selected_object == field_objects_list['lines']:
                gui.show_debug_window(lines_mat.frame, lines.name)
            draw_field()

            # Extract ball from soccer field and detect ball using ApproxPolyDP
            ball_mat = BallDetector(frame=original.frame)
            ball_mat.extract_ball(thresh_lb=ball.lower_bound, thresh_ub=ball.upper_bound)
            if selected_object == field_objects_list['ball']:
                gui.show_debug_window(ball_mat.frame, ball.name)
            track_ball()

            # Display GUI windows
            gui.show('camera', original.frame)
            gui.show('output', output.frame)

    # Clean up
    gui.teardown()
    cap.release()
