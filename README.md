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

Run the following:

    easy_install -U infi.projector
    projector devenv build

Python 3
========

Python 3 support is experimental at this stage.
