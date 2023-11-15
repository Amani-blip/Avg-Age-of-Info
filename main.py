import dataclasses
from dataclasses import dataclass
from typing import Protocol, Any
import numpy as np


class Stack:
    def __init__(self):
        # the last item is the top of the stack
        self.items: list[Any] = []

    def push(self, item: Any):
        self.items.append(item)

    def pop(self) -> Any:
        return self.items.pop(-1)

    def empty(self) -> bool:
        """returns true when the stack is empty"""
        return len(self.items) == 0


class Queue:
    def __init__(self):
        # the last item is the top of the stack
        self.items: list[Any] = []

    def push(self, item: Any):
        self.items.append(item)

    def insert(self, item: Any):
        # insert at the front of the queue
        self.items.insert(0, item)

    def pop(self) -> Any:
        if not self.empty():
            return self.items.pop(0)
        return None

    def empty(self) -> bool:
        """returns true when the queue is empty"""
        return len(self.items) == 0


@dataclass
class Packet:
    arrival_time: float
    service_time: float
    source: int


@dataclass
class PacketOutput:
    source: int
    arrival_time: float
    service_end_time: float


class Simulation(Protocol):
    def simulate(self, packets: list[Packet]) -> list[PacketOutput]:
        ...


class LCFS_W:
    def simulate(self, packets: list[Packet]) -> list[PacketOutput]:
        # check there's at least one packet to simulate
        if len(packets) == 0:
            return []

        # copy the packets since this method will modify the service_time
        # as the packets are processed.
        packets = [dataclasses.replace(packet) for packet in packets]

        # run the simulation
        last_update: list[float] = [-1, -1]
        lcfs = Stack()

        output: list[PacketOutput] = []

        def process_packets(previous_clock: float, clock: float):
            """given the previous clock time, and current clock time. we process
            packets in the lcfs queue.
            """
            processing_clock = previous_clock

            while not lcfs.empty() and processing_clock != clock:
                packet: Packet = lcfs.pop()

                # drop packets that contain old status updates
                if packet.arrival_time < last_update[packet.source]:
                    continue

                # process the packet
                available_processing_time = clock - processing_clock
                processing_time = min(packet.service_time, available_processing_time)
                processing_clock += processing_time
                packet.service_time -= processing_time

                # the packet was fully processed
                if packet.service_time == 0:
                    last_update[packet.source] = packet.arrival_time
                    output.append(
                        PacketOutput(
                            source=packet.source,
                            arrival_time=packet.arrival_time,
                            service_end_time=processing_clock,
                        )
                    )
                    continue

                # the packet was not fully processed
                # there wasn't enough processing time so we push it back to the top
                # of the lcfs queue to continue processing the next time.
                lcfs.push(packet)

        previous_packet_arrival = -1

        for packet in packets:
            process_packets(previous_packet_arrival, packet.arrival_time)
            previous_packet_arrival = packet.arrival_time

            # if the stack is empty we put the new packet at the top
            # otherwise we place the packet in the second position so
            # that it waits before being processed
            if lcfs.empty():
                lcfs.push(packet)
            else:
                temp = lcfs.pop()
                lcfs.push(packet)
                lcfs.push(temp)

        # process any remaining packets. packets with old status updates will be ignored.
        # so I can calculate the total remaining processing time and advance the clock that far
        # to ensure any remaining packets are processed.
        total_remaining_processing_time = sum(
            [packet.service_time for packet in lcfs.items]
        )
        process_packets(
            previous_packet_arrival,
            previous_packet_arrival + total_remaining_processing_time,
        )

        return output


