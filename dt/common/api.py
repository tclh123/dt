import os
import json
import logging

from dt.common.mixin.model import Model
from dt.common.chart import Chart
from dt.common.util import random_string
from dt.config import RELEASE_NAME_PREFIX, NAMESPACE_PREFIX, RANDOM_SUFFIX_LEN, HISTORY_RECORDS_SAVE_PATH

logger = logging.getLogger(__name__)


class DtApi(Model):
    __fields__ = [
        'chart',
        'values',
        'release_name',
        'namespace',
    ]

    def __init__(self, **kw):
        super().__init__(**kw)
        self.release_name = self.gen_release_name(self.chart.name)
        self.namespace = self.gen_release_name(self.chart.name)

    # TODO: save record
    # comsumed by checker
    def record(self, records):
        save_path = os.path.join(HISTORY_RECORDS_SAVE_PATH, self.gen_record_filename(self.chart.name))
        with open(save_path, 'w') as f:
            f.write(json.dumps(records, indent=4))
        logger.info('write records to %s', save_path)
        return True

    @classmethod
    def gen_record_filename(cls, chart_name):
        return '-'.join([chart_name, random_string(RANDOM_SUFFIX_LEN)])

    @classmethod
    def gen_release_name(cls, chart_name):
        return '-'.join([RELEASE_NAME_PREFIX, chart_name, random_string(RANDOM_SUFFIX_LEN)])

    @classmethod
    def gen_namespace(cls, chart_name):
        return '-'.join([NAMESPACE_PREFIX, chart_name, random_string(RANDOM_SUFFIX_LEN)])
