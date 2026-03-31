import numpy as np
from scipy.optimize import least_squares

def trilaterate(satellite_positions, measured_distances, initial_guess=None, fix_clock_bias=None):
    """
    Solves for the receiver position (x, y) and clock bias (delta_t)
    given satellite positions and measured pseudoranges.
    
    satellite_positions: list of (x, y) tuples or numpy array
    measured_distances: list or numpy array of distances
    initial_guess: (x, y, delta_t) starting point
    fix_clock_bias: if set, don't optimize delta_t, use this value
    
    Returns: (x, y, delta_t, residual_rmse)
    """
    satellite_positions = np.array(satellite_positions)
    measured_distances = np.array(measured_distances)
    
    if initial_guess is None:
        # Default guess: average of satellite positions, zero bias
        initial_guess = np.append(np.mean(satellite_positions, axis=0), 0)
    
    def residuals(params):
        if fix_clock_bias is not None:
            x_rec, y_rec = params
            delta_t = fix_clock_bias
        else:
            x_rec, y_rec, delta_t = params
        
        # Calculate distances from current guess to all satellites
        dx = satellite_positions[:, 0] - x_rec
        dy = satellite_positions[:, 1] - y_rec
        distances = np.sqrt(dx**2 + dy**2)
        
        # Predicted pseudorange = actual distance + clock bias
        # Residual = predicted - measured
        return (distances + delta_t) - measured_distances

    # Adjust initial guess if clock is fixed
    solve_params = initial_guess[:2] if fix_clock_bias is not None else initial_guess

    result = least_squares(residuals, solve_params)
    
    # Calculate RMSE of residuals
    rmse = np.sqrt(np.mean(result.fun**2))
    
    if fix_clock_bias is not None:
        x, y = result.x
        dt = fix_clock_bias
    else:
        x, y, dt = result.x
    return x, y, dt, rmse
