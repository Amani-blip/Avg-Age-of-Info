from dataclasses import dataclass
from typing import Protocol

@dataclass
class Packet:
    arrival_time: float
    service_time: float
    source: int


@dataclass
class PacketOutput:
    source: int
    service_end_time: int


class Simulation(Protocol):
    def simulate(self, packets: list[Packet]) -> PacketOutput:
        ...


class LCFS_W:
    # Amani
    def simulate(self, packets: list[Packet]) -> PacketOutput:
        ...

class LCFS_S:
    # Daniel
    def simulate(self, packets: list[Packet]) -> PacketOutput:
        ...

class ProposedPolicy:
    # Maria
    def simulate(self, packets: list[Packet]) -> PacketOutput:
        ...


# Aidan
def create_packets() -> list[Packet]:
    ...

# Aidan
def aoi(packets: list[PacketOutput]) -> float:
    ...
