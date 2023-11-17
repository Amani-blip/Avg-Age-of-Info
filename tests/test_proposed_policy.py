from main import Packet, PacketOutput, ProposedPolicy


def test_proposed():
    packets = [
        Packet(arrival_time=1, service_time=5, source=0),
        Packet(arrival_time=2, service_time=2, source=1),
        Packet(arrival_time=3, service_time=2, source=0),
        Packet(arrival_time=4, service_time=2, source=1),
    ]

    output = ProposedPolicy().simulate(packets)

    assert output == [
        PacketOutput(arrival_time=1, service_end_time=6, source=0),
        PacketOutput(arrival_time=4, service_end_time=8, source=1),
        PacketOutput(arrival_time=3, service_end_time=10, source=0),
    ]
