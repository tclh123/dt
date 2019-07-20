import os

DEBUG = DEVELOP_MODE = False

PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# TODO: config examples
CHARTS_PATHS = [os.path.join(PROJECT_ROOT, 'dtcharts')]
SUITE_PATHS = [os.path.join(PROJECT_ROOT, 'dtsuite')]

TILLER_HOST = '127.0.0.1'
CLUSTER_DOMAIN = 'cluster.local'

RELEASE_NAME_PREFIX = 'dtesting'
NAMESPACE_PREFIX = 'dtesting'
RANDOM_SUFFIX_LEN = 7

HISTORY_RECORDS_SAVE_PATH = os.path.join(PROJECT_ROOT, 'history_records')
CHECKER_PATH = os.path.join(PROJECT_ROOT, 'bin')
DEFAULT_CHECKER_BIN = os.path.join(CHECKER_PATH, 'checker-bank')


try:
    from local_config import *   # NOQA
except ImportError as e:
    print('Import from local_config failed, %s' % str(e))
