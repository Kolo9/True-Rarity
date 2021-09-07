from collections import defaultdict
from enum import Enum
from sympy.ntheory.modular import crt
from sympy import lcm
import json


weapons = [
    "Warhammer",
    "Quarterstaff",
    "Maul",
    "Mace",
    "Club",
    "Katana",
    "Falchion",
    "Scimitar",
    "Long Sword",
    "Short Sword",
    "Ghost Wand",
    "Grave Wand",
    "Bone Wand",
    "Wand",
    "Grimoire",
    "Chronicle",
    "Tome",
    "Book",
]

chest_armor = [
    "Divine Robe",
    "Silk Robe",
    "Linen Robe",
    "Robe",
    "Shirt",
    "Demon Husk",
    "Dragonskin Armor",
    "Studded Leather Armor",
    "Hard Leather Armor",
    "Leather Armor",
    "Holy Chestplate",
    "Ornate Chestplate",
    "Plate Mail",
    "Chain Mail",
    "Ring Mail",
]

head_armor = [
    "Ancient Helm",
    "Ornate Helm",
    "Great Helm",
    "Full Helm",
    "Helm",
    "Demon Crown",
    "Dragon's Crown",
    "War Cap",
    "Leather Cap",
    "Cap",
    "Crown",
    "Divine Hood",
    "Silk Hood",
    "Linen Hood",
    "Hood",
]

waist_armor = [
    "Ornate Belt",
    "War Belt",
    "Plated Belt",
    "Mesh Belt",
    "Heavy Belt",
    "Demonhide Belt",
    "Dragonskin Belt",
    "Studded Leather Belt",
    "Hard Leather Belt",
    "Leather Belt",
    "Brightsilk Sash",
    "Silk Sash",
    "Wool Sash",
    "Linen Sash",
    "Sash",
]

foot_armor = [
    "Holy Greaves",
    "Ornate Greaves",
    "Greaves",
    "Chain Boots",
    "Heavy Boots",
    "Demonhide Boots",
    "Dragonskin Boots",
    "Studded Leather Boots",
    "Hard Leather Boots",
    "Leather Boots",
    "Divine Slippers",
    "Silk Slippers",
    "Wool Shoes",
    "Linen Shoes",
    "Shoes",
]

hand_armor = [
    "Holy Gauntlets",
    "Ornate Gauntlets",
    "Gauntlets",
    "Chain Gloves",
    "Heavy Gloves",
    "Demon's Hands",
    "Dragonskin Gloves",
    "Studded Leather Gloves",
    "Hard Leather Gloves",
    "Leather Gloves",
    "Divine Gloves",
    "Silk Gloves",
    "Wool Gloves",
    "Linen Gloves",
    "Gloves",
]

necklaces = ["Necklace", "Amulet", "Pendant"]

rings = ["Gold Ring", "Silver Ring", "Bronze Ring", "Platinum Ring", "Titanium Ring"]

suffixes = [
    "of Power",
    "of Giants",
    "of Titans",
    "of Skill",
    "of Perfection",
    "of Brilliance",
    "of Enlightenment",
    "of Protection",
    "of Anger",
    "of Rage",
    "of Fury",
    "of Vitriol",
    "of the Fox",
    "of Detection",
    "of Reflection",
    "of the Twins",
]

name_prefixes = [
    "Agony",
    "Apocalypse",
    "Armageddon",
    "Beast",
    "Behemoth",
    "Blight",
    "Blood",
    "Bramble",
    "Brimstone",
    "Brood",
    "Carrion",
    "Cataclysm",
    "Chimeric",
    "Corpse",
    "Corruption",
    "Damnation",
    "Death",
    "Demon",
    "Dire",
    "Dragon",
    "Dread",
    "Doom",
    "Dusk",
    "Eagle",
    "Empyrean",
    "Fate",
    "Foe",
    "Gale",
    "Ghoul",
    "Gloom",
    "Glyph",
    "Golem",
    "Grim",
    "Hate",
    "Havoc",
    "Honour",
    "Horror",
    "Hypnotic",
    "Kraken",
    "Loath",
    "Maelstrom",
    "Mind",
    "Miracle",
    "Morbid",
    "Oblivion",
    "Onslaught",
    "Pain",
    "Pandemonium",
    "Phoenix",
    "Plague",
    "Rage",
    "Rapture",
    "Rune",
    "Skull",
    "Sol",
    "Soul",
    "Sorrow",
    "Spirit",
    "Storm",
    "Tempest",
    "Torment",
    "Vengeance",
    "Victory",
    "Viper",
    "Vortex",
    "Woe",
    "Wrath",
    "Light's",
    "Shimmering",
]

name_suffixes = [
    "Bane",
    "Root",
    "Bite",
    "Song",
    "Roar",
    "Grasp",
    "Instrument",
    "Glow",
    "Bender",
    "Shadow",
    "Whisper",
    "Shout",
    "Growl",
    "Tear",
    "Peak",
    "Form",
    "Sun",
    "Moon",
]


# print(len(weapons))
# print(len(chest_armor))
# print(len(head_armor))
# print(len(waist_armor))
# print(len(foot_armor))
# print(len(hand_armor))
# print(len(rings))
# print(len(necklaces))

