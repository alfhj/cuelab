# cuelab

Cross-platform QLab alternative running in the terminal, built using Python and MPV

The program works by playing files in `cues/cues.txt` with a terminal file selector

Text cues start with `"` and are converted to PNG files using a white font on a black background and placed in `cues/temp`

### Requirements

- Python ≥ 3.8
- mpv (download [here](https://mpv.io/installation/) or use your preferred package manager)
- ffprobe (download [here](https://www.gyan.dev/ffmpeg/builds/) or use your preferred package manager)

### Installation

```
git clone https://github.com/alfhj/cuelab.git
cd cuelab
pip install -r requirements.txt
```
- Install `mpv` and `ffprobe` or drag their executable files into `bin`

### Usage

`python cuelab.py`

Cuelab will automatically convert text cues and metadata will be generated for other cues using `ffprobe`

Keyboard shortcuts:
- `UP`/`DOWN`: select previous/next cue
- `Space`: play the currently selected cue and advance selection
- `Esc`: stop playback
- `f`: toggle fullscreen
- `0`-`9`: show media on specified screen. Usually, 0 = primary screen, 1 = secondary screen etc.

### TODO

- [ ] Prevent mpv from taking focus when starting cuelab
- [ ] Support playback of multiple cues at the same time
- [ ] Option to rescale the output to a quadrangle to fit the projection surface
- [ ] Improve loading of first cue
- [ ] Implement a way to drag and drop files
- [X] Option to rescale the output to fit the projection surface
- [X] Show icon and length of each cue and update currently playing position

### Acknowledgements

Built using [rich](https://github.com/Textualize/rich), [python-readchar](https://github.com/magmax/python-readchar) and [python-mpv-jsonipc](https://github.com/iwalton3/python-mpv-jsonipc)

Test media are (c) copyright 2008, Blender Foundation / www.bigbuckbunny.org
