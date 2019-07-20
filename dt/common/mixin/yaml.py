import os
import yaml
import logging

from dt.config import CLUSTER_DOMAIN

logger = logging.getLogger(__name__)


class YamlMixin:
    __fields__ = None
    __yaml_dirs__ = None

    @property
    def _fields(self):
        return self.__fields__ or self.__dict__.keys()

    @classmethod
    def from_yaml(cls, s):
        logger.debug('get yaml:\n%s', s)
        try:
            obj = yaml.safe_load(s)
        except Exception:
            logger.exception('Failed to load %s from_yaml: ', cls.__name__)
            return
        if not isinstance(obj, dict):
            logger.error('Failed to load %s from_yaml: obj is not a dict: %s', cls.__name__, obj)
            return
        params = {k: obj.get(k) for k in cls.__fields__} if cls.__fields__ else obj
        return cls(**params)

    def to_yaml(self):
        params = {k: getattr(self, k) for k in self._fields}
        return yaml.safe_dump(params)

    @classmethod
    def load_yaml(cls, filename):
        assert cls.__yaml_dirs__
        filename = filename + '.yaml' if not filename.endswith('.yaml') else filename
        for path in cls.__yaml_dirs__:
            filepath = os.path.join(path, filename)
            logger.debug('%s.load_yaml %s', cls.__class__.__name__, filepath)
            if os.path.exists(filepath):
                content = open(filepath, 'r', encoding='utf-8').read()
                # HACK: replace some placehold with config value
                content = content.replace('__CLUSTER_DOMAIN__', CLUSTER_DOMAIN)
                return content
        return ''

    @classmethod
    def load_from_yaml(cls, filename):
        return cls.from_yaml(cls.load_yaml(filename))

    @classmethod
    def list_yaml(cls):
        return [entry[:-len('.yaml')] if entry.endswith('.yaml') else entry
                for path in cls.__yaml_dirs__
                for entry in os.listdir(path)
                if entry != 'README.md' and not entry.startswith('__')]
