import random
from driver import Verstappen, Mostafa
from action import Move, Defense

class RaceSimulator:
    """Simulates a race between two drivers with player-controlled actions."""
    def __init__(self):
        self.v = Verstappen()
        self.m = Mostafa()
        self.round = 1
        self.player_driver = None
        self.opponent_driver = None
        self.player_active_defense = None  
        self.opponent_active_defense = None  

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
        print(f"\nAvailable offensive moves for {driver.name}:")
        for i, move in enumerate(available, 1):
            print(f"{i}. {move.name} (Fuel Cost: {move.fuel_cost}, Impact: {move.impact})")
        return available

    def _display_defenses(self, driver):
        """Display available defenses for a driver."""
        available = [d for d in driver.defenses() if d.can_perform(driver.fuel)]
        print(f"\nAvailable defensive moves for {driver.name}:")
        for i, defense in enumerate(available, 1):
            uses_left = defense.max_uses - defense.used if defense.max_uses is not None else "Unlimited"
            print(f"{i}. {defense.name} (Fuel Cost: {defense.fuel_cost}, Reduction: {defense.reduction_percent*100:.0f}%, Uses Left: {uses_left})")
        return available

    def choose_action(self, driver, is_player=False):
        """Select either an offensive or defensive move for the driver."""
        available_moves = [m for m in driver.moves() if m.can_perform(driver.fuel)]
        available_defenses = [d for d in driver.defenses() if d.can_perform(driver.fuel)]
        
        if not available_moves and not available_defenses:
            return None

        if is_player:
            # Display available actions
            print(f"\nChoose an action for {driver.name}:")
            if available_moves:
                self._display_moves(driver)
            if available_defenses:
                self._display_defenses(driver)
            
            # Create valid choice range
            total_options = len(available_moves) + len(available_defenses)
            valid_choices = set(range(1, total_options + 1))
            choice = self._get_user_choice(f"Choose an action (1-{total_options} for moves/defenses): ", valid_choices)
            
            # Map choice to action
            if choice <= len(available_moves):
                return available_moves[choice - 1]
            return available_defenses[choice - len(available_moves) - 1]
        else:
            # Opponent randomly chooses between available moves and defenses
            all_actions = available_moves + available_defenses
            if not all_actions:
                return None
            return random.choice(all_actions)

    def simulate_turn(self, attacker, is_player=False):
        """Simulate a single turn of the race."""
        action = self.choose_action(attacker, is_player=is_player)
        if not action:
            print(f"{attacker.name} has no fuel to perform any action!")
            return

        # Apply the action
        attacker.fuel -= action.fuel_cost
        defender = self.opponent_driver if is_player else self.player_driver
        active_defense = self.opponent_active_defense if is_player else self.player_active_defense

        if isinstance(action, Move):
            # Offensive move: apply damage, reduced by opponent's active defense
            if active_defense:
                damage = int(action.impact * (1 - active_defense.reduction_percent))
                print(f"{defender.name}'s {active_defense.name} (from previous turn) reduces damage!")
            else:
                damage = action.impact
                print(f"{defender.name} has no active defense!")
            defender.tire_health = max(0, defender.tire_health - damage)
            print(f"{attacker.name} used offensive move {action.name} | Damage: {damage}")
        else:
            # Defensive move: set active defense for next turn
            action.use()
            if is_player:
                self.player_active_defense = action
            else:
                self.opponent_active_defense = action
            print(f"{attacker.name} used defensive move {action.name}")

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
        player_can_act = bool([m for m in self.player_driver.moves() if m.can_perform(self.player_driver.fuel)] +
                            [d for d in self.player_driver.defenses() if d.can_perform(self.player_driver.fuel)])
        opponent_can_act = bool([m for m in self.opponent_driver.moves() if m.can_perform(self.opponent_driver.fuel)] +
                                [d for d in self.opponent_driver.defenses() if d.can_perform(self.opponent_driver.fuel)])
        if not player_can_act and not opponent_can_act:
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
        print(f"\n🏁 Race Start: {self.player_driver.name} vs {self.opponent_driver.name}!\n")
        while not self.player_driver.is_out() and not self.opponent_driver.is_out():
            result = self._check_fuel_and_tire()
            if result:
                print(result)
                break
            if self.round % 2 == 1 and not self.choose_action(self.player_driver, is_player=True):
                print(f"{self.player_driver.name} has no fuel to act, skipping turn!")
                self.round += 1
                continue
            if self.round % 2 == 0 and not self.choose_action(self.opponent_driver):
                print(f"{self.opponent_driver.name} has no fuel to act, skipping turn!")
                self.round += 1
                continue

            print(f"\n-- Round {self.round} --")
            if self.round % 2 == 1:
                self.simulate_turn(self.player_driver, is_player=True)
            else:
                self.simulate_turn(self.opponent_driver)
            self.round += 1

        result = self._check_game_end()
        if result:
            print(f"\n{result}")
        print("\nFinal Status:")
        print(f"{self.player_driver.status()}\n{self.opponent_driver.status()}")