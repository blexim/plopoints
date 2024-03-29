#!/usr/bin/pypy

import hand

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
      ret.append('suited_%s' % hand.idxr(rank))
    elif cnt == 3:
      flush3 = True
    elif cnt == 4:
      flush4 = True

  if flush4:
    ret.append('4flush')
  elif flush3:
    ret.append('3flush')

  return ret

def pairs(h):
  ret = []

  ranks = {}
  numpairs = 0

  for (r, _) in h.cards:
    if r in ranks:
      ranks[r] += 1
    else:
      ranks[r] = 1

  for (r, cnt) in ranks.items():
    if cnt > 1:
      ret.append('pair_%s' % hand.idxr(r))
      numpairs += 1

    if cnt == 3:
      ret.append('trips')

    if cnt == 4:
      ret.append('quads')

  if numpairs == 2:
    ret.append('double_pair')

  return ret

def connected(h):
  ret = []

  ranks = sorted(set(r for (r, _) in h.cards), reverse=True)

  if hand.ridx('A') in ranks:
    ranks.append(-1)

  bestrundown = (-1, -1, -1, -1)

  for i in xrange(len(ranks)):
    gaps = []
    lastrank = ranks[i]
    cnt = 1
    hi = ranks[i]

    for r in ranks[i+1:]:
      gap = lastrank - r - 1

      if gap + len(gaps) > 3:
        break

      gaps += range(hi - lastrank + 1, hi - r)
      cnt += 1
      lastrank = r

    rundown = (cnt, hi, gaps)

    if rundown > bestrundown:
      bestrundown = rundown

  (cnt, hi, gaps) = bestrundown

  if cnt >= 2:
    ret.append('rundown_%dcards_%shi' % (cnt, hand.idxr(hi)))
    #ret.append('rundown_%dcards' % cnt)

    #ret.append('rundown_hi_%s' % hand.idxr(hi))

    for g in gaps:
      ret.append('rundown_gap_%d' % g)

    #ret.append('rundown_gaps_%d' % len(gaps))

    #ret.append('rundown_%dcards_%dgaps' % (cnt, len(gaps)))

  return ret

def rankstrength(h):
  ret = []

  ranks = set(r for (r, _) in h.cards)

  for r in ranks:
    ret.append('rank_%s' % hand.idxr(r))

  return ret


def features(h):
  return suited(h) + pairs(h) + connected(h) + rankstrength(h)
