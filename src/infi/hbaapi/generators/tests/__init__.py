__import__("pkg_resources").declare_namespace(__name__)

import unittest
import mock

from .. import Generator

class UnavailableGenerator(Generator):
    @classmethod
    def is_available(cls):
        return False

class EmptyGenerator(Generator):
    @classmethod
    def is_available(cls):
        return True

    def iter_ports(cls):
        for nothing in []:
            yield

def get_list_of_generators():
    return [UnavailableGenerator, EmptyGenerator]