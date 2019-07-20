'''
DT is a distributed system testing framework for cloud native.
'''

import sys
import logging
import argparse

import pyhelm

from dt.common.chart import Chart
from dt.common.suite import Suite

logger = logging.getLogger(__name__)


def run(args):
    logger.info('run')

    # chart_name = 'tidb'
    # chart = Chart.from_yaml(Chart.load_yaml(chart_name))
    # print(chart)

    suite = Suite.from_yaml(Suite.load_yaml('redis/suite'))
    print(suite)
    suite.run(timeout=args.timeout)


def main(args=None):
    '''
    Examples:

    $ dt run -vvv
    '''
    parser = argparse.ArgumentParser(
        epilog=main.__doc__,
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-v', '--verbose', action='count', default=0, help='verbose.')

    subparsers = parser.add_subparsers(help='Sub commands', dest='subparser', required=True)

    run_parser = subparsers.add_parser('run', help='run a test suite')
    run_parser.add_argument('-t', '--timeout', help='run timeout, default is 0 means infinite', default=0, type=int)
    run_parser.set_defaults(func=run)

    args = parser.parse_args(args)

    level = logging.INFO - args.verbose * 10
    logging.basicConfig(level=level,
                        format='%(asctime)s %(name)s %(levelname)s %(message)s')

    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
