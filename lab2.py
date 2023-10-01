#!/usr/bin/env python3

# Standard imports as well as scipy:
from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt

def Ndt_predprey(t, N, a=1.0, b=2.0, c=1.0, d=3.0):
    '''
    This function calculates the Lotka-Volterra predator-prey equations for
    two sepcies. Given normalized populations, `N1` and `N2`, as well as the
    four coefficients representing population growth and decline,
    calculate the time derivatives dN_1/dt and dN_2/dt and return to the
    caller.

    This function accepts `t`, or time, as an input parameter to be
    compliant with Scipy's ODE solver. However, it is not used in this function.

    Parameters
    ----------
    t: float
        The current time (not used here).
    N: two-element list
        The current value of N1 and N2 as a list (e.g., [N1, N2]).
    a, b, c, d: float, defaults=1, 2, 1, 3
        The value of the Lotka-Volterra coefficients.

    Returns
    -------
    dN1dt, dN2dt: floats
        The time derivatives of `N1` and `N2`. 
    '''
    # Here, N is a two element list such that N1=N[0] and N2=N[1]
    dN1dt = a * N[0] - b*N[0]*N[1]
    dN2dt = -1 * c * N[1] + d * N[0]*N[1]

    return dN1dt, dN2dt
def Ndt_comp(t, N, a=1, b=2, c=1, d=3):
    '''
    This function calculates the Lotka-Volterra competition equations for
    two species. Given normalized populations, `N1` and `N2`, as well as the
    four coefficients representing population growth and decline,
    calculate the time derivatives dN_1/dt and dN_2/dt and return to the
    caller.

    This function accepts `t`, or time, as an input parameter to be
    compliant with Scipy's ODE solver. However, it is not used in this function.

    Parameters
    ----------
    t: float
        The current time (not used here).
    N: two-element list
        The current value of N1 and N2 as a list (e.g., [N1, N2]).
    a, b, c, d: float, defaults=1, 2, 1, 3
        The value of the Lotka-Volterra coefficients.

    Returns
    -------
    dN1dt, dN2dt: floats
        The time derivatives of `N1` and `N2`.
    '''

    # Here, N is a two element list such that N1=N[0] and N2=N[1]
    dN1dt = a*N[0]*(1-N[0]) - b*N[0]*N[1]
    dN2dt = c*N[1]*(1-N[1]) - d*N[1]*N[0]
    
    return dN1dt, dN2dt

def euler_solve(func, N1_init=.5, N2_init=.5, dT=.1, t_final=100.0, a=1, b=2, c=1, d=3):
    '''
    Solve the Lotka-Volterra competition and predator/prey equations using
    Euler's Method. Given a python function, the initial values of N1 and N2,
    the time step, and the final time, return the time elapsed as an array and
    the normalized population density solutions.

    Parameters
    ----------
    func: function
        A python function that takes `time`, [`N1`, `N2`] as inputs and
        returns the time derivative of N1 and N2.
    N1_init, N2_init: float
        Initial conditions for `N1` and `N2`, ranging from (0, 1]
    dT: float, default=0.1
        Timestep in years.
    t_final: float, default=100
        Integrate until this value is reached, in years.
    a,b,c,d: floats, defaults=1, 2, 1, 3
        The value of the Lotka-Volterra coefficients.
    Returns
    -------
    time: Numpy array
        Time elapsed in years.
    N1, N2: Numpy arrays
        Normalized population density solutions
    '''

    # Create time array.
    time = np.arange(0, t_final, dT)
    
    # Create containers for the solution, set initial condition.
    N1 = np.zeros(time.size)
    N2 = np.zeros(time.size)
    N1[0] = N1_init
    N2[0] = N2_init

    # Integrate forward:
    for i in range(1, time.size):
        dN1, dN2 = func(i, [N1[i-1], N2[i-1]])
        N1[i] = N1[i-1] + dT*dN1
        N2[i] = N2[i-1] + dT*dN2

    return time, N1, N2

