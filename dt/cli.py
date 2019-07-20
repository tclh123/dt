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

    suite = Suite.load_from_yaml('redis')
    logger.info(suite)
    suite.run(timeout=args.timeout, dry_run=args.dry_run)


def list_(args):
    resource_cls = Chart if args.resource == 'chart' else Suite
    [print(e) for e in resource_cls.list_yaml()]


def main(args=None):
    '''
    Examples:

    $ dt run redis -t 10 -d
    '''
    parser = argparse.ArgumentParser(
        epilog=main.__doc__,
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-v', '--verbose', action='count', default=0, help='verbose.')

    subparsers = parser.add_subparsers(help='Sub commands', dest='subparsers', required=True)

    run_parser = subparsers.add_parser('run', help='run a test suite')
    run_parser.add_argument('suite', help='the suite to run')
    run_parser.add_argument('-t', '--timeout', help='run timeout, default is 0 means infinite', default=0, type=int)
    run_parser.add_argument('-d', '--dry-run', action='store_true', help='dry run mode, will not start cluster')
    run_parser.set_defaults(func=run)

    list_parser = subparsers.add_parser('list', help='list resource')
    list_parser.add_argument('resource', choices=['chart', 'suite'], help='resource to list')
    list_parser.set_defaults(func=list_)

    args = parser.parse_args(args)

    level = logging.INFO - args.verbose * 10
    logging.basicConfig(level=level,
                        format='%(asctime)s %(name)s %(levelname)s %(message)s')

    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
