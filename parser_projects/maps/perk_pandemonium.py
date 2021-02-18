from parser_projects.parser_imports import *
from parser_projects.help_functions import *
NUMBER_OF_PLAYERS = 8
inname = f"BLANK_SCENARIO_FILE_NAME_FOR_APPROPRIATE_NUMBER_OF_PLAYERS"
outname = f"OUTPUT_SCENARIO_FILE_NAME"
scenario = AoE2Scenario.from_file(input_path+inname)
trigger_manager = scenario.trigger_manager

# define all constants

COLOUR = ["BLUE", "RED", "GREEN", "YELLOW", "AQUA", "PURPLE", "GREY", "ORANGE"]

CEASE_FIRE_DURATION = 60
CEASE_FIRE_CD = 300
EV_DURATION = 60
STRIKE_DURATION = 30
TRADE_WORKSHOP_TRAIN_TIME = 60

# variable ids
CEASE_FIRE_CD_VAR = 0
CEASE_FIRE_PLAYER_CD_VARS = [i for i in range(1, NUMBER_OF_PLAYERS+1)]
EV_CD_VAR = 9
PAGE_VAR = [247+i for i in range(1, NUMBER_OF_PLAYERS+1)]
STRIKE_CD_VAR = [9+i for i in range(1, NUMBER_OF_PLAYERS+1)]


KILL_ALL_VILLAGERS_COST = [10000, 0, 0, 0]
KILL_ALL_MILITARY_COST = [0, 0, 4000, 0]
CEASE_FIRE_COST = [0, 200, 200, 0]
EV_COST = [0, 0, 1000, 0]
KILL_ALL_CASTLES_COST = [0, 5000, 500, 500]
REPLACE_MILITARY_WOLF_COST = [0, 0, 2000, 0]
CYCLE_ARCHER_COST = [0, 0, 1000, 0]
REPLACE_MAA_SPEAR_COST = [0, 1000, 500, 0]
REPLACE_ARCHER_SKIRM_COST = [0, 1000, 500, 0]
REPLACE_SIEGE_PETARD_TREB_COST = [0, 1000, 500, 0]
STOP_ENEMY_VILLAGERS_COST = [500, 0, 500, 0]
LABOUR_STRIKE_COST = [0, 1000, 0, 500]
TRADE_WORKSHOP_COST = [0, 200, 0, 50]

# misc
GARRISONABLE = [Building.TOWN_CENTER, Building.WATCH_TOWER, Building.GUARD_TOWER, Building.KEEP, Building.BOMBARD_TOWER, Building.HOUSE]
GARRISONABLE_MILITARY = [Building.ARCHERY_RANGE, Building.BARRACKS, Building.STABLE, Building.SIEGE_WORKSHOP, Building.KREPOST, Building.CASTLE, Building.DOCK, Building.MONASTERY]
SIEGE_UNITS = [Unit.MANGONEL, Unit.ONAGER, Unit.SIEGE_ONAGER, Unit.SIEGE_TOWER, Unit.BATTERING_RAM, Unit.CAPPED_RAM, Unit.SIEGE_RAM, Unit.SCORPION, Unit.HEAVY_SCORPION, Unit.BOMBARD_CANNON, Unit.TREBUCHET, Unit.TREBUCHET_PACKED, Unit.ORGAN_GUN, Unit.ELITE_ORGAN_GUN]
VILLAGER = [Unit.VILLAGER_MALE, Unit.VILLAGER_FEMALE, Unit.BUILDER, 212, Unit.REPAIRER, 222, Unit.FARMER, 214, Unit.HUNTER, 216, Unit.FORAGER, 354, Unit.FISHERMAN, 57, Unit.SHEPHERD, 590, Unit.GOLD_MINER, 581, Unit.STONE_MINER, 220, Unit.LUMBERJACK, 218]
VILLAGER_DEAD = [224, 221, 225, 213, 225, 213, 226, 215, 227, 217, 353, 355, 58, 60, 591, 593, 229, 221, 229, 221, 228, 219]


def enable_unit(prefix, trigger_unit, train_location, train_button, train_time, cost, description):
    trigger = trigger_manager.add_trigger("{0} Change Train Location".format(prefix))
    for player in range(1, NUMBER_OF_PLAYERS + 1):
        effect = trigger.add_effect(Effect.CHANGE_TRAIN_LOCATION)
        effect.source_player = player
        effect.object_list_unit_id = trigger_unit
        effect.object_list_unit_id_2 = train_location
        effect.button_location = train_button

    trigger = trigger_manager.add_trigger("Change Cost pre")
    for player in range(1, NUMBER_OF_PLAYERS + 1):
        effect = trigger.add_effect(Effect.MODIFY_ATTRIBUTE)
        effect.source_player = player
        effect.object_list_unit_id = trigger_unit
        effect.item_id = trigger_unit
        effect.object_attributes = ObjectAttribute.GOLD_COSTS
        effect.operation = Operation.SET
        effect.quantity = 0

    trigger = trigger_manager.add_trigger("{0} Change Cost".format(prefix))
    for player in range(1, NUMBER_OF_PLAYERS + 1):
        effect = trigger.add_effect(Effect.CHANGE_OBJECT_COST)
        effect.source_player = player
        effect.object_list_unit_id = trigger_unit
        effect.food = cost[0]
        effect.wood = cost[1]
        effect.gold = cost[2]
        effect.stone = cost[3]

    trigger = trigger_manager.add_trigger("{0} Change Train Time".format(prefix))
    for player in range(1, NUMBER_OF_PLAYERS + 1):
        effect = trigger.add_effect(Effect.MODIFY_ATTRIBUTE)
        effect.quantity = train_time
        effect.object_list_unit_id = trigger_unit
        effect.source_player = player
        effect.item_id = trigger_unit
        effect.operation = Operation.SET
        effect.object_attributes = ObjectAttribute.TRAIN_TIME

    trigger = trigger_manager.add_trigger("{0} Change Description".format(prefix))
    for player in range(1, NUMBER_OF_PLAYERS + 1):
        effect = trigger.add_effect(Effect.CHANGE_OBJECT_DESCRIPTION)
        effect.source_player = player
        effect.object_list_unit_id = trigger_unit
        effect.message = "{0}".format(description)
