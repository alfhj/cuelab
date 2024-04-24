CUES_DIR = "cues"
OUTPUT_DIR = f"{CUES_DIR}/temp"
CUES_FILE = f"{CUES_DIR}/cues.txt"
METADATA_FILE = f"{OUTPUT_DIR}/metadata.json"
BINARY_DIR = "bin"
WIDTH = 1920  # text cue image width
HEIGHT = 1080  # text cue image height
FONT = "tahoma.ttf"
FONT_SIZE = 72  # px
FONT_POSITION = 2  # percent from top
LINE_SPACING = 1.15
CUE_LIST_MIDDLE = 50  # percent from top where current cue should be
NUM_INSTANCES = 3  # max number of simultaneous cues

# Warp mode: transform output
#   rect = rectangle - specify width, height, x, y
#       If only width is specified: scale the output image by amount
#       If width and height is specified: scale the output width and height independently
#       x and y: move image along X and Y by a fraction relative to image size
#       Examples:
#           [1, 1, 0, 0]: leave image as is
#           [0.8]: scale image to 80%
#           [0.5, 0.5, 0.5, -0.5]: scale image to 50% and put in the top right corner
#   quad = quadrangle - specify a list of four (x, y) coordinates to stretch each corner to the new points
#   none = disable warping
WARP_MODE = "none"
WARP_PARAMS = [1.0, 1.0, 0.0, 0.0]