def solve_rk8(func, N1_init=.5, N2_init=.5, dT=10, t_final=100.0, a=1, b=2, c=1, d=3):
    '''
    Solve the Lotka-Volterra competition and predator/prey equations using Scipy's ODE
    class and the adaptive step 8th order solver.

    Parameters
    ----------
    func: function
        A python function that takes `time`, [`N1`, `N2`] as inputs and returns the time
        derivative of N1 and N2.
    N1_init, N2_init: float
        Initial conditions for `N1` and `N2`, ranging from (0,1]
    dT: float, default=10
        Largest timestep allowed in years.
    t_final: float, default=100
        Integrate until this value is reached, in years.
    a, b, c, d: float, default=1, 2, 1, 3
        Lotka-Volterra coefficient values
    
    Returns
    -------
    time: Numpy array
        Time elapsed in years
    N1, N2: Numpy arrays
        Normalized population density solutions.
    '''

    # Configure the initial value problem solver
    result = solve_ivp(func, [0, t_final], [N1_init, N2_init], args=[a, b, c, d],
                       method='DOP853', max_step=dT)
    
    # Perform the integration
    time, N1, N2 = result.t, result.y[0, :], result.y[1, :]

    # Return values to caller.
    return time, N1, N2

def problem_one():
    '''
    This fuction solves the first problem in the assignment. 
    '''

    # Define our constants for this problem.
    a = 1
    b = 2
    c = 1
    d = 3
    max_T = 100
    init_N1 = 0.3
    init_N2 = 0.6

    # Define our changing values.
    comp_step = 1 # Euler time step for the competition model
    prey_step = 0.05 # Euler time step for the prey model

    # Run our models for the competition model.
    time_euler, N1_euler, N2_euler = euler_solve(Ndt_comp, N1_init=init_N1, N2_init=init_N2, dT=comp_step, t_final=max_T)
    time_rk, N1_rk, N2_rk = solve_rk8(Ndt_comp, N1_init=init_N1, N2_init=init_N2, t_final=max_T)

    # Plot our first graph.
    fig, axes = plt.subplots(1, 2, figsize=(10, 6))
    axes[0].plot(time_euler, N1_euler, ls='solid',color='C2',label='N1 Euler')
    axes[0].plot(time_euler, N2_euler, ls='solid',color='C3', label='N2 Euler')
    axes[0].plot(time_rk, N1_rk, ls='dashed',color='C2',label='N1 RKB')
    axes[0].plot(time_rk, N2_rk, ls='dashed',color='C3',label='N2 RKB')
    axes[0].set_title("Lotka-Volterra Competition Model")
    axes[0].legend()
    axes[0].set_xlabel('Time (years)')
    axes[0].set_ylabel('Population/Carrying Cap.')
    
    # Run our models for the predator-prey model.
    time_euler, N1_euler, N2_euler = euler_solve(Ndt_predprey, N1_init=init_N1, N2_init=init_N2, dT=prey_step, t_final=max_T)
    time_rk, N1_rk, N2_rk = solve_rk8(Ndt_predprey, N1_init=init_N1, N2_init=init_N2, t_final=max_T)

    # Plot our second graph.
    axes[1].plot(time_euler, N1_euler, ls='solid',color='C2',label='N1 (Prey) Euler')
    axes[1].plot(time_euler, N2_euler, ls='solid',color='C3', label='N2 (Predator) Euler')
    axes[1].plot(time_rk, N1_rk, ls='dashed',color='C2',label='N1 (Prey) RKB')
    axes[1].plot(time_rk, N2_rk, ls='dashed',color='C3',label='N2 (Predator) RKB')
    axes[1].set_title("Lotka-Volterra Predator-Prey Model")
    axes[1].legend()
    axes[1].set_xlabel('Time (years)')
    axes[1].set_ylabel('Population/Carrying Cap.')

    fig.suptitle("Coefficients: a=1, b=2, c=1, d=3")
    fig.show()
    fig.savefig(fname="question_one_init_lab2.png")
    
    for step in np.linspace(0.1, 2, 10):
         # Run our models for the competition model.
        time_euler, N1_euler, N2_euler = euler_solve(Ndt_comp, N1_init=init_N1, N2_init=init_N2, dT=step, t_final=max_T)
        time_rk, N1_rk, N2_rk = solve_rk8(Ndt_comp, N1_init=init_N1, N2_init=init_N2, t_final=max_T, dT=step)

        # Plot our first graphs.
        fig, axes = plt.subplots(1, 1, figsize=(10, 6))
        axes.plot(time_euler, N1_euler, ls='solid',color='C2',label='N1 Euler')
        axes.plot(time_euler, N2_euler, ls='solid',color='C3', label='N2 Euler')
        axes.plot(time_rk, N1_rk, ls='dashed',color='C2',label='N1 RKB')
        axes.plot(time_rk, N2_rk, ls='dashed',color='C3',label='N2 RKB')
        axes.set_title("Lotka-Volterra Competition Model")
        axes.legend()
        axes.set_xlabel('Time (years)')
        axes.set_ylabel('Population/Carrying Cap.')
    
        fig.suptitle("Coefficients: a=1, b=2, c=1, d=3; Step: " + str(step))
