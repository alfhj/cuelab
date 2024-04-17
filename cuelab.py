import logging
from src import application, convert_cues
from src.utils import get_binaries, log, generate_dummy_cues

if __name__ == "__main__":
    logging.basicConfig(filename="mpv.log", filemode="a", format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s", datefmt="%H:%M:%S", level=logging.DEBUG)
    logging.getLogger("main").addHandler(logging.StreamHandler())
    log(f"--- Starting cuelab ---", __name__)

    get_binaries()
    cues = convert_cues.convert()
    #cues = generate_dummy_cues()
    application.start(cues)