def setup():
    trigger = trigger_manager.add_trigger("==== Setup ====")
    correct_scout(NUMBER_OF_PLAYERS, trigger_manager)

    trigger = trigger_manager.add_trigger("Enable Trade Workshop")
    for player in range(1, NUMBER_OF_PLAYERS + 1):
        effect = trigger.add_effect(Effect.ENABLE_DISABLE_OBJECT)
        effect.source_player = player
        effect.item_id = Building.TRADE_WORKSHOP
        effect.enabled_or_victory = 1
        effect.object_list_unit_id = Building.TRADE_WORKSHOP

    trigger = trigger_manager.add_trigger("Disable Carto")
    for player in range(1, NUMBER_OF_PLAYERS + 1):
        effect = trigger.add_effect(Effect.ENABLE_DISABLE_TECHNOLOGY)
        effect.source_player = player
        effect.technology = Tech.CARTOGRAPHY
        effect.item_id = Tech.CARTOGRAPHY
        effect.enabled_or_victory = 0

        effect = trigger.add_effect(Effect.ENABLE_DISABLE_TECHNOLOGY)
        effect.source_player = player
        effect.technology = Tech.FREE_CARTOGRAPHY
        effect.item_id = Tech.FREE_CARTOGRAPHY
        effect.enabled_or_victory = 0

        effect = trigger.add_effect(Effect.MODIFY_RESOURCE)
        effect.source_player = player
        effect.quantity = 0
        effect.tribute_list = Attribute.REVEAL_ALLY
        effect.operation = Operation.SET

    trigger = trigger_manager.add_trigger("Disable Wonder")
    for player in range(1, NUMBER_OF_PLAYERS + 1):
        effect = trigger.add_effect(Effect.ENABLE_DISABLE_OBJECT)
        effect.source_player = player
        effect.item_id = Building.WONDER
        effect.enabled_or_victory = 0
        effect.object_list_unit_id = Building.WONDER

    trigger = trigger_manager.add_trigger("Change Train Location")
    for player in range(1, NUMBER_OF_PLAYERS + 1):
        effect = trigger.add_effect(Effect.CHANGE_TRAIN_LOCATION)
        effect.source_player = player
        effect.object_list_unit_id = Building.TRADE_WORKSHOP
        effect.object_list_unit_id_2 = Unit.VILLAGER_MALE
        effect.button_location = 12

    trigger = trigger_manager.add_trigger("Change Cost pre")
    for player in range(1, NUMBER_OF_PLAYERS + 1):
        effect = trigger.add_effect(Effect.MODIFY_ATTRIBUTE)
        effect.source_player = player
        effect.object_list_unit_id = Building.TRADE_WORKSHOP
        effect.item_id = Building.TRADE_WORKSHOP
        effect.object_attributes = ObjectAttribute.GOLD_COSTS
        effect.operation = Operation.SET
        effect.quantity = 0

    trigger = trigger_manager.add_trigger("Change Cost")
    for player in range(1, NUMBER_OF_PLAYERS + 1):
        effect = trigger.add_effect(Effect.CHANGE_OBJECT_COST)
        effect.source_player = player
        effect.object_list_unit_id = Building.TRADE_WORKSHOP
        effect.food = TRADE_WORKSHOP_COST[0]
        effect.wood = TRADE_WORKSHOP_COST[1]
        effect.gold = TRADE_WORKSHOP_COST[2]
        effect.stone = TRADE_WORKSHOP_COST[3]

    trigger = trigger_manager.add_trigger("Change Train Time")
    for player in range(1, NUMBER_OF_PLAYERS + 1):
        effect = trigger.add_effect(Effect.MODIFY_ATTRIBUTE)
        effect.quantity = TRADE_WORKSHOP_TRAIN_TIME
        effect.object_list_unit_id = Building.TRADE_WORKSHOP
        effect.source_player = player
        effect.item_id = Building.TRADE_WORKSHOP
        effect.operation = Operation.SET
        effect.object_attributes = ObjectAttribute.TRAIN_TIME

    trigger = trigger_manager.add_trigger("Change Description")
    for player in range(1, NUMBER_OF_PLAYERS + 1):
        effect = trigger.add_effect(Effect.CHANGE_OBJECT_DESCRIPTION)
        effect.source_player = player
        effect.object_list_unit_id = Building.TRADE_WORKSHOP
        effect.message = "Build Trade Workshop (<Cost>)\nAllows you to buy special perks\n<hp> <attack> <armor> <piercearmor> <garrison> LoS: 4"

    add_civ_bonuses(NUMBER_OF_PLAYERS, trigger_manager)
def perk_setup(name, cost, trigger_unit, train_button, description, enabled, icon_unit):
    trigger = trigger_manager.add_trigger("==== {0} ====".format(name))
    if enabled:
        trigger = trigger_manager.add_trigger("Enable")
        for player in range(1, NUMBER_OF_PLAYERS + 1):
            effect = trigger.add_effect(Effect.ENABLE_DISABLE_OBJECT)
            effect.source_player = player
            effect.item_id = trigger_unit
            effect.enabled_or_victory = 1
            effect.object_list_unit_id = trigger_unit

    trigger = trigger_manager.add_trigger("Change Train Location")
    for player in range(1, NUMBER_OF_PLAYERS + 1):
        effect = trigger.add_effect(Effect.CHANGE_TRAIN_LOCATION)
        effect.source_player = player
        effect.object_list_unit_id = trigger_unit
        effect.object_list_unit_id_2 = Building.TRADE_WORKSHOP
        effect.button_location = train_button

    trigger = trigger_manager.add_trigger("Change Icon")
    for player in range(1, NUMBER_OF_PLAYERS + 1):
        effect = trigger.add_effect(Effect.MODIFY_ATTRIBUTE)
        effect.source_player = player
        effect.quantity = icon_unit
        effect.object_list_unit_id = trigger_unit
        effect.item_id = trigger_unit
        effect.operation = Operation.SET
        effect.object_attributes = 25

    trigger = trigger_manager.add_trigger("Change Cost pre")
    for player in range(1, NUMBER_OF_PLAYERS + 1):
        effect = trigger.add_effect(Effect.MODIFY_ATTRIBUTE)
        effect.source_player = player
        effect.object_list_unit_id = trigger_unit
        effect.item_id = trigger_unit
        effect.object_attributes = ObjectAttribute.GOLD_COSTS
        effect.operation = Operation.SET
        effect.quantity = 0

    trigger = trigger_manager.add_trigger("Change Cost")
    for player in range(1, NUMBER_OF_PLAYERS + 1):
        effect = trigger.add_effect(Effect.CHANGE_OBJECT_COST)
        effect.source_player = player
        effect.object_list_unit_id = trigger_unit
        effect.food = cost[0]
        effect.wood = cost[1]
        effect.gold = cost[2]
        effect.stone = cost[3]

    trigger = trigger_manager.add_trigger("Change Train Time")
    for player in range(1, NUMBER_OF_PLAYERS + 1):
        effect = trigger.add_effect(Effect.MODIFY_ATTRIBUTE)
        effect.quantity = 0
        effect.object_list_unit_id = trigger_unit
        effect.source_player = player
        effect.item_id = trigger_unit
        effect.operation = Operation.SET
        effect.object_attributes = ObjectAttribute.TRAIN_TIME

    trigger = trigger_manager.add_trigger("Change Pop Requirement")
    for player in range(1, NUMBER_OF_PLAYERS + 1):
        effect = trigger.add_effect(Effect.MODIFY_ATTRIBUTE)
        effect.quantity = 0
        effect.object_list_unit_id = trigger_unit
        effect.source_player = player
        effect.item_id = trigger_unit
        effect.operation = Operation.SET
        effect.object_attributes = ObjectAttribute.AMOUNT_OF_1ST_RESOURCES

    trigger = trigger_manager.add_trigger("Change Description")
    for player in range(1, NUMBER_OF_PLAYERS + 1):
        effect = trigger.add_effect(Effect.CHANGE_OBJECT_DESCRIPTION)
        effect.source_player = player
        effect.object_list_unit_id = trigger_unit
        effect.message = "{0}".format(description)
