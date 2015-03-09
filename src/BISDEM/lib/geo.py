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
    ABperp = np.array([-AB[1], AB[0], A[2]])
    C1 = A + x/c * AB + y2/c * ABperp
    C2 = A + x/c * AB - y2/c * ABperp
    
    return C1, C2