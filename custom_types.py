from typing import TypedDict, Literal

class GamePropertyClass(TypedDict):
    name: str
    type: Literal["guess", "exact", "range"] 

class GameClass(TypedDict):
    id: int
    name: Literal["Loldle", "Pokédle", "Onepiecedle", "Smashdle", "Narutodle", "Dotadle"]
    properties: list[GamePropertyClass]
    dataPath: str
    