def kill_all_villagers(trigger_unit):
    for player in range(1, NUMBER_OF_PLAYERS + 1):
        trigger = trigger_manager.add_trigger("kill villagers (p{0})".format(player))
        trigger.looping = 1
        condition = trigger.add_condition(Condition.OWN_OBJECTS)
        condition.amount_or_quantity = 1
        condition.object_list = trigger_unit
        condition.source_player = player
        effect = trigger.add_effect(Effect.REMOVE_OBJECT)
        effect.source_player = player
        effect.object_list_unit_id = trigger_unit
        effect = trigger.add_effect(Effect.DISPLAY_INSTRUCTIONS)
        effect.object_list_unit_id = Unit.VILLAGER_MALE
        effect.source_player = player
        effect.display_time = 10
        effect.instruction_panel_position = PanelLocation.TOP
        effect.message = "<{1}>P{0} has killed all enemy villagers!".format(player, COLOUR[player-1])
        for affectedplayer in range(1, NUMBER_OF_PLAYERS + 1):
            for building in GARRISONABLE[:]+[Building.CASTLE, Building.KREPOST]:
                effect = trigger.add_effect(Effect.UNLOAD)
                effect.object_list_unit_id = building
                effect.source_player = affectedplayer
                effect.location_x = 1
                effect.location_y = 1
            effect = trigger.add_effect(Effect.KILL_OBJECT)
            effect.source_player = affectedplayer
            effect.object_type = 3
def kill_all_military(trigger_unit):
    for player in range(1, NUMBER_OF_PLAYERS + 1):
        trigger = trigger_manager.add_trigger("kill military (p{0})".format(player))
        trigger.looping = 1
        condition = trigger.add_condition(Condition.OWN_OBJECTS)
        condition.amount_or_quantity = 1
        condition.object_list = trigger_unit
        condition.source_player = player
        effect = trigger.add_effect(Effect.REMOVE_OBJECT)
        effect.source_player = player
        effect.object_list_unit_id = trigger_unit
        effect = trigger.add_effect(Effect.DISPLAY_INSTRUCTIONS)
        effect.object_list_unit_id = Building.BARRACKS
        effect.source_player = player
        effect.display_time = 10
        effect.instruction_panel_position = PanelLocation.TOP
        effect.message = "<{1}>P{0} has killed all enemy military!".format(player, COLOUR[player-1])
        for affectedplayer in range(1, NUMBER_OF_PLAYERS + 1):
            if affectedplayer != player:
                for building in GARRISONABLE+GARRISONABLE_MILITARY:
                    effect = trigger.add_effect(Effect.UNLOAD)
                    effect.object_list_unit_id = building
                    effect.source_player = affectedplayer
                    effect.location_x = 1
                    effect.location_y = 1
                effect = trigger.add_effect(Effect.KILL_OBJECT)
                effect.source_player = affectedplayer
                effect.object_type = 4
def cease_fire(trigger_unit):
    trigger = trigger_manager.add_trigger("make peace")
    trigger.enabled = 0
    trigger_id1 = trigger.trigger_id
    for source_player in range(1, NUMBER_OF_PLAYERS+1):
        for target_player in range(1, NUMBER_OF_PLAYERS+1):
            if source_player != target_player:
                effect = trigger.add_effect(Effect.CHANGE_DIPLOMACY)
                effect.diplomacy = DiplomacyState.ALLY
                effect.source_player = source_player
                effect.target_player = target_player

    trigger = trigger_manager.add_trigger("make war")
    trigger.enabled = 0
    condition = trigger.add_condition(Condition.VARIABLE_VALUE)
    condition.amount_or_quantity = 0
    condition.variable = CEASE_FIRE_CD_VAR
    condition.inverted = 0
    condition.comparison = Comparison.EQUAL
    effect = trigger.add_effect(Effect.DISPLAY_INSTRUCTIONS)
    effect.object_list_unit_id = GaiaUnit.HAWK
    effect.source_player = Player.GAIA
    effect.display_time = 10
    effect.instruction_panel_position = PanelLocation.TOP
    effect.message = "Cease Fire Has Ended!"
    for source_player in range(1, NUMBER_OF_PLAYERS+1):
        for target_player in range(1, NUMBER_OF_PLAYERS+1):
            if source_player != target_player:
                effect = trigger.add_effect(Effect.CHANGE_DIPLOMACY)
                effect.diplomacy = DiplomacyState.ENEMY
                effect.source_player = source_player
                effect.target_player = target_player
    trigger_id2 = trigger.trigger_id

    for player in range(1, NUMBER_OF_PLAYERS + 1):
        trigger = trigger_manager.add_trigger("cease fire (p{0})".format(player))
        trigger.looping = 1
        condition = trigger.add_condition(Condition.OWN_OBJECTS)
        condition.amount_or_quantity = 1
        condition.object_list = trigger_unit
        condition.source_player = player
        condition = trigger.add_condition(Condition.VARIABLE_VALUE)
        condition.amount_or_quantity = 0
        condition.variable = CEASE_FIRE_PLAYER_CD_VARS[player-1]
        condition.inverted = 0
        condition.comparison = Comparison.EQUAL
        effect = trigger.add_effect(Effect.REMOVE_OBJECT)
        effect.source_player = player
        effect.object_list_unit_id = trigger_unit
        effect = trigger.add_effect(Effect.ENABLE_DISABLE_OBJECT)
        effect.item_id = trigger_unit
        effect.object_list_unit_id = trigger_unit
        effect.enabled_or_victory = 0
        effect.source_player = player
        effect = trigger.add_effect(Effect.CHANGE_VARIABLE)
        effect.quantity = CEASE_FIRE_CD
        effect.from_variable = CEASE_FIRE_PLAYER_CD_VARS[player-1]
        effect.operation = Operation.SET
        effect = trigger.add_effect(Effect.CHANGE_VARIABLE)
        effect.quantity = CEASE_FIRE_DURATION
        effect.from_variable = CEASE_FIRE_CD_VAR
        effect.operation = Operation.ADD
        effect = trigger.add_effect(Effect.DISPLAY_INSTRUCTIONS)
        effect.object_list_unit_id = GaiaUnit.HAWK
        effect.source_player = Player.GAIA
        effect.display_time = 10
        effect.instruction_panel_position = PanelLocation.TOP
        effect.message = "<{1}>P{0} has called for a cease fire!".format(player, COLOUR[player-1])
        effect = trigger.add_effect(Effect.ACTIVATE_TRIGGER)
        effect.trigger_id = trigger_id1
        effect = trigger.add_effect(Effect.ACTIVATE_TRIGGER)
        effect.trigger_id = trigger.trigger_id+2
        effect = trigger.add_effect(Effect.ACTIVATE_TRIGGER)
        effect.trigger_id = trigger_id2

        trigger = trigger_manager.add_trigger("Cooldown (p{0})".format(player))
        trigger.looping = 1
        condition = trigger.add_condition(Condition.VARIABLE_VALUE)
        condition.variable = CEASE_FIRE_PLAYER_CD_VARS[player-1]
        condition.amount_or_quantity = 0
        condition.comparison = Comparison.LARGER
        condition.inverted = 0
        condition = trigger.add_condition(Condition.TIMER)
        condition.timer = 1
        effect = trigger.add_effect(Effect.CHANGE_VARIABLE)
        effect.from_variable = CEASE_FIRE_PLAYER_CD_VARS[player-1]
        effect.operation = Operation.SUBTRACT
        effect.quantity = 1

        trigger = trigger_manager.add_trigger("Enable Unit p({0})".format(player))
        trigger.enabled = 0
        condition = trigger.add_condition(Condition.TIMER)
        condition.timer = CEASE_FIRE_CD
        effect = trigger.add_effect(Effect.ENABLE_DISABLE_OBJECT)
        effect.item_id = trigger_unit
        effect.object_list_unit_id = trigger_unit
        effect.enabled_or_victory = 1
        effect.source_player = player

    trigger = trigger_manager.add_trigger("cease fire")
    trigger.looping = 1
    trigger.short_description = "Cease Fire Ends in: <Variable {0}>s".format(CEASE_FIRE_CD_VAR)
    trigger.description = trigger.short_description
    trigger.display_as_objective = 1
    trigger.display_on_screen = 1
    condition = trigger.add_condition(Condition.VARIABLE_VALUE)
    condition.variable = CEASE_FIRE_CD_VAR
    condition.amount_or_quantity = 0
    condition.comparison = Comparison.LARGER
    condition.inverted = 0
    condition = trigger.add_condition(Condition.TIMER)
    condition.timer = 1
    effect = trigger.add_effect(Effect.CHANGE_VARIABLE)
    effect.from_variable = CEASE_FIRE_CD_VAR
    effect.operation = Operation.SUBTRACT
    effect.quantity = 1
