from parser_projects.parser_imports import *
import copy

MESO_CIV = [TechInfo.AZTECS.ID, TechInfo.INCAS.ID, TechInfo.MAYANS.ID]
COLOUR = ["BLUE", "RED", "GREEN", "YELLOW", "AQUA", "PURPLE", "GREY", "ORANGE"]

def correct_scout(NUMBER_OF_PLAYERS, trigger_manager):
    for player in range(1, NUMBER_OF_PLAYERS + 1):
        trigger = trigger_manager.add_trigger(f"Replace Scout p({int(player)})\x00")
        for civ in MESO_CIV:
            trigger.new_condition.research_technology(source_player=player,
                                                      technology=civ)
            if civ != MESO_CIV[-1]:
                trigger.new_condition.or_()
        trigger.new_effect.replace_object(
                           object_list_unit_id=UnitInfo.SCOUT_CAVALRY.ID,
                           source_player=player,
                           target_player=player,
                           object_list_unit_id_2=UnitInfo.EAGLE_SCOUT.ID
                        )

    for player in range(1, NUMBER_OF_PLAYERS + 1):
        trigger = trigger_manager.add_trigger(f"Replace Scout p({player})\x00")
        for civ in MESO_CIV:
            trigger.new_condition.research_technology(
                                  source_player=player,
                                  technology=civ,
                                  inverted=1
                                )
        trigger.new_effect.replace_object(
                           object_list_unit_id=UnitInfo.EAGLE_SCOUT.ID,
                           source_player=player,
                           target_player=player,
                           object_list_unit_id_2=UnitInfo.SCOUT_CAVALRY.ID
                        )


def add_civ_bonuses(NUMBER_OF_PLAYERS, trigger_manager):
    for player in range(1, NUMBER_OF_PLAYERS + 1):
        trigger = trigger_manager.add_trigger(f"Chinese Bonus (p{player})\x00")
        trigger.new_condition.research_technology(
                              source_player=player,
                              technology=TechInfo.CHINESE.ID
                            )
        trigger.new_effect.modify_resource(
                           source_player=player,
                           quantity=50,
                           tribute_list=Attribute.WOOD,
                           operation=Operation.SUBTRACT
                        )
        trigger.new_effect.modify_resource(
                           source_player=player,
                           quantity=200,
                           tribute_list=Attribute.FOOD,
                           operation=Operation.SUBTRACT
                        )

    for player in range(1, NUMBER_OF_PLAYERS + 1):
        trigger = trigger_manager.add_trigger(f"Lithuanian Bonus (p{player})\x00")
        trigger.new_condition.research_technology(
                              source_player=player,
                              technology=TechInfo.LITHUANIANS.ID
                            )
        trigger.new_effect.modify_resource(
                           source_player=player,
                           quantity=150,
                           tribute_list=Attribute.FOOD,
                           operation=Operation.ADD
                        )

    for player in range(1, NUMBER_OF_PLAYERS + 1):
        trigger = trigger_manager.add_trigger(f"Hun Bonus (p{player})\x00")
        trigger.new_condition.research_technology(
                              source_player=player,
                              technology=TechInfo.HUNS.ID
                            )
        trigger.new_effect.modify_resource(
                           source_player=player,
                           quantity=100,
                           tribute_list=Attribute.WOOD,
                           operation=Operation.SUBTRACT
                        )

    for player in range(1, NUMBER_OF_PLAYERS + 1):
        trigger = trigger_manager.add_trigger(f"Mayan Bonus (p{player})\x00")
        trigger.new_condition.research_technology(
                              source_player=player,
                              technology=TechInfo.MAYANS.ID
                            )
        trigger.new_effect.modify_resource(
                           source_player=player,
                           quantity=50,
                           tribute_list=Attribute.FOOD,
                           operation=Operation.SUBTRACT
                            )

    for player in range(1, NUMBER_OF_PLAYERS + 1):
        trigger = trigger_manager.add_trigger(f"Persian Bonus (p{player})\x00")
        trigger.new_condition.research_technology(
                              source_player=player,
                              technology=TechInfo.PERSIANS.ID
                            )
        trigger.new_effect.modify_resource(
                           source_player=player,
                           quantity=50,
                           tribute_list=Attribute.FOOD,
                           operation=Operation.ADD
                            )
        trigger.new_effect.modify_resource(
                           source_player=player,
                           quantity=50,
                           tribute_list=Attribute.FOOD,
                           operation=Operation.ADD
                            )

