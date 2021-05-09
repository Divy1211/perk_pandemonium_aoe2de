from parser_projects.parser_imports import *
from parser_projects.help_functions import *

for NUMBER_OF_PLAYERS in range(1, 9):
    inname = f"Perk Pandemonium {NUMBER_OF_PLAYERS}P.aoe2scenario"
    outname = f"Perk Pandemonium {NUMBER_OF_PLAYERS}P.aoe2scenario"
    scenario = AoE2DEScenario.from_file(input_path + inname)
    trigger_manager = scenario.trigger_manager
    trigger_manager.triggers = []

    # define all constants, CD stands for COOLDOWN

    COLOUR = ["BLUE", "RED", "GREEN", "YELLOW", "AQUA", "PURPLE", "GREY", "ORANGE"]

    CEASE_FIRE_DURATION = 60
    CEASE_FIRE_CD = 300
    EV_DURATION = 60
    STRIKE_DURATION = 30
    TRADE_WORKSHOP_TRAIN_TIME = 60

    # variable ids
    CEASE_FIRE_CD_VAR = 0
    CEASE_FIRE_PLAYER_CD_VAR = [i for i in range(1, NUMBER_OF_PLAYERS + 1)]
    EV_CD_VAR = 9
    STRIKE_CD_VAR = [9 + i for i in range(1, NUMBER_OF_PLAYERS + 1)]
    DOPE_CD_VAR = [17 + i for i in range(1, NUMBER_OF_PLAYERS+1)]
    DOPE_PLAYER_CD_VAR = [25 + i for i in range(1, NUMBER_OF_PLAYERS+1)]
    PAGE_VAR = [247 + i for i in range(1, NUMBER_OF_PLAYERS + 1)]

    KILL_ALL_VILLAGERS_COST = [1000*(NUMBER_OF_PLAYERS-1), 0, 0, 0]
    KILL_ALL_MILITARY_COST = [0, 0, 500*(NUMBER_OF_PLAYERS-1), 0]
    CEASE_FIRE_COST = [0, 200, 200, 0]
    EV_COST = [0, 0, 1000, 0]
    KILL_ALL_CASTLES_COST = [0, 5000, 0, 200*(NUMBER_OF_PLAYERS-1)]
    REPLACE_MILITARY_WOLF_COST = [0, 0, 250*(NUMBER_OF_PLAYERS-1), 0]
    CYCLE_ARCHER_COST = [0, 0, 125*(NUMBER_OF_PLAYERS-1), 0]
    REPLACE_MAA_SPEAR_COST = [0, 1000, 100*(NUMBER_OF_PLAYERS-1), 0]
    REPLACE_ARCHER_SKIRM_COST = [0, 800, 100*(NUMBER_OF_PLAYERS-1), 0]
    REPLACE_KT_LC = [0, 1500, 100*(NUMBER_OF_PLAYERS-1), 0]
    REPLACE_CAM_LC = [0, 1200, 100*(NUMBER_OF_PLAYERS-1), 0]
    REPLACE_ELE_LC = [0, 2000, 150*(NUMBER_OF_PLAYERS-1), 0]
    REPLACE_SL_LC = [0, 1300, 100*(NUMBER_OF_PLAYERS-1), 0]
    REPLACE_SIEGE_PETARD_TREB_COST = [0, 1000, 100*(NUMBER_OF_PLAYERS-1), 0]
    STOP_ENEMY_VILLAGERS_COST = [500, 0, 75*(NUMBER_OF_PLAYERS-1), 0]
    LABOUR_STRIKE_COST = [1000, 0, 0, 100*(NUMBER_OF_PLAYERS-1)]
    DOPE_COST = [0, 1000, 200, 200]
    TRADE_WORKSHOP_COST = [0, 200, 0, 50]

    PAGES = [[]]
    CURRENT_PAGE = 0
    TRIGGER_UNITS = sorted([(hero.ID, hero.ICON_ID, hero.DEAD_ID, False) for hero in HeroInfo], key=lambda x : HeroInfo(x).name)
    TRIGGER_UNITS = [hero[0] for hero in TRIGGER_UNITS]
    CURRENT_TRIGGER_UNIT = 0
    BUTTON_LOCATIONS = [1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13]
    HOTKEY_ID_MAP = {
        1: 16344,
        2: 16157,
        3: 16487,
        4: 16464,
        5: 16144,
        6: 16149,
        7: 16131,
        8: 16161,
        9: 16138,
        10: 16176,
        11: 16164,
        12: 16182,
        13: 16159,
        14: 19054
    }
    CURRENT_BUTTON_LOCATION = 0
    CD_HEROES = []
    CD_VARS = []

    # misc
    GARRISONABLE_BY_ALL = [BuildingInfo.TOWN_CENTER.ID, BuildingInfo.WATCH_TOWER.ID, BuildingInfo.GUARD_TOWER.ID,
                                 BuildingInfo.KEEP.ID, BuildingInfo.BOMBARD_TOWER.ID, BuildingInfo.HOUSE.ID,
                                 BuildingInfo.DONJON.ID, BuildingInfo.KREPOST.ID, BuildingInfo.CASTLE.ID, UnitInfo.BATTERING_RAM.ID,
                                 UnitInfo.CAPPED_RAM.ID, UnitInfo.SIEGE_RAM.ID, UnitInfo.SIEGE_TOWER.ID, UnitInfo.TRANSPORT_SHIP.ID]

    GARRISONABLE_BY_MILITARY = [BuildingInfo.ARCHERY_RANGE.ID, BuildingInfo.BARRACKS.ID, BuildingInfo.STABLE.ID,
                             BuildingInfo.SIEGE_WORKSHOP.ID, BuildingInfo.DOCK.ID, BuildingInfo.MONASTERY.ID]

    SIEGE_UNITS = [UnitInfo.MANGONEL.ID, UnitInfo.ONAGER.ID, UnitInfo.SIEGE_ONAGER.ID, UnitInfo.SIEGE_TOWER.ID,
                   UnitInfo.BATTERING_RAM.ID, UnitInfo.CAPPED_RAM.ID, UnitInfo.SIEGE_RAM.ID, UnitInfo.SCORPION.ID,
                   UnitInfo.HEAVY_SCORPION.ID, UnitInfo.BOMBARD_CANNON.ID, UnitInfo.TREBUCHET.ID,
                   UnitInfo.TREBUCHET_PACKED.ID, UnitInfo.ORGAN_GUN.ID, UnitInfo.ELITE_ORGAN_GUN.ID]

    def prepare_unit(prefix: str,
                    trigger_unit: int,
                    train_location: int,
                    train_button: int,
                    train_time: int,
                    cost: list,
                    description: str,
                    hotkey_id: int = -1):

        hotkey_id = HOTKEY_ID_MAP[train_button] if hotkey_id == -1 else hotkey_id

        trigger = trigger_manager.add_trigger(f"{prefix}Change Hotkey")
        for player in range(1, NUMBER_OF_PLAYERS+1):
            trigger.new_effect.modify_attribute(
                                  quantity=hotkey_id,
                                  object_list_unit_id=trigger_unit,
                                  source_player=player,
                                  item_id=trigger_unit,
                                  operation=Operation.SET,
                                  object_attributes=58
                               )

        trigger = trigger_manager.add_trigger(f"{prefix}Change Train Location")
        for player in range(1, NUMBER_OF_PLAYERS+1):
            trigger.new_effect.change_train_location(
                                  object_list_unit_id=trigger_unit,
                                  source_player=player,
                                  object_list_unit_id_2=train_location,
                                  button_location=train_button
                               )


        trigger = trigger_manager.add_trigger(f"{prefix}Change Cost Pre")
        for player in range(1, NUMBER_OF_PLAYERS+1):
            trigger.new_effect.modify_attribute(
                                  quantity=0,
                                  object_list_unit_id=trigger_unit,
                                  source_player=player,
                                  item_id=trigger_unit,
                                  operation=Operation.SET,
                                  object_attributes=ObjectAttribute.GOLD_COSTS
                               )
            trigger.new_effect.modify_attribute(
                                  quantity=0,
                                  object_list_unit_id=trigger_unit,
                                  source_player=player,
                                  item_id=trigger_unit,
                                  operation=Operation.SET,
                                  object_attributes=ObjectAttribute.WOOD_COSTS
                               )
            trigger.new_effect.modify_attribute(
                                  quantity=0,
                                  object_list_unit_id=trigger_unit,
                                  source_player=player,
                                  item_id=trigger_unit,
                                  operation=Operation.SET,
                                  object_attributes=ObjectAttribute.FOOD_COSTS
                               )
            trigger.new_effect.modify_attribute(
                                  quantity=0,
                                  object_list_unit_id=trigger_unit,
                                  source_player=player,
                                  item_id=trigger_unit,
                                  operation=Operation.SET,
                                  object_attributes=ObjectAttribute.STONE_COSTS
                               )


        trigger = trigger_manager.add_trigger(f"{prefix}Change Cost")
        for player in range(1, NUMBER_OF_PLAYERS+1):
            trigger.new_effect.change_object_cost(
                                  object_list_unit_id=trigger_unit,
                                  source_player=player,
                                  food=cost[0],
                                  wood=cost[1],
                                  stone=cost[3],
                                  gold=cost[2]
                               )

        trigger = trigger_manager.add_trigger(f"{prefix}Change Train Time")
        for player in range(1, NUMBER_OF_PLAYERS+1):
            trigger.new_effect.modify_attribute(
                                  quantity=train_time,
                                  object_list_unit_id=trigger_unit,
                                  source_player=player,
                                  item_id=trigger_unit,
                                  operation=Operation.SET,
                                  object_attributes=ObjectAttribute.TRAIN_TIME
                               )

        trigger = trigger_manager.add_trigger(f"{prefix}Change Description")
        for player in range(1, NUMBER_OF_PLAYERS+1):
            trigger.new_effect.change_object_description(
                                  object_list_unit_id=trigger_unit,
                                  source_player=player,
                                  message=description
                               )

    def setup():
        trigger = trigger_manager.add_trigger("==== Setup ====")
        correct_scout(NUMBER_OF_PLAYERS, trigger_manager)

        scenario.sections['Options'].disabled_tech_ids_player_1 = [TechInfo.FREE_CARTOGRAPHY.ID]
        scenario.sections['Options'].disabled_tech_ids_player_2 = [TechInfo.FREE_CARTOGRAPHY.ID]
        scenario.sections['Options'].disabled_tech_ids_player_3 = [TechInfo.FREE_CARTOGRAPHY.ID]
        scenario.sections['Options'].disabled_tech_ids_player_4 = [TechInfo.FREE_CARTOGRAPHY.ID]
        scenario.sections['Options'].disabled_tech_ids_player_5 = [TechInfo.FREE_CARTOGRAPHY.ID]
        scenario.sections['Options'].disabled_tech_ids_player_6 = [TechInfo.FREE_CARTOGRAPHY.ID]
        scenario.sections['Options'].disabled_tech_ids_player_7 = [TechInfo.FREE_CARTOGRAPHY.ID]
        scenario.sections['Options'].disabled_tech_ids_player_8 = [TechInfo.FREE_CARTOGRAPHY.ID]
        scenario.sections['Options'].per_player_number_of_disabled_techs = [1]*8+[0]*8

        trigger = trigger_manager.add_trigger("Disable Cartography")
        for player in range(1, NUMBER_OF_PLAYERS+1):
            trigger.new_effect.enable_disable_technology(
                                  source_player=player,
                                  technology=TechInfo.CARTOGRAPHY.ID,
                                  enabled=0,
                                  item_id=TechInfo.CARTOGRAPHY.ID
                               )

        trigger = trigger_manager.add_trigger("Disable Wonder")
        for player in range(1, NUMBER_OF_PLAYERS+1):
            trigger.new_effect.enable_disable_object(
                                  object_list_unit_id=BuildingInfo.WONDER.ID,
                                  source_player=player,
                                  enabled=False,
                                  item_id=BuildingInfo.WONDER.ID
                               )

        trigger = trigger_manager.add_trigger("TW Enable Trade Workshop")
        for player in range(1, NUMBER_OF_PLAYERS+1):
            trigger.new_effect.enable_disable_object(
                                  object_list_unit_id=BuildingInfo.TRADE_WORKSHOP.ID,
                                  source_player=player,
                                  enabled=True,
                                  item_id=BuildingInfo.TRADE_WORKSHOP.ID
                               )
        description = "Build Trade Workshop (<Cost>)\nAllows you to buy "+\
                      "special perks\n<hp> <attack> <armor> <piercearmor> <garrison> LoS: 4"

        prepare_unit("TW ", BuildingInfo.TRADE_WORKSHOP.ID,
                    UnitInfo.VILLAGER_MALE.ID,
                    ButtonLocation.r3c2,
                    TRADE_WORKSHOP_TRAIN_TIME,
                    TRADE_WORKSHOP_COST,
                    description)

        add_civ_bonuses(NUMBER_OF_PLAYERS, trigger_manager)
        handle_chinese(NUMBER_OF_PLAYERS, trigger_manager)

    def perk_setup(name: str,
                   trigger_unit: int,
                   train_location: int,
                   train_button: int,
                   cost: list,
                   description: str,
                   enabled: int,
                   icon_unit: int):

        trigger = trigger_manager.add_trigger(f"==== {name} ====")
        if enabled:
            trigger = trigger_manager.add_trigger("Enable")
            for player in range(1, NUMBER_OF_PLAYERS+1):
                trigger.new_effect.enable_disable_object(
                                      object_list_unit_id=trigger_unit,
                                      source_player=player,
                                      enabled=True,
                                      item_id=trigger_unit
                                   )

        prepare_unit("", trigger_unit, train_location, train_button, 0, cost, description)

        trigger = trigger_manager.add_trigger("Change Icon")
        for player in range(1, NUMBER_OF_PLAYERS + 1):
            trigger.new_effect.modify_attribute(
                                  quantity=icon_unit,
                                  object_list_unit_id=trigger_unit,
                                  source_player=player,
                                  item_id=trigger_unit,
                                  operation=Operation.SET,
                                  object_attributes=ObjectAttribute.ICON_ID
                               )

        trigger = trigger_manager.add_trigger("Change Pop Requirement")
        for player in range(1, NUMBER_OF_PLAYERS + 1):
            trigger.new_effect.modify_attribute(
                                  quantity=0,
                                  object_list_unit_id=trigger_unit,
                                  source_player=player,
                                  item_id=trigger_unit,
                                  operation=Operation.SET,
                                  object_attributes=ObjectAttribute.AMOUNT_OF_1ST_RESOURCES
                               )

    def page_setup(trigger_unit: int,
                   pages: list):

        for player in range(1, NUMBER_OF_PLAYERS+1):
            trigger = trigger_manager.add_trigger(f"Set Page Vars p({player})")
            for var in PAGE_VAR:
                trigger.new_effect.change_variable(
                                      quantity=1,
                                      operation=Operation.SET,
                                      variable=var
                                   )

        for page in pages:
            page_no = pages.index(page)+1
            trigger = trigger_manager.add_trigger(f"---- Page {page_no} ----")
            activation_trigger = []
            for player in range(1, NUMBER_OF_PLAYERS + 1):
                trigger = trigger_manager.add_trigger(f"Is On Page {page_no} p({player})")
                trigger.looping = True
                activation_trigger.append(trigger)

                trigger.new_condition.own_objects(
                                      quantity=1,
                                      object_list=trigger_unit,
                                      source_player=player
                                   )
                trigger.new_condition.variable_value(
                                      quantity=page_no,
                                      variable=PAGE_VAR[player-1],
                                      comparison=Comparison.EQUAL
                                   )
                trigger.new_effect.remove_object(
                                      object_list_unit_id=trigger_unit,
                                      source_player=player
                                   )

                if page_no == len(pages):
                    trigger.new_effect.change_variable(
                        quantity=1,
                        operation=Operation.SET,
                        variable=PAGE_VAR[player - 1]
                    )

                else:
                    trigger.new_effect.change_variable(
                        quantity=1,
                        operation=Operation.ADD,
                        variable=PAGE_VAR[player-1]
                    )

            for player in range(1, NUMBER_OF_PLAYERS + 1):
                trigger = trigger_manager.add_trigger(f"Disable Units Page {page_no} p({player})")
                trigger.enabled = False
                for unit in page:
                    trigger.new_effect.enable_disable_object(
                                          object_list_unit_id=unit,
                                          source_player=player,
                                          enabled=False,
                                          item_id=unit
                                       )
                activation_trigger[player-1].new_effect.activate_trigger(
                                      trigger_id=trigger.trigger_id
                                   )

            next_page = pages[page_no] if page_no < len(pages) else pages[0]

            triggers = []
            for player in range(1, NUMBER_OF_PLAYERS+1):
                triggers.append(trigger_manager.add_trigger(f"Enable Units Page {pages.index(next_page)+1} p({player})"))

            for player in range(1, NUMBER_OF_PLAYERS + 1):
                trigger = triggers[player-1]
                trigger.enabled = False
                for unit in next_page:
                    if unit not in CD_HEROES:
                        trigger.new_effect.enable_disable_object(
                            object_list_unit_id=unit,
                            source_player=player,
                            enabled=True,
                            item_id=unit
                        )
                    else:
                        trigger2 = trigger_manager.add_trigger(f"Enable Unit {f'{unit:>4.0f}'.replace(' ', '0')} p({player})")
                        trigger2.enabled = False
                        trigger2.new_condition.variable_value(
                            quantity=0,
                            variable=CD_VARS[CD_HEROES.index(unit)][player - 1],
                            comparison=Comparison.EQUAL
                        )
                        trigger2.new_effect.enable_disable_object(
                            object_list_unit_id=unit,
                            source_player=player,
                            enabled=True,
                            item_id=unit
                        )
                        trigger.new_effect.activate_trigger(
                                              trigger_id=trigger2.trigger_id
                                           )


                activation_trigger[player-1].new_effect.activate_trigger(
                                      trigger_id=trigger.trigger_id
                                   )

    def update_location_unit():
        global CURRENT_BUTTON_LOCATION, CURRENT_TRIGGER_UNIT, CURRENT_PAGE
        PAGES[CURRENT_PAGE].append(TRIGGER_UNITS[CURRENT_TRIGGER_UNIT])
        CURRENT_BUTTON_LOCATION += 1
        CURRENT_TRIGGER_UNIT += 1
        if CURRENT_BUTTON_LOCATION >= len(BUTTON_LOCATIONS):
            CURRENT_BUTTON_LOCATION = 0
            PAGES.append([])
            CURRENT_PAGE += 1

    def kill_all_villagers(trigger_unit: int,
                           instruction_icon: int,
                           instruction_text: str):
        for player in range(1, NUMBER_OF_PLAYERS+1):
            trigger = trigger_manager.add_trigger(f"Kill All Villagers p({player})")
            trigger.looping = True
            trigger.new_condition.own_objects(
                                  quantity=1,
                                  object_list=trigger_unit,
                                  source_player=player
                               )
            trigger.new_effect.remove_object(
                                  object_list_unit_id=trigger_unit,
                                  source_player=player,
                               )
            trigger.new_effect.display_instructions(
                                  object_list_unit_id=instruction_icon,
                                  source_player=player,
                                  display_time=10,
                                  message=f"<{COLOUR[player-1]}>Player {player} Has "+instruction_text
                               )

            for targer_player in range(1, NUMBER_OF_PLAYERS+1):
                for garrisonable in GARRISONABLE_BY_ALL+[BuildingInfo.MARKET.ID]:
                    trigger.new_effect.unload(
                                          object_list_unit_id=garrisonable,
                                          source_player=targer_player,
                                          location_x=0,
                                          location_y=0
                                       )
                trigger.new_effect.kill_object(
                                      source_player=targer_player,
                                      object_type=3
                                   )
        update_location_unit()

    def kill_all_military(trigger_unit: int,
                          instruction_icon: int,
                          instruction_text: str):
        for player in range(1, NUMBER_OF_PLAYERS+1):
            trigger = trigger_manager.add_trigger(f"Kill All Military p({player})")
            trigger.looping = True
            trigger.new_condition.own_objects(
                                  quantity=1,
                                  object_list=trigger_unit,
                                  source_player=player
                               )
            trigger.new_effect.remove_object(
                                  object_list_unit_id=trigger_unit,
                                  source_player=player,
                               )
            trigger.new_effect.display_instructions(
                                  object_list_unit_id=instruction_icon,
                                  source_player=player,
                                  display_time=10,
                                  message=f"<{COLOUR[player-1]}>Player {player} Has "+instruction_text
                               )
            for targer_player in range(1, NUMBER_OF_PLAYERS+1):
                if player != targer_player:
                    for garrisonable in GARRISONABLE_BY_ALL+GARRISONABLE_BY_MILITARY:
                        trigger.new_effect.unload(
                                              object_list_unit_id=garrisonable,
                                              source_player=targer_player,
                                              location_x=0,
                                              location_y=0
                                           )
                    trigger.new_effect.kill_object(
                                          source_player=targer_player,
                                          object_type=4
                                       )
        update_location_unit()

    def cease_fire(trigger_unit: int,
                   instruction_icon: int,
                   instruction_text: str):
        trigger = trigger_manager.add_trigger("Display Information")
        trigger.short_description = f"Cease Fire Ends In: <Variable {CEASE_FIRE_CD_VAR}>"
        trigger.display_on_screen = True
        trigger.new_condition.player_defeated(
                              source_player=PlayerId.GAIA
                           )

        trigger = trigger_manager.add_trigger(f"Cease Fire cd")
        trigger.looping = True
        trigger.new_condition.variable_value(
            quantity=0,
            variable=CEASE_FIRE_CD_VAR,
            comparison=Comparison.LARGER
        )
        trigger.new_effect.change_variable(
            quantity=1,
            operation=Operation.SUBTRACT,
            variable=CEASE_FIRE_CD_VAR
        )

        trigger = trigger_manager.add_trigger(f"End Cease Fire")
        trigger.enabled = False
        trigger.new_condition.variable_value(
            quantity=0,
            variable=CEASE_FIRE_CD_VAR,
            comparison=Comparison.EQUAL
        )
        trigger.new_effect.display_instructions(
            object_list_unit_id=instruction_icon,
            source_player=PlayerId.GAIA,
            display_time=10,
            message=f"Cease Fire Has Ended!"
        )
        for source_player in range(1, NUMBER_OF_PLAYERS + 1):
            for target_player in range(1, NUMBER_OF_PLAYERS + 1):
                if source_player != target_player:
                    trigger.new_effect.change_diplomacy(
                        diplomacy=DiplomacyState.ENEMY,
                        source_player=source_player,
                        target_player=target_player
                    )
        activation_id = trigger.trigger_id

        reactivate_effect_trigger_ids = []
        for player in range(1, NUMBER_OF_PLAYERS+1):
            trigger = trigger_manager.add_trigger(f"Re-Enable p({player})")
            trigger.enabled = False
            trigger.new_condition.variable_value(
                                  quantity=0,
                                  variable=CEASE_FIRE_PLAYER_CD_VAR[player-1],
                                  comparison=Comparison.EQUAL
                               )
            trigger.new_effect.enable_disable_object(
                                  object_list_unit_id=trigger_unit,
                                  source_player=player,
                                  enabled=True,
                                  item_id=trigger_unit
                               )
            trigger.new_effect.activate_trigger(
                                  trigger_id=trigger.trigger_id+2*NUMBER_OF_PLAYERS
                               )
            reactivate_effect_trigger_ids.append(trigger.trigger_id)

        for player in range(1, NUMBER_OF_PLAYERS+1):
            trigger = trigger_manager.add_trigger(f"Player cd p({player})")
            trigger.looping = True
            trigger.new_condition.variable_value(
                                  quantity=0,
                                  variable=CEASE_FIRE_PLAYER_CD_VAR[player-1],
                                  comparison=Comparison.LARGER
                               )
            trigger.new_effect.change_variable(
                                  quantity=1,
                                  operation=Operation.SUBTRACT,
                                  variable=CEASE_FIRE_PLAYER_CD_VAR[player-1]
                               )

        for player in range(1, NUMBER_OF_PLAYERS+1):
            trigger = trigger_manager.add_trigger(f"Cease Fire p({player})")
            trigger.looping = True
            trigger.new_condition.own_objects(
                                  quantity=1,
                                  object_list=trigger_unit,
                                  source_player=player
                               )
            trigger.new_effect.remove_object(
                                  object_list_unit_id=trigger_unit,
                                  source_player=player,
                               )
            trigger.new_effect.display_instructions(
                                  object_list_unit_id=instruction_icon,
                                  source_player=PlayerId.GAIA,
                                  display_time=10,
                                  message=f"<{COLOUR[player-1]}>Player {player} Has "+instruction_text
                               )
            trigger.new_effect.deactivate_trigger(
                                  trigger_id=trigger.trigger_id
                               )
            trigger.new_effect.activate_trigger(
                                  trigger_id=activation_id
                               )
            trigger.new_effect.activate_trigger(
                                  trigger_id=reactivate_effect_trigger_ids[player-1]
                               )
            trigger.new_effect.change_variable(
                                  quantity=300,
                                  operation=Operation.SET,
                                  variable=CEASE_FIRE_PLAYER_CD_VAR[player-1]
                               )
            trigger.new_effect.enable_disable_object(
                                  object_list_unit_id=trigger_unit,
                                  source_player=player,
                                  enabled=False,
                                  item_id=trigger_unit
                               )
            trigger.new_effect.change_variable(
                                  quantity=60,
                                  operation=Operation.ADD,
                                  variable=CEASE_FIRE_CD_VAR
                               )
            for source_player in range(1, NUMBER_OF_PLAYERS+1):
                for target_player in range(1, NUMBER_OF_PLAYERS+1):
                    if source_player != target_player:
                        trigger.new_effect.change_diplomacy(
                                              diplomacy=DiplomacyState.ALLY,
                                              source_player=source_player,
                                              target_player=target_player

                                           )

        for player in range(1, NUMBER_OF_PLAYERS + 1):
            trigger = trigger_manager.add_trigger(f"Remove Unit p({player})")
            trigger.looping = True
            trigger.new_condition.own_objects(
                quantity=1,
                object_list=trigger_unit,
                source_player=player
            )
            trigger.new_effect.remove_object(
                object_list_unit_id=trigger_unit,
                source_player=player,
            )
        update_location_unit()

    def exploding_villagers(trigger_unit: int,
                            instruction_icon: int,
                            instruction_text: str):
        trigger = trigger_manager.add_trigger("Display Information")
        trigger.short_description = f"Exploding Villagers: <Variable {EV_CD_VAR}>"
        trigger.display_on_screen = True
        trigger.new_condition.player_defeated(
                              source_player=PlayerId.GAIA
                           )

        trigger = trigger_manager.add_trigger(f"Exploding Villagers Cooldown")
        trigger.looping = True
        trigger.new_condition.variable_value(
            quantity=0,
            variable=EV_CD_VAR,
            comparison=Comparison.LARGER
        )
        trigger.new_effect.change_variable(
            quantity=1,
            operation=Operation.SUBTRACT,
            variable=EV_CD_VAR
        )

        trigger = trigger_manager.add_trigger(f"End Exploding Villagers")
        trigger.enabled = False
        trigger.new_condition.variable_value(
            quantity=0,
            variable=EV_CD_VAR,
            comparison=Comparison.EQUAL
        )
        trigger.new_effect.display_instructions(
            object_list_unit_id=instruction_icon,
            source_player=PlayerId.GAIA,
            display_time=10,
            message=f"Exploding Villagers Has Ended!"
        )

        for player in range(1, NUMBER_OF_PLAYERS+1):
            for villager in [villager for villager in UnitInfo if "VILLAGER" in villager.name]:
                trigger.new_effect.modify_attribute(
                                      quantity=villager.DEAD_ID,
                                      object_list_unit_id=villager.ID,
                                      source_player=player,
                                      item_id=villager.ID,
                                      operation=Operation.SET,
                                      object_attributes=ObjectAttribute.DEAD_UNIT_ID
                                   )

        activation_id = trigger.trigger_id

        trigger = trigger_manager.add_trigger("Set Saboteur Attributes")
        for player in range(1, NUMBER_OF_PLAYERS+1):
            trigger.new_effect.modify_attribute(
                                  quantity=-2,
                                  object_list_unit_id=HeroInfo.SABOTEUR.ID,
                                  source_player=player,
                                  item_id=HeroInfo.SABOTEUR.ID,
                                  operation=Operation.SET,
                                  object_attributes=ObjectAttribute.HIT_POINTS
                               )
            trigger.new_effect.modify_attribute(
                                  quantity=1,
                                  object_list_unit_id=HeroInfo.SABOTEUR.ID,
                                  source_player=player,
                                  item_id=HeroInfo.SABOTEUR.ID,
                                  operation=Operation.SET,
                                  object_attributes=ObjectAttribute.BLAST_LEVEL
                               )
            trigger.new_effect.modify_attribute(
                                  quantity=2,
                                  object_list_unit_id=HeroInfo.SABOTEUR.ID,
                                  source_player=player,
                                  item_id=HeroInfo.SABOTEUR.ID,
                                  operation=Operation.SET,
                                  object_attributes=ObjectAttribute.MAX_RANGE
                               )

        for player in range(1, NUMBER_OF_PLAYERS+1):
            trigger = trigger_manager.add_trigger(f"Exploding Villagers p({player})")
            trigger.looping = True
            trigger.new_condition.own_objects(
                                  quantity=1,
                                  object_list=trigger_unit,
                                  source_player=player
                               )
            trigger.new_effect.remove_object(
                                  object_list_unit_id=trigger_unit,
                                  source_player=player,
                               )
            trigger.new_effect.display_instructions(
                                  object_list_unit_id=instruction_icon,
                                  source_player=player,
                                  display_time=10,
                                  message=f"<{COLOUR[player-1]}>Player {player} Has "+instruction_text
                               )
            trigger.new_effect.activate_trigger(
                                  trigger_id=activation_id
                               )
            trigger.new_effect.change_variable(
                                  quantity=60,
                                  operation=Operation.ADD,
                                  variable=EV_CD_VAR
                               )

            for player in range(1, NUMBER_OF_PLAYERS + 1):
                for villager in [villager for villager in UnitInfo if "VILLAGER" in villager.name]:
                    trigger.new_effect.modify_attribute(
                        quantity=HeroInfo.SABOTEUR.ID,
                        object_list_unit_id=villager.ID,
                        source_player=player,
                        item_id=villager.ID,
                        operation=Operation.SET,
                        object_attributes=ObjectAttribute.DEAD_UNIT_ID
                    )
        update_location_unit()

    def kill_all_castles(trigger_unit: int,
                          instruction_icon: int,
                          instruction_text: str):
        for player in range(1, NUMBER_OF_PLAYERS+1):
            trigger = trigger_manager.add_trigger(f"Kill All Castles p({player})")
            trigger.looping = True
            trigger.new_condition.own_objects(
                                  quantity=1,
                                  object_list=trigger_unit,
                                  source_player=player
                               )
            trigger.new_effect.remove_object(
                                  object_list_unit_id=trigger_unit,
                                  source_player=player,
                               )
            trigger.new_effect.display_instructions(
                                  object_list_unit_id=instruction_icon,
                                  source_player=player,
                                  display_time=10,
                                  message=f"<{COLOUR[player-1]}>Player {player} Has "+instruction_text
                               )
            for targer_player in range(1, NUMBER_OF_PLAYERS+1):
                if player != targer_player:
                    trigger.new_effect.kill_object(
                                          object_list_unit_id=BuildingInfo.CASTLE.ID,
                                          source_player=targer_player
                                       )
        update_location_unit()

    def military_to_t90woo(trigger_unit: int,
                          instruction_icon: int,
                          instruction_text: str):

        for player in range(1, NUMBER_OF_PLAYERS+1):
            trigger = trigger_manager.add_trigger(f"t90Woo p({player})")
            trigger.looping = True
            trigger.new_condition.own_objects(
                                  quantity=1,
                                  object_list=trigger_unit,
                                  source_player=player
                               )
            trigger.new_effect.remove_object(
                                  object_list_unit_id=trigger_unit,
                                  source_player=player,
                               )
            trigger.new_effect.display_instructions(
                                  object_list_unit_id=instruction_icon,
                                  source_player=player,
                                  display_time=10,
                                  message=f"<{COLOUR[player-1]}>Player {player} Has "+instruction_text
                               )
            for targer_player in range(1, NUMBER_OF_PLAYERS+1):
                if player != targer_player:
                    for garrisonable in GARRISONABLE_BY_ALL+GARRISONABLE_BY_MILITARY:
                        trigger.new_effect.unload(
                                              object_list_unit_id=garrisonable,
                                              source_player=targer_player,
                                              location_x=0,
                                              location_y=0
                                           )
                    trigger.new_effect.replace_object(
                                          source_player=targer_player,
                                          target_player=targer_player,
                                          object_type=4,
                                          object_list_unit_id_2=HeroInfo.HUNTING_WOLF.ID
                                       )
        update_location_unit()

    def cycle_archer_line(trigger_unit: int,
                          instruction_icon: int,
                          instruction_text: str):

        for player in range(1, NUMBER_OF_PLAYERS+1):
            trigger = trigger_manager.add_trigger(f"Cycle Archer Line p({player})")
            trigger.looping = True
            trigger.new_condition.own_objects(
                                  quantity=1,
                                  object_list=trigger_unit,
                                  source_player=player
                               )
            trigger.new_effect.remove_object(
                                  object_list_unit_id=trigger_unit,
                                  source_player=player,
                               )
            trigger.new_effect.display_instructions(
                                  object_list_unit_id=instruction_icon,
                                  source_player=player,
                                  display_time=10,
                                  message=f"<{COLOUR[player-1]}>Player {player} Has "+instruction_text
                               )
            for targer_player in range(1, NUMBER_OF_PLAYERS+1):
                if player != targer_player:
                    for garrisonable in GARRISONABLE_BY_ALL+GARRISONABLE_BY_MILITARY:
                        trigger.new_effect.unload(
                                              object_list_unit_id=garrisonable,
                                              source_player=targer_player,
                                              location_x=0,
                                              location_y=0
                                           )
                    trigger.new_effect.replace_object(
                                          object_list_unit_id=UnitInfo.ARBALESTER.ID,
                                          source_player=targer_player,
                                          target_player=targer_player,
                                          object_list_unit_id_2=HeroInfo.ZAWISZA_THE_BLACK.ID
                                       )
                    trigger.new_effect.replace_object(
                                          object_list_unit_id=UnitInfo.CROSSBOWMAN.ID,
                                          source_player=targer_player,
                                          target_player=targer_player,
                                          object_list_unit_id_2=HeroInfo.YODIT.ID
                                       )
                    trigger.new_effect.replace_object(
                                          object_list_unit_id=UnitInfo.ARCHER.ID,
                                          source_player=targer_player,
                                          target_player=targer_player,
                                          object_list_unit_id_2=UnitInfo.ARBALESTER.ID
                                       )
                    trigger.new_effect.replace_object(
                                          object_list_unit_id=HeroInfo.YODIT.ID,
                                          source_player=targer_player,
                                          target_player=targer_player,
                                          object_list_unit_id_2=UnitInfo.ARCHER.ID
                                       )
                    trigger.new_effect.replace_object(
                                          object_list_unit_id=HeroInfo.ZAWISZA_THE_BLACK.ID,
                                          source_player=targer_player,
                                          target_player=targer_player,
                                          object_list_unit_id_2=UnitInfo.CROSSBOWMAN.ID
                                       )
        update_location_unit()

    def replace_maa_spear(trigger_unit: int,
                          instruction_icon: int,
                          instruction_text: str):

        for player in range(1, NUMBER_OF_PLAYERS+1):
            trigger = trigger_manager.add_trigger(f"Replace Militia With Spears p({player})")
            trigger.looping = True
            trigger.new_condition.own_objects(
                                  quantity=1,
                                  object_list=trigger_unit,
                                  source_player=player
                               )
            trigger.new_effect.remove_object(
                                  object_list_unit_id=trigger_unit,
                                  source_player=player,
                               )
            trigger.new_effect.display_instructions(
                                  object_list_unit_id=instruction_icon,
                                  source_player=player,
                                  display_time=10,
                                  message=f"<{COLOUR[player-1]}>Player {player} Has "+instruction_text
                               )
            for targer_player in range(1, NUMBER_OF_PLAYERS+1):
                if player != targer_player:
                    for garrisonable in GARRISONABLE_BY_ALL+GARRISONABLE_BY_MILITARY:
                        trigger.new_effect.unload(
                                              object_list_unit_id=garrisonable,
                                              source_player=targer_player,
                                              location_x=0,
                                              location_y=0
                                           )
                    trigger.new_effect.replace_object(
                                          object_list_unit_id=UnitInfo.MILITIA.ID,
                                          source_player=targer_player,
                                          target_player=targer_player,
                                          object_list_unit_id_2=UnitInfo.SPEARMAN.ID
                                       )
                    trigger.new_effect.replace_object(
                                          object_list_unit_id=UnitInfo.MAN_AT_ARMS.ID,
                                          source_player=targer_player,
                                          target_player=targer_player,
                                          object_list_unit_id_2=UnitInfo.SPEARMAN.ID
                                       )
                    trigger.new_effect.replace_object(
                                          object_list_unit_id=UnitInfo.LONG_SWORDSMAN.ID,
                                          source_player=targer_player,
                                          target_player=targer_player,
                                          object_list_unit_id_2=UnitInfo.PIKEMAN.ID
                                       )
                    trigger.new_effect.replace_object(
                                          object_list_unit_id=UnitInfo.TWO_HANDED_SWORDSMAN.ID,
                                          source_player=targer_player,
                                          target_player=targer_player,
                                          object_list_unit_id_2=UnitInfo.HALBERDIER.ID
                                       )
                    trigger.new_effect.replace_object(
                                          object_list_unit_id=UnitInfo.CHAMPION.ID,
                                          source_player=targer_player,
                                          target_player=targer_player,
                                          object_list_unit_id_2=UnitInfo.HALBERDIER.ID
                                       )
        update_location_unit()

    def replace_archer_skirms(trigger_unit: int,
                              instruction_icon: int,
                              instruction_text: str):
        for player in range(1, NUMBER_OF_PLAYERS + 1):
            trigger = trigger_manager.add_trigger(f"Replace Archers With Skirms p({player})")
            trigger.looping = True
            trigger.new_condition.own_objects(
                quantity=1,
                object_list=trigger_unit,
                source_player=player
            )
            trigger.new_effect.remove_object(
                object_list_unit_id=trigger_unit,
                source_player=player,
            )
            trigger.new_effect.display_instructions(
                object_list_unit_id=instruction_icon,
                source_player=player,
                display_time=10,
                message=f"<{COLOUR[player - 1]}>Player {player} Has " + instruction_text
            )
            for targer_player in range(1, NUMBER_OF_PLAYERS + 1):
                if player != targer_player:
                    for garrisonable in GARRISONABLE_BY_ALL + GARRISONABLE_BY_MILITARY:
                        trigger.new_effect.unload(
                            object_list_unit_id=garrisonable,
                            source_player=targer_player,
                            location_x=0,
                            location_y=0
                        )
                    trigger.new_effect.replace_object(
                        object_list_unit_id=UnitInfo.ARCHER.ID,
                        source_player=targer_player,
                        target_player=targer_player,
                        object_list_unit_id_2=UnitInfo.SKIRMISHER.ID
                    )
                    trigger.new_effect.replace_object(
                        object_list_unit_id=UnitInfo.CROSSBOWMAN.ID,
                        source_player=targer_player,
                        target_player=targer_player,
                        object_list_unit_id_2=UnitInfo.ELITE_SKIRMISHER.ID
                    )
                    trigger.new_effect.replace_object(
                        object_list_unit_id=UnitInfo.ARBALESTER.ID,
                        source_player=targer_player,
                        target_player=targer_player,
                        object_list_unit_id_2=UnitInfo.IMPERIAL_SKIRMISHER.ID
                    )
        update_location_unit()

    def replace_kt_lc(trigger_unit: int,
                      instruction_icon: int,
                      instruction_text: str):
        for player in range(1, NUMBER_OF_PLAYERS + 1):
            trigger = trigger_manager.add_trigger(f"Replace Kt With Scouts p({player})")
            trigger.looping = True
            trigger.new_condition.own_objects(
                quantity=1,
                object_list=trigger_unit,
                source_player=player
            )
            trigger.new_effect.remove_object(
                object_list_unit_id=trigger_unit,
                source_player=player,
            )
            trigger.new_effect.display_instructions(
                object_list_unit_id=instruction_icon,
                source_player=player,
                display_time=10,
                message=f"<{COLOUR[player - 1]}>Player {player} Has " + instruction_text
            )
            for targer_player in range(1, NUMBER_OF_PLAYERS + 1):
                if player != targer_player:
                    for garrisonable in GARRISONABLE_BY_ALL + GARRISONABLE_BY_MILITARY:
                        trigger.new_effect.unload(
                            object_list_unit_id=garrisonable,
                            source_player=targer_player,
                            location_x=0,
                            location_y=0
                        )
                    trigger.new_effect.replace_object(
                        object_list_unit_id=UnitInfo.KNIGHT.ID,
                        source_player=targer_player,
                        target_player=targer_player,
                        object_list_unit_id_2=UnitInfo.LIGHT_CAVALRY.ID
                    )
                    trigger.new_effect.replace_object(
                        object_list_unit_id=UnitInfo.CAVALIER.ID,
                        source_player=targer_player,
                        target_player=targer_player,
                        object_list_unit_id_2=UnitInfo.HUSSAR.ID
                    )
                    trigger.new_effect.replace_object(
                        object_list_unit_id=UnitInfo.PALADIN.ID,
                        source_player=targer_player,
                        target_player=targer_player,
                        object_list_unit_id_2=UnitInfo.HUSSAR.ID
                    )
        update_location_unit()

    def replace_camel_lc(trigger_unit: int,
                         instruction_icon: int,
                         instruction_text: str):
        for player in range(1, NUMBER_OF_PLAYERS + 1):
            trigger = trigger_manager.add_trigger(f"Replace Camel With Scouts p({player})")
            trigger.looping = True
            trigger.new_condition.own_objects(
                quantity=1,
                object_list=trigger_unit,
                source_player=player
            )
            trigger.new_effect.remove_object(
                object_list_unit_id=trigger_unit,
                source_player=player,
            )
            trigger.new_effect.display_instructions(
                object_list_unit_id=instruction_icon,
                source_player=player,
                display_time=10,
                message=f"<{COLOUR[player - 1]}>Player {player} Has " + instruction_text
            )
            for targer_player in range(1, NUMBER_OF_PLAYERS + 1):
                if player != targer_player:
                    for garrisonable in GARRISONABLE_BY_ALL + GARRISONABLE_BY_MILITARY:
                        trigger.new_effect.unload(
                            object_list_unit_id=garrisonable,
                            source_player=targer_player,
                            location_x=0,
                            location_y=0
                        )
                    trigger.new_effect.replace_object(
                        object_list_unit_id=UnitInfo.CAMEL_RIDER.ID,
                        source_player=targer_player,
                        target_player=targer_player,
                        object_list_unit_id_2=UnitInfo.LIGHT_CAVALRY.ID
                    )
                    trigger.new_effect.replace_object(
                        object_list_unit_id=UnitInfo.HEAVY_CAMEL_RIDER.ID,
                        source_player=targer_player,
                        target_player=targer_player,
                        object_list_unit_id_2=UnitInfo.HUSSAR.ID
                    )
                    trigger.new_effect.replace_object(
                        object_list_unit_id=UnitInfo.IMPERIAL_CAMEL_RIDER.ID,
                        source_player=targer_player,
                        target_player=targer_player,
                        object_list_unit_id_2=UnitInfo.HUSSAR.ID
                    )
        update_location_unit()

    def replace_ele_lc(trigger_unit: int,
                       instruction_icon: int,
                       instruction_text: str):

        for player in range(1, NUMBER_OF_PLAYERS + 1):
            trigger = trigger_manager.add_trigger(f"Replace Ele With Scouts p({player})")
            trigger.looping = True
            trigger.new_condition.own_objects(
                quantity=1,
                object_list=trigger_unit,
                source_player=player
            )
            trigger.new_effect.remove_object(
                object_list_unit_id=trigger_unit,
                source_player=player,
            )
            trigger.new_effect.display_instructions(
                object_list_unit_id=instruction_icon,
                source_player=player,
                display_time=10,
                message=f"<{COLOUR[player - 1]}>Player {player} Has " + instruction_text
            )
            for targer_player in range(1, NUMBER_OF_PLAYERS + 1):
                if player != targer_player:
                    for garrisonable in GARRISONABLE_BY_ALL + GARRISONABLE_BY_MILITARY:
                        trigger.new_effect.unload(
                            object_list_unit_id=garrisonable,
                            source_player=targer_player,
                            location_x=0,
                            location_y=0
                        )
                    trigger.new_effect.replace_object(
                        object_list_unit_id=UnitInfo.BATTLE_ELEPHANT.ID,
                        source_player=targer_player,
                        target_player=targer_player,
                        object_list_unit_id_2=UnitInfo.LIGHT_CAVALRY.ID
                    )
                    trigger.new_effect.replace_object(
                        object_list_unit_id=UnitInfo.ELITE_BATTLE_ELEPHANT.ID,
                        source_player=targer_player,
                        target_player=targer_player,
                        object_list_unit_id_2=UnitInfo.HUSSAR.ID
                    )
        update_location_unit()

    def replace_sl_lc(trigger_unit: int,
                      instruction_icon: int,
                      instruction_text: str):
        for player in range(1, NUMBER_OF_PLAYERS + 1):
            trigger = trigger_manager.add_trigger(f"Replace Sl With Scouts p({player})")
            trigger.looping = True
            trigger.new_condition.own_objects(
                quantity=1,
                object_list=trigger_unit,
                source_player=player
            )
            trigger.new_effect.remove_object(
                object_list_unit_id=trigger_unit,
                source_player=player,
            )
            trigger.new_effect.display_instructions(
                object_list_unit_id=instruction_icon,
                source_player=player,
                display_time=10,
                message=f"<{COLOUR[player - 1]}>Player {player} Has " + instruction_text
            )
            for targer_player in range(1, NUMBER_OF_PLAYERS + 1):
                if player != targer_player:
                    for garrisonable in GARRISONABLE_BY_ALL + GARRISONABLE_BY_MILITARY:
                        trigger.new_effect.unload(
                            object_list_unit_id=garrisonable,
                            source_player=targer_player,
                            location_x=0,
                            location_y=0
                        )
                    trigger.new_effect.replace_object(
                        object_list_unit_id=UnitInfo.STEPPE_LANCER.ID,
                        source_player=targer_player,
                        target_player=targer_player,
                        object_list_unit_id_2=UnitInfo.LIGHT_CAVALRY.ID
                    )
                    trigger.new_effect.replace_object(
                        object_list_unit_id=UnitInfo.ELITE_STEPPE_LANCER.ID,
                        source_player=targer_player,
                        target_player=targer_player,
                        object_list_unit_id_2=UnitInfo.HUSSAR.ID
                    )
        update_location_unit()

    def replace_siege_petards_petards_trebs(trigger_unit: int,
                                            instruction_icon: int,
                                            instruction_text: str):
        for player in range(1, NUMBER_OF_PLAYERS + 1):
            trigger = trigger_manager.add_trigger(f"Siege Swap p({player})")
            trigger.looping = True
            trigger.new_condition.own_objects(
                quantity=1,
                object_list=trigger_unit,
                source_player=player
            )
            trigger.new_effect.remove_object(
                object_list_unit_id=trigger_unit,
                source_player=player,
            )
            trigger.new_effect.display_instructions(
                object_list_unit_id=instruction_icon,
                source_player=player,
                display_time=10,
                message=f"<{COLOUR[player - 1]}>Player {player} Has " + instruction_text
            )
            for targer_player in range(1, NUMBER_OF_PLAYERS + 1):
                if player != targer_player:
                    for garrisonable in GARRISONABLE_BY_ALL + GARRISONABLE_BY_MILITARY:
                        trigger.new_effect.unload(
                            object_list_unit_id=garrisonable,
                            source_player=targer_player,
                            location_x=0,
                            location_y=0
                        )
                    for siege in SIEGE_UNITS:
                        trigger.new_effect.replace_object(
                            object_list_unit_id=siege,
                            source_player=targer_player,
                            target_player=targer_player,
                            object_list_unit_id_2=HeroInfo.YEKUNA_AMLAK.ID
                        )
                    trigger.new_effect.replace_object(
                        object_list_unit_id=UnitInfo.PETARD.ID,
                        source_player=targer_player,
                        target_player=targer_player,
                        object_list_unit_id_2=UnitInfo.TREBUCHET_PACKED.ID
                    )
                    trigger.new_effect.replace_object(
                        object_list_unit_id=HeroInfo.YEKUNA_AMLAK.ID,
                        source_player=targer_player,
                        target_player=targer_player,
                        object_list_unit_id_2=UnitInfo.PETARD.ID
                    )
        update_location_unit()

    def idle_eco(trigger_unit: int,
                 instruction_icon: int,
                 instruction_text: str):
        for player in range(1, NUMBER_OF_PLAYERS+1):
            trigger = trigger_manager.add_trigger(f"idle eco p({player})")
            trigger.looping = True
            trigger.new_condition.own_objects(
                                  quantity=1,
                                  object_list=trigger_unit,
                                  source_player=player
                               )
            trigger.new_effect.remove_object(
                                  object_list_unit_id=trigger_unit,
                                  source_player=player,
                               )
            trigger.new_effect.display_instructions(
                                  object_list_unit_id=instruction_icon,
                                  source_player=player,
                                  display_time=10,
                                  message=f"<{COLOUR[player-1]}>Player {player} Has "+instruction_text
                               )
            for target_player in range(1, NUMBER_OF_PLAYERS+1):
                if target_player != player:
                    trigger.new_effect.stop_object(
                        source_player=target_player,
                        object_type=3
                    )
        update_location_unit()


    def labour_strike(trigger_unit: int,
                      instruction_icon: int,
                      instruction_text: str):
        for player in range(1, NUMBER_OF_PLAYERS+1):
            trigger = trigger_manager.add_trigger(f"Cooldown p({player})")
            trigger.looping = True
            trigger.new_condition.variable_value(
                                  quantity=0,
                                  variable=STRIKE_CD_VAR[player-1],
                                  comparison=Comparison.LARGER
                               )
            trigger.new_effect.change_variable(
                                  quantity=1,
                                  operation=Operation.SUBTRACT,
                                  variable=STRIKE_CD_VAR[player-1]
                               )

        activation_id = []
        for player in range(1, NUMBER_OF_PLAYERS+1):
            trigger = trigger_manager.add_trigger(f"Reset selection p({player})")
            trigger.enabled = False
            trigger.new_condition.variable_value(
                                  quantity=0,
                                  variable=STRIKE_CD_VAR[player-1],
                                  comparison=Comparison.EQUAL
                               )
            for vil in [villager for villager in UnitInfo if "VILLAGER" in villager.name]:
                trigger.new_effect.enable_object_selection(
                                      object_list_unit_id=vil.ID,
                                      source_player=player,
                                   )
            activation_id.append(trigger.trigger_id)

        for player in range(1, NUMBER_OF_PLAYERS+1):
            trigger = trigger_manager.add_trigger("Display Information")
            trigger.short_description = f"P{player}'s Strike Ends In: <Variable {STRIKE_CD_VAR[player-1]}>"
            trigger.display_on_screen = True
            trigger.new_condition.player_defeated(
                source_player=PlayerId.GAIA
            )

            trigger = trigger_manager.add_trigger(f"Strike p({player})")
            trigger.looping = True
            trigger.new_condition.own_objects(
                                  quantity=1,
                                  object_list=trigger_unit,
                                  source_player=player
                               )
            trigger.new_effect.remove_object(
                                  object_list_unit_id=trigger_unit,
                                  source_player=player,
                               )
            trigger.new_effect.display_instructions(
                                  object_list_unit_id=instruction_icon,
                                  source_player=player,
                                  display_time=10,
                                  message=f"<{COLOUR[player-1]}>Player {player} Has "+instruction_text
                               )
            for target_player in range(1, NUMBER_OF_PLAYERS+1):
                if target_player != player:
                    trigger.new_effect.activate_trigger(
                        trigger_id=activation_id[target_player - 1]
                    )
                    trigger.new_effect.change_variable(
                                          quantity=30,
                                          operation=Operation.ADD,
                                          variable=STRIKE_CD_VAR[target_player-1]
                                       )
                    for vil in [villager for villager in UnitInfo if "VILLAGER" in villager.name]:
                        trigger.new_effect.stop_object(
                                              object_list_unit_id=vil.ID,
                                              source_player=target_player,
                                           )
                        trigger.new_effect.disable_object_selection(
                                              object_list_unit_id=vil.ID,
                                              source_player=target_player,
                                           )
        update_location_unit()




    def dope(trigger_unit: int,
             instruction_icon: int,
             instruction_text: str):
        for player in range(1, NUMBER_OF_PLAYERS+1):
            trigger = trigger_manager.add_trigger(f"Dope cd p({player})")
            trigger.looping = True
            trigger.new_condition.variable_value(
                quantity=0,
                variable=DOPE_CD_VAR[player-1],
                comparison=Comparison.LARGER
            )
            trigger.new_effect.change_variable(
                quantity=1,
                operation=Operation.SUBTRACT,
                variable=DOPE_CD_VAR[player-1]
            )
        for player in range(1, NUMBER_OF_PLAYERS+1):
            trigger = trigger_manager.add_trigger(f"Player cd p({player})")
            trigger.looping = True
            trigger.new_condition.variable_value(
                quantity=0,
                variable=DOPE_PLAYER_CD_VAR[player-1],
                comparison=Comparison.LARGER
            )
            trigger.new_effect.change_variable(
                quantity=1,
                operation=Operation.SUBTRACT,
                variable=DOPE_PLAYER_CD_VAR[player-1]
            )

        activation_id = []
        for player in range(1, NUMBER_OF_PLAYERS+1):
            trigger = trigger_manager.add_trigger(f"Reset Villager stats p({player})")
            trigger.enabled = False
            trigger.new_condition.variable_value(
                quantity=0,
                variable=DOPE_CD_VAR[player-1],
                comparison=Comparison.EQUAL
            )
            trigger.new_effect.display_instructions(
                object_list_unit_id=instruction_icon,
                source_player=PlayerId.GAIA,
                display_time=10,
                message=f"Villager Doping Has Worn Off For Player {player}!"
            )
            for vil in [villager for villager in UnitInfo if "VILLAGER" in villager.name]:
                trigger.new_effect.modify_attribute(
                                      quantity=2,
                                      object_list_unit_id=vil.ID,
                                      source_player=player,
                                      item_id=vil.ID,
                                      operation=Operation.DIVIDE,
                                      object_attributes=ObjectAttribute.WORK_RATE
                                   )
                trigger.new_effect.modify_attribute(
                                      quantity=2,
                                      object_list_unit_id=vil.ID,
                                      source_player=player,
                                      item_id=vil.ID,
                                      operation=Operation.DIVIDE,
                                      object_attributes=ObjectAttribute.MOVEMENT_SPEED
                                   )
            trigger.new_effect.modify_attribute(
                quantity=2,
                object_list_unit_id=UnitInfo.FISHING_SHIP.ID,
                source_player=player,
                item_id=UnitInfo.FISHING_SHIP.ID,
                operation=Operation.DIVIDE,
                object_attributes=ObjectAttribute.WORK_RATE
            )
            trigger.new_effect.modify_attribute(
                quantity=2,
                object_list_unit_id=UnitInfo.FISHING_SHIP.ID,
                source_player=player,
                item_id=UnitInfo.FISHING_SHIP.ID,
                operation=Operation.DIVIDE,
                object_attributes=ObjectAttribute.MOVEMENT_SPEED
            )

            activation_id.append(trigger.trigger_id)

        reactivate_effect_trigger_ids = []
        for player in range(1, NUMBER_OF_PLAYERS+1):
            trigger = trigger_manager.add_trigger(f"Re-Enable p({player})")
            trigger.enabled = False
            trigger.new_condition.variable_value(
                                  quantity=0,
                                  variable=DOPE_PLAYER_CD_VAR[player-1],
                                  comparison=Comparison.EQUAL
                               )
            trigger.new_effect.enable_disable_object(
                                  object_list_unit_id=trigger_unit,
                                  source_player=player,
                                  enabled=True,
                                  item_id=trigger_unit
                               )
            trigger.new_effect.activate_trigger(
                                  trigger_id=trigger.trigger_id+NUMBER_OF_PLAYERS
                               )
            reactivate_effect_trigger_ids.append(trigger.trigger_id)

        for player in range(1, NUMBER_OF_PLAYERS+1):
            trigger = trigger_manager.add_trigger(f"Doping p({player})")
            trigger.looping = True
            trigger.new_condition.own_objects(
                                  quantity=1,
                                  object_list=trigger_unit,
                                  source_player=player
                               )
            trigger.new_effect.remove_object(
                                  object_list_unit_id=trigger_unit,
                                  source_player=player,
                               )
            trigger.new_effect.display_instructions(
                                  object_list_unit_id=instruction_icon,
                                  source_player=player,
                                  display_time=10,
                                  message=f"<{COLOUR[player-1]}>Player {player} Has "+instruction_text
                               )
            trigger.new_effect.activate_trigger(
                                  trigger_id=activation_id[player-1]
                               )
            trigger.new_effect.activate_trigger(
                                  trigger_id=reactivate_effect_trigger_ids[player-1]
                               )
            trigger.new_effect.deactivate_trigger(
                                  trigger_id=trigger.trigger_id
                               )
            trigger.new_effect.change_variable(
                                  quantity=60,
                                  operation=Operation.ADD,
                                  variable=DOPE_CD_VAR[player-1]
                               )
            trigger.new_effect.change_variable(
                                  quantity=300,
                                  operation=Operation.ADD,
                                  variable=DOPE_PLAYER_CD_VAR[player-1]
                               )
            trigger.new_effect.enable_disable_object(
                                  object_list_unit_id=trigger_unit,
                                  source_player=player,
                                  enabled=False,
                                  item_id=trigger_unit
                               )

            for vil in [villager for villager in UnitInfo if "VILLAGER" in villager.name]:
                trigger.new_effect.modify_attribute(
                                      quantity=2,
                                      object_list_unit_id=vil.ID,
                                      source_player=player,
                                      item_id=vil.ID,
                                      operation=Operation.MULTIPLY,
                                      object_attributes=ObjectAttribute.WORK_RATE
                                   )
                trigger.new_effect.modify_attribute(
                                      quantity=2,
                                      object_list_unit_id=vil.ID,
                                      source_player=player,
                                      item_id=vil.ID,
                                      operation=Operation.MULTIPLY,
                                      object_attributes=ObjectAttribute.MOVEMENT_SPEED
                                   )
            trigger.new_effect.modify_attribute(
                quantity=2,
                object_list_unit_id=UnitInfo.FISHING_SHIP.ID,
                source_player=player,
                item_id=UnitInfo.FISHING_SHIP.ID,
                operation=Operation.MULTIPLY,
                object_attributes=ObjectAttribute.WORK_RATE
            )
            trigger.new_effect.modify_attribute(
                quantity=2,
                object_list_unit_id=UnitInfo.FISHING_SHIP.ID,
                source_player=player,
                item_id=UnitInfo.FISHING_SHIP.ID,
                operation=Operation.MULTIPLY,
                object_attributes=ObjectAttribute.MOVEMENT_SPEED
            )
        for player in range(1, NUMBER_OF_PLAYERS+1):
            trigger = trigger_manager.add_trigger(f"Remove Unit p({player})")
            trigger.looping = True
            trigger.new_condition.own_objects(
                                  quantity=1,
                                  object_list=trigger_unit,
                                  source_player=player
                               )
            trigger.new_effect.remove_object(
                                  object_list_unit_id=trigger_unit,
                                  source_player=player,
                               )
        update_location_unit()




    add_credits_header("2.0.0", trigger_manager)

    setup()

    icon_unit = UnitInfo.VILLAGER_MALE
    perk_setup("kill all villagers",
               TRIGGER_UNITS[CURRENT_TRIGGER_UNIT],
               BuildingInfo.TRADE_WORKSHOP.ID,
               BUTTON_LOCATIONS[CURRENT_BUTTON_LOCATION],
               KILL_ALL_VILLAGERS_COST,
               "Black Death I (<Cost>)\nKill all villagers, trade and fishing ships on the map for EVERY player",
               CURRENT_PAGE == 0,
               icon_unit.ICON_ID)

    kill_all_villagers(TRIGGER_UNITS[CURRENT_TRIGGER_UNIT],
                       icon_unit.ID,
                       "Killed All Villagers!")

    icon_unit = UnitInfo.CHAMPION
    perk_setup("kill all military",
               TRIGGER_UNITS[CURRENT_TRIGGER_UNIT],
               BuildingInfo.TRADE_WORKSHOP.ID,
               BUTTON_LOCATIONS[CURRENT_BUTTON_LOCATION],
               KILL_ALL_MILITARY_COST,
               "Black Death II (<Cost>)\nKill all enemy military",
               CURRENT_PAGE == 0,
               icon_unit.ICON_ID)

    kill_all_military(TRIGGER_UNITS[CURRENT_TRIGGER_UNIT],
                      icon_unit.ID,
                      "Killed All Military!")

    icon_unit = HeroInfo.ARCHBISHOP
    CD_HEROES.append(TRIGGER_UNITS[CURRENT_TRIGGER_UNIT])
    CD_VARS.append(CEASE_FIRE_PLAYER_CD_VAR)
    perk_setup("cease fire",
               TRIGGER_UNITS[CURRENT_TRIGGER_UNIT],
               BuildingInfo.TRADE_WORKSHOP.ID,
               BUTTON_LOCATIONS[CURRENT_BUTTON_LOCATION],
               CEASE_FIRE_COST,
               "Cease Fire (<Cost>)\nCall a cease fire among all players for 60s\nCooldown: 300s",
               CURRENT_PAGE == 0,
               icon_unit.ICON_ID)

    cease_fire(TRIGGER_UNITS[CURRENT_TRIGGER_UNIT],
               UnitInfo.HAWK.ID,
               "Called For A Cease Fire!")

    icon_unit = HeroInfo.SABOTEUR
    perk_setup("exploding villagers",
               TRIGGER_UNITS[CURRENT_TRIGGER_UNIT],
               BuildingInfo.TRADE_WORKSHOP.ID,
               BUTTON_LOCATIONS[CURRENT_BUTTON_LOCATION],
               EV_COST,
               "Kamikaze (<Cost>)\nTurn ALL villagers into exploding villagers for 60s",
               CURRENT_PAGE == 0,
               icon_unit.ICON_ID)

    exploding_villagers(TRIGGER_UNITS[CURRENT_TRIGGER_UNIT],
                        icon_unit.ID,
                        "Has Activated Exploding Villagers!")

    PAGES[CURRENT_PAGE].append(TRIGGER_UNITS[CURRENT_TRIGGER_UNIT])

    icon_unit = UnitInfo.SIEGE_RAM
    perk_setup("kill all castles",
               TRIGGER_UNITS[CURRENT_TRIGGER_UNIT],
               BuildingInfo.TRADE_WORKSHOP.ID,
               BUTTON_LOCATIONS[CURRENT_BUTTON_LOCATION],
               KILL_ALL_CASTLES_COST,
               "Earthquake (<Cost>)\nKill all enemy castles",
               CURRENT_PAGE == 0,
               icon_unit.ICON_ID)

    kill_all_castles(TRIGGER_UNITS[CURRENT_TRIGGER_UNIT],
                      icon_unit.ID,
                      "Has Killed All Castles!")

    # FIVE

    icon_unit = HeroInfo.HUNTING_WOLF
    perk_setup("t90Woo",
               TRIGGER_UNITS[CURRENT_TRIGGER_UNIT],
               BuildingInfo.TRADE_WORKSHOP.ID,
               BUTTON_LOCATIONS[CURRENT_BUTTON_LOCATION],
               REPLACE_MILITARY_WOLF_COST,
               "t90Woo (<Cost>)\nReplace all enemy military with wolves",
               CURRENT_PAGE == 0,
               icon_unit.ICON_ID)

    military_to_t90woo(TRIGGER_UNITS[CURRENT_TRIGGER_UNIT],
                      icon_unit.ID,
                      "Has Converted All Military To Wolves!")

    icon_unit = UnitInfo.ARCHER
    perk_setup("cycle archer line",
               TRIGGER_UNITS[CURRENT_TRIGGER_UNIT],
               BuildingInfo.TRADE_WORKSHOP.ID,
               BUTTON_LOCATIONS[CURRENT_BUTTON_LOCATION],
               CYCLE_ARCHER_COST,
               "Ol' Betsy (<Cost>)\nReplace enemy arbalesters with crossbowmen, crossbowmen with "+
               "archers and archers with arbalesters",
               CURRENT_PAGE == 0,
               icon_unit.ICON_ID)

    cycle_archer_line(TRIGGER_UNITS[CURRENT_TRIGGER_UNIT],
                      icon_unit.ID,
                      "Has Cycled The Archer Line!")

    icon_unit = UnitInfo.HALBERDIER
    perk_setup("replace militia with spear",
               TRIGGER_UNITS[CURRENT_TRIGGER_UNIT],
               BuildingInfo.TRADE_WORKSHOP.ID,
               BUTTON_LOCATIONS[CURRENT_BUTTON_LOCATION],
               REPLACE_MAA_SPEAR_COST,
               "Pointi Bois (<Cost>)\nReplace enemy swordsman line units with corresponding age's spear line units ",
               CURRENT_PAGE == 0,
               icon_unit.ICON_ID)

    replace_maa_spear(TRIGGER_UNITS[CURRENT_TRIGGER_UNIT],
                      icon_unit.ID,
                      "Has Replaced Swordsman Line With Spearman Line!")

    icon_unit = UnitInfo.IMPERIAL_SKIRMISHER
    perk_setup("replace arhcer with skirmisher",
               TRIGGER_UNITS[CURRENT_TRIGGER_UNIT],
               BuildingInfo.TRADE_WORKSHOP.ID,
               BUTTON_LOCATIONS[CURRENT_BUTTON_LOCATION],
               REPLACE_MAA_SPEAR_COST,
               "Javlin Bois (<Cost>)\nReplace enemy archer line units with corresponding age's skirmisher line units ",
               CURRENT_PAGE == 0,
               icon_unit.ICON_ID)

    replace_archer_skirms(TRIGGER_UNITS[CURRENT_TRIGGER_UNIT],
                          icon_unit.ID,
                          "Has Replaced Archer Line With Skirmisher Line!")

    icon_unit = UnitInfo.SIEGE_TOWER
    perk_setup("replace siege petard trebs",
               TRIGGER_UNITS[CURRENT_TRIGGER_UNIT],
               BuildingInfo.TRADE_WORKSHOP.ID,
               BUTTON_LOCATIONS[CURRENT_BUTTON_LOCATION],
               REPLACE_SIEGE_PETARD_TREB_COST,
               "Siege Swap (<Cost>)\nReplace enemy siege units with petards and petards with trebuchets",
               CURRENT_PAGE == 0,
               icon_unit.ICON_ID)

    replace_siege_petards_petards_trebs(TRIGGER_UNITS[CURRENT_TRIGGER_UNIT],
                                        icon_unit.ID,
                                        "Has Replaced Siege With Petards And Petards With Trebuchets!")

    # TEN

    icon_unit = UnitInfo.PHOTONMAN
    perk_setup("idle eco",
               TRIGGER_UNITS[CURRENT_TRIGGER_UNIT],
               BuildingInfo.TRADE_WORKSHOP.ID,
               BUTTON_LOCATIONS[CURRENT_BUTTON_LOCATION],
               REPLACE_SIEGE_PETARD_TREB_COST,
               "Petrification (<Cost>)\nStop (idle) all enemy villagers",
               CURRENT_PAGE == 0,
               icon_unit.ICON_ID)

    idle_eco(TRIGGER_UNITS[CURRENT_TRIGGER_UNIT],
                                        icon_unit.ID,
                                        "Has Petrified Enemy Villagers!")

    icon_unit = UnitInfo.MERCHANT
    perk_setup("labour strike",
               TRIGGER_UNITS[CURRENT_TRIGGER_UNIT],
               BuildingInfo.TRADE_WORKSHOP.ID,
               BUTTON_LOCATIONS[CURRENT_BUTTON_LOCATION],
               REPLACE_SIEGE_PETARD_TREB_COST,
               "Labour Strike (<Cost>)\nEnemy villagers refuse to work for 30s",
               CURRENT_PAGE == 0,
               icon_unit.ICON_ID)

    labour_strike(TRIGGER_UNITS[CURRENT_TRIGGER_UNIT],
                                        icon_unit.ID,
                                        "Has Caused A Labour Strike In The Enemy Nations!")

    icon_unit = UnitInfo.KNIGHT
    perk_setup("replace kt with sc",
               TRIGGER_UNITS[CURRENT_TRIGGER_UNIT],
               BuildingInfo.TRADE_WORKSHOP.ID,
               BUTTON_LOCATIONS[CURRENT_BUTTON_LOCATION],
               REPLACE_KT_LC,
               "Pony Bois I (<Cost>)\nReplace enemy knights line units with the corresponding age's scout line units",
               CURRENT_PAGE == 0,
               icon_unit.ICON_ID)

    replace_kt_lc(TRIGGER_UNITS[CURRENT_TRIGGER_UNIT],
                  icon_unit.ID,
                  "Has Replaced The Knight Line With Scout Line!")

    icon_unit = UnitInfo.CAMEL_RIDER
    perk_setup("replace camels with sc",
               TRIGGER_UNITS[CURRENT_TRIGGER_UNIT],
               BuildingInfo.TRADE_WORKSHOP.ID,
               BUTTON_LOCATIONS[CURRENT_BUTTON_LOCATION],
               REPLACE_CAM_LC,
               "Pony Bois II (<Cost>)\nReplace enemy camel line units with the corresponding age's scout line units",
               CURRENT_PAGE == 0,
               icon_unit.ICON_ID)

    replace_camel_lc(TRIGGER_UNITS[CURRENT_TRIGGER_UNIT],
                     icon_unit.ID,
                     "Has Replaced The Camel Line With Scout Line!")

    icon_unit = UnitInfo.BATTLE_ELEPHANT
    perk_setup("replace ele with sc",
               TRIGGER_UNITS[CURRENT_TRIGGER_UNIT],
               BuildingInfo.TRADE_WORKSHOP.ID,
               BUTTON_LOCATIONS[CURRENT_BUTTON_LOCATION],
               REPLACE_ELE_LC,
               "Pony Bois III (<Cost>)\nReplace enemy battle elephant line units with the corresponding age's scout line units",
               CURRENT_PAGE == 0,
               icon_unit.ICON_ID)

    replace_ele_lc(TRIGGER_UNITS[CURRENT_TRIGGER_UNIT],
                   icon_unit.ID,
                   "Has Replaced The Battle Elephant Line With Scout Line!")

    # FIFTEEN

    icon_unit = UnitInfo.STEPPE_LANCER
    perk_setup("replace sl with sc",
               TRIGGER_UNITS[CURRENT_TRIGGER_UNIT],
               BuildingInfo.TRADE_WORKSHOP.ID,
               BUTTON_LOCATIONS[CURRENT_BUTTON_LOCATION],
               REPLACE_SL_LC,
               "Pony Bois IV (<Cost>)\nReplace enemy steppe lancer line units with the corresponding age's scout line units",
               CURRENT_PAGE == 0,
               icon_unit.ICON_ID)

    replace_sl_lc(TRIGGER_UNITS[CURRENT_TRIGGER_UNIT],
                  icon_unit.ID,
                  "Has Replaced The Steppe Lancer Line With Scout Line!")

    icon_unit = UnitInfo.ALFRED_THE_ALPACA
    CD_HEROES.append(TRIGGER_UNITS[CURRENT_TRIGGER_UNIT])
    CD_VARS.append(DOPE_PLAYER_CD_VAR)
    perk_setup("dope vils",
               TRIGGER_UNITS[CURRENT_TRIGGER_UNIT],
               BuildingInfo.TRADE_WORKSHOP.ID,
               BUTTON_LOCATIONS[CURRENT_BUTTON_LOCATION],
               DOPE_COST,
               "Doping (<Cost>)\nDouble the work rates and movement speeds of your own villagers and fishing ships for 60s"+
               "\nCooldown: 300s",
               CURRENT_PAGE == 0,
               icon_unit.ICON_ID)

    dope(TRIGGER_UNITS[CURRENT_TRIGGER_UNIT],
         icon_unit.ID,
         "Has Doped Their Villagers For 60s!")

    page_unit = HeroInfo.WILLIAM_WALLACE.ID
    perk_setup("change pages",
               page_unit,
               BuildingInfo.TRADE_WORKSHOP.ID,
               ButtonLocation.r3c4,
               [0, 0, 0, 0],
               "Next Page\nFlip over to the next page of perks",
               True,
               -2)

    page_setup(page_unit, PAGES)

    scenario.write_to_file(output_path + outname)