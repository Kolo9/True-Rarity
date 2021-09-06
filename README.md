# True-Rarity
True per-item rarity for [Loot (For Adventurers)](https://etherscan.io/address/0xff9c1b15b16263c61d017ee9f65c50e4ae0113d7) and [More Loot A.K.A mLoot](https://etherscan.io/address/0x1dfe7Ca09e99d10835Bf73044a23B73Fc20623DF)

## Background & personal notes
The community currently (2021-09-06) tends to judge bags based on a few different metrics, including:
  1. Rarity of individual items within the bag, where rarity is based on how many exist today
  2. Combined rarity of individual items within the bag, where rarity is based on how many exist today
  3. Combined `greatness` value of the items within the bag

1 and 2 are closely related, and the "true rarity" data in this repo is meant to complement those. Since mLoot is perpetually releasing new bags, an item that's rare today may not be that rare soon.  For example:
"Blight Peak Shoes of Perfection +1" are currently 1/1, but really are expected to come up every ~116k bags. It just so happened there was only 1 in the first 1.3m. Next will be in 1400184.
"True rarity" doesn't care about which mLoot bags are released today, and instead shows that actual rarity of each item, assuming infinite bags.

This repo does not focus on any `greatness` calculations (3), because AFAIA, `greatness` is not directly used by any derivatives.

Also, as demonstrated in the true rarity data, a lot of items are simply impossible. As an example, it's impossible to have Divine Robe with +1 or even a prefix.
