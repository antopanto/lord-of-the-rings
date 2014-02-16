from command import Command
import space_dictionary
import game_stats
import space

class WestCommand(Command):
    """
    West command.
    """

    def __init__(self, name, explanation):
        """
        Initializes new north command.
        """
        #Call parent's init method
        Command.__init__(self, name, explanation)

    def execute(self):
        """
        Run West command.
        """
        print "--------------------------------"
        print "         moving east"
        print "      ----------------->        "
        print ""
        #what is the current space?
        self.current_space = game_stats.current_space
        #what is north of the current space?
        west_space = space_dictionary.dictionary[self.current_space]['west']
        
        print "Welcome to ",west_space
        game_stats.current_space = west_space
        self.current_space=west_space
        print space.current_space.description
        
