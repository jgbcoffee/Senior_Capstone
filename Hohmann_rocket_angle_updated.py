###############################################################################################################################
# Jose G. Barrera
# Date: 20240214

# The purpose of this code is to simulate the Hohmann stransfer orbit from Earth's moon to Mars. 
# This code differs from the last hohmann transfer code in measuring the angle and distance between the rocket and earth.
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

r_earth_orbit = 1.496e11  # Radius of Earth's orbit in meters
r_mars_orbit = 2.279e11  # Radius of Mars orbit in meters

# Periods of orbits
T_earth = 2 * np.pi * np.sqrt(r_earth_orbit**3 / (G * M_sun))
T_mars = 2 * np.pi * np.sqrt(r_mars_orbit**3 / (G * M_sun))

# Semi-major axis of transfer orbit
a_transfer = (r_earth_orbit + r_mars_orbit) / 2

# Time array (up to one Martian year/orbit)
t = np.linspace(0, T_mars, 1000)

# Earth's position function w/ respect to time
theta_earth = (2 * np.pi / T_earth) * t
x_earth = r_earth_orbit * np.cos(theta_earth)
y_earth = r_earth_orbit * np.sin(theta_earth)

# Mars position function w/ respect to time, phase angle converted to radians
theta_mars = (2 * np.pi / T_mars) * t + np.deg2rad(44.75)
x_mars = r_mars_orbit * np.cos(theta_mars)
y_mars = r_mars_orbit * np.sin(theta_mars)

# Transfer orbit position as a function of time
theta_transfer = np.sqrt((G * M_sun) / a_transfer**3) * t
x_transfer = a_transfer * np.cos(theta_transfer) - a_transfer
y_transfer = a_transfer * np.sin(theta_transfer)

# Distance between the rocket and Mars
distances_to_mars = np.sqrt((x_transfer + x_earth[0] - x_mars)**2 + (y_transfer + y_earth[0] - y_mars)**2)

# Find the index where the rocket is closest to Mars
intercept_idx = np.argmin(distances_to_mars)

# Plot setup
fig, ax = plt.subplots()

# Earth and Mars orbits
earth_orbit = Circle((0, 0), r_earth_orbit, color='blue', fill=False)
mars_orbit = Circle((0, 0), r_mars_orbit, color='red', fill=False)
ax.add_patch(earth_orbit)
ax.add_patch(mars_orbit)

# Earth and Mars (initial positions)
earth, = plt.plot(x_earth[0], y_earth[0], 'o', color='blue', label='Earth')
mars, = plt.plot(x_mars[0], y_mars[0], 'o', color='red', label='Mars')

# Rocket (initially at Earth)
rocket, = plt.plot(x_earth[0], y_earth[0], 'o', color='green', label='Rocket')

# Setup labels and axes
plt.title("Simulation of Rocket from Earth to Mars")
ax.set_aspect('equal')
ax.set_xlim(-r_mars_orbit * 1.1, r_mars_orbit * 1.1)
ax.set_ylim(-r_mars_orbit * 1.1, r_mars_orbit * 1.1)
plt.xlabel('Distance (m)')
plt.ylabel('Distance (m)')
plt.legend()

# Line, angle text, and distance text initialization
line, = ax.plot([], [], 'g--')
angle_text = ax.text(0.02, 0.96, '', transform=ax.transAxes)  # Position adjusted for visibility
distance_text = ax.text(.55, 0.96, '', transform=ax.transAxes)  # Adding distance display

# Initialize animation
def init():
    rocket.set_data(x_earth[0], y_earth[0])
    earth.set_data(x_earth[0], y_earth[0])
    mars.set_data(x_mars[0], y_mars[0])
    line.set_data([], [])
    angle_text.set_text('')
    distance_text.set_text('')
    return rocket, earth, mars, line, angle_text, distance_text

# Animation function
def animate(i):
    if i < intercept_idx:
        rocket_x = x_transfer[i] + x_earth[0]
        rocket_y = y_transfer[i] + y_earth[0]
    else:
        rocket_x = x_mars[i]
        rocket_y = y_mars[i]
    
    rocket.set_data(rocket_x, rocket_y)
    earth.set_data(x_earth[i], y_earth[i])
    mars.set_data(x_mars[i], y_mars[i])
    line.set_data([x_earth[i], rocket_x], [y_earth[i], rocket_y])
    
    dx = rocket_x - x_earth[i]
    dy = rocket_y - y_earth[i]
    angle = np.arctan2(dy, dx) * (180 / np.pi)  # Calculate angle in degrees
    distance = np.sqrt(dx**2 + dy**2)  # Calculate distance between rocket and Earth
    angle_text.set_text(f'Angle: {angle:.2f}°')  # Update angle text
    distance_text.set_text(f'Distance: {distance:.2e} m')  # Update distance text
    
    return rocket, earth, mars, line, angle_text, distance_text

ani = FuncAnimation(fig, animate, frames=len(t), init_func=init, interval=20, blit=True)
# ani.save('rocket_from_Moon_to_mars_updated.gif', writer='imagemagick', fps=30)
plt.show()

# Calculate angles and distances for each time step
angles = np.arctan2(y_transfer + y_earth[0] - y_earth, x_transfer + x_earth[0] - x_earth) * (180 / np.pi)

rocket_distances = []
for i in range(len(t)):
    if i < np.argmin(np.sqrt((x_transfer + x_earth[0] - x_mars)**2 + (y_transfer + y_earth[0] - y_mars)**2)):
        rocket_x = x_transfer[i] + x_earth[0]
        rocket_y = y_transfer[i] + y_earth[0]
    else:
        rocket_x = x_mars[i]
        rocket_y = y_mars[i]
    
    dx = rocket_x - x_earth[i]
    dy = rocket_y - y_earth[i]
    distance = np.sqrt(dx**2 + dy**2)
    rocket_distances.append(distance)

# Plot angle vs. time in days
plt.figure(figsize=(10, 5))
plt.plot(t / (24 * 3600), angles, label='Angle vs Time')
plt.xlabel('Time (days)')
plt.ylabel('Angle (degrees)')
plt.title('Angle between Rocket and Earth over Time')
plt.legend()
plt.grid(True)
plt.show()

# Plot distance vs. time in days
plt.figure(figsize=(10, 5))
plt.plot(t / (24 * 3600), rocket_distances) 
plt.title('Distance Between Rocket and Earth Over Time')
plt.xlabel('Time (days)')
plt.ylabel('Distance (m)')
plt.grid(True)
plt.show()

        
