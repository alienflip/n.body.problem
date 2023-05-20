# Python Implementations


## Versions

This directory contains Pyhon implementations of the N-Body-Problem:
- 2d+1 version in `2d_sim.py`
- 3d version in `3d_sim.py`, with additional rendering and interactivity features.

https://github.com/tristandeborde/N-Body-Problem/assets/33256624/1262dd93-0413-4f05-be09-38a682ac6447

## Features

The driving idea behind the features is to increase the impression of 3d, otherwise hard to detect in a scene filled with quickly moving spheres.

- [x] Planet Trails: Display a trail of point on the n previous positions occupied by the body.
- [x] Attractor and Repulsor: Allow the user to influence the gravitational field. Left mouse button spawns an "attractor" with positive mass; right click button button spawns a "repulsor" with negative mass
- [ ] Collision Detection and Combining Bodies: Simulate bodies colliding and merging them into a larger body with bigger mass!
- [ ] 3D camera movement either through automatic rotation around the scene center, either through arrow keys movement. This doesn't seem trivial because it will influence the attractor/repulsor placement.
- [ ] Improved Rendering Beyond Plain Spheres: This idea aims to enhance the visual appeal of the simulation by rendering celestial bodies in more detail, rather than just plain spheres.

## How to Run

To use the Python implementation, activate the virtual environment and install the necessary dependencies, then run the script:

```
source ./bin/activate
./dependencies.sh
python3 Python/3d_sim.py
```
