#!/usr/bin/python

import random

import constants
import factories.monster_factory
from commands.use_potion_command import UsePotionCommand

def battle(player, context, monsters = None):
    """
    The battle engine of Lord of the Rings.

    @param player:     The player object.
    @param context:    Context constant for battle engine. Battle engine behaves differently
                       in different contexts: either random battle or fixed battle.
    @param monsters:   A list of monsters.

    A summary of differences between random battles and story-based battles:
    -Random battles: monster factory called by battle engine and monsters are supplied by
    monster factory. Player can choose to "run" in random battles.
    -Story-based battles: monsters must be supplied through the "monsters" parameter.
    Player cannot run from battle.
    """
    #Battle setup
    output = _battleSetup(player, context)
    if context == constants.BattleEngineContext.RANDOM:
        bonusDifficulty = output[0]
        monsters = output[1]
    else:
        bonusDifficulty = output
    
    #Main battle sequence
    while len(monsters) != 0:
        #User prompt
        print "Monsters:"
        for monster in monsters:
            print "\t%s: %s" % (monster.getName(), monster.getDescription())
        print ""
        choice = raw_input("You may: 'attack', 'use potion', 'run.' ")
        
        #Player attack option
        if choice == 'attack':
            earnings = _playerAttackPhase(player, monsters, bonusDifficulty)
            
        #Use potion option
        elif choice == "use potion":
            _usePotion(player)
            
        #Run option
        elif choice == "run":
            if context == constants.BattleEngineContext.RANDOM:
                if random.random() < constants.RUN_PROBABILITY_SUCCESS:
                    print "You ran away succesfully!"
                    print ""
                    return
                else:
                    print "Your path is blocked!"
            else:
                print "Your path is blocked!"
                
        #Code - eliminates all enemies
        elif choice == "explode":
            monsters = []
            earnings = [0,0]
    
        #For invalid user input
        else:
            print "Huh?"
        print ""

        #Break between player and monster phases
        raw_input("Press 'enter' to continue. ")
        print ""

        #Monsters attack phase
        continueBattle = _monsterAttackPhase(player, monsters)
        
        #Escape sequence given battle loss
        if not continueBattle:
            print ""
            print "Gandalf bails you out."
            player.heal(1)
            return

    #Battle end sequence - loot received
    _endSequence(player, earnings)

def _battleSetup(player, context):
    """
    Generates variables for battle engine and prints battle
    splash screen.
    """
    #For random battles
    if context == constants.BattleEngineContext.RANDOM:
        #Create variables
        location = player.getLocation()
        region = location.getRegion()
        bonusDifficulty = location.getBattleBonusDifficulty()

        #Spawn monsters
        monsterCount = _monsterNumGen(player)
        monsters = factories.monster_factory.getMonsters(monsterCount, region, bonusDifficulty)

        #Declare battle
        print "Zonkle-tronks! Wild monsters appeared!"
        print ""

        return bonusDifficulty, monsters
    
    #For story-based battles
    elif context == constants.BattleEngineContext.STORY:
        #Create variables
        location = player.getLocation()
        region = location.getRegion()
        bonusDifficulty = location.getBattleBonusDifficulty()
    
        #Display splash screen
        print \
"""
()==[:::::::::::::> ()==[:::::::::::::> ()==[:::::::::::::>
""" 
        return bonusDifficulty
    
    else:
        errorMsg = "_battleSetup given invalid context parameter."
        raise AssertionError(errorMsg)

