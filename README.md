Overview
========
A cross-platform Python binding to HBAAPI libraries, providing read-only access to the HBA attributes and remote ports.

Usage
-----

Here's an example on how to use this module:

```python
from infi.hbaapi import get_ports_collection
collection = get_ports_collection()
local_port = collection.get_ports()[0]
remote_port = local_port.discovered_ports
```

Checking out the code
=====================

This project uses buildout, and git to generate setup.py and __version__.py.
In order to generate these, run:

    python -S bootstrap.py -d -t
    bin/buildout -c buildout-version.cfg
    python setup.py develop

In our development environment, we use isolated python builds, by running the following instead of the last command:

    bin/buildout install development-scripts

