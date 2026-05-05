import magpylib as magpy
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

# 1. Function to build the Square Coil
def create_square_coil(current, side_length, height, num_loops, x_offset):
    loops = []
    z_positions = np.linspace(-height/2, height/2, num_loops)
    s = side_length / 2
    vertices = [(-s, -s, 0), (s, -s, 0), (s, s, 0), (-s, s, 0), (-s, -s, 0)]
    
    for z in z_positions:
        lp = magpy.current.Polyline(current=current, vertices=vertices, position=(0,0,z))
        loops.append(lp)
    
    collection = magpy.Collection(loops)
    collection.move((x_offset, 0, 0)) 
    return collection

# 2. Build the system (Opposing currents: 100 and -100)
coil1 = create_square_coil(current=100, side_length=15, height=25, num_loops=30, x_offset=-8)
coil2 = create_square_coil(current=-100, side_length=15, height=25, num_loops=30, x_offset=8)
system = magpy.Collection(coil1, coil2)

# 3. Define the Grid slice (X-Z plane) - Lower density for clear arrows
xs = np.linspace(-35, 35, 25)
zs = np.linspace(-35, 35, 25)
X, Z = np.meshgrid(xs, zs)
grid = np.stack([X, np.zeros_like(X), Z], axis=-1)

# 4. Calculate B-field
B = system.getB(grid.reshape(-1, 3)).reshape(grid.shape)

# 5. Plotting (Vector Style)
fig, ax = plt.subplots(figsize=(8, 8))
B_mag = np.linalg.norm(B, axis=2)

# Normalize arrows so they are the same length, but colored by strength
# This makes it easier to see direction in weak areas
U = B[..., 0] / B_mag
W = B[..., 2] / B_mag

quiv = ax.quiver(X, Z, U, W, B_mag, cmap='turbo', pivot='mid', scale=30)

# 6. Add rectangles to represent the coil cross-sections
ax.add_patch(Rectangle((-15.5, -12.5), 15, 25, color='blue', alpha=0.1, edgecolor='black'))
ax.add_patch(Rectangle((0.5, -12.5), 15, 25, color='blue', alpha=0.1, edgecolor='black'))

ax.set_title("Magnetic Field Simulation of Oppositely Wound Square Coils")
ax.set_xlabel("X (mm)")
ax.set_ylabel("Z (mm)")
ax.set_aspect('equal')
plt.colorbar(quiv, label='Field Strength (mT)')
plt.show()