from parser_projects.parser_imports import *
from parser_projects.common_vars import GameInfo
import copy

_condition_grammar = {
    "1": "OBJECT1 not AREA",
    "2": "OBJECT1 not near OBJECT2",
    "3": "has at least",
    "4": "has at most AREA",
    "5": "has at least AREA",
    "6": "OBJECT1 has not been destroyed",
    "7": "has not captured OBJECT1",
    "8": "has at least",
    "9": "has not researched",
    "10": "VALUE seconds have not passed",
    "11": "OBJECT1 is not selected",
    "12": "ai signal VALUE is not detected",
    "13": "has not been defeated",
    "14": "OBJECT1 is not targeting OBJECT2",
    "15": "OBJECT1 is visible",
    "16": "OBJECT1 is not visible",
    "17": "is not researching",
    "18": "OBJECT1 has at least VALUE objects garrisoned",
    "19": "difficulty level is not",
    "20": "with a probability of VALUE%",
    "21": "TECH_STATE",
    "22": "is not",
    "23": "OBJECT1 has exactly VALUE HP",
    "24": "is not DIPLO_STATE with",
    "25": "XS function returns true",
    "26": "cannot see OBJECT1",
    "27": "has not selected OBJECT1",
    "28": "OBJECT1 is not ACTION",
    "29": "or",
    "30": "ai signal VALUE is not detected"
}

_object_state_grammar = {
    "0": "that is a foundationPLURAL",
    "1": "that is almost alive",
    "2": "that is alive",
    "3": "that is a resourcePLURAL",
    "4": "that is dying",
    "5": "that is dead",
    "6": "that is undead",
    "7": "that is removed"
}

_tech_state_grammar = {
    "0": "is not ready to research",
    "1": "is not ready to research",
    "2": "is not researching",
    "3": "has not researched",
    "4": "has not queued",
    "-1": "is not able to research"
}

_diplo_state_grammar = {
    "0": "allied with",
    "1": "enemies with",
    "3": "neutral with",
}

_comparison_grammar = {
    "0": "equal to",
    "1": "less than",
    "2": "greater than",
    "3": "less than or equal to",
    "4": "greater than or equal to"
}

_action_grammar = {
    "0": "doing anything",
    "1": "attacking OBJECT2",
    "3": "building OBJECT2",
    "5": "converting OBJECT2",
    "2": "defending OBJECT2",
    "18": "entering OBJECT2",
    "17": "evading OBJECT2",
    "6": "exploring",
    "13": "following OBJECT2",
    "10": "gathering from OBJECT2",
    "4": "healing OBJECT2",
    "14": "hunting OBJECT2",
    "24": "idle",
    "11": "moving",
    "12": "patrolling",
    "23": "going to pick up OBJECT2",
    "19": "repairing OBJECT2",
    "21": "researching",
    "9": "retreating from OBJECT2",
    "8": "running away from OBJECT2",
    "7": "stopping",
    "16": "trading with OBJECT2",
    "20": "training",
    "15": "transporting OBJECT2",
    "22": "unloading OBJECT2"
}



def add_credits_header(map_version, trigger_manager, parser_version="0.1.12"):
    triggers = copy.deepcopy(trigger_manager.triggers)
    trigger_manager.triggers = []

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

    trigger_manager.triggers.extend(triggers)


def correct_scout(NUMBER_OF_PLAYERS, trigger_manager):
    for player in range(1, NUMBER_OF_PLAYERS + 1):
        trigger = trigger_manager.add_trigger(f"Replace Scout p({int(player)})")
        for civ in GameInfo.MESO_CIV:
            trigger.new_condition.research_technology(source_player=player,
                                                      technology=civ)
            if civ != GameInfo.MESO_CIV[-1]:
                trigger.new_condition.or_()
        trigger.new_effect.replace_object(
            object_list_unit_id=UnitInfo.SCOUT_CAVALRY.ID,
            source_player=player,
            target_player=player,
            object_list_unit_id_2=UnitInfo.EAGLE_SCOUT.ID
        )

    for player in range(1, NUMBER_OF_PLAYERS + 1):
        trigger = trigger_manager.add_trigger(f"Replace Scout p({player})")
        for civ in GameInfo.MESO_CIV:
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
        trigger = trigger_manager.add_trigger(f"Chinese Bonus p({player})")
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
        trigger = trigger_manager.add_trigger(f"Lithuanian Bonus p({player})")
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
        trigger = trigger_manager.add_trigger(f"Hun Bonus p({player})")
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
        trigger = trigger_manager.add_trigger(f"Mayan Bonus p({player})")
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
        trigger = trigger_manager.add_trigger(f"Persian Bonus p({player})")
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
    for player in range(1, NUMBER_OF_PLAYERS + 1):
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
            trigger_id=trigger.trigger_id + NUMBER_OF_PLAYERS
        )

    for player in range(1, NUMBER_OF_PLAYERS + 1):
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
            message=f"<{GameInfo.COLOUR[dialogue['player'] - 1]}>{dialogue['speaker']}: " + dialogue["message"]
        )
        total_time += dialogue["time"]
        number += 1