def exploding_villagers(trigger_unit):
    trigger = trigger_manager.add_trigger("Set Sab attribs")
    for player in range(1, NUMBER_OF_PLAYERS + 1):
        effect = trigger.add_effect(Effect.MODIFY_ATTRIBUTE)
        effect.object_list_unit_id = Hero.SABOTEUR
        effect.item_id = Hero.SABOTEUR
        effect.source_player = player
        effect.operation = Operation.SET
        effect.object_attributes = ObjectAttribute.HIT_POINTS
        effect.quantity = -2
        effect = trigger.add_effect(Effect.MODIFY_ATTRIBUTE)
        effect.object_list_unit_id = Hero.SABOTEUR
        effect.item_id = Hero.SABOTEUR
        effect.source_player = player
        effect.operation = Operation.SET
        effect.object_attributes = ObjectAttribute.BLAST_LEVEL
        effect.quantity = 1
        effect = trigger.add_effect(Effect.MODIFY_ATTRIBUTE)
        effect.object_list_unit_id = Hero.SABOTEUR
        effect.item_id = Hero.SABOTEUR
        effect.source_player = player
        effect.operation = Operation.SET
        effect.object_attributes = ObjectAttribute.MAX_RANGE
        effect.quantity = 2

    trigger = trigger_manager.add_trigger("Activate EV")
    trigger_id1 = trigger.trigger_id
    trigger.enabled = 0
    for player in range(1, NUMBER_OF_PLAYERS + 1):
        for vil in VILLAGER:
            effect = trigger.add_effect(Effect.MODIFY_ATTRIBUTE)
            effect.object_list_unit_id = vil
            effect.item_id = vil
            effect.source_player = player
            effect.operation = Operation.SET
            effect.object_attributes = ObjectAttribute.DEAD_UNIT_ID
            effect.quantity = Hero.SABOTEUR

    trigger = trigger_manager.add_trigger("Deactivate EV")
    trigger_id2 = trigger.trigger_id
    trigger.enabled = 0
    condition = trigger.add_condition(Condition.VARIABLE_VALUE)
    condition.amount_or_quantity = 0
    condition.variable = EV_CD_VAR
    condition.inverted = 0
    condition.comparison = Comparison.EQUAL
    effect = trigger.add_effect(Effect.DISPLAY_INSTRUCTIONS)
    effect.object_list_unit_id = Hero.SABOTEUR
    effect.source_player = Player.GAIA
    effect.display_time = 10
    effect.instruction_panel_position = PanelLocation.TOP
    effect.message = "Exploding Villagers Has passed!"
    for player in range(1, NUMBER_OF_PLAYERS + 1):
        for i in range(0, len(VILLAGER)):
            effect = trigger.add_effect(Effect.MODIFY_ATTRIBUTE)
            effect.object_list_unit_id = VILLAGER[i]
            effect.item_id = VILLAGER[i]
            effect.source_player = player
            effect.operation = Operation.SET
            effect.object_attributes = ObjectAttribute.DEAD_UNIT_ID
            effect.quantity = VILLAGER_DEAD[i]

    for player in range(1, NUMBER_OF_PLAYERS + 1):
        trigger = trigger_manager.add_trigger("EV (p{0})".format(player))
        trigger.looping = 1
        condition = trigger.add_condition(Condition.OWN_OBJECTS)
        condition.amount_or_quantity = 1
        condition.object_list = trigger_unit
        condition.source_player = player
        effect = trigger.add_effect(Effect.REMOVE_OBJECT)
        effect.source_player = player
        effect.object_list_unit_id = trigger_unit
        effect = trigger.add_effect(Effect.DISPLAY_INSTRUCTIONS)
        effect.object_list_unit_id = Hero.SABOTEUR
        effect.source_player = player
        effect.display_time = 10
        effect.instruction_panel_position = PanelLocation.TOP
        effect.message = "<{1}>P{0} has activated Exploding Villagers!".format(player, COLOUR[player-1])
        effect = trigger.add_effect(Effect.ACTIVATE_TRIGGER)
        effect.trigger_id = trigger_id1
        effect = trigger.add_effect(Effect.ACTIVATE_TRIGGER)
        effect.trigger_id = trigger_id2
        effect = trigger.add_effect(Effect.CHANGE_VARIABLE)
        effect.from_variable = EV_CD_VAR
        effect.operation = Operation.ADD
        effect.quantity = EV_DURATION

    trigger = trigger_manager.add_trigger("EV Display")
    trigger.looping = 1
    trigger.short_description = "EV Ends in: <Variable {0}>s".format(EV_CD_VAR)
    trigger.description = trigger.short_description
    trigger.display_as_objective = 1
    trigger.display_on_screen = 1
    condition = trigger.add_condition(Condition.VARIABLE_VALUE)
    condition.variable = EV_CD_VAR
    condition.amount_or_quantity = 0
    condition.comparison = Comparison.LARGER
    condition.inverted = 0
    condition = trigger.add_condition(Condition.TIMER)
    condition.timer = 1
    effect = trigger.add_effect(Effect.CHANGE_VARIABLE)
    effect.from_variable = EV_CD_VAR
    effect.operation = Operation.SUBTRACT
    effect.quantity = 1
