from main import PacketOutput, aoi


def test_aoi():
    packets = [
        PacketOutput(arrival_time=1, service_end_time=5, source=1),
        PacketOutput(arrival_time=2, service_end_time=6, source=1),
        PacketOutput(arrival_time=3, service_end_time=7, source=1),
        PacketOutput(arrival_time=6, service_end_time=8, source=1),
    ]

    output = aoi(packets)

    assert output == 3.5
