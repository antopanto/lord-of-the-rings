#!/usr/bin/python

class Place(object):
    """
    Parent class to both City and unique place classes.
    """
    def __init__(self, name, description, greetings):
        """
        Initialize Place object.
        
        @param name:           The name of the Place.
        @param description:    A description of the Place.
        @param greetings:      The greetings upon entering Place.
        """
        self._name = name
        self._description = description
        self._greetings = greetings
    
    def getName(self):
        """
        Returns name of place.

        @return:    The name of the place.
        """
        return self._name

    def getDescription(self):
        """
        Returns description of place.

        @return:    The description of the place.
        """
        return self._description

    def getGreeting(self):
        """
        Returns the greetings of place
        """
        return self._greetings
        
    def receiveSpaces(self, space, targetSpace):
        """
        Helper method used to create references to the two spaces
        used in quest-dependent port creation.
        
        @param space:         Player's current space.
        @param targetSpace:   The space to be linked with the 
                              current space.
        """
        self._space = space
        self._targetSpace = targetSpace
        
    def _createPort(self, direction):
        """
        Creates a port between the space and targetSpace. In this
        construction, targetSpace is to the direction of space.
        
        In LotR, this is used to unlock new space connections as a  
        reward for quest completion.
        
        @param direction:     The direction targetSpace is in with 
                              respect to space.
        """
        self._space.createExit(direction, self._targetSpace, 
        outgoingOnly = False)
        
        print "%s is now accessable to the %s." % (self._targetSpace.getName(), 
        direction)
        
    def enter(self, player):
        """
        Parent enter method. Should be overridden by child classes.
        
        @param player:  The current player.
        """
        print "This enter method should be overridden by child class."