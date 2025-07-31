from abc import ABC, abstractmethod
from action import Move, Defense
class Driver(ABC):
    """Abstract base class for a race driver."""
    def __init__(self, name):
        self.name = name
        self.tire_health = 100
        self.fuel = 500

    @abstractmethod
    def moves(self):
        """Return the driver's available moves."""
        pass

    @abstractmethod
    def defenses(self):
        """Return the driver's available defenses."""
        pass

    def is_out(self):
        """Check if the driver is out of the race (tire health <= 0)."""
        return self.tire_health <= 0

    def status(self):
        """Return the driver's current status as a formatted string."""
        return f"{self.name:<16} | Tire Health: {self.tire_health:>3} | Fuel: {self.fuel:>3}"


class Verstappen(Driver):
    """Max Verstappen driver with specific moves and defenses."""
    def __init__(self):
        super().__init__('Max Verstappen')
        self._moves = [
            Move("DRS Boost", 45, 12),
            Move("Red Bull Surge", 80, 20),
            Move("Precision Turn", 30, 8),
        ]
        self._defenses = [
            Defense("Brake Late", 25, 0.30),
            Defense("ERS Deployment", 40, 0.50, max_uses=3)
        ]

    def moves(self):
        return self._moves

    def defenses(self):
        return self._defenses


class Mostafa(Driver):
    """Hassan Mostafa driver with specific moves and defenses."""
    def __init__(self):
        super().__init__('Hassan Mostafa')
        self._moves = [
            Move("Turbo Start", 50, 10),
            Move("Mercedes Charge", 90, 22),
            Move("Corner Mastery", 25, 7),
        ]
        self._defenses = [
            Defense("Slipstream Cut", 20, 0.40),
            Defense("Aggressive Block", 35, 1.00, max_uses=2)
        ]

    def moves(self):
        return self._moves

    def defenses(self):
        return self._defenses