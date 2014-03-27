#!/usr/bin/python

from building import Building

class Inn(Building):
    """
    Inns are instances of the Building object.
    Inns have a special method that allows player to heal.
    """
    def __init__(self, name, description, greetings):
        """
        Initializes inn object.

        @param name:           The name of the inn.
        @param description:    A description of the inn.
        @param greetings:      The greetings the user gets as he enters a inn.
        @param talk:           What the local say when the user talks to the locale.
        """
        self._player = player
        
        self._name = name
        self._description = description
        self._greetings = greetings

    def getName(self):
        """
        Returns name of inn.

        @return:    The name of the inn.
        """
        return self._name

    def getDescription(self):
        """
        Returns description of inn.

        @return:    The description of the inn.
        """
        return self._description

    def greetings(self):
        """
        Prints a screen that represents a player greeting upon entering inn.
        """
        print self._greetings
        
    def heal(self):
        """
        Heals player.
        """
        
