import os
import logging

from dt.common.mixin.model import Model
from dt.common.mixin.yaml import YamlMixin
from dt.config import CHARTS_PATHS, TILLER_HOST

from pyhelm.chartbuilder import ChartBuilder
from pyhelm.tiller import Tiller


logger = logging.getLogger(__name__)


class Chart(Model, YamlMixin):
    __fields__ = [
        'name',
        'source',
        'rbac',
        'crd',
        'sub',
    ]

    __yaml_dirs__ = CHARTS_PATHS

    def __init__(self, **kw):
        super().__init__(**kw)
        if self.sub:
            self.sub = [self.__class__(**s) for s in self.sub]

    @classmethod
    def get_tiller(self):
        return Tiller(TILLER_HOST)

    def apply_extra_yaml(self, filepath):
        if not filepath:
            return True
        # TODO: read yaml, invoke k8s api
        return True

    def install(self, namespace, dry_run=False, name=None, values=None, wait=None):
        if self.sub:
            return [c.install(namespace, dry_run, name, values[i], wait) for i, c in enumerate(self.sub)]

        try:
            chart = ChartBuilder(dict(name=self.name, source=self.source))
            res = self.get_tiller().install_release(chart.get_helm_chart(), dry_run=dry_run, namespace=namespace,
                                         name=name, values=values, wait=wait)

            if not self.apply_extra_yaml(self.crd):
                logger.error('Failed to apply crd %s', self.crd)
            if not self.apply_extra_yaml(self.rbac):
                logger.error('Failed to apply rbac %s', self.rbac)
        except Exception:
            raise
        finally:
            chart.source_cleanup()

        return res

    def uninstall(self, name):
        return self.get_tiller().uninstall_release(name)
