from dt.common.mixin.model import Model


class Record(Model):
    __fields__ = [
        'input',
        'output',
        'call_time',
        'return_time',
    ]
