import dataclasses
from pathlib import Path
from typing import Dict, Union

RARITY_BRONZE = 1
RARITY_SILVER = 2
RARITY_GOLD = 3
RARITY_LEGEND = 4


def strToRarity(string: str) -> int:
    if string == "ブロンズレア":
        return RARITY_SILVER
    if string == "シルバーレア":
        return RARITY_SILVER
    if string == "ゴールドレア":
        return RARITY_GOLD
    return RARITY_LEGEND


@dataclasses.dataclass(frozen=True)
class ShadowVerseCard:
    rarity: int
    set: str
    cv: str
    cost: int

    def toDict(self) -> Dict[str, Union[str, int]]:
        return {
            "rarity": self.rarity,
            "set": self.set,
            "cv": self.cv,
            "cost": self.cost
        }


@dataclasses.dataclass(frozen=True)
class ShadowVerseFollower:
    base_info: ShadowVerseCard
    type: str
    base_hp: int
    base_attack: int
    base_effect: str
    base_flavor: str
    evolve_hp: int
    evolve_attack: int
    evolve_effect: str
    evolve_flavor: str
    base_image_file_name: str
    evolve_image_file_name: str
    play_audio_file_name: str
    attack_audio_file_name: str
    evolve_audio_file_name: str
    death_audio_file_name: str

    def toDict(self) -> Dict[str, Union[str, int, Dict[str, Union[str, int]]]]:
        return {
            "base_info": self.base_info.toDict(),
            "card_type": "Follower",
            "type": self.type,
            "base_hp": self.base_hp,
            "base_attack": self.base_attack,
            "base_effect": self.base_effect,
            "base_flavor": self.base_flavor,
            "evolve_hp": self.evolve_hp,
            "evolve_attack": self.evolve_attack,
            "evolve_effect": self.evolve_effect,
            "evolve_flavor": self.evolve_flavor,
            "base_image_file_name": self.base_image_file_name,
            "evolve_image_file_name": self.evolve_image_file_name,
            "play_audio_file_name": self.play_audio_file_name,
            "attack_audio_file_name": self.attack_audio_file_name,
            "evolve_audio_file_name": self.evolve_audio_file_name,
            "death_audio_file_name": self.death_audio_file_name,

        }


@dataclasses.dataclass(frozen=True)
class ShadowVerseSpell:
    base_info: ShadowVerseCard
    effect: str
    flavor: str
    image_file_name: str
    play_audio_file_name: str | None

    def toDict(self) -> Dict[str, Union[str, int, None, Dict[str, Union[str, int]]]]:
        return {
            "base_info": self.base_info.toDict(),
            "card_type": "Spell",
            "effect": self.effect,
            "flavor": self.flavor,
            "image_file_name": self.image_file_name,
            "play_audio_file_name": self.play_audio_file_name,
        }


@dataclasses.dataclass(frozen=True)
class ShadowVerseAmulet:
    base_info: ShadowVerseCard
    effect: str
    flavor: str
    image_file_name: str

    def toDict(self) -> Dict[str, Union[str, int, Dict[str, Union[str, int]]]]:
        return {
            "base_info": self.base_info.toDict(),
            "card_type": "Amulet",
            "effect": self.effect,
            "flavor": self.flavor,
            "image_file_name": self.image_file_name
        }


if __name__ == "__main__":
    pass
