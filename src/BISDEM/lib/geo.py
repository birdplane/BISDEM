import numpy as np

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

def rotx(theta,x1):
    
    """
    Rotate vector x1 around x axis with angle theta    
    """
    
    R_x = np.array([[1.,    0.,             0.],
                    [0.,    np.cos(theta),  np.sin(theta)],
                    [0.,    -np.sin(theta), np.cos(theta)]])
    
    return np.dot(R_x,x1)

def roty(theta,x1):
    
    """
    Rotate vector x1 around y axis with angle theta  
    """
       
    R_y = np.array([[np.cos(theta),     0.,     np.sin(theta)],
                    [0.,                1.,     0.],
                    [-np.sin(theta),    0.,     np.cos(theta)]])
    
    return np.dot(R_y,x1)

def rotz(theta,x1):
    
    """
    Rotate vector x1 around z axis with angle theta         
    """
    
    R_z = np.array([[np.cos(theta),     -np.sin(theta),     0.],
                    [np.sin(theta),     np.cos(theta),      0.],
                    [0.,                0.,                 1.]])
    
    return np.dot(R_z,x1)