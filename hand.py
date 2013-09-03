#!/usr/bin/pypy

ranks = '23456789TJQKA'

def ridx(r):
  return ranks.index(r)

def idxr(idx):
  if idx <= 7:
    return '0%s' % ranks[idx]
  elif idx == 8:
    return '1T'
  elif idx == 9:
    return '2J'
  elif idx == 10:
    return '3Q'
  elif idx == 11:
    return '4K'
  elif idx == 12:
    return '5A'

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
