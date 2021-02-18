from parser_projects.parser_imports import *

MESO_CIV_TECHS = [Tech.AZTECS, Tech.INCAS, Tech.MAYANS]


def correct_scout(NUMBER_OF_PLAYERS, trigger_manager: TriggersObject):
    for player in range(1, NUMBER_OF_PLAYERS + 1):
        trigger = trigger_manager.add_trigger(f"Replace Scout {int(player)}")
        for civ in MESO_CIV_TECHS:
            trigger.add_condition(Condition.RESEARCH_TECHNOLOGY,
                                  source_player=player,
                                  technology=civ)
            if civ != MESO_CIV_TECHS[-1]:
                trigger.add_condition(Condition.OR)
        trigger.add_effect(Effect.REPLACE_OBJECT,
                           object_list_unit_id=Unit.SCOUT_CAVALRY,
                           source_player=player,
                           target_player=player,
                           object_list_unit_id_2=Unit.EAGLE_SCOUT)

    for player in range(1, NUMBER_OF_PLAYERS + 1):
        trigger = trigger_manager.add_trigger(f"Replace Scout {player}")
        for civ in MESO_CIV_TECHS:
            trigger.add_condition(Condition.RESEARCH_TECHNOLOGY,
                                  source_player=player,
                                  technology=civ,
                                  inverted=1)
        trigger.add_effect(Effect.REPLACE_OBJECT,
                           object_list_unit_id=Unit.EAGLE_SCOUT,
                           source_player=player,
                           target_player=player,
                           object_list_unit_id_2=Unit.SCOUT_CAVALRY)


def add_civ_bonuses(NUMBER_OF_PLAYERS, trigger_manager: TriggersObject):
    for player in range(1, NUMBER_OF_PLAYERS + 1):
        trigger = trigger_manager.add_trigger(f"Chinese Bonus (p{player})")
        trigger.add_condition(Condition.RESEARCHING_TECH,
                              source_player=player,
                              technology=Tech.CHINESE)
        trigger.add_effect(Effect.MODIFY_RESOURCE,
                           source_player=player,
                           quantity=50,
                           tribute_list=Attribute.WOOD,
                           operation=Operation.SUBTRACT)
        trigger.add_effect(Effect.MODIFY_RESOURCE,
                           source_player=player,
                           quantity=200,
                           tribute_list=Attribute.FOOD,
                           operation=Operation.SUBTRACT)

    for player in range(1, NUMBER_OF_PLAYERS + 1):
        trigger = trigger_manager.add_trigger(f"Lithuanian Bonus (p{player})")
        trigger.add_condition(Condition.RESEARCHING_TECH,
                              source_player=player,
                              technology=Tech.LITHUANIANS)
        trigger.add_effect(Effect.MODIFY_RESOURCE,
                           source_player=player,
                           quantity=150,
                           tribute_list=Attribute.FOOD,
                           operation=Operation.ADD)

    for player in range(1, NUMBER_OF_PLAYERS + 1):
        trigger = trigger_manager.add_trigger(f"Hun Bonus (p{player})")
        trigger.add_condition(Condition.RESEARCHING_TECH,
                              source_player=player,
                              technology=Tech.HUNS)
        trigger.add_effect(Effect.MODIFY_RESOURCE,
                           source_player=player,
                           quantity=100,
                           tribute_list=Attribute.WOOD,
                           operation=Operation.SUBTRACT)

    for player in range(1, NUMBER_OF_PLAYERS + 1):
        trigger = trigger_manager.add_trigger(f"Mayan Bonus (p{player})")
        trigger.add_condition(Condition.RESEARCHING_TECH,
                              source_player=player,
                              technology=Tech.MAYANS)
        trigger.add_effect(Effect.MODIFY_RESOURCE,
                           source_player=player,
                           quantity=50,
                           tribute_list=Attribute.FOOD,
                           operation=Operation.SUBTRACT)

    for player in range(1, NUMBER_OF_PLAYERS + 1):
        trigger = trigger_manager.add_trigger(f"Persian Bonus (p{player})")
        trigger.add_condition(Condition.RESEARCHING_TECH,
                              source_player=player,
                              technology=Tech.PERSIANS)
        trigger.add_effect(Effect.MODIFY_RESOURCE,
                           source_player=player,
                           quantity=50,
                           tribute_list=Attribute.FOOD,
                           operation=Operation.ADD)
        trigger.add_effect(Effect.MODIFY_RESOURCE,
                           source_player=player,
                           quantity=50,
                           tribute_list=Attribute.FOOD,
                           operation=Operation.ADD)


def add_credits_header(map_version, trigger_manager: TriggersObject, parser_version = "0.0.20"):
    trigger_manager.add_trigger("")
    trigger_manager.add_trigger("")
    trigger_manager.add_trigger("")
    trigger_manager.add_trigger(f"       Map By Alian713 ({map_version})")
    trigger_manager.add_trigger(f" Made Using AoE2ScenarioParser v{parser_version}")
    trigger_manager.add_trigger(" AoE2ScenarioParser by MrKirby:")
    trigger_manager.add_trigger("https://github.com/KSneijders/AoE2ScenarioParser")
    trigger_manager.add_trigger("")
    trigger_manager.add_trigger("")
    trigger_manager.add_trigger("")
