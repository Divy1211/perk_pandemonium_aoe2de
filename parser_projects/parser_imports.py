# parser's imports
from AoE2ScenarioParser.aoe2_scenario import AoE2Scenario

from AoE2ScenarioParser.datasets.players import Player

from AoE2ScenarioParser.datasets.conditions import Condition
from AoE2ScenarioParser.datasets.effects import Effect
from AoE2ScenarioParser.datasets.buildings import Building, GaiaBuilding, GaiaBuildingIcon, BuildingIcon
from AoE2ScenarioParser.datasets.heroes import Hero, HeroIcon
from AoE2ScenarioParser.datasets.other import UnitOther, GaiaUnitOther
from AoE2ScenarioParser.datasets.units import Unit, GaiaUnit, UnitIcon, GaiaUnitIcon
from AoE2ScenarioParser.datasets.techs import Tech

from AoE2ScenarioParser.datasets.trigger_lists import Attribute
from AoE2ScenarioParser.datasets.trigger_lists import ButtonLocation
from AoE2ScenarioParser.datasets.trigger_lists import Comparison
from AoE2ScenarioParser.datasets.trigger_lists import DiplomacyState
from AoE2ScenarioParser.datasets.trigger_lists import ObjectAttribute
from AoE2ScenarioParser.datasets.trigger_lists import Operation
from AoE2ScenarioParser.datasets.trigger_lists import PanelLocation

from AoE2ScenarioParser.objects.triggers_obj import TriggersObject
from AoE2ScenarioParser.objects.triggers_obj import TriggerSelect

from AoE2ScenarioParser.datasets.terrains import Terrain
from AoE2ScenarioParser.pieces.structs.terrain import TerrainStruct

# gobal vars
output_path = input_path = "PATH_TO_THE_FOLDER_CONTAINING_SCENARIO"