def implement_guardstate(unit, NUMBER_OF_PLAYERS, trigger_manager):
    for player in range(1, NUMBER_OF_PLAYERS + 1):
        trigger = trigger_manager.add_trigger(f"Guard {unit.name} p{player}")
        trigger.new_condition.own_fewer_objects(
            quantity=0,
            object_list=unit.ID,
            source_player=player
        )
        trigger.new_effect.declare_victory(
            source_player=player,
            enabled=False
        )


def implement_regicide(NUMBER_OF_PLAYERS, trigger_manager):
    implement_guardstate(UnitInfo.KING, NUMBER_OF_PLAYERS, trigger_manager)


def implement_koth(NUMBER_OF_PLAYERS, trigger_manager):
    MONUMENT_OWNER_VAR = 246
    COUNTDOWN_VAR = 247

    for player in range(1, NUMBER_OF_PLAYERS + 1):
        trigger = trigger_manager.add_trigger(f"Set Trickle Res p({player})")
        trigger.new_effect.modify_resource(
            quantity=1,
            tribute_list=Attribute.FOOD_TRICKLE_FROM_MONUMENT,
            source_player=player,
            operation=Operation.SET
        )
        trigger.new_effect.modify_resource(
            quantity=1,
            tribute_list=Attribute.WOOD_TRICKLE_FROM_MONUMENT,
            source_player=player,
            operation=Operation.SET
        )
        trigger.new_effect.modify_resource(
            quantity=1,
            tribute_list=Attribute.GOLD_TRICKLE_FROM_MONUMENT,
            source_player=player,
            operation=Operation.SET
        )
        trigger.new_effect.modify_resource(
            quantity=1,
            tribute_list=Attribute.STONE_TRICKLE_FROM_MONUMENT,
            source_player=player,
            operation=Operation.SET
        )

    trigger = trigger_manager.add_trigger("Set Vars")
    trigger.new_effect.change_variable(
        quantity=9,
        operation=Operation.SET,
        variable=MONUMENT_OWNER_VAR
    )
    trigger.new_effect.change_variable(
        quantity=551,
        operation=Operation.SET,
        variable=COUNTDOWN_VAR
    )

    trigger = trigger_manager.add_trigger("Under 100 Years Reset")
    trigger.enabled = False
    trigger.new_condition.variable_value(
        quantity=100,
        variable=COUNTDOWN_VAR,
        comparison=Comparison.LESS_OR_EQUAL
    )
    trigger.new_effect.change_variable(
        quantity=100,
        operation=Operation.SET,
        variable=COUNTDOWN_VAR
    )

    activate_trigger_id = trigger.trigger_id

    for player in range(1, NUMBER_OF_PLAYERS + 1):
        trigger = trigger_manager.add_trigger(f"Set Owner to p({player})")
        trigger.new_condition.own_objects(
            quantity=1,
            object_list=BuildingInfo.MONUMENT.ID,
            source_player=player
        )
        trigger.new_effect.change_variable(
            quantity=player,
            operation=Operation.SET,
            variable=MONUMENT_OWNER_VAR
        )
        trigger.new_effect.activate_trigger(
            trigger_id=activate_trigger_id
        )
        for trigger_ids in range(trigger.trigger_id - player + 1, trigger.trigger_id + NUMBER_OF_PLAYERS - player + 1):
            if trigger_ids != trigger.trigger_id:
                trigger.new_effect.activate_trigger(
                    trigger_id=trigger_ids
                )
    trigger = trigger_manager.add_trigger("Update Countdown")
    trigger.looping = True
    trigger.new_condition.own_fewer_objects(
        quantity=0,
        object_list=BuildingInfo.MONUMENT.ID,
        source_player=PlayerId.GAIA
    )
    trigger.new_condition.timer(
        timer=5
    )
    trigger.new_effect.change_variable(
        quantity=1,
        operation=Operation.SUBTRACT,
        variable=COUNTDOWN_VAR
    )

    trigger = trigger_manager.add_trigger("Display Countdown")
    trigger.description = trigger.short_description = f"<Variable {COUNTDOWN_VAR}> Years Remaining\nMonument Owned By" + \
                                                      f" P<Variable {MONUMENT_OWNER_VAR}>"
    trigger.display_as_objective = trigger.display_on_screen = True
    trigger.new_condition.player_defeated(
        source_player=PlayerId.GAIA
    )

    for player in range(1, NUMBER_OF_PLAYERS + 1):
        trigger = trigger_manager.add_trigger(f"Win p({player})")
        trigger.new_condition.variable_value(
            quantity=0,
            variable=COUNTDOWN_VAR,
            comparison=Comparison.EQUAL
        )
        trigger.new_condition.own_objects(
            quantity=1,
            object_list=BuildingInfo.MONUMENT.ID,
            source_player=player
        )
        trigger.new_effect.declare_victory(
            source_player=player,
            enabled=True
        )


