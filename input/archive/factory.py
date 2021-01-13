from Utilities.base import FactoryType
from typing import Union
import json


class ArchiveFactory(FactoryType):
    """ FactoryType object to assist future updates and implementation. """

    def register(self, key: Union[str, None], archiver: object):
        super(ArchiveFactory, self).__setitem__(key, archiver)

    def set_config(self, config: dict):
        self.data = config

    def __str__(self) -> str:
        """ String in json format """
        def _mapper(kv):
            k, v = kv
            return k, {'name': v.__class__.__name__, 'id': id(v)}

        dict_gen = map(_mapper, self.data.items())
        return json.dumps(dict(dict_gen), indent=2)


factory = ArchiveFactory()
