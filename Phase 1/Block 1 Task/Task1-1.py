import os
import time

def display_gear(n):
    patterns = [
        ['####', '#  #', '#  #', '#  #', '####'],  # 0
        ['   #', '   #', '   #', '   #', '   #'],  # 1
        ['####', '   #', '####', '#   ', '####'],  # 2
        ['####', '   #', '####', '   #', '####'],  # 3
        ['#  #', '#  #', '####', '   #', '   #'],  # 4
        ['####', '#   ', '####', '   #', '####'],  # 5
        ['####', '#   ', '####', '#  #', '####'],  # 6
        ['####', '   #', '   #', '   #', '   #'],  # 7
        ['####', '#  #', '####', '#  #', '####']   # 8
    ]
    
    print(*patterns[n], sep='\n')

def clean_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def animate_shift(from_gear, to_gear):
    display_gear(from_gear)
    time.sleep(2)
    clean_screen()
    display_gear(to_gear)
    time.sleep(2)
    clean_screen()

def get_gear_input(prompt):
    while True:
        value = input(prompt).strip()
        if value.isdigit():
            n = int(value)
            if 0 <= n <= 8:
                return n
            else:
                print("Invalid range. Please enter a number between 0 and 8.")
        else:
            print("Invalid input. Please enter a number between 0 and 8.")

while True:
    print("=== Gear Shift Simulator ===")
    from_gear = get_gear_input("Enter current gear (0 to 8): ")
    to_gear = get_gear_input("Enter next gear (0 to 8): ")
    
    clean_screen()
    animate_shift(from_gear, to_gear)
    clean_screen()
    decision = input("Do you want to continue? (yes/no): ").strip().lower()
    if decision == 'no':
        print("Exiting program.")
        break
    clean_screen()
