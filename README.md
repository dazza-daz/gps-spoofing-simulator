# GPS Trilateration & Spoofing Simulation

This project is an interactive Python simulation that visually demonstrates how GPS trilateration works and how a single-source spoofer causes location fixes to degrade for nearby receivers.

## The Concept

In a standard GPS scenario, a receiver calculates its position by measuring the distance to multiple satellites. When a spoofer is present, it transmits "fake" signals from a single physical location. 

While the spoofer can perfectly calculate the signal delays needed to make a receiver at a **specific target location** think it is at a **fake goal location**, any receiver even slightly away from that target will experience geometric inconsistencies. This is because the signal travel time from the spoofer to the receiver changes differently than the expected signal travel time from the satellites.

## Visual Indicators

- **Orange Dot**: Your actual physical location (movable with your mouse).
- **Green Dot**: The "Sweet Spot" where the spoofer is perfectly calibrated.
- **Red X**: The calculated GPS fix (where your receiver *thinks* it is).
- **Purple Circle**: The "Fake" location the spoofer wants to trick you into believing you are at.
- **Red Shaded Area**: The **Position Uncertainty (RMSE)**. The larger this circle, the more inconsistent the satellite signals are, indicating a poor or spoofed fix.

## Prerequisites

- Python 3.x
- `numpy`
- `scipy`
- `matplotlib`

## Installation

1. Clone the repository.
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Linux/macOS
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the simulation:
```bash
python3 main.py
```

### Observations to make:
1. **The Perfect Spoof**: Move the **Orange Dot** exactly over the **Green Dot**. The **Red X** should land perfectly inside the **Purple Circle** with a near-zero uncertainty radius.
2. **Geometric Degradation**: Move the **Orange Dot** away from the Green Target. Watch how the **Red X** drifts away from the goal and the **Red Uncertainty Circle** grows rapidly, showing the "fuzziness" of the spoofed fix.
3. **Satellite Intersection**: Observe the dashed gray circles (representing measured distances). At the target, they intersect at a point. Away from the target, they fail to meet, illustrating why the trilateration residual (RMSE) increases.

## Project Structure

- `main.py`: Interactive entry point and simulation setup.
- `src/simulation.py`: Core logic for satellites, spoofer, and receiver models.
- `src/trilateration.py`: Least-squares solver for $(x, y, \delta t)$.
- `src/visualizer.py`: Matplotlib-based interactive plotting.