#        fig.show()
        fig.savefig(fname="question_one_"+str(step)+"comp_lab2.png")
    
    for step in np.linspace(0.01, 0.1, 10):
        # Run our models for the predator-prey model.
        time_euler, N1_euler, N2_euler = euler_solve(Ndt_predprey, N1_init=init_N1, N2_init=init_N2, dT=step, t_final=max_T)
        time_rk, N1_rk, N2_rk = solve_rk8(Ndt_predprey, N1_init=init_N1, N2_init=init_N2, dT=step,t_final=max_T)    

         # Plot our second graphs.
        fig, axes = plt.subplots(1, 1, figsize=(10, 6))
        axes.plot(time_euler, N1_euler, ls='solid',color='C2',label='N1 (Prey) Euler')
        axes.plot(time_euler, N2_euler, ls='solid',color='C3', label='N2 (Predator) Euler')
        axes.plot(time_rk, N1_rk, ls='dashed',color='C2',label='N1 (Prey) RKB')
        axes.plot(time_rk, N2_rk, ls='dashed',color='C3',label='N2 (Predator) RKB')
        axes.set_title("Lotka-Volterra Predator-Prey Model")
        axes.legend()
        axes.set_xlabel('Time (years)')
        axes.set_ylabel('Population/Carrying Cap.')
    
        fig.suptitle("Coefficients: a=1, b=2, c=1, d=3; Step: " + str(step))
#        fig.show()
        fig.savefig(fname="question_one_"+str(step)+"predprey_lab2.png")
def problem_two():
    '''
    This function solves the second problem in the assignment.
    '''
     # Define our constants for this problem.
    max_T = 100
    comp_step = 1

    # Define our changing values.
    a = 1
    b = 2
    c = 1
    d = 3
    init_N1 = 0.3
    init_N2 = 0.6
    for init_N1 in np.linspace(0.1, 0.5, 5): # Vary initial N1
        time_rk, N1_rk, N2_rk = solve_rk8(Ndt_comp, N1_init=init_N1, N2_init=init_N2, t_final=max_T, dT = comp_step)
        fig, axes = plt.subplots(1, 1, figsize=(10, 6))
        axes.plot(time_rk, N1_rk, ls='dashed',color='C2',label='N1 RKB')
        axes.plot(time_rk, N2_rk, ls='dashed',color='C3',label='N2 RKB')
        axes.set_title("Lotka-Volterra Competition Model")
        axes.legend()
        axes.set_xlabel('Time (years)')
        axes.set_ylabel('Population/Carrying Cap.')
    
        fig.suptitle("Coefficients: a=1, b=2, c=1, d=3; initial N1: " + str(init_N1))
