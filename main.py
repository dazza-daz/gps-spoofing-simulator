import sys
import os
import numpy as np

# Add src to python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from simulation import Satellite, Receiver, Spoofer
from trilateration import trilaterate
from visualizer import Visualizer

def main():
    # Setup Satellites (2D wide area)
    # Placing satellites at varied distances to break the 'common bias' symmetry
    satellites = [
        Satellite(1, [0, 800]),
        Satellite(2, [1200, 1000]),
        Satellite(3, [500, -300]),
        Satellite(4, [-200, 400]),
        Satellite(5, [1500, 200]),
        Satellite(6, [200, 1200]) # Added 6th satellite
    ]

    # Spoofer location (Physical)
    spoofer_pos = np.array([400, 400])
    # Target location (Receiver must be here for 'perfect' spoof)
    target_pos = np.array([100, 100])
    # Fake position goal (Receiver should think it's here)
    fake_pos = np.array([900, 100])

    spoofer = Spoofer(spoofer_pos)
    spoofer.setup_spoof(satellites, target_pos, fake_pos)

    # Initial receiver calculation to find the 'correct' spoofed bias
    receiver = Receiver(target_pos)
    spoofer.spoof_receiver(receiver)
    fix_x, fix_y, initial_dt, rmse = trilaterate([s.pos for s in satellites], receiver.measured_distances)
    
    viz = Visualizer(satellites, spoofer, target_pos, fake_pos)

    def on_mouse_move(event):
        if event.inaxes != viz.ax:
            return
        
        # Update actual receiver position based on mouse
        receiver.actual_pos = np.array([event.xdata, event.ydata])
        
        # Apply spoofing
        spoofer.spoof_receiver(receiver)
        
        # Solve for fix
        # By fixing the clock bias to what it should be at the target, 
        # any geometric inconsistency will show up as a high residual (RMSE).
        fix_x, fix_y, dt, rmse = trilaterate([s.pos for s in satellites], 
                                            receiver.measured_distances, 
                                            fix_clock_bias=initial_dt)
        
        # Update plot
        viz.update(receiver, fix_x, fix_y, rmse)

    viz.fig.canvas.mpl_connect('motion_notify_event', on_mouse_move)
    
    # Run initial update
    viz.update(receiver, fix_x, fix_y, rmse)

    print("\n" + "="*50)
    print("GPS SPOOFING SIMULATION")
    print("="*50)
    print("ORANGE DOT: Your actual physical location (Move with mouse)")
    print("GREEN DOT:  The target location the spoofer is optimized for")
    print("RED X:       Where your GPS receiver thinks it is (Calculated Fix)")
    print("PURPLE CIRCLE: The 'Fake' location the spoofer wants you to be at")
    print("-"*50)
    print("OBSERVATION:")
    print("1. Hover over the GREEN dot: The RED X should be exactly on the PURPLE circle.")
    print("2. Move away from the GREEN dot: The RED X will drift and the RMSE will spike.")
    print("="*50 + "\n")
    viz.show()

if __name__ == "__main__":
    main()
