# Pyext library only available within PD/pyext environment.
try:
    import pyext
except:
    print "ERROR: This script must be loaded by the PD/Max pyext external"

# Set my working directory to the one where this script is located
import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
print(dname)

#import modules (yours or python's)
#from generator import Generator 

# This class represents a pd object
# [pyext my_pd_objects.simple_object]
class simple_object(pyext._class): 
    # There is one inlet (the leftmost) and one outlet (the rightmost) by default.
    # Add more here:
    _inlets=2  # 3 inlets total. 
    # The leftmost inlet is used to receive a "reload" message to refresh the object
    # when you chnage the code
    
    _outlets=2 # 3 outlets total

    # This method will be triggered when a "load" message is received on the third inlet
    def load_2(self, *args):
        # Args is a tuple with the atoms of the load message from PD
        print args
        print args[0]
        self.variable = args[1]

    # This method will be triggered when a "search" message is received on the second inlet
    def search_1(self, *args): 
        # DONT USE outlet 0, it is the rightmost outlet and it's used by pyext.
        # self._outlet(0, "whaa")   # DONT.

        # Outlet 1 is the leftmost
        self._outlet(1, self.variable)
        self._outlet(2, "Hello There")

##########################################################################


# This class represents another pd object called generator_pd
# [pyext my_pd_objects.generator_pd]
class generator_pd(pyext._class): 
    _inlets=2  
    _outlets=1 

    # When a load message is received, create an instance of Generator
    def load_2(self, *args):
        self.generator = Generator("the_bum")

    def generate_1(self, *args): 
        notes = self.generator.generate()
        self._outlet(1, notes)