def handle_chinese(NUMBER_OF_PLAYERS, trigger_manager):
    for player in range(1, NUMBER_OF_PLAYERS+1):
        trigger = trigger_manager.add_trigger(f"if training villagers p({player})")
        trigger.new_condition.timer(
                              timer=2,
                              inverted=True
                           )
        trigger.new_condition.research_technology(
                              source_player=player,
                              technology=TechInfo.CHINESE.ID
                           )
        trigger.new_condition.accumulate_attribute(
                              attribute=Attribute.TRAINING_COUNT,
                              quantity=1,
                              source_player=player
                           )
        trigger.new_effect.change_ownership(
                              object_list_unit_id=BuildingInfo.TOWN_CENTER.ID,
                              source_player=player,
                              target_player=PlayerId.GAIA,
                           )
        trigger.new_effect.change_ownership(
                              object_list_unit_id=BuildingInfo.TOWN_CENTER.ID,
                              target_player=player,
                              source_player=PlayerId.GAIA,
                           )

    for player in range(1, NUMBER_OF_PLAYERS + 1):
        trigger = trigger_manager.add_trigger(f"if queued villagers p({player})")
        trigger.new_condition.timer(
            timer=2,
            inverted=True
        )
        trigger.new_condition.research_technology(
            source_player=player,
            technology=TechInfo.CHINESE.ID
        )
        trigger.new_condition.researching_tech(
                              source_player=player,
                              technology=TechInfo.LOOM.ID
                           )
        trigger.new_condition.accumulate_attribute(
                              attribute=Attribute.QUEUED_COUNT,
                              quantity=1,
                              source_player=player
                           )
        trigger.new_effect.activate_trigger(
                              trigger_id=trigger.trigger_id+NUMBER_OF_PLAYERS
                           )

    for player in range(1, NUMBER_OF_PLAYERS+1):
        trigger = trigger_manager.add_trigger(f"Dequeue TC p({player})")
        trigger.enabled = False
        trigger.new_condition.research_technology(
                              source_player=player,
                              technology=TechInfo.LOOM.ID
                           )
        trigger.new_condition.accumulate_attribute(
                              attribute=Attribute.TRAINING_COUNT,
                              quantity=1,
                              source_player=player
                           )
        trigger.new_effect.change_ownership(
                              object_list_unit_id=BuildingInfo.TOWN_CENTER.ID,
                              source_player=player,
                              target_player=PlayerId.GAIA,
                           )
        trigger.new_effect.change_ownership(
                              object_list_unit_id=BuildingInfo.TOWN_CENTER.ID,
                              target_player=player,
                              source_player=PlayerId.GAIA,
                           )

def dialogue_sequence(dialogues, trigger_manager):
    trigger = trigger_manager.add_trigger("-- Dialogue Sequence --")
    number = 1
    total_time = 0
    for dialogue in dialogues:
        trigger = trigger_manager.add_trigger(f"Dialogue {number}: {dialogue['speaker']}")
        trigger.new_condition.timer(
                              timer=total_time
                           )
        trigger.new_effect.display_instructions(
                              object_list_unit_id=dialogue["unit"],
                              source_player=dialogue["player"],
                              display_time=dialogue["time"],
                              instruction_panel_position=PanelLocation.CENTER,
                              message=f"<{COLOUR[dialogue['player']-1]}>{dialogue['speaker']}: "+dialogue["message"]
                           )
        total_time += dialogue["time"]
        number += 1

def add_credits_header(map_version, trigger_manager, parser_version = "0.1.8"):
    triggers = copy.deepcopy(trigger_manager.triggers)
    trigger_manager.triggers = []

    trigger_manager.add_trigger("\x00")
    trigger_manager.add_trigger("\x00")
    trigger_manager.add_trigger("\x00")
    trigger_manager.add_trigger(f"       Map By Alian713 ({map_version})\x00")
    trigger_manager.add_trigger(f" Made Using AoE2ScenarioParser v{parser_version}\x00")
    trigger_manager.add_trigger(" AoE2ScenarioParser by MrKirby:\x00")
    trigger_manager.add_trigger("https://github.com/KSneijders/AoE2ScenarioParser\x00")
    trigger_manager.add_trigger("\x00")
    trigger_manager.add_trigger("\x00")
    trigger_manager.add_trigger("\x00")

    trigger_manager.triggers.extend(triggers)
