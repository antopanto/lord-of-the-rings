#!/usr/bin/python

from unique_place import UniquePlace
from monsters.nazgul import Nazgul
from battle_engine import battle
from items.weapon import Weapon
from items.armor import Armor
from items.item import Item
import constants
import random

class Tharbad(UniquePlace):
    """
    A unique place in Mitheithel. Here the user is given the option of
    exploring the ruins. Exploring the ruins grants the player the ability
    to find items at the risk of a chance encounter with Nazgul.
    """
    def __init__(self, name, description, greetings):
        """
        Initializes Tharbad.
        
        @param name:            The name of the UniquePlace.
        @param description:     A description of the UniquePlace.
	@param greetings:	The greetings the user gets as he enters.        
	"""
        #Call parent class init function
        UniquePlace.__init__(self, name, description, greetings)

        #Generates list of Nazgul that user may fight
        self._monsters = []
        numberNazgul = random.randrange(0, 5)
        for monster in range(numberNazgul):
            nazgul = Nazgul(constants.MONSTER_STATS[Nazgul])
            self._monsters.append(nazgul)

        #Generate loot
        scroll = Item("Ancient Scroll", "Ancient runes and symbols", 0)
        weapon = Weapon("Rotting Staff", "Looks like it can break at any second", 1, 1, 1)
        armor = Armor("Rotting Shield", "Maybe one or two hits and it's through", 1, 1, 1)
        self._loot = [scroll, weapon, armor]
        
    def enter(self, player):
        """
        Enter Tharbad.

        @param player:  The current player.
        """
        print self._greetings
        print ""
        
        print "You gaze upon the ancient ruins of the once great city of Tharbad and see some very strange sights."
        raw_input("Press enter to continue. ")
        print ""

        #Solicit user input
        choice = None
        acceptable = ["explore", "leave"]
        while choice not in acceptable:
            choice = raw_input("What would you like to do? Choices: 'explore' and 'leave.' ")
            print ""
            
        if choice == "explore":
            self._explore(player)
        else:
            print "You bid farewell to the ruins of Tharbad and continue on your journey."
            print ""

    def _explore(self, player):
        """
        Player explores Tharbad. 
        """
        #Solicit user input
        choice = None
        acceptable = ["ruined mill", "ancient bridge"]
        while choice not in acceptable:
            choice = raw_input("Where would you like to explore? Options: 'ruined mill' and 'ancient bridge.' ")
        print ""

        #If user chooses to explore ruined mill
        if choice == "ruined mill":
            print "You find lots of rotting instruments and the remains of farming equipment."
            raw_input("Press enter to continue. ")
            print ""
            self._itemFind(player)
            self._chanceBattle(player)

        #If user choose to explore ancient bridge
        elif choice == "ancient bridge":
            print "You find the ruins of the ancient North-South Road bridge crossing. This was once one of the greatest causeways in all of Middle Eart."
            raw_input("Press enter to continue. ")
            print ""
            self._itemFind(player)
            self._chanceBattle(player)

        #Give player option to keep exploring
        choice = None
        acceptable = ["yes", "no"]
        while choice not in acceptable:
            choice = raw_input("Would you like to keep exploring? Options: 'yes' and 'no.' ")
        print ""
        
        if choice == "yes":
            self._explore(player)
        else:
            print "You leave Tharbad with a sense of loss."
            print ""
            
    def _itemFind(self, player):
        """
        Determines if player finds an item and then gives player that item.
        """
        #If there are no items to find
        if len(self._loot) == 0:
            return
        
        #Determines if player finds item and which item player receives
        if random.random() < constants.UniquePlaceConstants.TharbadItemFindProb:
            print "You find something that may be of some value!"
            item = random.choice(self._loot)
            self._loot.remove(item)
            player.addToInventory(item)
            print ""

    def _chanceBattle(self, player):
        """
        Determines if a random battle is to occur."
        """
        if random.random() < constants.UniquePlaceConstants.TharbadBattleProb:
            print "You hear some rustling in the shadows...."
            raw_input("Press enter to continue. ")
            print ""
            
            battle(player, constants.BattleEngineContext.STORY, self._monsters)