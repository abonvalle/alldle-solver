from custom_types import GamePropertyClass, GameClass
from bcolors import bcolors

LODLE_PROPERTIES :list[GamePropertyClass] = [
    {"name":"Champion","type":"guess"},
    {"name":"Gender","type":"exact"},
    {"name":"Position(s)","type":"exact"},
    {"name":"Species","type":"exact"},
    {"name":"Resource","type":"exact"},
    {"name":"Range type","type":"exact"},
    {"name":"Region(s)","type":"exact"},
    {"name":"Release year","type":"range"}]

POKEDLE_PROPERTIES:list[GamePropertyClass]  = [
    {"name":"Pokémon","type":"guess"},
    {"name":"Type 1","type":"exact"},
    {"name":"Type 2","type":"exact"},
    {"name":"Habitat","type":"exact"},
    {"name":"Color(s)","type":"exact"},
    {"name":"Evolution stage","type":"range"},
    {"name":"Height","type":"range"},
    {"name":"Weight","type":"range"}]

ONEPIECEDLE_PROPERTIES:list[GamePropertyClass]  = [
    {"name":"Character","type":"guess"},
    {"name":"Gender","type":"exact"},
    {"name":"Affiliation","type":"exact"},
    {"name":"Devil fruit","type":"exact"},
    {"name":"Haki","type":"exact"},
    {"name":"Last bounty","type":"range"},
    {"name":"Height","type":"range"},
    {"name":"Origin","type":"exact"},
    {"name":"First arc","type":"range"}]

SMASHDLE_PROPERTIES:list[GamePropertyClass]  = [
    {"name":"Character","type":"guess"},
    {"name":"Gender","type":"exact"},
    {"name":"Species","type":"exact"},
    {"name":"Universe","type":"exact"},
    {"name":"Weight","type":"range"},
    {"name":"First appearance","type":"exact"},
    {"name":"Platform of origin","type":"exact"},
    {"name":"Origin date","type":"range"}]

NARUTODLE_PROPERTIES:list[GamePropertyClass]  = [
    {"name":"Character","type":"guess"},
    {"name":"Gender","type":"exact"},
    {"name":"Affiliations","type":"exact"},
    {"name":"Jutsu types","type":"exact"},
    {"name":"Kekkei genkai","type":"exact"},
    {"name":"Nature types","type":"exact"},
    {"name":"Attributes","type":"exact"},
    {"name":"Debut arc","type":"range"}]

DOTADLE_PROPERTIES:list[GamePropertyClass] = [
    {"name":"Hero","type":"guess",},
    {"name":"Gender","type":"exact"},
    {"name":"Species","type":"exact"},
    {"name":"Position(s)","type":"exact"},
    {"name":"Attribute","type":"exact"},
    {"name":"Range type","type":"exact"},
    {"name":"Complexity","type":"exact"},
    {"name":"Release year","type":"range"}]

AVAILABLE_GAMES: list[GameClass] = [
    {"id":1, "name":'Loldle',"properties":LODLE_PROPERTIES, "dataPath": "data/loldle.csv"},
    {"id":2, "name":'Pokédle',"properties":POKEDLE_PROPERTIES, "dataPath": "data/pokedle.csv"},
    {"id":3, "name":'Onepiecedle',"properties":ONEPIECEDLE_PROPERTIES, "dataPath": "data/onepiecedle.csv"},
    {"id":4, "name":'Smashdle',"properties":SMASHDLE_PROPERTIES, "dataPath": "data/smashdle.csv"},
    {"id":5, "name":'Narutodle',"properties":NARUTODLE_PROPERTIES, "dataPath": "data/narutodle.csv"},
    {"id":6, "name":'Dotadle',"properties":DOTADLE_PROPERTIES, "dataPath": "data/dotadle.csv"}]

FEEDBACKS={
    "correct":{"letter":"T", "label":f"{bcolors.BOLD}{bcolors.OKGREEN}T{bcolors.ENDC}","description":"Correct"},
    "partial":{"letter":"P", "label":f"{bcolors.BOLD}{bcolors.WARNING}P{bcolors.ENDC}","description":"Partial"},
    "incorrect":{"letter":"F", "label":f"{bcolors.BOLD}{bcolors.FAIL}F{bcolors.ENDC}","description":"Incorrect"},
    "greater":{"letter":"G", "label":f"{bcolors.BOLD}{bcolors.FAIL}G{bcolors.ENDC}","description":"Greater"},
    "lower":{"letter":"L", "label":f"{bcolors.BOLD}{bcolors.FAIL}L{bcolors.ENDC}","description":"Lower"}}