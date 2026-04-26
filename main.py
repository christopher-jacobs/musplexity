import argparse
from musiplexity import musiplexity

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--wav_file', type=str, help="Wav file that will be processed", required=True)
    parser.add_argument('-v', '--visualize', action="store_true")
    args = parser.parse_args()

    musiplexity(args)