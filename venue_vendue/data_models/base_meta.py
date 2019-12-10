from inflection import underscore
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import instrument_declarative
from sqlalchemy.ext.declarative import declared_attr


class BaseMeta(type):

    classes = set()

    def __init__(cls, classname, bases, dict_):
        klass = type.__init__(cls, classname, bases, dict_)
        if 'metadata' not in dict_:
            BaseMeta.classes.add(cls)
        return klass


class Base(object, metaclass=BaseMeta):

    metadata = MetaData()

    def __init__(self, **kw):
        for k in kw:
            setattr(self, k, kw[k])

    @declared_attr
    def __tablename__(cls):
        return underscore(cls.__name__)

    @classmethod
    def configure(cls, *klasses):
        registry = {}
        for bmc in BaseMeta.classes:
            instrument_declarative(bmc, registry, cls.metadata)

    def __repr__(self):
        id_ = getattr(self, 'id', False)
        id_ = ' id: {}'.format(id_) * bool(id_)
        name = getattr(self, 'name', False)
        name = ' name: {}'.format(name) * bool(name)
        return '<{}{}{}>'.format(self.__class__.__name__, id_, name)
