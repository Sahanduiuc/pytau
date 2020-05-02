from unittest.mock import Mock

from tau.core import Network, Event


def test_event_propagation():
    network = Network()

    a = Mock(spec=Event)
    a.on_activate.return_value = True
    b = Mock(spec=Event)
    c = Mock(spec=Event)

    network.connect(a, b)
    network.connect(a, c)
    network.activate(a)
    a.on_activate.assert_called_once()
    b.on_activate.assert_called_once()
    c.on_activate.assert_called_once()


def test_event_short_circuit():
    network = Network()

    a = Mock(spec=Event)
    a.on_activate.return_value = False
    b = Mock(spec=Event)
    c = Mock(spec=Event)

    network.connect(a, b)
    network.connect(a, c)
    network.activate(a)
    a.on_activate.assert_called_once()
    b.on_activate.assert_not_called()
    c.on_activate.assert_not_called()

