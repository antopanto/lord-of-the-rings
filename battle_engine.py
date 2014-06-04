#!/usr/bin/python

import constants
import factories.monster_factory
from commands.use_potion_command import UsePotionCommand

import random

def battle(player):
    """
    Battle engine for Lord of the Rings

    @param player:     The player object.
    """
    location = player.getLocation()
    region = location.getRegion()
    bonusDifficulty = location.getBattleBonusDifficulty()

    #Calculate region spawn
    if region == constants.RegionType.ERIADOR:
        number = (1 + bonusDifficulty) * constants.RegionBaseSpawn.ERIADOR
    elif region == constants.RegionType.BARROW_DOWNS:
        number = (1 + bonusDifficulty) * constants.RegionBaseSpawn.BARROW_DOWNS
    elif region == constants.RegionType.HIGH_PASS:
        number = (1 + bonusDifficulty) * constants.RegionBaseSpawn.HIGH_PASS
    elif region == constants.RegionType.ENEDWAITH:
        number = (1 + bonusDifficulty) * constants.RegionBaseSpawn.ENEDWAITH
    elif region == constants.RegionType.MORIA:
        number = (1 + bonusDifficulty) * constants.RegionBaseSpawn.MORIA
    elif region == constants.RegionType.RHOVANION:
        number = (1 + bonusDifficulty) * constants.RegionBaseSpawn.RHOVANION   
    elif region == constants.RegionType.ROHAN:
        number = (1 + bonusDifficulty) * constants.RegionBaseSpawn.ROHAN       
    elif region == constants.RegionType.GONDOR:
        number = (1 + bonusDifficulty) * constants.RegionBaseSpawn.GONDOR      
    elif region == constants.RegionType.MORDOR:
        number = (1 + bonusDifficulty) * constants.RegionBaseSpawn.MORDOR
    else:
        errorMsg = "Invalid region - region base monster determination."
        raise AssertionError(errorMsg)
    
    #Spawn monsters
    monsters = factories.monster_factory.getMonsters(number, region, bonusDifficulty)

    #User prompt
    print "Zonkle-tronks! Wild monsters appeared!"
    print ""

    #Battle sequence
    while len(monsters) != 0:
        #User prompt
        print "Monsters:"
        for monster in monsters:
            print "\t%s: %s" % (monster.getName(), monster.getDescription())
        print ""
        choice = raw_input("You may: 'attack', 'use potion', 'run.' ")
        #Attack
        if choice == 'attack':
            earnings = playerAttackPhase(player, monsters, bonusDifficulty)
        #Use potion - TODO
        elif choice == "use potion":
            usePotion(player)
        #Attempt run
        elif choice == 'run':
            #TODO: Magic number
            if random.random() < constants.RUN_PROBABILITY_SUCCESS:
                print "You ran away succesfully!"
                return
            else:
                print "Your path is blocked!"
        #Invalid selection
        else:
            print "Huh?"
        print ""
        
        #Monsters attack phase
        monsterAttackPhase(player, monsters)

    #Battle end sequence - loot received
    endSequence(player, earnings)

def playerAttackPhase(player, monsters, bonusDifficulty):
    """
    When the user gets to attack a single monster object.
    If monster health is reduced to zero, monster is removed
    from battle.

    Additionally, experience and money is calculated for winnings.

    @param player:        The player object.
    @param monsters:      The list of monster objects.

    @return experience:   The experience Player is to receive upon winning the battle.
    @return money:        The money Player is to receive upon winning the battle.
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

def monsterAttackPhase(player, monsters):
    """
    Monster attack phase - when monsters attack player.

    @param player:      The player object.
    @param monsters:    The offending list of monsters.
    """
    #Monsters attack
    for monster in monsters:
        monster.attack(player)
        print "%s %s for %s damage!" % (monster.getName(), monster.getAttackString(), monster.getAttack())
        print "%s has %s hp remaining." % (player.getName(), player.getHp())
        #TODO: check if player is still alive
    print ""

def usePotion(player):
    """
    Creates an additional UsePotionCommand object
    for battle purposes only.

    @param player:   The player object.
    """
    usePotionCmd = UsePotionCommand(" ", " ", player)
    usePotionCmd.execute()
    
def endSequence(player, earnings):
    """
    Battle cleanup - player experience and money increases, etc.

    @param player:      The player object.
    @param earnings:    2-element list: first element is money and second is experience.
    """
    money = earnings[0]
    experience = earnings[1]
    #Calculate splash screen variables
    lengthBar = len("%s gains %s %s and %s experience!" % (player.getName(), money, constants.CURRENCY, experience))
    bar = "$" * lengthBar
    victoryDeclaration = "Enemies are vanguished!"
    victoryDeclaration = victoryDeclaration.center(lengthBar)
    
    #TODO: add items to victory sequence
    
    print bar
    print victoryDeclaration
    print "%s gains %s %s and %s experience!" % (player.getName(), money, constants.CURRENCY, experience)
    player.increaseMoney(money)
    player.increaseExperience(experience)
    print bar
    
