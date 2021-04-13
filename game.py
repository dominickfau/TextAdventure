# import cmd
from room import get_room
import todb
import textwrap
import shutil
import tempfile
import inspect
import re
# import logging

class Game():
    DATABASE_NAME = "game.db"
    MAX_COPY_ATTEMPTS = 3

    def __init__(self):
        self.dbfile = tempfile.mktemp()
        self.copyAttempts = 0
        self.copyDatabaseFile()
        print("-" * 40)
        
        self.loc = get_room(1, self.dbfile)
        self.input = ""
        self.validCommands = []
        self.getValidCommands()
        self.printStartMessage()
        self.look()


    def copyDatabaseFile(self):
        print("[INFO] Copying database file to temp directory.")
        try:
            shutil.copyfile(self.DATABASE_NAME, self.dbfile)
        except FileNotFoundError as err:
            print(f"[WARNING] Database file not found. Attempting to create with file name: {self.DATABASE_NAME}")
            todb.main(self.DATABASE_NAME)
            print("[INFO] Done creating database.")

            self.copyAttempts += 1
            if self.MAX_COPY_ATTEMPTS < self.copyAttempts: raise RuntimeError(f"[ERROR] Could not create game database {self.DATABASE_NAME}. Error: {err}")
            print(f"[INFO] Copy attempts: {self.copyAttempts}")
            self.copyDatabaseFile()


    def printStartMessage(self):
        startMessage = "Welcome to the game. Below is a list of available commands."
        print()
        print(startMessage)
        self.do_help()


    def getValidCommands(self):
        commands = inspect.getmembers(Game, predicate=inspect.isfunction)
        for command in commands:
            name = command
            if bool(re.match(r"do_+", name[0])):
                self.validCommands.append({'Command': name[0].split('_', 1)[1], 'HelpString': name[1].__doc__})


    def getInput(self):
        nextInput = input().strip().lower()

        commands = []
        for command in self.validCommands:
            commands.append(command['Command'])

        if nextInput in commands:
            if nextInput == 'help':
                self.do_help()
                self.look()
            elif nextInput == 'save':
                print("Game saving has not been implemented yet.")
                self.look()
            elif nextInput == 'load':
                print("Game loading has not been implemented yet.")
                self.look()
            else:
                self.move(nextInput)
        else:
            print(f"I don't know what {nextInput} is.")
            self.getInput()


    def move(self, dir):
        newroom = self.loc.neighbor(dir)
        if newroom is None:
            print("you can't go that way")
            self.look()
        else:
            self.loc = get_room(newroom, self.dbfile)
            self.look()
            
        if newroom==13:
            exit()


    def look(self):
        print()
        print(self.loc.name)
        print("")
        for line in textwrap.wrap(self.loc.description, 72):
            print(line)
        self.getInput()


    def do_up(self, args):
        """Go up."""
        self.move('up')


    def do_down(self, args):
        """Go down."""
        self.move('down')


    def do_n(self, args):
        """Go north."""
        self.move('n')


    def do_s(self, args):
        """Go south."""
        self.move('s')


    def do_e(self, args):
        """Go east."""
        self.move('e')


    def do_w(self, args):
        """Go west."""
        self.move('w')


    def do_quit(self, args):
        """Leaves the game."""
        print("Thank you for playing")
        return True


    def do_help(self):
        """Shows all commands."""
        print()
        print("Command list")
        print("Case does not matter.")
        print()
        print("-" * 40)
        # Find longest command string.
        longestCommandLength = 0
        for x in self.validCommands:
            if len(x['Command']) > longestCommandLength:
                longestCommandLength = len(x['Command'])

        # Print all commands and space evenly.
        for x in self.validCommands:
            padLength = 0
            if len(x['Command']) < longestCommandLength:
                padLength = longestCommandLength - len(x['Command'])
            padding = " " * padLength
            print(f"{x['Command']}      {padding + x['HelpString']}")
        print("-" * 40)


    def do_save(self, args):
        """Saves game prograss to file name."""
        #TODO: Implement game saving.
        pass


    def do_load(self, args):
        """Loads a game save from file name."""
        #TODO: Implement game loading.
        pass


if __name__ == "__main__":
    g = Game()