class LCFS_S:
    # Daniel
    def simulate(self, packets: list[Packet]) -> list[PacketOutput]:
        # check there's at least one packet to simulate
        if len(packets) == 0:
            return []

        # copy the packets since this method will modify the service_time
        # as the packets are processed.
        packets = [dataclasses.replace(packet) for packet in packets]

        # run the simulation
        last_update: list[float] = [-1, -1]
        lcfs = Stack()

        output: list[PacketOutput] = []

        def process_packets(previous_clock: float, clock: float):
            """given the previous clock time, and current clock time. we process
            packets in the lcfs queue.
            """
            processing_clock = previous_clock

            while not lcfs.empty() and processing_clock != clock:
                packet: Packet = lcfs.pop()

                # drop packets that contain old status updates
                if packet.arrival_time < last_update[packet.source]:
                    continue

                # process the packet
                available_processing_time = clock - processing_clock
                processing_time = min(packet.service_time, available_processing_time)
                processing_clock += processing_time
                packet.service_time -= processing_time

                # the packet was fully processed
                if packet.service_time == 0:
                    last_update[packet.source] = packet.arrival_time
                    output.append(
                        PacketOutput(
                            source=packet.source,
                            arrival_time=packet.arrival_time,
                            service_end_time=processing_clock,
                        )
                    )
                    continue

                # the packet was not fully processed
                # there wasn't enough processing time so we push it back to the top
                # of the lcfs queue to continue processing the next time.
                lcfs.push(packet)

        previous_packet_arrival = -1

        for packet in packets:
            # process packets in lcfs queue
            process_packets(previous_packet_arrival, packet.arrival_time)
            previous_packet_arrival = packet.arrival_time

            # push the new packet to the top of lcfs queue
            # gives this packet priority, preempts previous packet.
            lcfs.push(packet)

        # process any remaining packets. packets with old status updates will be ignored.
        # so I can calculate the total remaining processing time and advance the clock that far
        # to ensure any remaining packets are processed.
        total_remaining_processing_time = sum(
            [packet.service_time for packet in lcfs.items]
        )
        process_packets(
            previous_packet_arrival,
            previous_packet_arrival + total_remaining_processing_time,
        )

        return output


class ProposedPolicy:
    # Marija
    def simulate(self, packets: list[Packet]) -> list[PacketOutput]:
        # check there's at least one packet to simulate
        if len(packets) == 0:
            return []

        # copy the packets since this method will modify the service_time
        # as the packets are processed.
        packets = [dataclasses.replace(packet) for packet in packets]

        # run the simulation
        queue = Queue()

        output: list[PacketOutput] = []

        def process_packets(previous_clock: float, clock: float):
            """given the previous clock time, and current clock time. we process
            packets in the lcfs queue.
            """
            processing_clock = previous_clock

            while not queue.empty() and processing_clock != clock:
                packet: Packet = queue.pop()

                # process the packet
                available_processing_time = clock - processing_clock
                processing_time = min(packet.service_time, available_processing_time)
                processing_clock += processing_time
                packet.service_time -= processing_time

                # the packet was fully processed
                if packet.service_time == 0:
                    output.append(
                        PacketOutput(
                            source=packet.source,
                            arrival_time=packet.arrival_time,
                            service_end_time=processing_clock,
                        )
                    )
                    continue

                # the packet was not fully processed
                # there wasn't enough processing time so we push it back to the top
                # of the lcfs queue to continue processing the next time.
                queue.insert(packet)

        previous_packet_arrival = -1

        for packet in packets:
            # process packets in lcfs queue
            process_packets(previous_packet_arrival, packet.arrival_time)
            previous_packet_arrival = packet.arrival_time

            # push the new packet to the top of lcfs queue
            # gives this packet priority, preempts previous packet.
            if queue.empty():
                queue.push(packet)
            else:
                replaced = False

                for i, waiting_packet in enumerate(queue.items[1:]):
                    if waiting_packet.source == packet.source:
                        queue.items[i + 1] = packet
                        replaced = True
                        break

                if not replaced:
                    queue.push(packet)

        # process any remaining packets. packets with old status updates will be ignored.
        # so I can calculate the total remaining processing time and advance the clock that far
        # to ensure any remaining packets are processed.
        total_remaining_processing_time = sum(
            [packet.service_time for packet in queue.items]
        )
        process_packets(
            previous_packet_arrival,
            previous_packet_arrival + total_remaining_processing_time,
        )

        return output


def sort_packets(*packet_lists: list[Packet]) -> list[Packet]:
    """sort multiple lits of packets by ascending arrival time"""
    packets = []
    for packet_list in packet_lists:
        packets.extend(packet_list)
    return sorted(packets, key=lambda packet: packet.arrival_time)


def create_packets(
    n: int, source: int, arrival_rate: float, service_time_mean: float, seed=None
) -> list[Packet]:
    """create packets for a source with an arrival rate, and service time mean"""
    packets: list[Packet] = []
    arrival_time: int = 0
    rng: np.random.Generator = np.random.default_rng(seed)

    for _ in range(n):
        arrival_time += rng.poisson(lam=arrival_rate)
        packets.append(
            Packet(
                arrival_time=arrival_time,
                service_time=rng.exponential(scale=1 / service_time_mean),
                source=source,
            )
        )

    return packets


def aoi(packets: list[PacketOutput]) -> float:
    def age_of_packet(packet: PacketOutput) -> float:
        return packet.service_end_time - packet.arrival_time

    return sum(map(age_of_packet, packets)) / len(packets)
