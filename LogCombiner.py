#! /usr/bin/env python

def blocks(files, size=65536):
    while True:
        b = files.read(size)
        if not b: break
        yield b

def count_samples(filename):
    f = open(filename)
    lines = 0
    hashes = 0
    for bl in blocks(f):
        lines += bl.count("\n")
        hashes += bl.count("#")
    f.close()
    # exclude header and initial state, hence -2
    return lines-hashes-2

def main():
    import argparse as ap

    parser = ap.ArgumentParser(description='Combine Beast Logs')
    parser.add_argument(
        '-l', '--logs', nargs='+', type=str
    )
    parser.add_argument(
        '-b', '--burnin', type=int, default=10
    )
    parser.add_argument(
        '-t', '--thin', type=int, default=0
    )
    args = parser.parse_args()


    for log in args.logs:
        samples = count_samples(log)
        print(samples)


if __name__ == '__main__':
    main()
