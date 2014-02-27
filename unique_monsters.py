#!/usr/bin/python

from monster import Monster

class Nazgul(Monster):
    """
    A Nazg�l monster.
    """

    def __init__(self, name, description, player):
        """
        Initializes the Nazg�l. Nazg�l is a monster that player fights throughout the game
        and whose difficulty is dependent on player level.

        @param name:        Name of monster
        @param description: Description of monster.
        @param experience:  Experienced gained for defeating monster.
        @param player:      Player stats are used for deteremining Nazg�l difficulty.
        """
        Monster.__init__(self, name, description, experience)

    def getName(self):
        """
        Gets monster name.

        @return: Monster's name.
        """
        return self._name

    def getDescription(self):
        """
        Gets monster's description.

        @return: Monster's description.
        """
        return self._description

    def getExperience(self):
        """
        Gets monster's experience.

        @return: Monster's experience.
        """
        return self._experience
