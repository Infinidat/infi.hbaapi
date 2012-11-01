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

This project uses buildout and infi-projector, and git to generate setup.py and __version__.py.
In order to generate these, first get infi-projector:

    easy_install infi.projector

    and then run in the project directory:

        projector devenv build
