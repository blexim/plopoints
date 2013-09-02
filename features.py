#!/usr/bin/python

def suited(h):
  ret = []

  rank = None
  cnt = 0
  suit = -1
  flush3 = False
  flush4 = False

  for (r, s) in h.cards:
    if s == suit:
      cnt += 1
    else:
      cnt = 1
      suit = s
      rank = r

    if cnt == 2:
      ret.append('suited%d' % rank)
    elif cnt == 3:
      flush3 = True
    elif cnt == 4:
      flush4 = True

  if flush4:
    ret.append('4flush')
  elif flush3:
    ret.append('3flush')

  return ret
