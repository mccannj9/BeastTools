#!/usr/bin/env python

from argparse import ArgumentParser, FileType
from sys import argv, exit

import Graph
import Parser

from Parser import thin_items


def formatNewick(graphs, outfile):

    for graph in graphs:
        outfile.write(graph.getNewick() + "\n")


def formatNEXUS(graphs, outfile):
    outfile.write("#nexus\n")
    outfile.write("begin trees;\n")
    for i,graph in enumerate(graphs):
        # outfile.write("tree TREE_" + str(i) + " = " + graph.getNewick() + "\n")
        print("tree TREE_" + str(i) + " = " + graph.getNewick(), file=outfile)
    outfile.write("end;\n")


def formatExpoTree(graphs, outfile):
    """Translates graph into something akin to the format used by Gabriel's expoTree."""

    if len(graphs) != 1:
        print("ExpoTree format applicable only to files containing a single graph.")
        exit(1)

    for node in sorted(graphs[0].getNodeList(), key=lambda node: node.height):

        # skip singletons:
        if len(node.children) == 1:
            continue

        if node.height > 0:
            if node.isLeaf():
                code = 0
            else:
                code = 1
            outfile.write("{} {}\n".format(node.height, code))

    outfile.write(str(graphs[0].getGraphOrigin()) + " 99\n")

formatFuncs = {
    "newick": formatNewick,
    "nexus": formatNEXUS,
    "expoTree": formatExpoTree}


if __name__ == '__main__':

    parser = ArgumentParser(description="Convert between different phylogenetic network description formats.")
    parser.add_argument(
        "-i", "--infiles", type=FileType('r'), nargs='+',
        help="Files containing graph data (Newick or NEXUS)."
    )
    parser.add_argument(
        "-o", "--outfile", type=FileType('w'),
        help="Output file to write."
    )
    parser.add_argument(
        "-f", "--format", type=str,
        help="Format of output file.  May be one of the following: " + ", ".join(formatFuncs.keys()))
    parser.add_argument(
        "-t", "--thin", type=int,
        help="Number of trees for final sample"
    )
    parser.add_argument(
        "-b", "--burnin", type=int,
        help="Number of trees to burn"
    )
    # Parse arguments
    # args = parser.parse_args(argv[1:])
    args = parser.parse_args()

    trees_list = []
    flatten = lambda l: [item for sublist in l for item in sublist]
    # Parse graph file
    for treefile in args.infiles:
        graphs = Parser.readFile(treefile)
        if args.thin == 0:
            pass
        else:
            graphs = thin_items(graphs, args.thin, args.burnin)

        if len(graphs) == 0:
            print("Skipping empty graph file.")
            exit(0)

        trees_list.append(graphs)
        print("Length tree list = %s" % len(trees_list))
    all_trees = flatten(trees_list)
    # formatNEXUS(all_trees, args.outfile)
    if args.format in formatFuncs.keys():
        formatFuncs[args.format](all_trees, args.outfile)
    else:
        print("Unrecognized format '{}'".format(args.format))
