import numpy as np

class Satellite:
    def __init__(self, id, pos):
        self.id = id
        self.pos = np.array(pos)

class Receiver:
    def __init__(self, pos):
        self.actual_pos = np.array(pos)
        self.measured_distances = []
        self.calculated_fix = None
        self.residual_rmse = 0.0

    def measure_true_distances(self, satellites):
        """Standard GPS measurement without spoofing."""
        self.measured_distances = [
            np.linalg.norm(self.actual_pos - sat.pos) for sat in satellites
        ]

class Spoofer:
    def __init__(self, pos):
        self.pos = np.array(pos)
        self.delays = []

    def setup_spoof(self, satellites, target_pos, fake_pos):
        """
        Calculates the static delays needed to make a receiver at target_pos
        think it is at fake_pos.
        
        delay_i = dist(fake_pos, sat_i) - dist(spoofer, target_pos)
        """
        self.delays = []
        dist_spoofer_to_target = np.linalg.norm(self.pos - target_pos)
        
        for sat in satellites:
            dist_fake_to_sat = np.linalg.norm(fake_pos - sat.pos)
            # When target receives signal from spoofer, it travels dist_spoofer_to_target
            # We want measured distance to be dist_fake_to_sat
            # delay = dist_fake_to_sat - dist_spoofer_to_target
            self.delays.append(dist_fake_to_sat - dist_spoofer_to_target)

    def spoof_receiver(self, receiver):
        """
        Modifies receiver's measured distances based on its physical distance
        from the spoofer and the pre-calculated delays.
        """
        # Always update true distances first for reference (though not used by spoofer logic itself)
        # np.linalg.norm(self.pos - receiver.actual_pos) is the physical distance from spoofer to receiver.
        dist_spoofer_to_receiver = np.linalg.norm(self.pos - receiver.actual_pos)
        
        # In a single-source spoofing scenario, the signal from the spoofer
        # is the only one the receiver gets. It's as if all satellites are at the spoofer's location.
        receiver.measured_distances = [
            dist_spoofer_to_receiver + delay for delay in self.delays
        ]
