import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

class Visualizer:
    def __init__(self, satellites, spoofer, target_pos, fake_pos):
        self.satellites = satellites
        self.spoofer = spoofer
        self.target_pos = target_pos
        self.fake_pos = fake_pos
        
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.circles = []
        self.setup_plot()
        
    def setup_plot(self):
        # Draw Satellites
        sat_pos = np.array([sat.pos for sat in self.satellites])
        self.ax.scatter(sat_pos[:, 0], sat_pos[:, 1], c='blue', marker='^', s=100, label='Satellites')
        for sat in self.satellites:
            self.ax.text(sat.pos[0], sat.pos[1], f'Sat {sat.id}', verticalalignment='bottom')

        # Draw Spoofer
        self.ax.scatter(self.spoofer.pos[0], self.spoofer.pos[1], c='red', marker='X', s=150, label='Spoofer')
        
        # Draw Target and Fake points
        self.ax.scatter(self.target_pos[0], self.target_pos[1], c='green', marker='o', s=50, label='Spoof Target (Perfect)')
        self.ax.scatter(self.fake_pos[0], self.fake_pos[1], edgecolors='purple', facecolors='none', marker='o', s=100, label='Fake Position Goal')
        
        # Plot markers for dynamic elements
        self.receiver_marker, = self.ax.plot([], [], 'o', color='orange', markersize=8, label='Actual Receiver (Movable)')
        self.fix_marker, = self.ax.plot([], [], 'rx', markersize=12, label='Calculated Fix')
        
        # Uncertainty circle (radius proportional to RMSE)
        self.uncertainty_circle = patches.Circle((0, 0), 0, color='red', fill=True, alpha=0.2, label='Position Uncertainty (RMSE)')
        self.ax.add_patch(self.uncertainty_circle)
        
        self.ax.set_aspect('equal')
        self.ax.set_xlim(-500, 1500)
        self.ax.set_ylim(-500, 1500)
        self.ax.grid(True)
        self.ax.legend(loc='upper right')
        
        self.info_text = self.ax.text(0.02, 0.98, '', transform=self.ax.transAxes, 
                                     verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.5))

    def update(self, receiver, fix_x, fix_y, rmse):
        self.receiver_marker.set_data([receiver.actual_pos[0]], [receiver.actual_pos[1]])
        self.fix_marker.set_data([fix_x], [fix_y])
        
        # Update uncertainty circle
        self.uncertainty_circle.set_center((fix_x, fix_y))
        # Multiply RMSE by a scaling factor for visibility if it's too small
        # Given our coordinates are in hundreds/thousands, RMSE should be significant.
        self.uncertainty_circle.set_radius(rmse * 1.5) 
        
        # Remove old satellite circles
        for c in self.circles:
            c.remove()
        self.circles = []
        
        # Draw new circles for measured distances
        for i, sat in enumerate(self.satellites):
            radius = receiver.measured_distances[i]
            # In GPS, measured_distance = distance + bias.
            # Here we don't know bias exactly but the trilateration solver found it.
            # To visualize the 'fuzzy' intersection, we can subtract the found bias.
            # Wait, actually, the 'degradation' is seen when the circles don't meet.
            # Let's draw the raw measured circles. They won't meet at a point but will be offset by the same 'bias'.
            circle = patches.Circle((sat.pos[0], sat.pos[1]), radius, fill=False, color='gray', alpha=0.3, linestyle='--')
            self.ax.add_patch(circle)
            self.circles.append(circle)
            
        status = (f"Receiver Position: ({receiver.actual_pos[0]:.1f}, {receiver.actual_pos[1]:.1f})\n"
                  f"Calculated Fix: ({fix_x:.1f}, {fix_y:.1f})\n"
                  f"Residual (RMSE): {rmse:.4f}\n"
                  f"Dist from Target: {np.linalg.norm(receiver.actual_pos - self.target_pos):.1f}")
        self.info_text.set_text(status)
        self.fig.canvas.draw_idle()

    def show(self):
        plt.show()
