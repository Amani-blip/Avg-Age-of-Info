from main import create_packets


def test_create_packets():
    source = 1
    n = 5
    packets = create_packets(n, source, 0.45, 1.0)

    for packet in packets:
        assert type(packet.arrival_time) is int
        assert type(packet.service_time) is float
        assert packet.source == source

    assert len(packets) == n
