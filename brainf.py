import argparse

from brainf import Interpreter


def get_args():
    parser = argparse.ArgumentParser(description="Brainfuck interpreter written in Python 3.7. Pass a file path to the interpreter and it will run it. "
                                                 "If no file is provided, it will run an interactive Brainfuck mode.")
    parser.add_argument('file', nargs='?', default='.', help='Path to .bf file to interpret.')
    parser.add_argument('--output', '-o', help='File where the program output will be saved.')
    parser.add_argument('--size', '-s', type=int, default=30_000, help="Memory size of the byte table.")
    return parser.parse_args()


def main():
    args = get_args()
    brainf_i = Interpreter(args.size)
    if args.output:
        brainf_i.set_file_out(args.output)
    if args.file != '.':
        brainf_i.interpret_file(args.file)


if __name__ == '__main__':
    main()
