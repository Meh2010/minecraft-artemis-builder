import random
import time
import os
import sys


COMPONENTS = [
    "hull",
    "engine",
    "life_support",
    "navigation",
    "fuel_tank",
    "command_module",
    "solar_array",
]


class Game:
    def __init__(self, size=7):
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        self.launchpad = (size // 2, size // 2)
        self.player = (0, 0)
        self.inventory = []
        self.placed = {}
        self.running = True
        self.launched = False
        self.place_components()

    def place_components(self):
        positions = set()
        positions.add(self.launchpad)
        positions.add(self.player)
        spots = []
        while len(spots) < len(COMPONENTS):
            r = random.randrange(self.size)
            c = random.randrange(self.size)
            if (r, c) in positions:
                continue
            positions.add((r, c))
            spots.append((r, c))

        for comp, pos in zip(COMPONENTS, spots):
            r, c = pos
            self.grid[r][c] = comp

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def draw(self):
        self.clear_screen()
        print("Artemis Builder — collect components and assemble the spacecraft")
        print(f"Player: {self.player}  Inventory: {self.inventory}")
        print("Map legend: P=you, L=launchpad, first-letter=component")
        for r in range(self.size):
            row = []
            for c in range(self.size):
                if (r, c) == self.player:
                    row.append("P")
                elif (r, c) == self.launchpad:
                    row.append("L")
                elif self.grid[r][c] is None:
                    row.append(".")
                else:
                    # show first letter to help user hunt components
                    row.append(self.grid[r][c][0].upper())
            print(" ".join(row))
        print("")
        print("Commands: w/a/s/d move, place <component>, inventory, blueprint, help, quit")

    def move(self, dr, dc):
        r, c = self.player
        nr = max(0, min(self.size - 1, r + dr))
        nc = max(0, min(self.size - 1, c + dc))
        self.player = (nr, nc)
        # auto-pick
        if self.grid[nr][nc]:
            comp = self.grid[nr][nc]
            print(f"You found a component: {comp}")
            self.inventory.append(comp)
            self.grid[nr][nc] = None
            time.sleep(0.6)

    def show_inventory(self):
        print("Inventory:", self.inventory)

    def show_blueprint(self):
        print("Blueprint (required components):")
        for comp in COMPONENTS:
            status = "PLACED" if comp in self.placed else "MISSING"
            print(f" - {comp}: {status}")

    def place_component(self, comp_name):
        if self.player != self.launchpad:
            print("You must be at the launchpad to place components.")
            return
        if comp_name not in self.inventory:
            print("You don't have that component in your inventory.")
            return
        if comp_name not in COMPONENTS:
            print("That's not a valid component for the Artemis build.")
            return
        if comp_name in self.placed:
            print("That component is already placed.")
            return
        # place it
        self.placed[comp_name] = True
        self.inventory.remove(comp_name)
        print(f"Placed {comp_name} into the build.")
        time.sleep(0.5)
        if len(self.placed) == len(COMPONENTS):
            self.launch_sequence()

    def launch_sequence(self):
        self.clear_screen()
        print("All components placed — starting pre-launch checks...")
        time.sleep(1.0)
        checks = [
            ("Structural integrity", True),
            ("Engine systems", True),
            ("Life support", True),
            ("Navigation", True),
            ("Fuel", True),
        ]
        for name, ok in checks:
            print(f"{name}: {'OK' if ok else 'FAIL'}")
            time.sleep(0.6)
        print("Launch in 3...")
        time.sleep(0.8)
        print("2...")
        time.sleep(0.8)
        print("1...")
        time.sleep(0.8)
        for i in range(6):
            self.clear_screen()
            pad = "\n" * (6 - i)
            print(pad)
            print("   /\\")
            print("  /  \\")
            print(" | ARTMIS |")
            print(" |  🚀   |")
            print("  \\  /")
            print("   \/")
            time.sleep(0.25)
        self.launched = True
        self.mission_phase()

    def mission_phase(self):
        self.clear_screen()
        print("The Artemis spacecraft has launched you to lunar orbit!")
        print("You are now part of the Artemis crew. Choose experiments to run:")
        experiments = {
            "seismometer": "Deploy seismometer on lunar surface",
            "regolith": "Analyze regolith samples",
            "radiation": "Measure radiation levels",
        }
        while True:
            print("")
            for key, desc in experiments.items():
                print(f" - {key}: {desc}")
            print(" - status: show mission status")
            print(" - exit: end mission")
            cmd = input("Select experiment> ").strip().lower()
            if cmd == "exit":
                print("Mission complete. Returning to Earth. Congratulations!")
                break
            if cmd == "status":
                print("Crew: You (Commander). Mission: Science & simulations.")
                continue
            if cmd in experiments:
                print(f"Running {cmd}...")
                time.sleep(1.0)
                outcome = random.choice(["Success", "Partial data", "Instrument error"])
                print(f"Outcome: {outcome}")
                if outcome == "Success":
                    print("Valuable scientific data returned to Mission Control.")
                time.sleep(0.8)
            else:
                print("Unknown experiment. Try again.")

    def help(self):
        print("Commands:")
        print(" - w/a/s/d: move up/left/down/right")
        print(" - place <component>: place component at launchpad")
        print(" - inventory: show inventory")
        print(" - blueprint: show required components and status")
        print(" - quit: exit game")

    def loop(self):
        while self.running and not self.launched:
            self.draw()
            cmd = input("Cmd> ").strip().lower()
            if cmd in ("w", "up"):
                self.move(-1, 0)
            elif cmd in ("s", "down"):
                self.move(1, 0)
            elif cmd in ("a", "left"):
                self.move(0, -1)
            elif cmd in ("d", "right"):
                self.move(0, 1)
            elif cmd.startswith("place "):
                _, comp = cmd.split(" ", 1)
                self.place_component(comp.strip())
            elif cmd == "inventory":
                self.show_inventory()
                input("Press Enter to continue...")
            elif cmd == "blueprint":
                self.show_blueprint()
                input("Press Enter to continue...")
            elif cmd == "help":
                self.help()
                input("Press Enter to continue...")
            elif cmd == "quit":
                print("Quitting game. Bye.")
                self.running = False
            else:
                print("Unknown command. Type 'help' for commands.")
                time.sleep(0.6)


def main():
    game = Game()
    try:
        game.loop()
    except KeyboardInterrupt:
        print("\nExiting.")


if __name__ == "__main__":
    main()

