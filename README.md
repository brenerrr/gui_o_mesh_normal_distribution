# GUI O Mesh Normal Distribution

When working with a O mesh, it is often useful to specify how the grid should stretch in the normal direction y. In other words, how the grid should stretch when you "walk" from the airfoil wall towards the far field. For this you can use this GUI with the following steps:

- Choose how many points are there in the normal direction (ny);
- Start from a dy0 (this is the distance between the point at the airfoil surface (y0) and the next normal point (y1) (if this is too small you will be wasting computational resources but if it is too big you will lose too much accuracy) and increase dy values until reaching a dyFreeze after nyUntilFreeze points;
- Then dy will be kept the same until there are only nyFarField points left (I did this because I needed to maintain a fine mesh on the surroundings of the airfoil to properly capture the dynamic stall vortex as already mentioned);
- The idea now is to grow dy until dyFarField with the remaining points (if this is too small the far field will be close to the airfoil and this could be a problem but if it is too big the stretching could be too much and cause some weird effects on the boundaries of the domain). The truncateFarField is just for fine tuning things around the far field but overall this probably will not be needed. 


Press the Export button and a file called "y.csv" will be generated. 