def _monsterNumGen(player):
    """
    Helper function used to determine the number of monsters to spawn.
    
    Default spawn comes from a parameter supplied by space. bonusDifficulty
    is then applied applied to increase the number of monsters spawned as
    a percentage increase over base spawn.
    
    @param player:     Player object.

    @return:           Number of monsters to spawn.
    """
    location = player.getLocation()
    region = location.getRegion()
    bonusDifficulty = location.getBattleBonusDifficulty()

    #Calculate region spawn
    if region == constants.RegionType.ERIADOR:
        monsterCount = (1 + bonusDifficulty) * constants.RegionBaseSpawn.ERIADOR
    elif region == constants.RegionType.BARROW_DOWNS:
        monsterCount = (1 + bonusDifficulty) * constants.RegionBaseSpawn.BARROW_DOWNS
    elif region == constants.RegionType.HIGH_PASS:
        monsterCount = (1 + bonusDifficulty) * constants.RegionBaseSpawn.HIGH_PASS
    elif region == constants.RegionType.ENEDWAITH:
        monsterCount = (1 + bonusDifficulty) * constants.RegionBaseSpawn.ENEDWAITH
    elif region == constants.RegionType.MORIA:
        monsterCount = (1 + bonusDifficulty) * constants.RegionBaseSpawn.MORIA
    elif region == constants.RegionType.RHOVANION:
        monsterCount = (1 + bonusDifficulty) * constants.RegionBaseSpawn.RHOVANION   
    elif region == constants.RegionType.ROHAN:
        monsterCount = (1 + bonusDifficulty) * constants.RegionBaseSpawn.ROHAN       
    elif region == constants.RegionType.GONDOR:
        monsterCount = (1 + bonusDifficulty) * constants.RegionBaseSpawn.GONDOR      
    elif region == constants.RegionType.MORDOR:
        monsterCount = (1 + bonusDifficulty) * constants.RegionBaseSpawn.MORDOR
    else:
        errorMsg = "Invalid region - region base monster determination."
        raise AssertionError(errorMsg)

    return monsterCount

def _playerAttackPhase(player, monsters, bonusDifficulty):
    """
    When the user gets to attack a single monster object.
    If monster health is reduced to zero, monster is removed
    from battle.

    Additionally, experience and money is calculated for winnings.

    @param player:        The player object.
    @param monsters:      The list of monster objects.

    @return:              2-element tuple carrying battle earnings.
                          First element is money earned, second
                          element is experience received.
    """
    #Starting battle earnings - by default, 0
    money      = 0
    experience = 0

    #Solicit attack target
    target = raw_input("Whom? ")
    print ""
    #Find monster object
    for monster in monsters:
        if monster.getName() == target:
            #Carry out attack
            player.attack(monster)
            print "%s did %s damage to %s!" % (player.getName(), player.getTotalAttack(), monster.getName())
            #If monster is still alive
            if monster.getHp() > 0:
                print "%s has %s hp remaining." % (monster.getName(), monster.getHp())
            #If monster has died
            else:
                print "%s" % monster.getDeathString()
                #Generate earnings from winning battle
                money += constants.BATTLE_EARNINGS * monster.getExperience() * (1 + bonusDifficulty)
                experience += monster.getExperience() * (1 + bonusDifficulty)
                #Remove monster from monsters list
                for monster in monsters:
                    if monster.getName() == target:
                        monsters.remove(monster)
                        #No need to keep iterating through monsters
                        break
            #No need to keep iterating through monsters
            break
    else:
        print "%s looks at you in confusion." % player.getName()
        
    return money, experience

def _usePotion(player):
    """
    Creates an additional UsePotionCommand object
    for battle purposes only.

    @param player:   The player object.
    """
    usePotionCmd = UsePotionCommand(" ", " ", player)
    usePotionCmd.execute()

def _monsterAttackPhase(player, monsters):
    """
    Monster attack phase - when monsters attack player.

    @param player:      The player object.
    @param monsters:    The offending list of monsters.

    @return:            True if battle is to continue. False
                        otherwise.
    """
    #Monsters attack
    for monster in monsters:
        monster.attack(player)
        print "%s %s for %s damage!" % (monster.getName(), monster.getAttackString(), monster.getAttack())
        print "%s has %s hp remaining." % (player.getName(), player.getHp())
        #If player loses battle
        if player.getHp() == 0:
            return False
    print ""
    return True
    
def _endSequence(player, earnings):
    """
    Battle cleanup:
    -Victory sequence displayed.
    -Player experience and money increase.

    @param player:      The player object.
    @param earnings:    2-element tuple: first element is money and second is experience.
    """
    money = earnings[0]
    experience = earnings[1]
    
    #Calculate splash screen variables
    victoryDeclaration = "Enemies are vanguished!"
    gainsDeclaration = "%s gains %s %s and %s experience!" % (player.getName(), money, constants.CURRENCY, experience)
    
    lengthBar = len(gainsDeclaration)
    victoryDeclaration = victoryDeclaration.center(lengthBar)
    bar = "$" * lengthBar
    
    #TODO: add items to victory sequence
    
    #Victory sequence
    print bar
    print victoryDeclaration
    print gainsDeclaration
    player.increaseMoney(money)
    player.increaseExperience(experience)
    print bar
    print ""
    
