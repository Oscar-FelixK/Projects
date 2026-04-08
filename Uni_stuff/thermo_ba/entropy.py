import Uni_stuff.thermo_ba.ba as ba
import numpy as np
import random
import matplotlib.pyplot as plt
import copy
import math 
#
# function to perform site exchange MC step
#
def doMC():
    #
    # Randomly choose the x and y coordinates of two sites of differeing type
    #
    ix1=np.random.randint(mySystem.Nx)
    iy1=np.random.randint(mySystem.Ny)
    type1=mySystem.latticeState[ix1,iy1]
    type2=type1
    while (type2==type1):
        ix2=np.random.randint(mySystem.Nx)
        iy2=np.random.randint(mySystem.Ny)
        type2=mySystem.latticeState[ix2,iy2]
    #
    # Change the chosen site's state, calculate the change in eneryy
    #
    deltaEnergy=mySystem.changeSiteState(ix1,iy1)
    deltaEnergy+=mySystem.changeSiteState(ix2,iy2)
    #
    # Perform site exchange MC step
    #
    if (deltaEnergy>0.0):
        if (random.random()<np.exp(-beta*deltaEnergy)):
            return deltaEnergy,True
        else:
            #
            # Undo the change if the energy increases
            #
            mySystem.changeSiteState(ix1,iy1,calcDeltaEnergy=False)
            mySystem.changeSiteState(ix2,iy2,calcDeltaEnergy=False)
            return 0.0,False
    else:
        #
        # If the energy decreases update the current total energy
        #
        return deltaEnergy,True
#
# Initialize system (10*10 lattice)
#
mySystem=ba.baClass(Nx=10,Ny=10,J00=0.15,J11=0.15,J01=-0.15,concentration=0.1) #Omega<0
#mySystem=ba.baClass(Nx=10,Ny=10,J00=-0.5,J11=-0.5,J01=0.5,concentration=0.12) #Omega>0
#
# Record the initial state for later visualization
#
initialState=copy.deepcopy(mySystem.latticeState)
#
# Calculate initial total energy 
#
currentEnergy=mySystem.calcEnergy()
#
# Define temperature quench range
#
temperatureStart=6.0
temperatureEnd=0.01
temperatureDelta=0.01
#
# Set number of equilibriation MC sweeps per temperature
#
equilibriumMCSweepNumber=1
equilibriumNumber=equilibriumMCSweepNumber*mySystem.Nx*mySystem.Ny
#
# Set number of sampling MC sweeps per temperature
#
iterationMCSweepNumber=10
iterationNumber=iterationMCSweepNumber*mySystem.Nx*mySystem.Ny
#
# Initialize lists which record simulation evolution
#
temperatureEvolution=[]
acceptFractionEvolution=[]
averageEnergyEvolution=[]
averageHeatCapacityEvolution=[]
#
# Quench from temperature temperatureStart to temperatureEnd measuring energy and internal energy
#
for temperature in np.arange(temperatureStart,temperatureEnd-temperatureDelta,-temperatureDelta):
    #
    # Define inverse temperature
    #
    beta=1.0/temperature
    #
    # Perform equilibriumNumber MC steps before sampling observables
    #
    for i in range(equilibriumNumber):
        deltaEnergy,accept=doMC()
        currentEnergy+=deltaEnergy
    #
    # Perform iterationNumner MC steps
    #
    averageEnergy=0.0
    averageEnergy2=0.0
    acceptNumber=0
    #
    # Perform iterationNumber MC sweeps to calculate averqages
    #
    for i in range(iterationNumber):
        deltaEnergy,accept=doMC()
        if accept: acceptNumber+=1
        currentEnergy+=deltaEnergy
        averageEnergy+=currentEnergy
        averageEnergy2+=currentEnergy**2
    averageEnergy/=float(iterationNumber)
    averageHeatCapacity=(averageEnergy2/float(iterationNumber)-averageEnergy**2)/temperature**2
    #
    # Record system variables for later plotting
    #
    temperatureEvolution.append(temperature)
    acceptFractionEvolution.append(float(acceptNumber)/float(iterationNumber))
    averageEnergyEvolution.append(averageEnergy/float(mySystem.siteNumber))
    averageHeatCapacityEvolution.append(averageHeatCapacity/float(mySystem.siteNumber))