def kill_all_castles(trigger_unit):
    for player in range(1, NUMBER_OF_PLAYERS + 1):
        trigger = trigger_manager.add_trigger("kill castles (p{0})".format(player))
        trigger.looping = 1
        condition = trigger.add_condition(Condition.OWN_OBJECTS)
        condition.amount_or_quantity = 1
        condition.object_list = trigger_unit
        condition.source_player = player
        effect = trigger.add_effect(Effect.REMOVE_OBJECT)
        effect.source_player = player
        effect.object_list_unit_id = trigger_unit
        effect = trigger.add_effect(Effect.DISPLAY_INSTRUCTIONS)
        effect.object_list_unit_id = Building.BARRACKS
        effect.source_player = player
        effect.display_time = 10
        effect.instruction_panel_position = PanelLocation.TOP
        effect.message = "<{1}>P{0} has destroyed all enemy castles!".format(player, COLOUR[player-1])
        for affectedplayer in range(1, NUMBER_OF_PLAYERS + 1):
            if affectedplayer != player:
                effect = trigger.add_effect(Effect.KILL_OBJECT)
                effect.source_player = affectedplayer
                effect.object_list_unit_id = Building.CASTLE
def replace_all_military_with_wolves(trigger_unit):
    for player in range(1, NUMBER_OF_PLAYERS + 1):
        trigger = trigger_manager.add_trigger("replace mil with wolves (p{0})".format(player))
        trigger.looping = 1
        condition = trigger.add_condition(Condition.OWN_OBJECTS)
        condition.amount_or_quantity = 1
        condition.object_list = trigger_unit
        condition.source_player = player
        effect = trigger.add_effect(Effect.REMOVE_OBJECT)
        effect.source_player = player
        effect.object_list_unit_id = trigger_unit
        effect = trigger.add_effect(Effect.DISPLAY_INSTRUCTIONS)
        effect.object_list_unit_id = Hero.ORNLU_THE_WOLF
        effect.source_player = player
        effect.display_time = 10
        effect.instruction_panel_position = PanelLocation.TOP
        effect.message = "<{1}>P{0} has converted all enemy military to wolves!".format(player, COLOUR[player-1])
        for affectedplayer in range(1, NUMBER_OF_PLAYERS + 1):
            if affectedplayer != player:
                for building in GARRISONABLE+GARRISONABLE_MILITARY:
                    effect = trigger.add_effect(Effect.UNLOAD)
                    effect.object_list_unit_id = building
                    effect.source_player = affectedplayer
                    effect.location_x = 1
                    effect.location_y = 1
                effect = trigger.add_effect(Effect.REPLACE_OBJECT)
                effect.source_player = affectedplayer
                effect.target_player = affectedplayer
                effect.object_list_unit_id_2 = Hero.HUNTING_WOLF
                effect.object_type = 4
def cycle_archer_line(trigger_unit):
    for player in range(1, NUMBER_OF_PLAYERS + 1):
        trigger = trigger_manager.add_trigger("cycle archer line (p{0})".format(player))
        trigger.looping = 1
        condition = trigger.add_condition(Condition.OWN_OBJECTS)
        condition.amount_or_quantity = 1
        condition.object_list = trigger_unit
        condition.source_player = player
        effect = trigger.add_effect(Effect.REMOVE_OBJECT)
        effect.source_player = player
        effect.object_list_unit_id = trigger_unit
        effect = trigger.add_effect(Effect.DISPLAY_INSTRUCTIONS)
        effect.object_list_unit_id = Unit.ARCHER
        effect.source_player = player
        effect.display_time = 10
        effect.instruction_panel_position = PanelLocation.TOP
        effect.message = "<{1}>P{0} has cycled the archer line of enemies!".format(player, COLOUR[player-1])
        for affectedplayer in range(1, NUMBER_OF_PLAYERS + 1):
            if affectedplayer != player:
                for building in GARRISONABLE + [Building.ARCHERY_RANGE]:
                    effect = trigger.add_effect(Effect.UNLOAD)
                    effect.object_list_unit_id = building
                    effect.source_player = affectedplayer
                    effect.location_x = 1
                    effect.location_y = 1
                effect = trigger.add_effect(Effect.REPLACE_OBJECT)
                effect.source_player = affectedplayer
                effect.target_player = affectedplayer
                effect.object_list_unit_id = Unit.ARBALESTER
                effect.object_list_unit_id_2 = Hero.ARCHBISHOP
                effect = trigger.add_effect(Effect.REPLACE_OBJECT)
                effect.source_player = affectedplayer
                effect.target_player = affectedplayer
                effect.object_list_unit_id = Unit.CROSSBOWMAN
                effect.object_list_unit_id_2 = Hero.CUMAN_CHIEF
                effect = trigger.add_effect(Effect.REPLACE_OBJECT)
                effect.source_player = affectedplayer
                effect.target_player = affectedplayer
                effect.object_list_unit_id = Unit.ARCHER
                effect.object_list_unit_id_2 = Unit.ARBALESTER
                effect = trigger.add_effect(Effect.REPLACE_OBJECT)
                effect.source_player = affectedplayer
                effect.target_player = affectedplayer
                effect.object_list_unit_id = Hero.ARCHBISHOP
                effect.object_list_unit_id_2 = Unit.CROSSBOWMAN
                effect = trigger.add_effect(Effect.REPLACE_OBJECT)
                effect.source_player = affectedplayer
                effect.target_player = affectedplayer
                effect.object_list_unit_id = Hero.CUMAN_CHIEF
                effect.object_list_unit_id_2 = Unit.ARCHER
