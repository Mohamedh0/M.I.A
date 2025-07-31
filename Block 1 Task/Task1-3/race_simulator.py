import random
from driver import Verstappen, Mostafa


class RaceSimulator:
    """Simulates a race between two drivers with player-controlled actions."""
    def __init__(self):
        self.v = Verstappen()
        self.m = Mostafa()
        self.round = 1
        self.player_driver = None
        self.opponent_driver = None

    def _get_user_choice(self, prompt, valid_range):
        """Get and validate user input for a choice within a range."""
        while True:
            try:
                choice = int(input(prompt).strip())
                if choice in valid_range:
                    return choice
                print(f"Please choose a number between {min(valid_range)} and {max(valid_range)}.")
            except ValueError:
                print("Invalid input! Please enter a number.")

    def choose_player(self):
        """Prompt the user to select a driver."""
        print("Choose your driver:")
        print("1. Max Verstappen")
        print("2. Hassan Mostafa")
        choice = self._get_user_choice("Enter 1 or 2: ", {1, 2})
        self.player_driver = self.v if choice == 1 else self.m
        self.opponent_driver = self.m if choice == 1 else self.v
        print(f"You are playing as {self.player_driver.name}!")

    def _display_moves(self, driver):
        """Display available moves for a driver."""
        available = [m for m in driver.moves() if m.can_perform(driver.fuel)]
        print(f"\nAvailable moves for {driver.name}:")
        for i, move in enumerate(available, 1):
            print(f"{i}. {move.name} (Fuel Cost: {move.fuel_cost}, Impact: {move.impact})")
        return available

    def _display_defenses(self, driver):
        """Display available defenses for a driver."""
        available = [d for d in driver.defenses() if d.can_perform(driver.fuel)]
        print(f"\nAvailable defenses for {driver.name}:")
        for i, defense in enumerate(available, 1):
            uses_left = defense.max_uses - defense.used if defense.max_uses is not None else "Unlimited"
            print(f"{i}. {defense.name} (Fuel Cost: {defense.fuel_cost}, Reduction: {defense.reduction_percent*100:.0f}%, Uses Left: {uses_left})")
        return available

    def choose_move(self, driver, is_player=False):
        """Select a move for the driver, either by player input or randomly."""
        available = [m for m in driver.moves() if m.can_perform(driver.fuel)]
        if not available:
            return None
        if is_player:
            available = self._display_moves(driver)
            choice = self._get_user_choice("Choose a move (enter the number): ", set(range(1, len(available) + 1)))
            return available[choice - 1]
        return random.choice(available)

    def choose_defense(self, driver, is_player=False):
        """Select a defense for the driver, either by player input or optimally."""
        available = [d for d in driver.defenses() if d.can_perform(driver.fuel)]
        if not available:
            return None
        if is_player:
            available = self._display_defenses(driver)
            choice = self._get_user_choice("Choose a defense (enter the number, or 0 to skip): ", set(range(0, len(available) + 1)))
            return available[choice - 1] if choice != 0 else None
        return max(available, key=lambda d: (-d.reduction_percent, d.fuel_cost))

    def simulate_turn(self, attacker, defender, attacker_is_player=False):
        """Simulate a single turn of the race."""
        move = self.choose_move(attacker, is_player=attacker_is_player)
        if not move:
            print(f"{attacker.name} has no fuel to attack!")
            return

        attacker.fuel -= move.fuel_cost
        defense = self.choose_defense(defender, is_player=not attacker_is_player)

        if defense and defender.fuel >= defense.fuel_cost:
            defender.fuel -= defense.fuel_cost
            defense.use()
            damage = int(move.impact * (1 - defense.reduction_percent))
            print(f"{defender.name} used {defense.name} to reduce damage!")
        else:
            damage = move.impact
            print(f"{defender.name} couldn't defend due to {'insufficient fuel' if defense else 'no available defense'}!")

        defender.tire_health = max(0, defender.tire_health - damage)
        print(f"{attacker.name} used {move.name} | Damage: {damage}")
        print(f"{attacker.status()}\n{defender.status()}")

    def _check_game_end(self):
        """Check if the game has ended and return the result."""
        if self.player_driver.is_out() and self.opponent_driver.is_out():
            return "Both drivers' tires failed. No winner!"
        if self.player_driver.is_out():
            return f"Winner: {self.opponent_driver.name}!"
        if self.opponent_driver.is_out():
            return f"Winner: {self.player_driver.name}!"
        return None

    def _check_fuel_and_tire(self):
        """Check fuel availability and tire health for a draw condition."""
        player_can_move = bool([m for m in self.player_driver.moves() if m.can_perform(self.player_driver.fuel)])
        opponent_can_move = bool([m for m in self.opponent_driver.moves() if m.can_perform(self.opponent_driver.fuel)])
        if not player_can_move and not opponent_can_move:
            print("\nBoth drivers are out of fuel.")
            if self.player_driver.tire_health > self.opponent_driver.tire_health:
                return f"Winner by tire health: {self.player_driver.name}!"
            if self.opponent_driver.tire_health > self.player_driver.tire_health:
                return f"Winner by tire health: {self.opponent_driver.name}!"
            return "It's a draw! Both tire health and fuel are equal."
        return None

    def start_race(self):
        """Start and run the race simulation."""
        self.choose_player()
        print(f"\nRace Start: {self.player_driver.name} vs {self.opponent_driver.name}!\n")
        while not self.player_driver.is_out() and not self.opponent_driver.is_out():
            result = self._check_fuel_and_tire()
            if result:
                print(result)
                break
            if self.round % 2 == 1 and not self.choose_move(self.player_driver, is_player=True):
                print(f"{self.player_driver.name} has no fuel to attack, skipping turn!")
                self.round += 1
                continue
            if self.round % 2 == 0 and not self.choose_move(self.opponent_driver):
                print(f"{self.opponent_driver.name} has no fuel to attack, skipping turn!")
                self.round += 1
                continue

            print(f"\n-- Round {self.round} --")
            if self.round % 2 == 1:
                self.simulate_turn(self.player_driver, self.opponent_driver, attacker_is_player=True)
            else:
                self.simulate_turn(self.opponent_driver, self.player_driver)
            self.round += 1

        result = self._check_game_end()
        if result:
            print(f"\n{result}")
        print("\nFinal Status:")
        print(f"{self.player_driver.status()}\n{self.opponent_driver.status()}")