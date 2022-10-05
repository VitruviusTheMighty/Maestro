### 09 - 19 - 2022
### CSC 245
### *Vector Math*

*The motion of balls is represented by a vector*

This vector is represented by a tuple.

--> (Vx, Vy)

**Adding vectors**
V1 + V2 = (v1x + v2x, v1y + v2y)

**Scalar Multipy**
*M* * V = (mvx * mvy)

**Getting vector length**
L = sqrt( vx^2 + vy^2 )

**Unit vector (norm)**
vector of L = I 

= (vx/L, vy/L)

**Dot product**
(v1x * v2x + v1y * v2y) --> *single number not a scalar*

-----------------------------------------------------------

v1 * (norm v2)

-----------------------------------------------------------
When two spheres collide, there are two vectors involved in collison.

- Vector joining two balls from each of their radii
- Vector orthagonal to this other vector

The **only** vector we care about is the one joining the two, based off of the original vectors of these balls..
what is their resulting collision vector?

-----------------------------------------------------------
**Momentum is conserved across collisions**
p = mv

m1v1 + m2v2 = m1v1 + m2v2

**Kinetic Energy**

KE = 1/2 * mv^2

(m1*v1^2)/2 + (m2*v2^2)/2 = 

v1 = ( v1 * (m1 - m2) + 2m2v2 ) / m1 + m2 
--**swap velocities upon contact**


---------------------------------------------------------------

**unit normal vector**

unit_norm = (norm) / sqrt( (normx^2 + normy^2) )