def replace_maa_line(trigger_unit):
    for player in range(1, NUMBER_OF_PLAYERS + 1):
        trigger = trigger_manager.add_trigger("replace maa (p{0})".format(player))
        trigger.looping = 1
        condition = trigger.add_condition(Condition.OWN_OBJECTS)
        condition.amount_or_quantity = 1
        condition.object_list = trigger_unit
        condition.source_player = player
        effect = trigger.add_effect(Effect.REMOVE_OBJECT)
        effect.source_player = player
        effect.object_list_unit_id = trigger_unit
        effect = trigger.add_effect(Effect.DISPLAY_INSTRUCTIONS)
        effect.object_list_unit_id = Unit.CHAMPION
        effect.source_player = player
        effect.display_time = 10
        effect.instruction_panel_position = PanelLocation.TOP
        effect.message = "<{1}>P{0} has swapped all swords with spears!".format(player,COLOUR[player - 1])
        for affectedplayer in range(1, NUMBER_OF_PLAYERS + 1):
            if affectedplayer != player:
                for building in GARRISONABLE + [Building.BARRACKS]:
                    effect = trigger.add_effect(Effect.UNLOAD)
                    effect.object_list_unit_id = building
                    effect.source_player = affectedplayer
                    effect.location_x = 1
                    effect.location_y = 1
                effect = trigger.add_effect(Effect.REPLACE_OBJECT)
                effect.source_player = affectedplayer
                effect.target_player = affectedplayer
                effect.object_list_unit_id = Unit.CHAMPION
                effect.object_list_unit_id_2 = Unit.HALBERDIER
                effect = trigger.add_effect(Effect.REPLACE_OBJECT)
                effect.source_player = affectedplayer
                effect.target_player = affectedplayer
                effect.object_list_unit_id = Unit.TWO_HANDED_SWORDSMAN
                effect.object_list_unit_id_2 = Unit.HALBERDIER
                effect = trigger.add_effect(Effect.REPLACE_OBJECT)
                effect.source_player = affectedplayer
                effect.target_player = affectedplayer
                effect.object_list_unit_id = Unit.LONG_SWORDSMAN
                effect.object_list_unit_id_2 = Unit.PIKEMAN
                effect = trigger.add_effect(Effect.REPLACE_OBJECT)
                effect.source_player = affectedplayer
                effect.target_player = affectedplayer
                effect.object_list_unit_id = Unit.MAN_AT_ARMS
                effect.object_list_unit_id_2 = Unit.SPEARMAN
                effect = trigger.add_effect(Effect.REPLACE_OBJECT)
                effect.source_player = affectedplayer
                effect.target_player = affectedplayer
                effect.object_list_unit_id = Unit.MILITIA
                effect.object_list_unit_id_2 = Unit.SPEARMAN
def replace_archer_line(trigger_unit):
    for player in range(1, NUMBER_OF_PLAYERS + 1):
        trigger = trigger_manager.add_trigger("replace archer (p{0})".format(player))
        trigger.looping = 1
        condition = trigger.add_condition(Condition.OWN_OBJECTS)
        condition.amount_or_quantity = 1
        condition.object_list = trigger_unit
        condition.source_player = player
        effect = trigger.add_effect(Effect.REMOVE_OBJECT)
        effect.source_player = player
        effect.object_list_unit_id = trigger_unit
        effect = trigger.add_effect(Effect.DISPLAY_INSTRUCTIONS)
        effect.object_list_unit_id = Unit.IMPERIAL_SKIRMISHER
        effect.source_player = player
        effect.display_time = 10
        effect.instruction_panel_position = PanelLocation.TOP
        effect.message = "<{1}>P{0} has swapped all bows with javlins!".format(player,COLOUR[player - 1])
        for affectedplayer in range(1, NUMBER_OF_PLAYERS + 1):
            if affectedplayer != player:
                for building in GARRISONABLE + [Building.ARCHERY_RANGE]:
                    effect = trigger.add_effect(Effect.UNLOAD)
                    effect.object_list_unit_id = building
                    effect.source_player = affectedplayer
                    effect.location_x = 1
                    effect.location_y = 1
                effect = trigger.add_effect(Effect.REPLACE_OBJECT)
                effect.source_player = affectedplayer
                effect.target_player = affectedplayer
                effect.object_list_unit_id = Unit.ARBALESTER
                effect.object_list_unit_id_2 = Unit.IMPERIAL_SKIRMISHER
                effect = trigger.add_effect(Effect.REPLACE_OBJECT)
                effect.source_player = affectedplayer
                effect.target_player = affectedplayer
                effect.object_list_unit_id = Unit.CROSSBOWMAN
                effect.object_list_unit_id_2 = Unit.ELITE_SKIRMISHER
                effect = trigger.add_effect(Effect.REPLACE_OBJECT)
                effect.source_player = affectedplayer
                effect.target_player = affectedplayer
                effect.object_list_unit_id = Unit.ARCHER
                effect.object_list_unit_id_2 = Unit.SKIRMISHER
def replace_siege_petard_treb(trigger_unit):
    for player in range(1, NUMBER_OF_PLAYERS + 1):
        trigger = trigger_manager.add_trigger("replace  (p{0})".format(player))
        trigger.looping = 1
        condition = trigger.add_condition(Condition.OWN_OBJECTS)
        condition.amount_or_quantity = 1
        condition.object_list = trigger_unit
        condition.source_player = player
        effect = trigger.add_effect(Effect.REMOVE_OBJECT)
        effect.source_player = player
        effect.object_list_unit_id = trigger_unit
        effect = trigger.add_effect(Effect.DISPLAY_INSTRUCTIONS)
        effect.object_list_unit_id = Unit.CHAMPION
        effect.source_player = player
        effect.display_time = 10
        effect.instruction_panel_position = PanelLocation.TOP
        effect.message = "<{1}>P{0} has swapped all siege with petards and petards with trebs!".format(player,COLOUR[player - 1])
        for affectedplayer in range(1, NUMBER_OF_PLAYERS + 1):
            if affectedplayer != player:
                for building in GARRISONABLE + [Building.SIEGE_WORKSHOP]:
                    effect = trigger.add_effect(Effect.UNLOAD)
                    effect.object_list_unit_id = building
                    effect.source_player = affectedplayer
                    effect.location_x = 1
                    effect.location_y = 1
                effect = trigger.add_effect(Effect.REPLACE_OBJECT)
                effect.source_player = affectedplayer
                effect.target_player = affectedplayer
                effect.object_list_unit_id = Unit.PETARD
                effect.object_list_unit_id_2 = Hero.BELISARIUS
                for siege_unit in SIEGE_UNITS:
                    effect = trigger.add_effect(Effect.REPLACE_OBJECT)
                    effect.source_player = affectedplayer
                    effect.target_player = affectedplayer
                    effect.object_list_unit_id = siege_unit
                    effect.object_list_unit_id_2 = Unit.PETARD
                effect = trigger.add_effect(Effect.REPLACE_OBJECT)
                effect.source_player = affectedplayer
                effect.target_player = affectedplayer
                effect.object_list_unit_id_2 = Unit.TREBUCHET_PACKED
                effect.object_list_unit_id = Hero.BELISARIUS