# print(len(suffixes))
# print(len(name_prefixes))
# print(len(name_suffixes))


class LootType(Enum):
    WEAPON = 1
    CHEST = 2
    HEAD = 3
    WAIST = 4
    FOOT = 5
    HAND = 6
    NECK = 7
    RING = 8


options_by_type = {
    LootType.WEAPON: weapons,
    LootType.CHEST: chest_armor,
    LootType.HEAD: head_armor,
    LootType.WAIST: waist_armor,
    LootType.FOOT: foot_armor,
    LootType.HAND: hand_armor,
    LootType.NECK: necklaces,
    LootType.RING: rings,
}


def optimal_crt(mods, remainders):
    """CRT that returns optimal result even if mods are not coprime.

    SymPy doesn't necessarily return the optimal solution if mods
    are not coprime.
    Example:
        crt([15, 21], [0, 0]) => (0, 315)
        crt([3, 5, 7], [0, 0, 0]) => (0, 105)

        optimal_crt([15, 21], [0, 0]) => (0, 105)
        optimal_crt([3, 5, 7], [0, 0, 0]) => (0, 105)
    """
    result = crt(mods, remainders)
    return (result[0], int(lcm(mods))) if result else None


def calc_true_rarity():
    true_rarity = {}
    for type in LootType:
        true_rarity[type] = {}
        for option in options_by_type[type]:
            true_rarity[type][option] = defaultdict(lambda: 0)

    for type in LootType:
        options = options_by_type[type]
        num_options = len(options)
        for option_idx in range(num_options):
            short_name = options[option_idx]
            for greatness in range(0, 15):
                full_name = short_name
                result = optimal_crt([num_options, 21], [option_idx, greatness])
                true_rarity[type][short_name][full_name] += (
                    1 / result[1] if result else 0
                )
            for greatness in range(15, 19):
                for suffix_idx in range(len(suffixes)):
                    full_name = "{option} {suffix}".format(
                        option=options[option_idx], suffix=suffixes[suffix_idx]
                    )
                    result = optimal_crt(
                        [num_options, 21, len(suffixes)],
                        [option_idx, greatness, suffix_idx],
                    )
                    true_rarity[type][short_name][full_name] += (
                        1 / result[1] if result else 0
                    )
            for greatness in range(19, 21):
                for suffix_idx in range(len(suffixes)):
                    for name_prefix_idx in range(len(name_prefixes)):
                        for name_suffix_idx in range(len(name_suffixes)):
                            full_name = (
                                "{name_prefix} {name_suffix} {name} {suffix}".format(
                                    name_prefix=name_prefixes[name_prefix_idx],
                                    name_suffix=name_suffixes[name_suffix_idx],
                                    name=options[option_idx],
                                    suffix=suffixes[suffix_idx],
                                )
                            )
                            if greatness == 20:
                                full_name += " +1"
                            result = optimal_crt(
                                [
                                    num_options,
                                    21,
                                    len(suffixes),
                                    len(name_prefixes),
                                    len(name_suffixes),
                                ],
                                [
                                    option_idx,
                                    greatness,
                                    suffix_idx,
                                    name_prefix_idx,
                                    name_suffix_idx,
                                ],
                            )
                            true_rarity[type][short_name][full_name] += (
                                1 / result[1] if result else 0
                            )
        with open(
            "out/true_rarity_{type}.json".format(type=type.name.lower()), "w"
        ) as f:
            json.dump(true_rarity[type], f, indent=4)

    true_rarity_condensed = {}
    for type in true_rarity:
        for short_name in true_rarity[type]:
            true_rarity_condensed[short_name] = {}
            for full_name in true_rarity[type][short_name]:
                if true_rarity[type][short_name][full_name]:
                    true_rarity_condensed[short_name][full_name] = true_rarity[type][
                        short_name
                    ][full_name]
    with open(
        "out/true_rarity_condensed.json".format(type=type.name.lower()), "w"
    ) as f:
        json.dump(true_rarity_condensed, f, indent=4)


if __name__ == "__main__":
    calc_true_rarity()

    # Verification per type: sum up probabiliies of all items per type
    # Expected: 1
    total_items = 0
    for type in LootType:
        with open(
            "out/true_rarity_{type}.json".format(type=type.name.lower()), "r"
        ) as f:
            data = json.load(f)
            total_probability = 0
            for full_name in data:
                for short_name in data[full_name]:
                    total_probability += data[full_name][short_name]
                    total_items += 1
            print(
                "{type}: {total_probability}".format(
                    type=type, total_probability=total_probability
                )
            )

    # Verification for condensed version: sum up probabiliies of all items
    # Expected: 8 (Since there are 8 items per bag)
    possible_items = 0
    with open("out/true_rarity_condensed.json", "r") as f:
        data = json.load(f)
        total_probability = 0
        for short_name in data:
            for full_name in data[full_name]:
                total_probability += data[short_name][full_name]
                possible_items += 1
        print(
            "condensed: {total_probability}".format(total_probability=total_probability)
        )
    print(
        "Total items: {total_items}\nPossible items: {possible_items}({possible_items_percent:.2f}%)".format(
            total_items=total_items,
            possible_items=possible_items,
            possible_items_percent=100 * possible_items / total_items,
        )
    )
