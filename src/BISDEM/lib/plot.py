import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def mechanimation2D(lpos,spos,speed):
    
    """ 
    Animates mechanism and wing movement in a 2D animation
    
    Input:
        
    lpos(MechLegPosVT): mechanism leg position information over time
    spos(SparPosVT):  spar position information over time
    speed(Float): desired animation speed (numbers around 10 recommended)
    
    Output:

    Animation
    
    """
    
    # Defines matrix of to be animated links in the reoccuring order x1,y1,x2,y2
     
    data = np.array([lpos.Q[0],lpos.Q[1],lpos.B[0],lpos.B[1],lpos.P[0],lpos.P[1],lpos.A[0],lpos.A[1],lpos.O[0],lpos.O[1],lpos.A[0],lpos.A[1],lpos.O[0],lpos.O[1],lpos.B[0],lpos.B[1], \
                     spos.O[0],spos.O[1],spos.C[0],spos.C[1],spos.C[0],spos.C[1],spos.E[0],spos.E[1],spos.A[0],spos.A[1],spos.E[0],spos.E[1],spos.C[0],spos.C[1],spos.D[0],spos.D[1]])
    
    fig = plt.figure()
    ax = plt.axes(xlim=(-0.1, 0.8), ylim=(-0.45, 0.45))
    
    # Initialize 
    lines = []
    for index in range(len(data)/4):
        lobj = ax.plot([],[],"r",lw=2)[0]
        lines.append(lobj)
    
    def init():
        for line in lines:
            line.set_data([],[])
        return lines
    
    def animate(i):
        
        for lnum,line in enumerate(lines):
    
            line.set_data((data[4*lnum,i],data[4*lnum+2,i]),(data[4*lnum+1,i],data[4*lnum+3,i]))
            
        return tuple(lines)
    
    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(lpos.P[0]), interval=speed, blit=False)
    plt.plot(lpos.Q[0],lpos.Q[1],'b')
    plt.plot(lpos.P[0],lpos.P[1],'b')
    plt.show()
    
def mechplot2D(mpos,wpos,i):
    
    """ 
    
    Plots front and back mechanism and wing traces in a 2D plot
    
    Input:
        
    mpos(MechPosVT): mechanism position information over time
    wpos(WingPosVT):  wing position information over time
    i(Float): instance to plot link position. For i=-1 no links are displayed
    
    Output:

    Plots
    
    """
   
    plt.figure('Front leg')
    plt.title('Mechanism front leg hinge traces')
    plt.axis('equal')
    
    plt.plot(mpos.front.Q[0],mpos.front.Q[1],'b')
    plt.plot(mpos.front.P[0],mpos.front.P[1],'b')
    plt.plot(mpos.front.B[0],mpos.front.B[1],'b')
    plt.plot(mpos.front.A[0],mpos.front.A[1],'b')
    plt.plot(mpos.front.O[0],mpos.front.O[1],'bx')
    
    plt.plot(wpos.front.E[0],wpos.front.E[1],'r')
    plt.plot(wpos.front.C[0],wpos.front.C[1],'r')
    plt.plot(wpos.front.D[0],wpos.front.D[1],'r')
    
    plt.plot(wpos.eqspar_geom[1].x, wpos.eqspar_geom[1].y, 'k*')
    
    if i>=0:

        plt.plot((mpos.front.B[0,i],0),(mpos.front.B[1,i],0),'g')
        plt.plot((mpos.front.B[0,i],mpos.front.Q[0,i]),(mpos.front.B[1,i],mpos.front.Q[1,i]),'g')
        plt.plot((mpos.front.A[0,i],mpos.front.P[0,i]),(mpos.front.A[1,i],mpos.front.P[1,i]),'g')
        plt.plot((mpos.front.A[0,i],0),(mpos.front.A[1,i],0),'g')
        
        plt.plot((wpos.front.A[0,i],wpos.front.E[0,i]),(wpos.front.A[1,i],wpos.front.E[1,i]),'g')
        plt.plot((wpos.front.O[0,i],wpos.front.C[0,i]),(wpos.front.O[1,i],wpos.front.C[1,i]),'g')
        plt.plot((wpos.front.C[0,i],wpos.front.E[0,i]),(wpos.front.C[1,i],wpos.front.E[1,i]),'g')
        plt.plot((wpos.front.C[0,i],wpos.front.D[0,i]),(wpos.front.C[1,i],wpos.front.D[1,i]),'g')
      
    plt.figure('Back leg')
    plt.title('Mechanism front back hinge traces')
    plt.axis('equal')
    
    plt.plot(mpos.back.Q[0],mpos.back.Q[1],'b')
    plt.plot(mpos.back.P[0],mpos.back.P[1],'b')
    plt.plot(mpos.back.B[0],mpos.back.B[1],'b')
    plt.plot(mpos.back.A[0],mpos.back.A[1],'b')
    plt.plot(mpos.back.O[0],mpos.back.O[1],'bx')
    
    plt.plot(wpos.back.E[0],wpos.back.E[1],'r')
    plt.plot(wpos.back.C[0],wpos.back.C[1],'r')
    plt.plot(wpos.back.D[0],wpos.back.D[1],'r')

    if i>=0:

        plt.plot((mpos.back.B[0,i],0),(mpos.back.B[1,i],0),'g')
        plt.plot((mpos.back.B[0,i],mpos.back.Q[0,i]),(mpos.back.B[1,i],mpos.back.Q[1,i]),'g')
        plt.plot((mpos.back.A[0,i],mpos.back.P[0,i]),(mpos.back.A[1,i],mpos.back.P[1,i]),'g')
        plt.plot((mpos.back.A[0,i],0),(mpos.back.A[1,i],0),'g')
        
        plt.plot((wpos.back.A[0,i],wpos.back.E[0,i]),(wpos.back.A[1,i],wpos.back.E[1,i]),'g')
        plt.plot((wpos.back.O[0,i],wpos.back.C[0,i]),(wpos.back.O[1,i],wpos.back.C[1,i]),'g')
        plt.plot((wpos.back.C[0,i],wpos.back.E[0,i]),(wpos.back.C[1,i],wpos.back.E[1,i]),'g')
        plt.plot((wpos.back.C[0,i],wpos.back.D[0,i]),(wpos.back.C[1,i],wpos.back.D[1,i]),'g')
    
    plt.show()