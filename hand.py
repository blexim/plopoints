#!/usr/bin/pypy

ranks = '23456789TJQKA'

def ridx(r):
  return ranks.index(r)

def idxr(idx):
  return ranks[idx]

class Hand(object):
  cards = []

  def __init__(self, s):
    self.cards = self.parse(s)

  def parse(self, s):
    suited = False
    suit = 0
    ret = []

    for c in s:
      if c == '(':
        suited = True
      elif c == ')':
        suited = False
        suit += 1
      elif c in ranks:
        rank = ridx(c)
        card = (rank, suit)
        ret.append(card)

        if not suited:
          suit += 1
      else:
        break

    return ret
