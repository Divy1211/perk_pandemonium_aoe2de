# Perk Pandemonium AoE2DE
This python code can be used to generate a custom scenario called Perk Pandemonium from scratch for the game Age of Empires II: Definitive Edition.
The ingame mod can be found [here](https://www.ageofempires.com/mods/details/19751/)

# Dependencies
This requires installing the [AoE2ScenarioParser](https://github.com/KSneijders/AoE2ScenarioParser) library:

1. `pip install AoE2ScenarioParser==0.0.20`

# How to run the program:
Navigate to the `parser_projects/maps/` folder and then do `py perk_pandemonium.py`

# About the Scenario

Perk Pandemonium is a scenario where players can create trade workshops for 200W and 50S and buy the following perks:

1. kill all enemy military units for 4kG
2. kill all villagers for 10kF
3. cease fire for 60s (cooldown of 300s) for 200F+200G
4. transform all villagers into EV for 60s for 1kG
5. kill all enemy castles for 5kF 500G 500S
6. replace all enemy military with hunting wolves for 2kG
7. transform arbs -> xbow -> archers -> arbs for 1kG
8. convert enemy champ to halbs 1kW and 500G
9. convert enemy archers to skirms 1kW and 500G
10. swap all enemy siege with petards and petards with trebs for 1kW and 500G
11. petrify enemy vils for 500F + 500S (only idle them)
12. labor strike for 1kF+500S for 30s
