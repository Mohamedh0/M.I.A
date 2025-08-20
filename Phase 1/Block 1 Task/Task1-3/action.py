from abc import ABC, abstractmethod

class Action(ABC):
    """Abstract base class for race actions (moves or defenses)."""
    def __init__(self, name, fuel_cost):
        self.name = name
        self.fuel_cost = fuel_cost

    @abstractmethod
    def can_perform(self, fuel):
        """Check if the action can be performed with the given fuel."""
        pass


class Move(Action):
    """Represents an offensive action in the race."""
    def __init__(self, name, fuel_cost, impact):
        super().__init__(name, fuel_cost)
        self.impact = impact

    def can_perform(self, fuel):
        return fuel >= self.fuel_cost


class Defense(Action):
    """Represents a defensive action in the race."""
    def __init__(self, name, fuel_cost, reduction_percent, max_uses=None):
        super().__init__(name, fuel_cost)
        self.reduction_percent = reduction_percent
        self.max_uses = max_uses
        self.used = 0

    def can_perform(self, fuel):
        if self.max_uses is not None and self.used >= self.max_uses:
            return False
        return fuel >= self.fuel_cost

    def use(self):
        """Increment the usage count for limited-use defenses."""
        if self.max_uses is not None:
            self.used += 1