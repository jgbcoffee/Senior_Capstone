###############################################################################################################################
# Jose G. Barrera
# Date: 20240128

# The purpose of this code is to simulate the Hohmann stransfer orbit from Earth's moon to Mars. 
# Some things to note, typically, the ideal phase angle of Mars is 44.36 degrees (Mars position relative to the Sun and Earth)
# In this code, however, I used 44.75 degrees to get the rocket to intercept with Mars
# This discrepancy in degrees can be attributed to the fact that Earth and mars dont orbit the sun in perfect circles.
# In the future, I will look to apply this code to other planets since most of the framework remains the same.

###############################################################################################################################

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle

# Defining celestial constants
G = 6.67430e-11  # In m^3 kg^-1 s^-2
M_sun = 1.989e30  # In kg

r_earth_orbit = 1.496e11  # Radius of Earths orbit in meters
r_mars_orbit = 2.279e11  # Radius of Mars orbit in meters

# Periods of of orbits (Here is where I simplified it to circles)
T_earth = 2 * np.pi * np.sqrt(r_earth_orbit**3 / (G * M_sun))
T_mars = 2 * np.pi * np.sqrt(r_mars_orbit**3 / (G * M_sun))

# Semi-major axis of transfer orbit
a_transfer = (r_earth_orbit + r_mars_orbit) / 2

# Time array (up to one Martian year/orbit)
t = np.linspace(0, T_mars, 1000)  

# Earth's starting position and function w/ respect to time
theta_earth = (2 * np.pi / T_earth) * t
x_earth = r_earth_orbit * np.cos(theta_earth)
y_earth = r_earth_orbit * np.sin(theta_earth)

# Mars Starting position and function w/ respect to time - Typically, the ideal phase angle is 44.36, but I used 44.75
theta_mars = (2 * np.pi / T_mars) * t + 44.75
x_mars = r_mars_orbit * np.cos(theta_mars)
y_mars = r_mars_orbit * np.sin(theta_mars)

# Transfer orbit position as a function of time starting at launch_time
theta_transfer = np.sqrt((G * M_sun) / a_transfer**3) * (t)
x_transfer = a_transfer * (np.cos(theta_transfer) - 1)
y_transfer = a_transfer * np.sin(theta_transfer)

# Distance between the rocket and Mars
distances_to_mars = np.sqrt((x_transfer + x_earth[0] - x_mars)**2 + (y_transfer + y_earth[0] - y_mars)**2)

# Find the index where the rocket is closest to Mars (Used later to have the rocket stick to Mars)
intercept_idx = np.argmin(distances_to_mars)

# Plot
fig, ax = plt.subplots()

# Earth and Mars orbits
earth_orbit = Circle((0, 0), r_earth_orbit, color='blue', fill=False)
mars_orbit = Circle((0, 0), r_mars_orbit, color='red', fill=False)

ax.add_patch(earth_orbit)
ax.add_patch(mars_orbit)

# Earth and Mars (initially at their starting positions)
earth = plt.plot(x_earth[0], y_earth[0], 'o', color='blue', label='Earth')[0]
mars = plt.plot(x_mars[0], y_mars[0], 'o', color='red', label='Mars')[0]

# Rocket (initially at Earth)
rocket, = plt.plot(x_earth, y_earth, 'o', color='green', label='Rocket')

# Labels
plt.title("Simulation of Rocket from Earth's Moon to Mars")
ax.set_aspect('equal')
ax.set_xlim(-r_mars_orbit * 1.1, r_mars_orbit * 1.1)
ax.set_ylim(-r_mars_orbit * 1.1, r_mars_orbit * 1.1)
plt.xlabel('Distance (m)')
plt.ylabel('Distance (m)')
plt.legend()

# Start animation
def init():
    rocket.set_data(x_earth[0], y_earth[0])
    earth.set_data(x_earth[0], y_earth[0])
    mars.set_data(x_mars[0], y_mars[0])
    return rocket, earth, mars

# Animation function
def animate(i):
    if i < intercept_idx:
        # Before the interception, the rocket will follow transfer trajectory
        idx = i
        rocket_x = x_transfer[idx] + x_earth[0]
        rocket_y = y_transfer[idx] + y_earth[0]
    else:
        # After interception, the rocket will stay with Mars
        rocket_x, rocket_y = x_mars[i], y_mars[i]
    
    rocket.set_data(rocket_x, rocket_y)
    earth.set_data(x_earth[i], y_earth[i])
    mars.set_data(x_mars[i], y_mars[i])
    return rocket, earth, mars

ani = FuncAnimation(fig, animate, init_func=init, frames=len(t), interval=20, blit=True)
# ani.save('rocket_from_Moon_to_mars.gif', writer='imagemagick', fps=30)
plt.show()
        