#
# Calculate the ideal solid solution internal energy and entropy (large T) 
#
x0=float(mySystem.type0SiteNumber)/float(mySystem.siteNumber)
x1=float(mySystem.type1SiteNumber)/float(mySystem.siteNumber)
highTemperatureU=0.5*mySystem.J00*4.0*x0+0.5*mySystem.J11*4.0*x1+4.0*x0*x1*(mySystem.J01-0.5*(mySystem.J00+mySystem.J11))
highTemperatureS=-(x0*np.log(x0)+x1*np.log(x1))
#
# Cacluate entropy via thermodynamic integration of C(T)/T
#        
entropyEvolution=[]
dt=temperatureEvolution[1]-temperatureEvolution[0]
currentEntropyInt=highTemperatureS
for it in range(len(temperatureEvolution)):
    currentEntropyInt += (dt) * (averageHeatCapacityEvolution[it]/temperatureEvolution[it])
    entropyEvolution.append(currentEntropyInt)
#
# Fill in the numerical integration, appending each integral to the list entropyEvolution 
#
    
#
# Define subplot arrangement
#
fig = plt.figure(constrained_layout=True)
gs = fig.add_gridspec(3,2)
panel00 = fig.add_subplot(gs[0,0])
panel01 = fig.add_subplot(gs[0,1])
panel10 = fig.add_subplot(gs[1,0])
panel11 = fig.add_subplot(gs[1,1])
panel20 = fig.add_subplot(gs[2,0])
panel21 = fig.add_subplot(gs[2,1])
#
# Plot the energy evolution
#
panel00.set_xlabel(r'temperature')
panel00.set_ylabel(r'internal energy per site')
panel00.plot(temperatureEvolution,averageEnergyEvolution,c='C0',label='simulation')
panel00.axhline(highTemperatureU,c='C1',label='ideal solid solution')
handles, labels = panel00.get_legend_handles_labels()
panel00.legend(handles, labels)
panel00.text(-0.3,0.95,'a)',transform=panel00.transAxes)
#
# Plot the heat capacity evolution
#
panel01.set_xlabel(r'temperature')
panel01.set_ylabel(r'heat capacity per site')
panel01.plot(temperatureEvolution,averageHeatCapacityEvolution)
panel01.text(-0.3,0.95,'b)',transform=panel01.transAxes)
#
# Visualize the initial configuration
#
panel10.set_xlabel(r'x position')
panel10.set_ylabel(r'y position')
panel10.matshow(initialState,extent=(0,mySystem.Nx,mySystem.Ny,0),aspect="auto",vmin=0,vmax=1)
panel10.xaxis.set_ticks_position('bottom')
panel10.text(-0.3,0.95,'c)',transform=panel10.transAxes)
#
# Visualize the final configuration
#
panel11.set_xlabel(r'x position')
panel11.set_ylabel(r'y position')
panel11.matshow(mySystem.latticeState,extent=(0,mySystem.Nx,mySystem.Ny,0),aspect="auto",vmin=0,vmax=1)
panel11.xaxis.set_ticks_position('bottom')
panel11.text(-0.3,0.95,'d)',transform=panel11.transAxes)
#
# Plot the fraction of accepted MC moves
#
panel20.set_xlabel(r'temperature')
panel20.set_ylabel(r'MC accept fraction')
panel20.plot(temperatureEvolution,acceptFractionEvolution)
panel20.text(-0.3,0.95,'e)',transform=panel20.transAxes)
#
# Plot the entropy evolution
#
panel21.set_xlabel(r'temperature')
panel21.set_ylabel(r'entropy per site')
panel21.plot(temperatureEvolution,entropyEvolution,label='simulation')
panel21.axhline(highTemperatureS,c='C1',label='ideal solid solution')
handles, labels = panel21.get_legend_handles_labels()
panel21.legend(handles, labels)
panel21.text(-0.3,0.95,'f)',transform=panel21.transAxes)
#
#
# Set figure size and plot
#
fig.set_figheight(15)
fig.set_figwidth(12)
plt.show()
fig.savefig('0quenchMCEntropy_'+str(iterationMCSweepNumber)+'.png') 