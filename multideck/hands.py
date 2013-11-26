#!/usr/bin/pypy

import random

CLUBS = 0
DIAMONDS = 1
HEARTS = 2
SPADES = 3

suits = [CLUBS, DIAMONDS, HEARTS, SPADES]

ACE = 0
TWO = 1
THREE = 2
FOUR = 3
FIVE = 4
SIX = 5
SEVEN = 6
EIGHT = 7
NINE = 8
TEN = 9
JACK = 10
QUEEN = 11
KING = 12
ACE_HI = 13

ranks = [ACE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN,
    JACK, QUEEN, KING]

NOTHING = 0
PAIR = 1
TWO_PAIR = 2
TRIPS = 3
STRAIGHT = 4
FLUSH = 5
BOAT = 6
FOUR_OF_A_KIND = 7
STRAIGHT_FLUSH = 8
FIVE_OF_A_KIND = 9

hand_types = [
    (NOTHING, "Nothing"),
    (PAIR, "Pair"),
    (TWO_PAIR, "Two pair"),
    (TRIPS, "Trips"),
    (STRAIGHT, "Straight"),
    (FLUSH, "Flush"),
    (BOAT, "Full house"),
    (FOUR_OF_A_KIND, "Four of a kind"),
    (STRAIGHT_FLUSH, "Straight flush"),
    (FIVE_OF_A_KIND, "Five of a kind")
  ]

def contains_five_of_a_kind(cards):
  hand_ranks = [r for (r, s) in cards]

  for rank in ranks:
    if hand_ranks.count(rank) >= 5:
      return True

  return False

def contains_straight_flush(cards):
  for suit in suits:
    suit_ranks = sorted(set(r for (r, s) in cards if s == suit))

    if ACE in suit_ranks:
      suit_ranks.append(ACE_HI)

    run = 1
    last = -9999

    for r in suit_ranks:
      if r == last+1:
        last = r
        run += 1

        if run >= 5:
          return True
      else:
        last = r
        run = 1

  return False

def contains_four_of_a_kind(cards):
  hand_ranks = [r for (r, s) in cards]

  for rank in ranks:
    if hand_ranks.count(rank) >= 4:
      return True

  return False

def contains_boat(cards):
  hand_ranks = [r for (r, s) in cards]
  got_trips = False
  got_pair = False

  for rank in ranks:
    if hand_ranks.count(rank) >= 3:
      if got_trips or got_pair:
        return True

      got_trips = True
    elif hand_ranks.count(rank) >= 2:
      if got_trips:
        return True

      got_pair = True


  return False

def contains_flush(cards):
  for suit in suits:
    suit_cnt = len([r for (r, s) in cards if s == suit])

    if suit_cnt >= 5:
      return True

  return False

def contains_straight(cards):
  ranks = sorted(set(r for (r, s) in cards))

  if ACE in ranks:
    ranks.append(ACE_HI)

  run = 1
  last = -9999

  for r in ranks:
    if r == last+1:
      last = r
      run += 1

      if run == 5:
        return True
    else:
      last = r
      run = 1

  return False

def contains_trips(cards):
  hand_ranks = [r for (r, s) in cards]

  for rank in ranks:
    if hand_ranks.count(rank) >= 3:
      return True

  return False

def contains_two_pair(cards):
  hand_ranks = [r for (r, s) in cards]
  pairs = 0

  for rank in ranks:
    if hand_ranks.count(rank) >= 2:
      pairs += 1

  return pairs >= 2

def contains_pair(cards):
  hand_ranks = [r for (r, s) in cards]

  for rank in ranks:
    if hand_ranks.count(rank) >= 2:
      return True

  return False

def best_hand(cards):
  if contains_five_of_a_kind(cards):
    return FIVE_OF_A_KIND
  elif contains_straight_flush(cards):
    return STRAIGHT_FLUSH
  elif contains_four_of_a_kind(cards):
    return FOUR_OF_A_KIND
  elif contains_boat(cards):
    return BOAT
  elif contains_flush(cards):
    return FLUSH
  elif contains_straight(cards):
    return STRAIGHT
  elif contains_trips(cards):
    return TRIPS
  elif contains_two_pair(cards):
    return TWO_PAIR
  elif contains_pair(cards):
    return PAIR
  else:
    return NOTHING

def decks(n):
  ret = []

  for r in ranks:
    for s in suits:
      ret.append((r, s))

  return ret*n

def histogram(num_cards, num_decks, trials):
  cnts = {}
  deck = decks(num_decks)

  for n in xrange(trials):
    cards = random.sample(deck, num_cards)
    best = best_hand(cards)

    if best not in cnts:
      cnts[best] = 1
    else:
      cnts[best] += 1

  print_histogram(cnts, trials)

def print_histogram(cnts, trials):
  for (ty, desc) in reversed(hand_types):
    if ty in cnts:
      cnt = cnts[ty]
      pct = (100.0 * cnt) / trials

      print "%s: %d (%.04f%%)" % (desc, cnt, pct)

if __name__ == '__main__':
  import sys

  num_cards = int(sys.argv[1])
  num_decks = int(sys.argv[2])
  num_trials = int(sys.argv[3])

  histogram(num_cards, num_decks, num_trials)
