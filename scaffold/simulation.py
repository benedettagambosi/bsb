import abc
import numpy as np
from .helpers import ConfigurableClass, assert_attr

class SimulationComponent(ConfigurableClass):
    def __init__(self):
        super().__init__()
        self.simulation = None

class SimulatorAdapter(ConfigurableClass):

    def __init__(self):
        super().__init__()
        self.cell_models = {}
        self.connection_models = {}
        self.devices = {}

    def get_configuration_classes(self):
        if not hasattr(self.__class__, 'simulator_name'):
            raise Exception("The SimulatorAdapter {} is missing the class attribute 'simulator_name'".format(self.__class__))
        # Check for the 'configuration_classes' class attribute
        if not hasattr(self.__class__, 'configuration_classes'):
            raise Exception("The '{}' adapter class needs to set the 'configuration_classes' class attribute to a dictionary of configurable classes (str or class).".format(self.simulator_name))
        classes = self.configuration_classes
        # Check for the presence of required classes
        if not 'cell_models' in classes:
            raise Exception("{} adapter: The 'configuration_classes' dictionary requires a class to handle the simulation configuration of cells under the 'cell_models' key.".format(self.simulator_name))
        if not 'connection_models' in classes:
            raise Exception("{} adapter: The 'configuration_classes' dictionary requires a class to handle the simulation configuration of cell connections under the 'connection_models' key.".format(self.simulator_name))
        if not 'devices' in classes:
            raise Exception("{} adapter: The 'configuration_classes' dictionary requires a class to handle the simulation configuration of devices under the 'devices' key.".format(self.simulator_name))

        # Test if they are all children of the ConfigurableClass class
        keys = ['cell_models', 'connection_models', 'devices']
        for class_key in keys:
            if not issubclass(classes[class_key], ConfigurableClass):
                raise Exception("{} adapter: The configuration class '{}' should inherit from ConfigurableClass".format(self.simulator_name, class_key))
        return self.configuration_classes

    @abc.abstractmethod
    def prepare(self, hdf5, simulation_config):
        '''
            This method turns a stored HDF5 network architecture and returns a runnable simulator.

            :returns: A simulator prepared to run a simulation according to the given configuration.
        '''
        pass

    @abc.abstractmethod
    def simulate(self, simulator):
        '''
            Start a simulation given a simulator object.
        '''
        pass