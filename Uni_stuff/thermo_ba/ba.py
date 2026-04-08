import random
import numpy as np

class baClass:
    """
    A class to simulate a two dimensional model binary alloy
    
    Attributes
    
    Nx : int
        periodicity length in x-direction
    Ny : int
        periodicity length in y-direction
    siteNumber : int
        number of lattice sites (Nx*Ny)
    type0SiteNumber : int
        number of type 0 sites
    type1SiteNumber : int
        number of type 1 sites
    J00 : float
        nearest neighbour bond energy between sites of type 0
    J11 : float
        nearest neighbour bond energy between sites of type 1
    J01 : float
        nearest neighbour bond energy between sitess of differeing type
    latticeState : int array of size Nx*Ny
        array defining current state (atom type) of each lattice site

    Methods
    
    calcEnergy()
        calculates total energy of the current configuration
    calcDeltaEnergy(ix,iy)
        calculates the change in energy when changing the state of the (ix,iy) lattice site
    writeConfiguration(fileName)
        writes the current state of the simulation to the file fileName
        
    """
 
    def __init__(self,Nx=10,Ny=10,J00=1.0,J11=1.0,J01=1.0,initialStructure="random",concentration=0.5,inputFilename="",randomSeed=220368):
        """
        
        Initializes an instance of the ba class
        
        Creates an 2D square lattice of atoms which can either be of type 0 or type 1
 
        Parameters
        
        Nx : int
            periodicity length in x-direction (default is 10)
        Ny : int
            periodicity length in y-direction (default is 10)
        J00 : float
            nearest neighbour bond energy between atoms of type 0 (default is 1.0)
        J11 : float
            nearest neighbour bond energy between atoms of type 1 (default is 1.0)
        J01 : float
            nearest neighbour bond energy between atoms of differeing type (default is 1.0)
        initialStructure : string
            sets how the initial structure is created with "random" giving a random concentration:1-concentration 
            structure of type 0 and type 1 sites, "type0" giving only type 0 sites, and "type1" giving only 
            type1 sites (default is "random")
        concentration : float
            concentration of type 0 sites for initialStructure="random" (default is 0.5)
        inputFilename : string
            if len(inputFilename) does not equal zero, then read in a simulation state from the file inputFilename (default is "")
        randomSeed : int, option
            random seed for pseudorandom sequence (default is 220368), if set to zero then each run uses a different random seed

        """
        #
        # If randomSeed>0 set random seed (allows for reproducable psuedo-random sequence)
        #
        if (randomSeed>0) : np.random.seed(randomSeed)
        #
        # Set up initial system
        #
        if len(inputFilename)==0:
            #
            # Construct an entirely new system
            #
            self.Nx=Nx
            self.Ny=Ny
            self.J00=J00
            self.J11=J11
            self.J01=J01
            self.siteNumber=self.Nx*self.Ny
            self.latticeState=np.zeros((self.Nx,self.Ny),dtype=int)
            self.type0SiteNumber=0
            self.type1SiteNumber=0
            for ix in range(self.Nx):
                for iy in range(self.Ny):
                    if initialStructure=="random":
                        if random.random()<concentration:
                            self.latticeState[ix,iy]=0
                            self.type0SiteNumber+=1
                        else:
                            self.latticeState[ix,iy]=1
                            self.type1SiteNumber+=1
                    elif initialStructure=="type0":
                        self.latticeState[ix,iy]=0
                        self.type0SiteNumber+=1
                    elif initialStructure=="type1":
                        self.latticeState[ix,iy]=1
                        self.type1SiteNumber+=1
                    else:
                        print("Unknown initialStructure option")
                        exit()
        else:
            #
            # Read in a system from the file inputFileName
            #
            f0=open(inputFilename)
            header=f0.readline()
            self.Nx=int(header.split(" ")[0])
            self.Ny=int(header.split(" ")[1])
            self.J00=float(header.split(" ")[2])
            self.J11=float(header.split(" ")[3])
            self.J01=float(header.split(" ")[4])
            self.siteNumber=self.Nx*self.Ny
            self.latticeState=np.zeros((self.Nx,self.Ny),dtype=int)
            self.type0SiteNumber=0
            self.type1SiteNumber=0            
            for ix in range(self.Nx):
                for iy in range(self.Ny):
                    line=f0.readline()
                    self.latticeState[ix,iy]=int(line.split(" ")[2])
                    if self.latticeState[ix,iy]==0:
                        self.type0SiteNumber+=1
                    else:
                        self.type1SiteNumber+=1

            f0.close()
        #
        # Create interaction matrix
        #
        self.JMatrix=np.array([[J00,J01],[J01,J11]])

    def writeConfiguration(self,filename):
        """
        writes current simulation state to the file "filename"
        
        Parameters
        
        filename : string
        
        file name of output file
        """
        f0=open(filename,"w+")
        #
        # Header line is Nx,Ny,J00,J11,J10
        #
        f0.write("%d %d %s %s %s \r\n" % (self.Nx,self.Ny,self.J00,self.J11,self.J01))
        #
        # Each line gives the spatial position and corresponding state 
        #
        for ix in range(self.Nx):
            for iy in range(self.Ny):
                f0.write("%d %d %d \r\n" % (ix,iy,self.latticeState[ix,iy]))
        f0.close()
        return

    def calcEnergy(self):
        """
        Calculates the total energy of the current configuration
        
        Returns
        
        Total energy : float
        """
        totalEnergy=0.0
        for ix in range(self.Nx):
            for iy in range(self.Ny):
                totalEnergy+=self.JMatrix[self.latticeState[ix,iy],self.latticeState[(ix+1)%self.Nx,iy]]+\
                        self.JMatrix[self.latticeState[ix,iy],self.latticeState[ix,(iy+1)%self.Ny]]
        return  totalEnergy

    def changeSiteState(self,ix,iy,calcDeltaEnergy=True):
        """
        Changes the state of the requested site and can calculate the resulting change in energy (default)
        
        Parameters
        
        ix : int
            x coordinate of requested site
        iy : int
            y coordinate of requested site
        calcDeltaEnergy : logical
            if True (default) calculate the resulting change in total energy
        
        Returns
        
        Total energy : float
        
            this is only the case if calcDeltaEnergy=True
        
        """
        if calcDeltaEnergy:
            deltaEnergy=-(self.JMatrix[self.latticeState[ix,iy],self.latticeState[(ix+1)%self.Nx,iy]]+\
                    self.JMatrix[self.latticeState[ix,iy],self.latticeState[(ix-1)%self.Nx,iy]]+\
                    self.JMatrix[self.latticeState[ix,iy],self.latticeState[ix,(iy+1)%self.Ny]]+\
                    self.JMatrix[self.latticeState[ix,iy],self.latticeState[ix,(iy-1)%self.Ny]])
            if self.latticeState[ix,iy]==0:
                self.latticeState[ix,iy]=1
                self.type0SiteNumber-=1
                self.type1SiteNumber+=1
            else:
                self.latticeState[ix,iy]=0
                self.type0SiteNumber+=1
                self.type1SiteNumber-=1
            deltaEnergy+=(self.JMatrix[self.latticeState[ix,iy],self.latticeState[(ix+1)%self.Nx,iy]]+\
                    self.JMatrix[self.latticeState[ix,iy],self.latticeState[(ix-1)%self.Nx,iy]]+\
                    self.JMatrix[self.latticeState[ix,iy],self.latticeState[ix,(iy+1)%self.Ny]]+\
                    self.JMatrix[self.latticeState[ix,iy],self.latticeState[ix,(iy-1)%self.Ny]])
            return deltaEnergy
        else:
            if self.latticeState[ix,iy]==0:
                self.latticeState[ix,iy]=1
                self.type0SiteNumber-=1
                self.type1SiteNumber+=1
            else:
                self.latticeState[ix,iy]=0
                self.type0SiteNumber+=1
                self.type1SiteNumber-=1
            return

