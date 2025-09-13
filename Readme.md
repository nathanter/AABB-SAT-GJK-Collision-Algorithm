# Everything about collisions

Implementations of the AABB, SAT, GJK and particle(with pruning) collision algorithms in python animated with pygame-ce

control shapes with arrow keys.

View supports shows support vectors for SAT

Add shape adds extra particles.


## Agorithms

### AABB 

works with rectangles.
Compares the max x and y values and min x and y values of each box
can be expressed in a simple equation

$$\text{min x}_\text{rectangle 1} >= \text{min x}_\text{rectange 2} \text{and} \text{ minx}_\text{rectangle 1} <= \text{max x}_\text{rectangle 2} $$


$$\text{max x}_\text{rectangle 1} >= \text{min x}_\text{rectange 2} \text{and} \text{ max x}_\text{rectangle 1} <= \text{max x}_\text{rectangle 2} $$


### SAT


Works by taking the equation of the normal lines to each side of each shape.

"Flattens" shapes against this normal line by taking the dot product of each vertex and the normal line.
The max and min point of each shape on this normal line are compared to see whether this line seperates the shapes.
If all normal lines fail this check then the shapes are colliding


### GJK

takes random direction, then takes the most and least "extreme" vertex of each shape in that directions.
Extreme just means farthest in a direction; this is determined by taking the dot product of the directions vector and all vertexes.

combines vector of most and least extreme vertexes to make simple shapes. This simple shape should be somewhat oriented around the center.


IE: if both vertexes are (2,1) the difference is 0 and the shapes which contain these vertexes are colliding that point.

Check if origin is inside the region of the simple shape. 

If not use a combination of dot products to take another direction to find the least and most extreme point.
