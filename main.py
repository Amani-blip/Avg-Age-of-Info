import dataclasses
from dataclasses import dataclass
from typing import Protocol, Any


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


class Simulation(Protocol):
    def simulate(self, packets: list[Packet]) -> list[PacketOutput]:
        ...

class LCFS_W:
    # Amani
    def simulate(self, packets: list[Packet]) -> list[PacketOutput]:
        ...

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
                    last_update[packet.source] = packet.arrival_time # update last_update for this source
                    output.append(
                        PacketOutput(
                            source=packet.source, 
                            arrival_time=packet.arrival_time, 
                            service_end_time=processing_clock
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
        total_remaining_processing_time = sum([packet.service_time for packet in lcfs.items])
        process_packets(previous_packet_arrival, previous_packet_arrival + total_remaining_processing_time)

        return output

class ProposedPolicy:
    # Marija
    def simulate(self, packets: list[Packet]) -> list[PacketOutput]:
        # check there's at least one packet to simulate
        if len(packets) == 0:
            return []
        
        # This ensures that all the packets are only from source 1 or 2 as explicitly stated in the paper.
        packets = [p for p in packets if p.source in [1, 2]]

        # Initialize the queue
        queue = Queue()
        # Initialize the list of processed packets
        sink: list[PacketOutput] = []
        # Keep track if server is busy
        server_busy = False

        def process_packets(previous_clock: float, clock: float):
            processing_clock = previous_clock
            server_busy = True
            
            while not queue.empty() and processing_clock != clock:
                #get the first item of the list
                packet = queue.pop()

                # process the packet
                available_processing_time = clock - processing_clock
                processing_time = min(packet.service_time, available_processing_time)
                processing_clock += processing_time
                packet.service_time -= processing_time

                # the packet was fully processed
                if packet.service_time == 0:
                    sink.append(
                        PacketOutput(
                            source=packet.source, 
                            arrival_time=packet.arrival_time, 
                            service_end_time=processing_clock
                        )
                    )
                    server_busy = False
                else:
                    # If it wasn't fully processed add it in the end of the list
                    queue.insert(packet)
      
        # Because the simulation time starts at 0
        previous_packet_arrival = 0

        for packet in packets:
            # Here we process the packets
            process_packets(previous_packet_arrival, packet.arrival_time)
            previous_packet_arrival = packet.arrival_time
            # If the queue is empty regardless of the source immediately enter the queue
            if queue.empty():
                queue.push(packet)
                server_busy = True
            else:
                # Recall: packet of a source c ∈ {1, 2} waiting in the queue is replaced if a new packet of the same source arrives.
                replaced = False
                # If there's only one packet in the queue, check if it's the same source and not being processed
                if not server_busy and queue.items[0].source == packet.source:
                    # Replace the packet only if it's the same source and the queue has not started processing
                    queue.items[0] = packet
                    replaced = True
                elif len(queue.items) == 2:
                    # If there are two packets, check the second one for replacement possibility
                    if queue.items[1].source == packet.source:
                        queue.items[1] = packet
                        replaced = True

                # If no packet from the same source was found and the queue isn't full, add the packet
                if not replaced and len(queue.items) < 2:
                    queue.push(packet)
                    server_busy = True if len(queue.items) == 1 else server_busy

        # process any remaining packets after the last arrival
        total_remaining_processing_time = sum([packet.service_time for packet in queue.items])
        process_packets(previous_packet_arrival, previous_packet_arrival + total_remaining_processing_time)


        return sink


# Aidan
def create_packets() -> list[Packet]:
    ...

# Aidan
def aoi(packets: list[PacketOutput]) -> float:
    ...