#        fig.show()
        fig.savefig(fname="question_two_varied_N1"+str(init_N1)+"comp_lab2.png")
    init_N1 = 0.3 # Reset initial N1 back to original value.
    for init_N2 in np.linspace(0.1,0.5,5): # Vary N2
        time_rk, N1_rk, N2_rk = solve_rk8(Ndt_comp, N1_init=init_N1, N2_init=init_N2, t_final=max_T, dT = comp_step)
        fig, axes = plt.subplots(1, 1, figsize=(10, 6))
        axes.plot(time_rk, N1_rk, ls='dashed',color='C2',label='N1 RKB')
        axes.plot(time_rk, N2_rk, ls='dashed',color='C3',label='N2 RKB')
        axes.set_title("Lotka-Volterra Competition Model")
        axes.legend()
        axes.set_xlabel('Time (years)')
        axes.set_ylabel('Population/Carrying Cap.')
    
        fig.suptitle("Coefficients: a=1, b=2, c=1, d=3; initial N2: " + str(init_N2))
#        fig.show()
        fig.savefig(fname="question_two_varied_N2"+str(init_N2)+"comp_lab2.png")
    init_N2 = 0.6 # Reset initial N2 back to original value
    for a in range(1,5): # Vary a
        time_rk, N1_rk, N2_rk = solve_rk8(Ndt_comp, N1_init=init_N1, N2_init=init_N2, t_final=max_T, dT = comp_step, a=a)
        fig, axes = plt.subplots(1, 1, figsize=(10, 6))
        axes.plot(time_rk, N1_rk, ls='dashed',color='C2',label='N1 RKB')
        axes.plot(time_rk, N2_rk, ls='dashed',color='C3',label='N2 RKB')
        axes.set_title("Lotka-Volterra Competition Model")
        axes.legend()
        axes.set_xlabel('Time (years)')
        axes.set_ylabel('Population/Carrying Cap.')
    
        fig.suptitle("Coefficients: a="+str(a)+", b=2, c=1, d=3")
#        fig.show()
        fig.savefig(fname="question_two_varied_a"+str(a)+"comp_lab2.png")
    a = 1 # Reset a back to original value
    for b in range(1,5): # Vary b
        time_rk, N1_rk, N2_rk = solve_rk8(Ndt_comp, N1_init=init_N1, N2_init=init_N2, t_final=max_T, dT = comp_step, b=b)
        fig, axes = plt.subplots(1, 1, figsize=(10, 6))
        axes.plot(time_rk, N1_rk, ls='dashed',color='C2',label='N1 RKB')
        axes.plot(time_rk, N2_rk, ls='dashed',color='C3',label='N2 RKB')
        axes.set_title("Lotka-Volterra Competition Model")
        axes.legend()
        axes.set_xlabel('Time (years)')
        axes.set_ylabel('Population/Carrying Cap.')
    
        fig.suptitle("Coefficients: a=1,b="+str(b)+",c=1, d=3")
#        fig.show()
        fig.savefig(fname="question_two_varied_b"+str(b)+"comp_lab2.png")
    b = 2 # Reset b back to original value
    for c in range(1,5): # Vary c
        time_rk, N1_rk, N2_rk = solve_rk8(Ndt_comp, N1_init=init_N1, N2_init=init_N2, t_final=max_T, dT = comp_step, c=c)
        fig, axes = plt.subplots(1, 1, figsize=(10, 6))
        axes.plot(time_rk, N1_rk, ls='dashed',color='C2',label='N1 RKB')
        axes.plot(time_rk, N2_rk, ls='dashed',color='C3',label='N2 RKB')
        axes.set_title("Lotka-Volterra Competition Model")
        axes.legend()
        axes.set_xlabel('Time (years)')
        axes.set_ylabel('Population/Carrying Cap.')
    
        fig.suptitle("Coefficients: a=1,b=2,c="+str(c)+", d=3")
