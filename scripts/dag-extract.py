#!/usr/bin/env python3

# Copyright IBM Inc. 2022. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# Author(s):
#   Vassilis Vassiliadis


import argparse
import json
import logging

import experiment.model.graph
import experiment.model.storage

LOG_FORMAT = '%(levelname)-9s %(name)-30s: %(funcName)-20s %(asctime)-15s: %(message)s'


def parser_prep() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='dag-extract',
        description='Parses the DAG of a virtual experiment that '
                    'uses the Simulation Toolkit For Scientific Discovery (ST4SD)',
        epilog='Visit https://github.com/st4sd/ for more')

    parser.add_argument('--manifest', dest="manifest", metavar="PATH_TO_MANIFEST_FILE", default=None,
                        help="Optional path to manifest YAML file to use when setting up package directory from a "
                             "FlowIR YAML file. The manifest should contain a dictionary, with "
                             "targetFolder: sourceFolder entries.")

    parser.add_argument("package", metavar="PATH_TO_PACKAGE", help="Path to FlowIR package (dir/filename)")

    parser.add_argument("-l", "--logLevel", type=int, default=20, help="The level of logging. Default %default",
                        metavar="LOG_LEVEL")

    return parser


def main():
    parser = parser_prep()
    args = parser.parse_args()
    logging.basicConfig(format=LOG_FORMAT)
    log = logging.getLogger()
    log.setLevel(args.logLevel)

    pkg = experiment.model.storage.ExperimentPackage.packageFromLocation(
        args.package, args.manifest, validate=False, createInstanceFiles=False)

    wgraph = experiment.model.graph.WorkflowGraph.graphFromPackage(pkg)

    dependencies = {x: list(wgraph.graph.predecessors(x)) for x in wgraph.graph.nodes}

    log.info("Dependencies are (in stdout):")

    print(json.dumps(dependencies, indent=2))


if __name__ == "__main__":
    main()
