import numpy as np
import math

def triangle(A,B,a,b,c):
    
    """ 
    Calculates position of third point (C) in triangle (ABC) which lies in the xy-plane
    
    Input:
        
    Positions of points A and B
    Lengths of sides a,b,c
    
    Output:
    
    The two possible positions of point C. In case C1 is the point right to vector AB and C2 is left to vector AB.
    
    Note: Calculation is done according to http://math.stackexchange.com/questions/543961/determine-third-point-of-triangle-when-two-points-and-all-sides-are-known
    """
    
    x = (a**2-b**2-c**2)/(-2*c)
    
    y1 =np.sqrt(b**2-x**2)  #np.sqrt(a**2-(x-b)**2) #
    y2 = -y1
    
    # Transformation into actual coordinate system
    
    AB = B-A
    ABperp = np.array([-AB[1], AB[0], np.zeros(len(A[2]))])
    C1 = A + x/c * AB + y2/c * ABperp
    C2 = A + x/c * AB - y2/c * ABperp
    
    return C1, C2

def rotx(theta,x):
    
    """
    Rotate vector x around x axis with angle theta    
    """
    
    R_x = np.array([[1.,    0.,             0.],
                    [0.,    np.cos(theta),  -np.sin(theta)],
                    [0.,    np.sin(theta), np.cos(theta)]])
    
    return np.dot(R_x,x)

def roty(theta,x):
    
    """
    Rotate vector x around y axis with angle theta  
    """
       
    R_y = np.array([[np.cos(theta),     0.,     np.sin(theta)],
                    [0.,                1.,     0.],
                    [-np.sin(theta),    0.,     np.cos(theta)]])
    
    return np.dot(R_y,x)

def rotz(theta,x):
    
    """
    Rotate vector x around z axis with angle theta         
    """
    
    R_z = np.array([[np.cos(theta),     -np.sin(theta),     0.],
                    [np.sin(theta),     np.cos(theta),      0.],
                    [0.,                0.,                 1.]])
    
    return np.dot(R_z,x)

def rot_axis(axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    axis = np.asarray(axis)
    theta = np.asarray(theta)
    axis = axis/math.sqrt(np.dot(axis, axis))
    a = math.cos(theta/2)
    b, c, d = -axis*math.sin(theta/2)
    aa, bb, cc, dd = a*a, b*b, c*c, d*d
    bc, ad, ac, ab, bd, cd = b*c, a*d, a*c, a*b, b*d, c*d
    return np.array([[aa+bb-cc-dd, 2*(bc+ad), 2*(bd-ac)],
                     [2*(bc-ad), aa+cc-bb-dd, 2*(cd+ab)],
                     [2*(bd+ac), 2*(cd-ab), aa+dd-bb-cc]])