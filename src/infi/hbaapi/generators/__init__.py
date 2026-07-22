__import__("pkg_resources").declare_namespace(__name__)


from logging import getLogger
logger = getLogger(__name__)


class Generator(object):
    def __init__(self):
        object.__init__(self)

    def iter_ports(self):
        raise NotImplementedError

    @classmethod
    def is_available(cls):
        raise NotImplementedError

class CompositeGenerator(Generator):
    def __init__(self):
        self._children = []

    def iter_ports(self):
        for child_class in self._children:
            try:
                child = child_class()
                for port in child.iter_ports():
                    yield port
            except Exception:
                logger.exception(
                    "HBAAPI generator %s raised an exception; "
                    "skipping the remaining output from this generator",
                    child_class.__name__,
                )
                continue

    @classmethod
    def is_available(cls):
        return True

    def add_generator(self, generator):
        if generator not in self._children:
            self._children.append(generator)

    def remove_generator(self, generator):
        self._children.remove(generator)

    def iter_generators(self):
        for generator in self._children:
            yield generator()

def get_list_of_generators():
    from .hbaapi import HbaApi
    from .sysfs import Sysfs
    return [HbaApi, Sysfs]
