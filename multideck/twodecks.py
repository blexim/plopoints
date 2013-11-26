#!/usr/bin/python

import scipy.misc

def choose(n, k):
  return scipy.misc.comb(n, k, exact=1)

def p(combos, cards):
  return float(combos) / float(choose(cards, 5))

def sf_52():
  return 10 * 4

def four_of_a_kind_52():
  return 13 * (52 - 4)

def boat_52():
  return (choose(4, 3) * 13) * (choose(4, 2) * 12)

def flush_52():
  return (4 * choose(13, 5)) - sf_52()

def straight_52():
  return 10 * ((4**5) - 4)

def trips_52():
  return (choose(4, 3) * 13) * (choose(12, 2) * 4**2)

def two_pair_52():
  return (choose(4, 2) * 13) * (choose(4, 2) * 12) * (52 - 8) / 2

def pair_52():
  return (choose(4, 2) * 13) * (choose(12, 3)) * 4**3

def hi_52():
  return (choose(52, 5) - pair_52() - two_pair_52() - trips_52() - straight_52() -
      flush_52() - boat_52() - four_of_a_kind_52() - sf_52())

combos_52 = [
    ("Straight flush", sf_52()),
    ("Four of a kind", four_of_a_kind_52()),
    ("Full house", boat_52()),
    ("Flush", flush_52()),
    ("Straight", straight_52()),
    ("Three of a kind", trips_52()),
    ("Two pair", two_pair_52()),
    ("Pair", pair_52()),
    ("High card", hi_52())
  ]

def summary_52():
  print "5 card hands, single deck:"

  for (desc, combos) in combos_52:
    print "%s: %d (%.04f%%)" % (desc, combos, 100 * p(combos, 52))

def five_of_a_kind_104():
  return 13 * (choose(8, 5))

def sf_104():
  return (10 * 4) * (2**5)

def four_of_a_kind_104():
  return 13 * (choose(8, 4)) * (104 - 8)

def boat_104():
  return (choose(8, 3) * 13) * (choose(8, 2) * 12)

def flush_104():
  return (4 * choose(26, 5)) - sf_104()

def straight_104():
  return 10 * (2**5) * ((4 ** 5) - 4)

def trips_104():
  return (choose(8, 3) * 13) * (104 - 8) * (104 - 16) / 2

def two_pair_104():
  return (choose(8, 2) * 13) * (choose(8, 2) * 12) * (104 - 16) / 2

def pair_104():
  return (choose(8, 2) * 13) * (choose(12, 3) * 2**3 * 4**3)

def hi_104():
  return (choose(104, 5) - pair_104() - two_pair_104() - trips_104() - straight_104() -
      flush_104() - boat_104() - four_of_a_kind_104() - sf_104() - five_of_a_kind_104())

combos_104 = [
    ("Five of a kind", five_of_a_kind_104()),
    ("Straight flush", sf_104()),
    ("Four of a kind", four_of_a_kind_104()),
    ("Full house", boat_104()),
    ("Flush", flush_104()),
    ("Straight", straight_104()),
    ("Three of a kind", trips_104()),
    ("Two pair", two_pair_104()),
    ("Pair", pair_104()),
    ("High card", hi_104())
  ]

def summary_104():
  print "5 card hands, 2 decks:"

  for (desc, combos) in combos_104:
    print "%s: %d (%.04f%%)" % (desc, combos, 100 * p(combos, 104))

if __name__ == '__main__':
  summary_52()
  print ""
  summary_104()
