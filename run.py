import argparse
from src import application, convert_cues
from src.utils import get_binaries

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cuelab")
    parser.add_argument("--convert-text", action="store_true", help="Convert text cues to PNG images")
    args = parser.parse_args()
    
    get_binaries()
    if args.convert_text == True:
        convert_cues.convert()
    application.start()
