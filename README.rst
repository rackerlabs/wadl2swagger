***********************
wadl2swagger |PyPI|
***********************

wadl2swagger is a command line tool for converting WADL_ description of an API into Swagger_. It's intended to work with generic WADL documents as much as possible, but some of the conversion is mapped to conventions used in OpenStack WADL rather concepts defined in the WADL standard itself.

============
Installation
============

wadl2swagger can be installed (and updated) from PyPI using `pip`_:

.. code-block:: bash

    $ pip install --upgrade wadl2swagger


Conversely, it can be uninstalled using `pip`_ as well.

.. code-block:: bash

    $ pip uninstall wadl2swagger


=====
Usage
=====

wadl2swagger provides two utilities. The ``wadlcrawler`` utility can be used to fetch WADL files off a website. For example:

.. code-block:: bash

    $ wadlcrawler http://api.rackspace.com/wadls/
    INFO:root:Downloading http://api.rackspace.com/wadls/ to wadls/OS-KSADM-admin.wadl
    INFO:root:Downloading http://api.rackspace.com/wadls/ to wadls/RAX-AUTH.wadl
    INFO:root:Downloading http://api.rackspace.com/wadls/ to wadls/RAX-KSKEY-admin.wadl
    INFO:root:Downloading http://api.rackspace.com/wadls/ to wadls/autoscale.wadl
    INFO:root:Downloading http://api.rackspace.com/wadls/ to wadls/cbd-devguide.wadl
    INFO:root:Downloading http://api.rackspace.com/wadls/ to wadls/cloud_monitoring.wadl
    INFO:root:Downloading http://api.rackspace.com/wadls/ to wadls/cq-devguide.wadl
    ...

Now that you have a set of WADL files, you can use wadl2swagger to convert them:

.. code-block:: bash

    $ wadl2swagger --autofix wadls/*.wadl --swagger-dir swagger/
    Saving swagger to swagger/OS-KSADM-admin.yaml
    Saving swagger to swagger/RAX-AUTH.yaml
    Saving swagger to swagger/RAX-KSKEY-admin.yaml
    Saving swagger to swagger/autoscale.yaml
    Saving swagger to swagger/cbd-devguide.yaml
    Saving swagger to swagger/cq-devguide.yaml
    ...

===
Options
===

See ``wadlcrawler -h`` and ``wadl2swagger -h`` for a full list of options. Some important options are below.

``--autofix``
----------------

Tells wadl2swagger to detect and attempt to fix common problems, like inferring a default value for a required Swagger concept that is optional and not specified in one of the WADLs. If you don't use this option than wadl2swagger may fail until you clean up your WADL files.

``--wadl-dir WADL_DIR``
----------------

The directory to save WADL files to when downloading via wadlcrawler.

``--swagger-dir SWAGGER_DIR``
----------------

The directory to save Swagger files to when converting via wadl2swagger.

============
Contributing
============

See `CONTRIBUTING.rst`_.

=======
License
=======

wadl2swagger is licensed under the `Apache License`_.


.. |PyPI| image:: http://img.shields.io/pypi/v/wadl2swagger.svg?style=flat
          :alt: PyPI Version
          :target: https://pypi.python.org/pypi/wadl2swagger/

.. _pip: http://www.pip-installer.org/en/latest/index.html
.. _WADL: http://www.w3.org/Submission/wadl/
.. _Swagger: http://swagger.io
.. _CONTRIBUTING.rst: https://github.com/rackerlabs/wadl2swagger/blob/master/CONTRIBUTING.rst
.. _Apache License: https://github.com/rackerlabs/wadl2swagger/blob/master/LICENSE
