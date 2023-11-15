from main import Packet, PacketOutput, ProposedPolicy


def test_proposed_policy():
    # Create a sequence of packets with whole number arrival times and service times
    packets = [
        Packet(arrival_time=0, service_time=1, source=1),  # Processed immediately
        Packet(
            arrival_time=2, service_time=6, source=2
        ),  # Processed immediately because Packet 1 has already finished
        Packet(arrival_time=3, service_time=7, source=2),  # Waiting in the Queue
        Packet(
            arrival_time=6, service_time=2, source=2
        ),  # This one is of the same source as Packet 3, so it replaces it in the queue
    ]

    # Run the simulation
    policy = ProposedPolicy()
    output = policy.simulate(packets)

    # Check the output
    assert (
        len(output) == 3
    ), "Three packets should be processed."  # Because Packet 4 replaced Packet 3
    assert (
        output[0].source == 1 and output[0].service_end_time == 1
    ), "First packet processed incorrectly."
    assert (
        output[1].source == 2 and output[1].service_end_time == 8
    ), "Second packet processed incorrectly."
    assert (
        output[2].source == 2 and output[2].service_end_time == 10
    ), "Third packet processed incorrectly."

    print("Test passed!")


# Run the test
test_proposed_policy()
