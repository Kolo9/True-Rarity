from enum import Enum
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re
import sys
from collections import defaultdict
from heapq import heapify, heappush, heappop

from pandas.core import base

# normal: base item
# good: base item with suffix
# great: base item with prefix and sufix
# great+: Like great, but +1


class LootType(Enum):
    WEAPON = 1
    CHEST = 2
    HEAD = 3
    WAIST = 4
    FOOT = 5
    HAND = 6
    NECK = 7
    RING = 8


# TODO: Add loot type to rarity data.
LAST_ITEM_PER_LOOT_TYPE = {
    LootType.WEAPON: "Book",
    LootType.CHEST: "Ring Mail",
    LootType.HEAD: "Hood",
    LootType.WAIST: "Sash",
    LootType.FOOT: "Shoes",
    LootType.HAND: "Gloves",
    LootType.NECK: "Pendant",
    LootType.RING: "Titanium Ring",
}


def analyze_by_item_and_rarity(data):
    df = pd.DataFrame(
        columns=[
            "Base Item",
            "Normal Prob",
            "Good Prob (sfx)",
            "Great Prob (pfx+sfx)",
            "Great+ Prob (pfx+sfx+1)",
        ]
    )
    cur_loot_type = LootType(1)

    for base_item in data:
        normal_prob = 0
        good_prob = 0
        great_prob = 0
        great_plus_prob = 0
        for specific_item in data[base_item]:
            prob = data[base_item][specific_item]
            if specific_item.endswith("+1"):
                great_plus_prob += prob
            elif not specific_item.startswith(base_item):
                great_prob += prob
            elif " of " in specific_item:
                good_prob += prob
            else:
                normal_prob += prob
        df.loc[df.shape[0]] = [
            base_item,
            normal_prob,
            good_prob,
            great_prob,
            great_plus_prob,
        ]
        if base_item == LAST_ITEM_PER_LOOT_TYPE[cur_loot_type]:
            if cur_loot_type != LootType(len(LootType)):
                cur_loot_type = LootType(cur_loot_type.value + 1)
            figure = df.plot(
                x="Base Item",
                kind="bar",
                stacked=True,
                title="Tier probability distribution by item ({})".format(
                    cur_loot_type.name.lower()
                ),
                color=["grey", "green", "blue", "purple"],
            ).get_figure()
            plt.tight_layout()
            plt.legend(loc="lower right")
            figure.savefig(
                os.path.join(
                    sys.path[0],
                    "{}.png".format(cur_loot_type.name.lower()),
                )
            )
            # Clear the dataframe.
            df = df.iloc[0:0]
    # plt.show()


def analyze_rarest_items(data):
    prob_min_heap = []
    unique_probs = set()
    heapify(prob_min_heap)
    items_per_prob = defaultdict(lambda: [])

    for base_item in data:
        for specific_item in data[base_item]:
            prob = data[base_item][specific_item]
            items_per_prob[prob].append(specific_item)
            if prob not in unique_probs:
                heappush(prob_min_heap, prob)
                unique_probs.add(prob)
    item_count = 0
    while len(prob_min_heap):
        prob = heappop(prob_min_heap)
        print(
            "{} items expected to show up every {} bags".format(
                len(items_per_prob[prob]), int(1 / prob)
            )
        )
        item_count += len(items_per_prob[prob])
    print("total items: {}".format(item_count))


def find_item_sets(data):
    set_piece_count = defaultdict(lambda: set())
    cur_loot_type = LootType(1)
    for base_item in data:
        for specific_item in data[base_item]:
            if data[base_item][specific_item] > 0 and not specific_item.startswith(
                base_item
            ):
                match = re.match(r"^(\S+ \S+).*( of .*?( \+1)?)$", specific_item)
                set_piece_count[match.group(1) + match.group(2)].add(cur_loot_type)
        if base_item == LAST_ITEM_PER_LOOT_TYPE[cur_loot_type]:
            if cur_loot_type != LootType(len(LootType)):
                cur_loot_type = LootType(cur_loot_type.value + 1)

    possible_sets = sorted([k for (k, v) in set_piece_count.items() if len(v) == 8])
    with open(os.path.join(sys.path[0], "possible_sets.json"), "w") as f:
        json.dump(possible_sets, f, indent=4)
    print("Possible sets: {}".format(len(possible_sets)))


if __name__ == "__main__":
    with open("out/true_rarity_condensed.json", "r") as f:
        data = json.load(f)
    # analyze_by_item_and_rarity(data)
    # analyze_rarest_items(data)
    find_item_sets(data)