def stop_enemy_villagers(trigger_unit):
    for player in range(1, NUMBER_OF_PLAYERS + 1):
        trigger = trigger_manager.add_trigger("stop vils (p{0})".format(player))
        trigger.looping = 1
        condition = trigger.add_condition(Condition.OWN_OBJECTS)
        condition.amount_or_quantity = 1
        condition.object_list = trigger_unit
        condition.source_player = player
        effect = trigger.add_effect(Effect.REMOVE_OBJECT)
        effect.source_player = player
        effect.object_list_unit_id = trigger_unit
        effect = trigger.add_effect(Effect.DISPLAY_INSTRUCTIONS)
        effect.object_list_unit_id = Unit.VILLAGER_MALE
        effect.source_player = player
        effect.display_time = 10
        effect.instruction_panel_position = PanelLocation.TOP
        effect.message = "<{1}>P{0} has petrified all enemy villagers!".format(player,COLOUR[player - 1])
        for affectedplayer in range(1, NUMBER_OF_PLAYERS + 1):
            if affectedplayer != player:
                for villager in VILLAGER:
                    effect = trigger.add_effect(Effect.STOP_OBJECT)
                    effect.object_list_unit_id = villager
                    effect.source_player = affectedplayer
def labour_strike(trigger_unit):
    trigger_id_list = []
    active_id_list = []
    for player in range(1, NUMBER_OF_PLAYERS+1):
        trigger = trigger_manager.add_trigger(f"cd p({player})")
        trigger.short_description = f"P{player}'s Strike ends in <Variable {STRIKE_CD_VAR[player-1]}>s"
        trigger.description = f"P{player}'s Strike ends in <Variable {STRIKE_CD_VAR[player-1]}>s"
        trigger.display_as_objective = 1
        trigger.display_on_screen = 1
        trigger.looping = 1
        condition = trigger.add_condition(Condition.VARIABLE_VALUE)
        condition.amount_or_quantity = 0
        condition.variable = STRIKE_CD_VAR[player-1]
        condition.comparison = Comparison.LARGER
        condition = trigger.add_condition(Condition.TIMER)
        condition.timer = 1
        effect = trigger.add_effect(Effect.CHANGE_VARIABLE)
        effect.from_variable = STRIKE_CD_VAR[player-1]
        effect.operation = Operation.SUBTRACT
        effect.quantity = 1

        trigger = trigger_manager.add_trigger(f"stop vils p({player})")
        trigger.looping = 1
        condition = trigger.add_condition(Condition.VARIABLE_VALUE)
        condition.amount_or_quantity = 0
        condition.variable = STRIKE_CD_VAR[player-1]
        condition.comparison = Comparison.LARGER
        for villager in VILLAGER:
            effect = trigger.add_effect(Effect.STOP_OBJECT)
            effect.source_player = player
            effect.object_list_unit_id = villager
            effect = trigger.add_effect(Effect.DISABLE_OBJECT_SELECTION)
            effect.object_list_unit_id = villager
            effect.source_player = player

        trigger = trigger_manager.add_trigger(f"Make Villagers selectable p({player})")
        trigger.enabled = 0
        condition = trigger.add_condition(Condition.VARIABLE_VALUE)
        condition.amount_or_quantity = 0
        condition.variable = STRIKE_CD_VAR[player - 1]
        condition.comparison = Comparison.EQUAL
        for vil in VILLAGER:
            effect = trigger.add_effect(Effect.ENABLE_OBJECT_SELECTION)
            effect.object_list_unit_id = vil
            effect.source_player = player
        active_id_list.append(trigger.trigger_id)

    for player in range(1, NUMBER_OF_PLAYERS + 1):
        trigger = trigger_manager.add_trigger("strike (p{0})".format(player))
        trigger.looping = 1
        condition = trigger.add_condition(Condition.OWN_OBJECTS)
        condition.amount_or_quantity = 1
        condition.object_list = trigger_unit
        condition.source_player = player
        effect = trigger.add_effect(Effect.REMOVE_OBJECT)
        effect.source_player = player
        effect.object_list_unit_id = trigger_unit
        effect = trigger.add_effect(Effect.DISPLAY_INSTRUCTIONS)
        effect.object_list_unit_id = Unit.VILLAGER_MALE
        effect.source_player = player
        effect.display_time = 10
        effect.instruction_panel_position = PanelLocation.TOP
        effect.message = "<{1}>P{0} has caused a labour strike among the enemy villages!".format(player,COLOUR[player - 1])
        for affectedplayer in range(1, NUMBER_OF_PLAYERS + 1):
            if affectedplayer != player:
                effect = trigger.add_effect(Effect.CHANGE_VARIABLE)
                effect.from_variable = STRIKE_CD_VAR[affectedplayer - 1]
                effect.operation = Operation.ADD
                effect.quantity = STRIKE_DURATION
                effect = trigger.add_effect(Effect.ACTIVATE_TRIGGER)
                effect.trigger_id = active_id_list[affectedplayer-1]
def pages_setu(trigger_unit, pages):
    for player in range(1, NUMBER_OF_PLAYERS + 1):
        trigger_ids = []
        for i in range(0, len(pages)):
            trigger2 = trigger_manager.add_trigger(f"page {i+1} p({player})")
            trigger2.looping = 1
            condition = trigger2.add_condition(Condition.OWN_OBJECTS)
            condition.amount_or_quantity = 1
            condition.object_list = trigger_unit
            condition.source_player = player
            effect = trigger2.add_effect(Effect.REMOVE_OBJECT)
            effect.source_player = player
            effect.object_list_unit_id = trigger_unit
            trigger_ids.append(trigger2.trigger_id)
            condition = trigger2.add_condition(Condition.VARIABLE_VALUE)
            condition.amount_or_quantity = i
            condition.variable = PAGE_VAR[player-1]
            condition.comparison = Comparison.EQUAL
            effect = trigger2.add_effect(Effect.CHANGE_VARIABLE)
            effect.quantity = 1
            effect.operation = Operation.ADD
            effect.from_variable = PAGE_VAR[player-1]
            for unit in pages[i]:
                effect = trigger2.add_effect(Effect.ENABLE_DISABLE_OBJECT)
                effect.enabled_or_victory = 0
                effect.source_player = player
                effect.object_list_unit_id = unit
                effect.item_id = unit
            for unit in pages[i+1 if i < len(pages)-1 else 0]:
                effect = trigger2.add_effect(Effect.ENABLE_DISABLE_OBJECT)
                effect.enabled_or_victory = 1
                effect.source_player = player
                effect.object_list_unit_id = unit
                effect.item_id = unit

        trigger2 = trigger_manager.add_trigger(f"reset var p({player})")
        condition = trigger2.add_condition(Condition.VARIABLE_VALUE)
        condition.amount_or_quantity = len(pages)
        condition.variable = PAGE_VAR[player - 1]
        condition.comparison = Comparison.LARGER_OR_EQUAL
        effect = trigger2.add_effect(Effect.CHANGE_VARIABLE)
        effect.quantity = 0
        effect.operation = Operation.SET
        effect.from_variable = PAGE_VAR[player - 1]

add_credits_header("1.2.1", trigger_manager)

setup()

PAGE_ONE = []

perk_setup(name="Kill All Villagers",
            cost=KILL_ALL_VILLAGERS_COST,
            trigger_unit=Hero.ORNLU_THE_WOLF,
            icon_unit=UnitIcon.VILLAGER_MALE,
            train_button=ButtonLocation.LOCATION_0_0,
            description="Black Death I (<Cost>)\nKill ALL villagers",
            enabled=True)
