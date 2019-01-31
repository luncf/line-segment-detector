# Vision Module

This is the vision module used for the RoboCup Humanoid League. The vision can be used to detect various features on
the soccer field, such as lines and a ball.

## Getting Started

### Requirements

This module has the following requirements:

1. OpenCV 3.2+
2. Python 2.7

### Features

This module has three major features:

1. Filtering out the background
2. Detecting a solid colour ball
3. Detecting line segments and determining parts of the field

### How to run the project

```python
cd <project root directory>
python vision/src/vision.py
```

The vision can be tuned via the GUI. To start, select the desired object to tune using the `Object` trackbar in
the `debug` window. Change the average colour space value by selecting a range in the `camera` window. Modify the
threshold values via the other three trackbars.

### Configuration

This module has a configuration file under `config/configuration.json`.
Use this file to tune the vision based on the environment it is used in.

The configuration file gives the ability to change the setting of the
camera image and the detected features.

Camera:

- camera_index: the index of the video camera device (default: 0)
- resized_frame_height: height of the resized frame, useful
    to reduce processing load (default: 320)

Ball:

- min_area: minimum area of contours (default: 20)
- max_area: maximum area of contours (default: 4000)
- output_ball_colour: line colour of the ball in the output frame (default: green)
- threshold: value added to calculate the min/max range of the colour space (default: [0, 0, 0])
- value: average value of the selected range in the colour space (default: [0, 0, 0])

Field:

- min_area: smallest contour area to consider as part of the field (default: 1500)
- threshold: value added to calculate the min/max range of the colour space (default: [0, 0, 0])
- value: average value of the selected range in the colour space (default: [0, 0, 0])

Lines:

- corner_max_distance_apart: maximum distance between lines to be consider as a corner (default: 20)
- max_distance_apart: maximum distance between line segments to be considered as a line (default: 20)
- max_width: maximum width of each line (default: 20)
- min_length: minimum length of each line segment (default: 20)
- output_boundary_line_colour: line colour of the boundary lines in the output frame (default: blue)
- output_center_line_colour: line colour of the center line in the output frame (default: cyan)
- output_goal_area_line_colour: line colour of the goal area lines in the output frame (default: magenta)
- output_undefined_line_colour: line colour of any lines that can not be classified (default: red)
- threshold: value added to calculate the min/max range of the colour space (default: [0, 0, 0])
- value: average value of the selected range in the colour space (default: [0, 0, 0])

## Future additions:

- [ ] Differentiating the center line
- [ ] Hotswap colour space
- [ ] Converting GUI to QT