def condition_to_text(condition: Condition, trigger_manager):
    _condition = condition.condition_type
    quantity = condition.quantity
    resource = condition.attribute
    ref1 = condition.unit_object
    ref2 = condition.next_object
    unit = condition.object_list
    src = condition.source_player
    tech = condition.technology
    timer = condition.timer
    x1 = condition.area_x1
    y1 = condition.area_y1
    x2 = condition.area_x2
    y2 = condition.area_y2
    group = condition.object_group
    _type = condition.object_type
    state = condition.object_state
    ai_signal = condition.ai_signal
    inverted = condition.inverted
    var = condition.variable
    comparison = condition.comparison
    trg = condition.target_player
    action = condition.unit_ai_action
    xs = condition.xs_function

    output = ""
    if _condition not in [20, 29]:
        output = "if VARIABLE "

    if src == 0:
        src = "Gaia"
    elif src != -1:
        src = f"p{src}"

    if trg == 0:
        trg = "Gaia"
    elif trg != -1:
        trg = f"p{src}"

    output += {"-1": ""}.get(f"{src}", f"{src} ")
    output += _condition_grammar[f"{_condition}"]
    output = output.replace("least", "most") if inverted else output.replace(" not", "").replace("not ", " ")

    if var != -1:
        try:
            output = output.replace("VARIABLE", f"{trigger_manager.get_variable(variable_id=var).name}")
        except AttributeError:
            output = output.replace("VARIABLE", f"Variable {var}")

        output += f" {_comparison_grammar[f'{comparison}']} {quantity}"
        return output

    output = output.replace("VARIABLE ", "")

    if timer != -1:
        output = output.replace("VALUE", f"{timer}")
        return output

    if ai_signal != -1:
        output = output.replace("VALUE", f"{ai_signal}")
        return output

    if xs:
        return output

    if action != -1:
        output = output.replace("ACTION", _action_grammar.get(f"{action}", f"action: {action}"))

    if ref1 != -1:
        output = output.replace("OBJECT1", f"object: {ref1}")
        if ref2 != -1:
            output = output.replace("OBJECT2", f"object: {ref2}")
        else:
            output = output.replace("OBJECT2", f"another object")

    need_quantity = False
    if _condition != 21 and quantity != -1:
        need_quantity = True
        placeholders = ["VALUE", "DIPLO_STATE"]
        replacements = [{"-1": ""}, _diplo_state_grammar]
        for placeholder, replacement in zip(placeholders, replacements):
            if placeholder in output:
                output = output.replace(placeholder, replacement.get(f"{quantity}", f"{quantity}"))
                need_quantity = False
                if quantity == 1:
                    output.replace("objects", "object")
                break
        if need_quantity:
            output += f" {quantity}"

    if tech != -1:
        try:
            output += " " + TechInfo.from_id(tech).name.lower().replace("_", " ")
        except ValueError:
            output += " " + f"tech: {tech}"

        if _condition == 21:
            output = output.replace("TECH_STATE", _tech_state_grammar.get(f"{quantity}", f"{quantity}"))
            if not inverted:
                output = output.replace(" not", "") if quantity not in [-1, 0] else output
            else:
                output = output.replace(" not", "") if quantity in [-1, 0] else output

        if tech in GameInfo.CIV:
            output = output.replace(" researched", "")
            output = output.replace(" able to research", "")
            if quantity != 4:
                output = output.replace("has", "is")

        return output

    if trg != -1:
        output += f" {trg}"
        return output

    if unit != -1:
        unit_name = ""
        for dataset in [UnitInfo, BuildingInfo, HeroInfo, OtherInfo]:
            try:
                unit_enum = dataset.from_id(unit)
                if unit_enum is None:
                    continue
                unit_name = unit_enum.name.lower().replace("_", " ")
            except ValueError:
                continue

        output += " " + (unit_name or f"{unit}")
        if need_quantity:
            output += "" if quantity == 1 else "s"

    elif group != -1 or _type != -1:
        if _type != -1:
            output += " unit of type: " if quantity == 1 else " units of type: "
            try:
                output += ObjectType(_type).name.lower().replace("_", " ")
            except ValueError:
                output += f"{_type}"
        if group != -1:
            if _type != -1:
                output += " and"
            output += " belonging to class: "
            try:
                output += ObjectClass(group).name.lower().replace("_", " ")
            except ValueError:
                output += f"{group}"

    output_parts = output.partition(" AREA")
    output = output_parts[0] + output_parts[2] + output_parts[1]

    if x1 != -1:
        state_if_present = ""
        if state != -1:
            state_if_present = _object_state_grammar[f"{state}"] + " "
            if quantity > 1:
                state_if_present = state_if_present.replace("is a", "are")
                state_if_present = state_if_present.replace("is", "are")
                state_if_present = state_if_present.replace("PLURAL", "s")
            else:
                state_if_present = state_if_present.replace("PLURAL", "")

        output = output.replace("AREA", f"{state_if_present}in the area from ({x1}, {y1}) to ({x2}, {y2})")
    else:
        output = output.replace("AREA", f"on the map")

    if resource != -1:
        try:
            output += " " + Attribute(resource).name.lower().replace("_", " ")
        except ValueError:
            output += " " + f"{resource}"

    return output