kill_all_villagers(trigger_unit=Hero.ORNLU_THE_WOLF)
PAGE_ONE.append(Hero.ORNLU_THE_WOLF)

perk_setup(name="Kill All Military",
            cost=KILL_ALL_MILITARY_COST,
            trigger_unit=Hero.ABRAHA_ELEPHANT,
            icon_unit=UnitIcon.CHAMPION,
            train_button=ButtonLocation.LOCATION_1_0,
            description="Black Death II (<Cost>)\nKill all enemy military",
            enabled=True)
kill_all_military(trigger_unit=Hero.ABRAHA_ELEPHANT)
PAGE_ONE.append(Hero.ABRAHA_ELEPHANT)

perk_setup(name="Cease Fire",
            cost=CEASE_FIRE_COST,
            trigger_unit=Hero.FRIAR_TUCK,
            icon_unit=UnitIcon.MONK,
            train_button=ButtonLocation.LOCATION_2_0,
            description="Cease Fire (<Cost>)\nCease Fire for 60s (cd:300s)",
            enabled=True)
cease_fire(trigger_unit=Hero.FRIAR_TUCK)
PAGE_ONE.append(Hero.FRIAR_TUCK)

perk_setup(name="Exploding Villagers",
            cost=EV_COST,
            trigger_unit=Hero.EMPEROR_IN_A_BARREL,
            icon_unit=UnitIcon.PETARD,
            train_button=ButtonLocation.LOCATION_3_0,
            description="Kamikaze (<Cost>)\nTransform all villagers into Exploding Villagers for 60s",
            enabled=True)
exploding_villagers(trigger_unit=Hero.EMPEROR_IN_A_BARREL)
PAGE_ONE.append(Hero.EMPEROR_IN_A_BARREL)

perk_setup(name="Kill All Castles",
            cost=KILL_ALL_CASTLES_COST,
            trigger_unit=Hero.BAD_NEIGHBOR,
            icon_unit=HeroIcon.BAD_NEIGHBOR,
            train_button=ButtonLocation.LOCATION_0_1,
            description="Earthquake (<Cost>)\nDestroy all enemy castles",
            enabled=True)
kill_all_castles(trigger_unit=Hero.BAD_NEIGHBOR)
PAGE_ONE.append(Hero.BAD_NEIGHBOR)

perk_setup(name="Replace Mil with Wolf",
            cost=REPLACE_MILITARY_WOLF_COST,
            trigger_unit=Hero.BUI_BI,
            icon_unit=GaiaUnitIcon.WOLF,
            train_button=ButtonLocation.LOCATION_1_1,
            description="Full Moon (<Cost>)\nConvert all enemy military to wolves",
            enabled=True)
replace_all_military_with_wolves(trigger_unit=Hero.BUI_BI)
PAGE_ONE.append(Hero.BUI_BI)

perk_setup(name="Cycle Archer Line",
            cost=CYCLE_ARCHER_COST,
            trigger_unit=Hero.ARCHER_OF_THE_EYES,
            icon_unit=UnitIcon.ARCHER,
            train_button=ButtonLocation.LOCATION_2_1,
            description="Ol' Betsy (<Cost>)\nConverts all enemy Arbalesters to Crossbowmen, Crossbowmen to Archers and Archers to Arbalesters",
            enabled=True)
cycle_archer_line(trigger_unit=Hero.ARCHER_OF_THE_EYES)
PAGE_ONE.append(Hero.ARCHER_OF_THE_EYES)

perk_setup(name="Replace MAA with Spearmen",
            cost=REPLACE_MAA_SPEAR_COST,
            trigger_unit=Hero.FRANKISH_PALADIN,
            icon_unit=UnitIcon.SPEARMAN,
            train_button=ButtonLocation.LOCATION_3_1,
            description="Pointi Bois (<Cost>)\nConvert all enemy Militia Line units to the corresponding age's Spearman line unit",
            enabled=True)
replace_maa_line(trigger_unit=Hero.FRANKISH_PALADIN)
PAGE_ONE.append(Hero.FRANKISH_PALADIN)

perk_setup(name="Replace Archers with Skirmishers",
            cost=REPLACE_ARCHER_SKIRM_COST,
            trigger_unit=Hero.AETHELFRITH,
            icon_unit=UnitIcon.SKIRMISHER,
            train_button=ButtonLocation.LOCATION_4_1,
            description="Javlin Bois (<Cost>)\nConvert all Archer line units to the corresponding age's Skirm line unit",
            enabled=True)
replace_archer_line(trigger_unit=Hero.AETHELFRITH)
PAGE_ONE.append(Hero.AETHELFRITH)

perk_setup(name="Replace Siege with Petards with Trebs",
            cost=REPLACE_SIEGE_PETARD_TREB_COST,
            trigger_unit=Hero.BAD_NEIGHBOR_PACKED,
            icon_unit=UnitIcon.SIEGE_TOWER,
            train_button=ButtonLocation.LOCATION_0_2,
            description="Siege Swap (<Cost>)\nConvert all enemy siege to Petards and enemy Petards to Trebuchets",
            enabled=True)
replace_siege_petard_treb(trigger_unit=Hero.BAD_NEIGHBOR_PACKED)
PAGE_ONE.append(Hero.BAD_NEIGHBOR_PACKED)

perk_setup(name="Idle Vils",
            cost=STOP_ENEMY_VILLAGERS_COST,
            trigger_unit=Hero.JEAN_BUREAU,
            icon_unit=UnitIcon.VILLAGER_FEMALE,
            train_button=ButtonLocation.LOCATION_1_2,
            description="Petrification (<Cost>)\nStop (idle) all enemy villagers",
            enabled=True)
stop_enemy_villagers(trigger_unit=Hero.JEAN_BUREAU)
PAGE_ONE.append(Hero.JEAN_BUREAU)

perk_setup(name="Labour Strike",
            cost=LABOUR_STRIKE_COST,
            trigger_unit=Hero.CHAND_BARDAI,
            icon_unit=UnitIcon.FLEMISH_MILITIA,
            train_button=ButtonLocation.LOCATION_2_2,
            description="Labour Strike (<Cost>)\nEnemy villagers refuse to work for 30s",
            enabled=True)
labour_strike(trigger_unit=Hero.CHAND_BARDAI)
PAGE_ONE.append(Hero.CHAND_BARDAI)

PAGE_TWO = []

perk_setup(name="Next Page",
            cost=[0, 0, 0, 0],
            trigger_unit=Unit.MOVEABLE_MAP_REVEALER,
            icon_unit=UnitIcon.MOVEABLE_MAP_REVEALER,
            train_button=ButtonLocation.LOCATION_3_2,
            description="Next Page\nFlip to the next page of perks",
            enabled=False)
pages_setu(trigger_unit=Unit.MOVEABLE_MAP_REVEALER, pages=(PAGE_ONE, PAGE_TWO))
scenario.write_to_file(output_path+outname)