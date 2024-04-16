#import argparse
import logging
from src import application, convert_cues
from src.utils import get_binaries, log

if __name__ == "__main__":
    #parser = argparse.ArgumentParser(description="Cuelab")
    #parser.add_argument("--convert-text", action="store_true", help="Convert text cues to PNG images")
    #args = parser.parse_args()

    logging.basicConfig(filename="mpv.log", filemode="a", format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s", datefmt="%H:%M:%S", level=logging.DEBUG)
    logging.getLogger("main").addHandler(logging.StreamHandler())
    log(f"--- Starting cuelab ---", __name__)

    get_binaries()
    #if args.convert_text == True:
    metadata = convert_cues.convert()
    application.start(metadata["cues"])
