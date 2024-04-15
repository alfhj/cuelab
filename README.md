# cuelab
Cross-platform QLab alternative using the terminal, built using Python and MPV

The program works by playing files in `cues/cues.txt` with a terminal file selector

Text cues start with `"` and are converted to PNG files using a white font on a black background and placed in `cues/temp`

### Installation
- Install `python`
- Install `mpv` or drag a `mpv` executable into `bin`

### Usage

`python run.py`

To convert text cues for the first time: `python run.py --convert-text`. This must be run when text cues are changed. The program will assume the PNG files in `cues/temp` are in the same order as in `cues/cues.txt`