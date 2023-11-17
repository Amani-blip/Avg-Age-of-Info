from main import (
    PacketOutput,
    AoiUpdate,
    get_age_of_information_updates,
    calculate_average_age_information,
)


def test_aoi():
    outputs = [
        PacketOutput(source=0, arrival_time=2, service_end_time=4),
        PacketOutput(source=0, arrival_time=6, service_end_time=7),
        PacketOutput(source=0, arrival_time=7, service_end_time=8),
    ]

    updates = get_age_of_information_updates(outputs=outputs, source=0)
    assert updates == [
        AoiUpdate(time=0, age=0),
        AoiUpdate(time=4, age=4),
        AoiUpdate(time=4, age=2),
        AoiUpdate(time=7, age=5),
        AoiUpdate(time=7, age=1),
        AoiUpdate(time=8, age=2),
        AoiUpdate(time=8, age=1),
    ]

    assert calculate_average_age_information(outputs, source=0) == 2.5
