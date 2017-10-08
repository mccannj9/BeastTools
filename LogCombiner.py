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


def prepare_chain(infile, outfile, comb_log_state, start, thin):

    # account for header line and initial sample i.e. Iter 0
    counter = 0
    for line in infile:
        if line.startswith('#'):
            continue
        if counter >= start:
            break
        counter += 1

    counter = 1
    for line in infile:
        if counter % thin == 0:
            line = line.rstrip().split()
            line[0] = str(comb_log_state)
            line = "\t".join(line)
            print(line, file=outfile)
        counter += 1
        comb_log_state += 1

    return comb_log_state


def get_header(log):
    f = open(log)
    for line in f:
        if not(line.startswith('#')):
            print(line)
            break
    f.close()
    return line.rstrip()


def main():
    import argparse as ap
    import sys

    parser = ap.ArgumentParser(description='Combine Beast Logs')
    parser.add_argument(
        '-l', '--logs', nargs='+', type=str
    )
    parser.add_argument(
        '-b', '--burnin', type=int, default=0
    )
    parser.add_argument(
        '-t', '--thin', type=int, default=1
    )
    parser.add_argument(
        '-o', '--output', type=ap.FileType(mode='w'), default=sys.stdout
    )
    args = parser.parse_args()

    header = get_header(args.logs[0])
    print(header, file=args.output)

    comb_log_state = 0
    for log in args.logs:
        # samples = count_samples(log)
        # print(samples)
        f = open(log)
        comb_log_state = prepare_chain(f, args.output, comb_log_state, args.burnin, args.thin)
        f.close()


if __name__ == '__main__':
    main()

