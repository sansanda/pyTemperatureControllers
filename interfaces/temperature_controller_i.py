import abc


class Temperature_Controller_I(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'update_temperature_sp') and
                callable(subclass.update_temperature_sp) and
                hasattr(subclass, 'get_temperature_sp') and
                callable(subclass.get_temperature_sp) and
                hasattr(subclass, 'get_actual_temperature') and
                callable(subclass.get_actual_temperature) or
                NotImplemented)

    @abc.abstractmethod
    def update_temperature_sp(self, temperature=0):
        """Updates the temperature controller setpoint"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_temperature_sp(self):
        """Gets the temperature controller setpoint"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_actual_temperature(self):
        """Gets the actual temperature of the process"""
        raise NotImplementedError
