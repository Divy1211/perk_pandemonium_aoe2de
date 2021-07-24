from parser_projects.parser_imports import *

class Paths:
    SCENARIO_DIR = "C:/Users/LENOVO PC/Games/Age of Empires 2 DE/76561198276345085/resources/_common/scenario/"
    DESKTOP = "C:/Users/LENOVO PC/Desktop/"

class GameInfo:
    MESO_CIV = [TechInfo.AZTECS.ID, TechInfo.INCAS.ID, TechInfo.MAYANS.ID]

    CIV = [
        TechInfo.BRITONS.ID,
        TechInfo.BYZANTINES.ID,
        TechInfo.CELTS.ID,
        TechInfo.CHINESE.ID,
        TechInfo.FRANKS.ID,
        TechInfo.GOTHS.ID,
        TechInfo.JAPANESE.ID,
        TechInfo.MONGOLS.ID,
        TechInfo.PERSIANS.ID,
        TechInfo.SARACENS.ID,
        TechInfo.TEUTONS.ID,
        TechInfo.TURKS.ID,
        TechInfo.VIKINGS.ID,
        TechInfo.AZTECS.ID,
        TechInfo.HUNS.ID,
        TechInfo.KOREANS.ID,
        TechInfo.MAYANS.ID,
        TechInfo.SPANISH.ID,
        TechInfo.INCAS.ID,
        TechInfo.INDIANS.ID,
        TechInfo.ITALIANS.ID,
        TechInfo.MAGYARS.ID,
        TechInfo.SLAVS.ID,
        TechInfo.BERBERS.ID,
        TechInfo.ETHIOPIANS.ID,
        TechInfo.MALIANS.ID,
        TechInfo.PORTUGUESE.ID,
        TechInfo.BURMESE.ID,
        TechInfo.KHMER.ID,
        TechInfo.MALAY.ID,
        TechInfo.VIETNAMESE.ID,
        TechInfo.BULGARIANS.ID,
        TechInfo.CUMANS.ID,
        TechInfo.LITHUANIANS.ID,
        TechInfo.TATARS.ID,
        TechInfo.BURGUNDIANS.ID,
        TechInfo.SICILIANS.ID
    ]

    COLOUR = ["<BLUE>", "<RED>", "<GREEN>", "<YELLOW>", "<AQUA>", "<PURPLE>", "<GREY>", "<ORANGE>", ""]

    BUTTON_LOCATIONS = [1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13]

    HOTKEY_ID_MAP = {
        1: 16344,
        2: 16157,
        3: 16487,
        4: 16464,
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

    GARRISONABLE_BY_ALL = [
        BuildingInfo.TOWN_CENTER.ID,
        BuildingInfo.WATCH_TOWER.ID,
        BuildingInfo.GUARD_TOWER.ID,
        BuildingInfo.KEEP.ID,
        BuildingInfo.BOMBARD_TOWER.ID,
        BuildingInfo.HOUSE.ID,
        BuildingInfo.DONJON.ID,
        BuildingInfo.KREPOST.ID,
        BuildingInfo.CASTLE.ID,
        UnitInfo.BATTERING_RAM.ID,
        UnitInfo.CAPPED_RAM.ID,
        UnitInfo.SIEGE_RAM.ID,
        UnitInfo.SIEGE_TOWER.ID,
        UnitInfo.TRANSPORT_SHIP.ID
    ]

    GARRISONABLE_BY_MILITARY = [
        BuildingInfo.ARCHERY_RANGE.ID,
        BuildingInfo.BARRACKS.ID,
        BuildingInfo.STABLE.ID,
        BuildingInfo.SIEGE_WORKSHOP.ID,
        BuildingInfo.DOCK.ID,
        BuildingInfo.MONASTERY.ID
    ]

    SIEGE_UNITS = [
        UnitInfo.MANGONEL.ID,
        UnitInfo.ONAGER.ID,
        UnitInfo.SIEGE_ONAGER.ID,
        UnitInfo.SIEGE_TOWER.ID,
        UnitInfo.BATTERING_RAM.ID,
        UnitInfo.CAPPED_RAM.ID,
        UnitInfo.SIEGE_RAM.ID,
        UnitInfo.SCORPION.ID,
        UnitInfo.HEAVY_SCORPION.ID,
        UnitInfo.BOMBARD_CANNON.ID,
        UnitInfo.TREBUCHET.ID,
        UnitInfo.TREBUCHET_PACKED.ID,
        UnitInfo.ORGAN_GUN.ID,
        UnitInfo.ELITE_ORGAN_GUN.ID
    ]