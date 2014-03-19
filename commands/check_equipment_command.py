from command import Command
from items.weapon import Weapon
from items.armor import Armor

class CheckEquipmentCommand(Command):
    """
    Prints player equipment and details equipment stats.
    """
    def __init__(self, name, explanation, player):
        """
        Initializes new check equipment command.

        @param name:         Command name.
        @param explanation:  Explanation of command.
        @param player:       The player object
        """
        #Call parent's init method
        Command.__init__(self, name, explanation)

        #Finish initializing help-specific settings
        self._player = player

    def execute(self):
        """
        Equips player with item in inventory.
        """
        playerName = self._player.getName()
        equipment = self._player.getEquipped()
        
        for item in equipment:
            nameItem = item.getName()
            if isinstance(item, Weapon):
                attack = item.getAttack()
                print "%s currently wields %s as a his weapon." %(namePlayer, nameItem)
                print "%s yields a %s attack bonus." %attack
            elif isinstance(item, Armor):
                defense = item.getDefense()
                print "%s currently wields %s as a his weapon." %(namePlayer, nameItem)
                print "%s yields a %s attack bonus." %defense