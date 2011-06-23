__import__("pkg_resources").declare_namespace(__name__)

from sys import argv

def _print_hbaapi_example():
    import json
    from infi.hbaapi import get_ports_collection
    print "from infi.hbaapi import Port, PortStatistics"
    print "import json"
    print "example = json.loads(\"\"\"",
    print json.dumps([port for port in get_ports_collection().get_ports()], sort_keys=True, indent=4)
    print "\"\"\")"
    print "ports = [Port().update_not_none_values(item) for item in example]"

def hbaapi_mock(argv=argv):
    from os.path import exists, join, sep, dirname, pardir, abspath
    MOCK_ROOT_FS = abspath(join(dirname(__file__), pardir, pardir, pardir, pardir, 'mock_fs'))
    import infi.hbaapi.generators.sysfs
    infi.hbaapi.generators.sysfs.ROOT_FS = MOCK_ROOT_FS
    _print_hbaapi_example()

def hbaapi_real(argv=argv):
    _print_hbaapi_example()

def main(argv=argv):
    print 'hello world'

