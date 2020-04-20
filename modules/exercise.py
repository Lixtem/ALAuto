from util.logger import Logger
from util.config import Config
from util.utils import Utils, Region


class ExerciseModule(object):
    def __init__(self, config, stats):
        """Initializes the Exercise module.

        Args:
            config (Config): ALAuto Config instance
        """
        self.enabled = True
        self.config = config
        self.stats = stats
        self.region = {
            'menu_battle_button': Region(1515, 440, 213, 206),
            'entry_exercise_tab': Region(1664, 976, 204, 76),
            'main_menu_exit_button': Region(1821, 28, 46, 46),
            'first_player': Region(162, 122, 308, 443),
            'start_attack_tab': Region(815, 808, 296, 91),
            'start_battle_tab': Region(1565, 911, 295, 90),
            'confirm_tab': Region(1501, 948, 258, 84),
            'close_defeat_tab': Region(777, 885, 332, 76),
            'go_back_button': Region(48, 45, 78, 73)
        }

    def exercise_logic_wrapper(self):
        Logger.log_msg("Initialized exercise module.")
        Utils.menu_navigate("menu/button_battle")
        Utils.touch_randomly(self.region['menu_battle_button'])
        Utils.script_sleep(1)
        Utils.touch_randomly(self.region['entry_exercise_tab'])
        attempts = True
        while attempts:
            Utils.wait_update_screen(2)
            if Utils.find('exercise/0_of_10', 0.99) and not Utils.find('exercise/full', 0.99):
                #ocr
                attempts = False
                break
            if self.attack_player():
                Logger.log_success("Successfully attacked player.")
            else:
                attempts = False
                break

        Logger.log_msg("There are no more exercises.")
        Utils.touch_randomly(self.region['main_menu_exit_button'])
        Utils.wait_update_screen(1)
        return True
        
    def attack_player(self):
        Logger.log_msg("Attacking player.")
        Utils.touch_randomly(self.region['first_player'])
        Utils.wait_update_screen(1)
        Utils.touch_randomly(self.region['start_attack_tab'])
        Utils.script_sleep(1)
        Utils.touch_randomly(self.region['start_battle_tab'])
        Utils.wait_update_screen(1)
        if Utils.find("exercise/NotEnough"):
            Logger.log_msg("Not enough exercises.")
            Utils.touch_randomly(self.region['go_back_button'])
            return False
        Utils.wait_update_screen(1)
        while Utils.find("combat/menu_loading", 0.7) or Utils.find("combat/combat_pause", 0.7):
            Utils.wait_update_screen(5)
        Utils.touch_randomly(self.region['confirm_tab'])
        Utils.script_sleep(2)
        Utils.touch_randomly(self.region['confirm_tab'])
        Utils.script_sleep(3)
        Utils.touch_randomly(self.region['confirm_tab'])
        Utils.wait_update_screen(1)
        if Utils.find("combat/defeat_close_button", 0.7):
            Logger.log_msg("Fight result: Annihilated.")
            Utils.touch_randomly(self.region['close_defeat_tab'])
        else:
            Logger.log_msg("Fight result: Victory.")
        return True



