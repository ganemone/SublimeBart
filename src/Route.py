from .station_map import station_map


class Route:

    def __init__(self, trip_attrs, legs):
        self.origin = trip_attrs['origin']
        self.destination = trip_attrs['destination']
        self.fare = trip_attrs['fare']
        self.departs = trip_attrs['origTimeMin']
        self.arrives = trip_attrs['destTimeMin']
        self.legs = legs

    def has_transfer(self):
        return len(self.legs) > 1

    def num_transfers(self):
        return len(self.legs) - 1

    def short_description(self):
        return [
            'Departs: ' + self.departs,
            'Arrives: ' + self.arrives,
            'Transfers: {0}'.format(self.num_transfers())
        ]

    def long_description(self):
        s = []
        for leg in self.legs:
            attrs = leg.attrib
            s.append('{departs}: {origin} to {dest} \n'.format(
                departs=attrs['origTimeMin'],
                origin=station_map[attrs['origin'].lower()],
                dest=station_map[attrs['destination'].lower()]
            ))

        s.append('{arrives}: Arrive at {destination}'.format(
            destination=station_map[self.destination.lower()],
            arrives=self.arrives
        ))
        return s
