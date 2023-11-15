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

    """
        packets = [
        Packet(arrival_time=1, service_time=5, source=0),
        Packet(arrival_time=2, service_time=2, source=1),
        Packet(arrival_time=3, service_time=2, source=0),
    ]
    """

    def simulate(self, packets: list[Packet]) -> list[PacketOutput]:
        ...
        if len(packets) == 0:
            return []

        packets = [dataclasses.replace(packet) for packet in packets]

        last_update: list[float] = [-1, -1]
        lcfs = Stack()

        output: list[PacketOutput] = []

        server_busy = False

        def process_packets():
            # while not lcfs.empty() and processing_clock != clock:
            if not lcfs.empty():
                pck: Packet = lcfs.pop()

                if pck.arrival_time < last_update[pck.source]:
                    return

                # departure = arrival + wait + service
                prev_departure = 0
                if output:
                    prev_departure = output[len(output) - 1].service_end_time
                waiting_time = 0
                if prev_departure > pck.arrival_time:
                    waiting_time = prev_departure - pck.arrival_time

                last_update[pck.source] = pck.arrival_time
                output.append(
                    PacketOutput(
                        source=pck.source,
                        arrival_time=pck.arrival_time,
                        service_end_time=pck.arrival_time
                        + waiting_time
                        + pck.service_time,
                    )
                )

        seen = []

        while packets:
            packet = packets[0]
            if packet.arrival_time <= last_update[packet.source]:
                print(packet.arrival_time)
                print(last_update[packet.source])
                print("amani")
                packets.pop(0)
                continue
            prev_departure = 0

            if output:
                prev_departure_packet = output[len(output) - 1]
                if prev_departure_packet not in seen:
                    seen.append(prev_departure_packet)
                    prev_departure = prev_departure_packet.service_end_time

                print(prev_departure)

            # if a packet arrives while the server is busy
            if packet.arrival_time < prev_departure:
                server_busy = True
            else:
                server_busy = False

            print("this is the packet")
            print(packet)
            print(packets)

            if not server_busy:
                lcfs.push(packet)
                process_packets()
                packet_popped = packets.pop(0)

                print(packet_popped)
                print("packets after pop")
                print(packets)
                print("here")
            elif server_busy:
                print("here2")
                waiting = []
                if packets:
                    # temp_arrival = packets[i].arrival_time
                    while packets:
                        temp_arrival = packets[0].arrival_time
                        if temp_arrival <= prev_departure:
                            popped = packets.pop(0)
                            waiting.append(popped)
                        else:
                            break

                    print("final waint")
                    print(waiting)
                waiting.sort(key=lambda x: x.arrival_time, reverse=True)
                print()
                packets = waiting + packets

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
                    last_update[
                        packet.source
                    ] = packet.arrival_time  # update last_update for this source
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


# Aidan
def create_packets(n: int, source: int, lam: float, scale: float) -> list[Packet]:
    packets: list[Packet] = []
    time: int = 0
    rng: np.random.Generator = np.random.default_rng()

    for _ in range(n):
        time += rng.poisson(lam=lam)
        packets.append(
            Packet(
                arrival_time=time,
                service_time=rng.exponential(scale=scale),
                source=source,
            )
        )

    return packets


# Aidan
def aoi(packets: list[PacketOutput]) -> float:
    def age_of_packet(packet: PacketOutput) -> float:
        return packet.service_end_time - packet.arrival_time

    return sum(map(age_of_packet, packets)) / len(packets)
