import argparse
import logging

from weather.moisture import get_current_moisture

from reddit.crawler import acquire_meme

def read_arguments() -> dict:
    """
    Reads in optional arguments provided

    Returns:
        (argparse.Namespace) : Contains the provided args
    """
    parser = argparse.ArgumentParser(description=("Let's make some fucking memes"))
    parser.add_argument('-l', '--location', nargs=1, required=False, default='Vancouver', help='Enter a location')

    return parser.parse_args()


if __name__ == "__main__":
    """
    main
    """
    logging.basicConfig(level=logging.INFO)
    args = read_arguments()

    current_moisture = get_current_moisture(location=args.location[0])
    acquire_meme(moisture=current_moisture)