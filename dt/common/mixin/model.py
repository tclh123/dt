from datetime import datetime


class Model:
    __fields__ = None

    def __init__(self, *a, **kw):
        if not self.__fields__:
            self.__fields__ = kw.keys()
        for k in self.__fields__:
            setattr(self, k, kw.get(k))

    @property
    def _fields(self):
        return self.__fields__ or self.__dict__.keys()

    def __str__(self):
        attrs = []
        for k in sorted(self._fields):
            v = getattr(self, k)
            v = '"%s"' % str(v) if type(v) in (str, datetime) else str(v)
            attrs.append('%s=%s' % (k, v))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def to_dict(self):
        vs = [getattr(self, k) for k in self._fields]
        return {k: v.to_dict() if isinstance(v, Model) else v for k, v in zip(self._fields, vs)}
