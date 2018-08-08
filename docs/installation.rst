Installation
=======================================
.. code-block:: bash
   :caption: installation
   :name: installation
    # using pypi
    sudo -H python -m pip install rawsocketpy

    # for development
    git clone https://github.com/AlexisTM/rawsocket_python
    cd rawsocket_python
    sudo python pip . -e

    # manually
    git clone https://github.com/AlexisTM/rawsocket_python
    sudo python setup.py install


`gevent` is an optional dependency that allow concurrency for the RawServer. 

You can install it using: 

.. code-block:: bash
   :caption: installation
   :name: installation

   sudo -H python -m pip install gevent

