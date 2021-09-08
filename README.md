# True-Rarity
True per-item rarity for [Loot (For Adventurers)](https://etherscan.io/address/0xff9c1b15b16263c61d017ee9f65c50e4ae0113d7) and [More Loot A.K.A mLoot](https://etherscan.io/address/0x1dfe7Ca09e99d10835Bf73044a23B73Fc20623DF)

  * each `out/true_rarity_{item_type}.json` file contains probabilities for each item of that type, even if the item is impossible.
  * `out/true_rarity_condensed.json` contains probabilities for every *possible* item.

## Item probabilities by tier:
<img src="analysis/probability/weapon.png?raw=true" width="400"> <img src="analysis/probability/chest.png?raw=true" width="400">
<img src="analysis/probability/head.png?raw=true" width="400"> <img src="analysis/probability/waist.png?raw=true" width="400">
<img src="analysis/probability/foot.png?raw=true" width="400"> <img src="analysis/probability/hand.png?raw=true" width="400">
<img src="analysis/probability/neck.png?raw=true" width="400"> <img src="analysis/probability/ring.png?raw=true" width="400">

## Item counts by tier:
<img src="analysis/count/weapon.png?raw=true" width="400"> <img src="analysis/count/chest.png?raw=true" width="400">
<img src="analysis/count/head.png?raw=true" width="400"> <img src="analysis/count/waist.png?raw=true" width="400">
<img src="analysis/count/foot.png?raw=true" width="400"> <img src="analysis/count/hand.png?raw=true" width="400">
<img src="analysis/count/neck.png?raw=true" width="400"> <img src="analysis/count/ring.png?raw=true" width="400">

## Background & personal notes

### Rarity metrics
The community currently (2021-09-06) tends to judge bags based on a few different metrics, including:
  1. Rarity of individual items within the bag, where rarity is based on how many exist today
  2. Combined rarity of individual items within the bag, where rarity is based on how many exist today
  3. Combined `greatness` value of the items within the bag

1 and 2 are closely related, and the "true rarity" data in this repo is meant to complement those. Since mLoot is perpetually releasing new bags, an item that's rare today may not be that rare soon.  For example:
"Blight Peak Shoes of Perfection +1" are currently 1/1, but really are expected to come up every ~116k bags. It just so happened there was only 1 in the first 1.3m. Next will be in 1400184.  
**"True rarity" doesn't care about which mLoot bags are released today, and instead shows the actual rarity of each item, assuming infinite bags.**

This repo does not focus on any `greatness` calculations (3), because AFAIA, `greatness` is not directly used by any derivatives.

### Impossible items
Also, as demonstrated in the true rarity data, a huge number of items are simply impossible. As an example, it's impossible to have Divine Robe with +1 or even a prefix. This is due to the modular arithmetic in the original implementation.

Of 4,015,861 total items, only 72,229 (1.8%) are possible.
