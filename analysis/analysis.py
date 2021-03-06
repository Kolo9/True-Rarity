from enum import Enum
import json
import matplotlib.pyplot as plt
import os
import pandas as pd
import re
import sys
from collections import defaultdict
from heapq import heapify, heappush, heappop

plt.style.use("dark_background")

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


def analyze_by_item_and_tier(data):
    def plot(df, metric):
        ax = df.plot(
            x="Base Item",
            ylabel=metric.title(),
            kind="bar",
            stacked=True,
            title="Tier {} distribution by item ({})".format(
                metric.lower(), cur_loot_type.name.lower()
            ),
            color=["grey", "green", "blue", "purple"],
        )
        plt.tight_layout()
        # reverse legend order.
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::-1], labels[::-1], loc="lower right")
        ax.get_figure().savefig(
            os.path.join(
                sys.path[0],
                "{}/{}.png".format(metric.lower(), cur_loot_type.name.lower()),
            )
        )

    df_prob = pd.DataFrame(
        columns=[
            "Base Item",
            "Normal",
            "Good (sfx)",
            "Great (pfx+sfx)",
            "Great+ (pfx+sfx+1)",
        ]
    )
    df_count = pd.DataFrame(
        columns=[
            "Base Item",
            "Normal",
            "Good (sfx)",
            "Great (pfx+sfx)",
            "Great+ (pfx+sfx+1)",
        ]
    )
    cur_loot_type = LootType(1)

    for base_item in data:
        normal_prob = 0
        good_prob = 0
        great_prob = 0
        great_plus_prob = 0
        normal_count = 0
        good_count = 0
        great_count = 0
        great_plus_count = 0
        for specific_item, prob in data[base_item].items():
            if specific_item.endswith("+1"):
                great_plus_prob += prob
                great_plus_count += 1
            elif not specific_item.startswith(base_item):
                great_prob += prob
                great_count += 1
            elif " of " in specific_item:
                good_prob += prob
                good_count += 1
            else:
                normal_prob += prob
                normal_count += 1
        df_prob.loc[df_prob.shape[0]] = [
            base_item,
            normal_prob,
            good_prob,
            great_prob,
            great_plus_prob,
        ]
        df_count.loc[df_count.shape[0]] = [
            base_item,
            normal_count,
            good_count,
            great_count,
            great_plus_count,
        ]
        if base_item == LAST_ITEM_PER_LOOT_TYPE[cur_loot_type]:
            plot(df_prob, "probability")
            plot(df_count, "count")
            # Clear the dataframes.
            df_prob = df_prob.iloc[0:0]
            df_count = df_count.iloc[0:0]
            if cur_loot_type != LootType(len(LootType)):
                cur_loot_type = LootType(cur_loot_type.value + 1)


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
        for specific_item, prob in data[base_item].items():
            if prob > 0 and not specific_item.startswith(base_item):
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
    analyze_by_item_and_tier(data)
    analyze_rarest_items(data)
    find_item_sets(data)
