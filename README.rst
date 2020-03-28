Tau: Python Reactive Programming
================================

.. image:: https://img.shields.io/pypi/v/pytau.svg
    :target: https://pypi.org/project/pytau/

.. image:: https://img.shields.io/pypi/l/pytau.svg
    :target: https://pypi.org/project/pytau/

.. image:: https://img.shields.io/pypi/pyversions/pytau.svg
    :target: https://pypi.org/project/pytau/

*A library for composing asynchronous and event-based programs in Python*

About Tau
---------

Tau is a `functional reactive programming <https://en.wikipedia.org/wiki/Functional_reactive_programming>`_ framework
designed for Python from the ground up.

.. code:: python

    from tau.event import Lambda
    from tau.signal import OneShot
    from tau.testing import TestSchedulerContextManager

    with TestSchedulerContextManager() as scheduler:
        signal = OneShot(scheduler, ["world"])
        Lambda(scheduler.get_network(), signal, lambda x: print(f"Hello, {x[0].get_value()}!"))


Installation
------------

Tau runs on `Python <http://www.python.org/>`_ 3.8 or above. To install Tau:

.. code:: console

    pip3 install pytau
