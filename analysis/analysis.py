import json
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import sys
from collections import defaultdict
from heapq import heapify, heappush, heappop

from pandas.core import base

# normal: base item
# good: base item with suffix
# great: base item with prefix and sufix
# great+: Like great, but +1


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
    item_types = [
        "weapon",
        "chest",
        "head",
        "waist",
        "foot",
        "hand",
        "neck",
        "ring",
    ]
    item_type_idx = 0

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
        if base_item in [
            "Book",
            "Ring Mail",
            "Hood",
            "Sash",
            "Shoes",
            "Gloves",
            "Pendant",
            "Titanium Ring",
        ]:
            item_type = item_types[item_type_idx]
            item_type_idx += 1
            figure = df.plot(
                x="Base Item",
                kind="bar",
                stacked=True,
                title="Tier probability distribution by item ({})".format(item_type),
                color=["grey", "green", "blue", "purple"],
            ).get_figure()
            plt.tight_layout()
            plt.legend(loc="lower right")
            figure.savefig(
                os.path.join(
                    sys.path[0],
                    "{}.png".format(item_type),
                )
            )
            # Clear the dataframe.
            df = df.iloc[0:0]
    # plt.show()


def analyze_rarest_items(data):
    prob_min_heap = []
    unique_probs = set()
    heapify(prob_min_heap)
    items_per_prob = defaultdict(lambda:[])

    for base_item in data:
        for specific_item in data[base_item]:
            prob = data[base_item][specific_item]
            items_per_prob[prob].append(specific_item)
            if prob not in unique_probs:
                heappush(prob_min_heap, prob)
                unique_probs.add(prob)
    while len(prob_min_heap):
        prob = heappop(prob_min_heap)
        print("1/{}: {}".format(int(1/prob), items_per_prob[prob]))


if __name__ == "__main__":
    with open("out/true_rarity_condensed.json", "r") as f:
        data = json.load(f)
    analyze_by_item_and_rarity(data)
    analyze_rarest_items(data)