#        fig.show()
        fig.savefig(fname="question_two_varied_c"+str(c)+"comp_lab2.png")
    c = 1 # Reset c back to original value
    for d in range(1,5): # Vary d
        time_rk, N1_rk, N2_rk = solve_rk8(Ndt_comp, N1_init=init_N1, N2_init=init_N2, t_final=max_T, dT = comp_step, d=d)
        fig, axes = plt.subplots(1, 1, figsize=(10, 6))
        axes.plot(time_rk, N1_rk, ls='dashed',color='C2',label='N1 RKB')
        axes.plot(time_rk, N2_rk, ls='dashed',color='C3',label='N2 RKB')
        axes.set_title("Lotka-Volterra Competition Model")
        axes.legend()
        axes.set_xlabel('Time (years)')
        axes.set_ylabel('Population/Carrying Cap.')
    
        fig.suptitle("Coefficients: a=1,b=2,c=1,d="+str(d))
#        fig.show()
        fig.savefig(fname="question_two_varied_d"+str(d)+"comp_lab2.png")
    d = 5
    b = 0.1
    c = 5
    a = 0.1
    init_N1 = 0.5
    init_N2 = 0.5
    max_T = 100000 # Increase max T so we can ensure that the destabilization point is not simply further along.
    time_rk, N1_rk, N2_rk = solve_rk8(Ndt_comp, N1_init=init_N1, N2_init=init_N2, t_final=max_T, dT = comp_step, a=a, b=b,c=c,d=d)
    fig, axes = plt.subplots(1, 1, figsize=(10, 6))
    axes.plot(time_rk, N1_rk, ls='dashed',color='C2',label='N1 RKB')
    axes.plot(time_rk, N2_rk, ls='dashed',color='C3',label='N2 RKB')
    axes.set_title("Lotka-Volterra Competition Model")
    axes.legend()
    axes.set_xlabel('Time (years)')
    axes.set_ylabel('Population/Carrying Cap.')
    
    fig.suptitle("Coefficients: a=0.1,b=0.1,c=5,d=5; initial N1 = 0.5, initial N2 = 0.5.")
    fig.show()
    fig.savefig(fname="question_two_final_comp_lab2.png")
'''    for a in np.linspace(0.1, 5, 9):
        for b in np.linspace(0.1, 5, 9):
            for c in np.linspace(0.1, 5, 9):
                for d in np.linspace(0.1, 5, 9):
                    time_rk, N1_rk, N2_rk = solve_rk8(Ndt_comp, N1_init=init_N1, N2_init=init_N2, t_final=max_T, dT = comp_step, a=a, b=b,c=c,d=d)
                    if(N1_rk[-1] > 0.2 and N2_rk[-1] > 0.2):
                        print("a: "+ str(a) + ",b:"+str(b)+",c:"+str(c)+",d:"+str(d)+",N1_init:"+str(init_N1)+",N2_init:"+str(init_N2))
'''


