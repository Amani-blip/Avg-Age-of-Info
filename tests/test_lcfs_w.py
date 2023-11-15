from main import Packet, PacketOutput, LCFS_W


def test_lcfs_w():
    packets = [
        Packet(arrival_time=1, service_time=5, source=0),
        Packet(arrival_time=2, service_time=2, source=1),
        Packet(arrival_time=3, service_time=2, source=1),
    ]

    output = LCFS_W().simulate(packets)

    assert output == [
        PacketOutput(source=0, arrival_time=1, service_end_time=6),
        PacketOutput(source=1, arrival_time=3, service_end_time=8),
    ]
