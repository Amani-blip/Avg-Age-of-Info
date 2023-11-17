from main import create_packets, sort_packets


def test_create_packets():
    packets_source0 = create_packets(
        max_arrival_time=100, source=0, arrival_rate=1, service_time_mean=1
    )

    packets_source1 = create_packets(
        max_arrival_time=100, source=1, arrival_rate=1, service_time_mean=1
    )

    packets = sort_packets(packets_source0, packets_source1)

    for i in range(len(packets) - 1):
        assert packets[i].arrival_time <= packets[i + 1].arrival_time