def problem_three():
    '''
    This function solves the third problem in the assignment.
    '''
     # Define our constants for this problem.
    max_T = 100

    # Define our changing values.
    a = 1
    b = 2
    c = 1
    d = 3
    init_N1 = 0.3
    init_N2 = 0.6

    # Run our model
    time_rk, N1_rk, N2_rk = solve_rk8(Ndt_predprey, N1_init=init_N1, N2_init=init_N2, t_final=max_T, a=a, b=b,c=c,d=d)
    for init_N1 in np.linspace(0.1, 0.5, 3): # Vary initial N1
        time_rk, N1_rk, N2_rk = solve_rk8(Ndt_comp, N1_init=init_N1, N2_init=init_N2, t_final=max_T)
        fig, axes = plt.subplots(1, 2, figsize=(10, 6))
        # Time plot
        axes[0].plot(time_rk, N1_rk, ls='dashed',color='C2',label='N1 RKB')
        axes[0].plot(time_rk, N2_rk, ls='dashed',color='C3',label='N2 RKB')
        axes[0].set_title("Plot over Time")
        axes[0].legend()
        axes[0].set_xlabel('Time (years)')
        axes[0].set_ylabel('Population/Carrying Cap.')
        
        # Phase plot
        axes[1].plot(N1_rk, N2_rk)
        axes[1].set_title("Phase Diagram")
        axes[1].set_xlabel("N1 Population/Carrying Cap.")
        axes[1].set_ylabel("N2 Population/Carrying Cap.")    
        fig.suptitle("Lotka-Volterra Predator-Prey Model. Coefficients: a=1, b=2, c=1, d=3; initial N1: " + str(init_N1))
#        fig.show()
        fig.savefig(fname="question_three_varied_N1"+str(init_N1)+"predprey_lab2.png")
    init_N1 = 0.3 # Reset initial N1 back to original value.
    for init_N2 in np.linspace(0.1,0.5,3): # Vary N2
        time_rk, N1_rk, N2_rk = solve_rk8(Ndt_comp, N1_init=init_N1, N2_init=init_N2, t_final=max_T)
        fig, axes = plt.subplots(1, 2, figsize=(10, 6))
        # Time plot
        axes[0].plot(time_rk, N1_rk, ls='dashed',color='C2',label='N1 RKB')
        axes[0].plot(time_rk, N2_rk, ls='dashed',color='C3',label='N2 RKB')
        axes[0].set_title("Plot over Time")
        axes[0].legend()
        axes[0].set_xlabel('Time (years)')
        axes[0].set_ylabel('Population/Carrying Cap.')
        # Phase plot
        axes[1].plot(N1_rk, N2_rk)
        axes[1].set_title("Phase Diagram")
        axes[1].set_xlabel("N1 Population/Carrying Cap.")
        axes[1].set_ylabel("N2 Population/Carrying Cap.")
    
        fig.suptitle("Lotka-Volterra Predator-Prey Model. Coefficients: a=1, b=2, c=1, d=3; initial N2: " + str(init_N2))
#        fig.show()
        fig.savefig(fname="question_three_varied_N2"+str(init_N2)+"predprey_lab2.png")
    init_N2 = 0.6 # Reset initial N2 back to original value
    for a in range(1,5): # Vary a
        time_rk, N1_rk, N2_rk = solve_rk8(Ndt_comp, N1_init=init_N1, N2_init=init_N2, t_final=max_T, a=a,b=b,c=c,d=d)
        fig, axes = plt.subplots(1, 2, figsize=(10, 6))
        # Time plot
        axes[0].plot(time_rk, N1_rk, ls='dashed',color='C2',label='N1 RKB')
        axes[0].plot(time_rk, N2_rk, ls='dashed',color='C3',label='N2 RKB')
        axes[0].set_title("Plot over Time")
        axes[0].legend()
        axes[0].set_xlabel('Time (years)')
        axes[0].set_ylabel('Population/Carrying Cap.')
        # Phase plot
        axes[1].plot(N1_rk, N2_rk)
        axes[1].set_title("Phase Diagram")
        axes[1].set_xlabel("N1 Population/Carrying Cap.")
        axes[1].set_ylabel("N2 Population/Carrying Cap.")
    
        fig.suptitle("Lotka-Volterra Predator-Prey Model. Coefficients: a="+str(a)+", b=2, c=1, d=3")
#        fig.show()
        fig.savefig(fname="question_three_varied_a"+str(a)+"predprey_lab2.png")
    a = 1 # Reset a back to original value
    for b in range(1,5): # Vary b
        time_rk, N1_rk, N2_rk = solve_rk8(Ndt_comp, N1_init=init_N1, N2_init=init_N2, t_final=max_T, a=a,b=b,c=c,d=d)
        fig, axes = plt.subplots(1, 2, figsize=(10, 6))
        # Time plot
        axes[0].plot(time_rk, N1_rk, ls='dashed',color='C2',label='N1 RKB')
        axes[0].plot(time_rk, N2_rk, ls='dashed',color='C3',label='N2 RKB')
        axes[0].set_title("Plot over Time")
        axes[0].legend()
        axes[0].set_xlabel('Time (years)')
        axes[0].set_ylabel('Population/Carrying Cap.')
        # Phase plot
        axes[1].plot(N1_rk, N2_rk)
        axes[1].set_title("Phase Diagram")
        axes[1].set_xlabel("N1 Population/Carrying Cap.")
        axes[1].set_ylabel("N2 Population/Carrying Cap.")
    
        fig.suptitle("Lotka-Volterra Predator-Prey Model. Coefficients: a=1, b="+str(b)+", c=1, d=3")
#        fig.show()
        fig.savefig(fname="question_three_varied_b"+str(b)+"predprey_lab2.png")
    b = 2 # Reset b back to original value
    for c in range(1,5): # Vary c
        time_rk, N1_rk, N2_rk = solve_rk8(Ndt_comp, N1_init=init_N1, N2_init=init_N2, t_final=max_T, a=a,b=b,c=c,d=d)
        fig, axes = plt.subplots(1, 2, figsize=(10, 6))
        # Time plot
        axes[0].plot(time_rk, N1_rk, ls='dashed',color='C2',label='N1 RKB')
        axes[0].plot(time_rk, N2_rk, ls='dashed',color='C3',label='N2 RKB')
        axes[0].set_title("Plot over Time")
        axes[0].legend()
        axes[0].set_xlabel('Time (years)')
        axes[0].set_ylabel('Population/Carrying Cap.')
        # Phase plot
        axes[1].plot(N1_rk, N2_rk)
        axes[1].set_title("Phase Diagram")
        axes[1].set_xlabel("N1 Population/Carrying Cap.")
        axes[1].set_ylabel("N2 Population/Carrying Cap.")
    
        fig.suptitle("Lotka-Volterra Predator-Prey Model. Coefficients: a=1,b=2,c="+str(c)+", d=3")
#        fig.show()
        fig.savefig(fname="question_three_varied_c"+str(c)+"predprey_lab2.png")
    c = 1 # Reset c back to original value
    for d in range(1,5): # Vary d
        time_rk, N1_rk, N2_rk = solve_rk8(Ndt_comp, N1_init=init_N1, N2_init=init_N2, t_final=max_T, a=a,b=b,c=c,d=d)
        fig, axes = plt.subplots(1, 2, figsize=(10, 6))
        # Time plot
        axes[0].plot(time_rk, N1_rk, ls='dashed',color='C2',label='N1 RKB')
        axes[0].plot(time_rk, N2_rk, ls='dashed',color='C3',label='N2 RKB')
        axes[0].set_title("Plot over Time")
        axes[0].legend()
        axes[0].set_xlabel('Time (years)')
        axes[0].set_ylabel('Population/Carrying Cap.')
        # Phase plot
        axes[1].plot(N1_rk, N2_rk)
        axes[1].set_title("Phase Diagram")
        axes[1].set_xlabel("N1 Population/Carrying Cap.")
        axes[1].set_ylabel("N2 Population/Carrying Cap.")
    
        fig.suptitle("Lotka-Volterra Predator-Prey Model. Coefficients: a=1,b=2,c=1,d="+str(d))
#        fig.show()
        fig.savefig(fname="question_two_varied_d"+str(d)+"comp_lab2.png")


problem_one() # Run problem one
problem_two() # Run problem two
problem_three() # Run problem three