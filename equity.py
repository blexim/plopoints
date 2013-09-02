#!/usr/bin/python

import subprocess
import os
import re
import tempfile
import hand

def hand2pql(h):
  suits = 'WXYZ'
  cards = []

  for (r, s) in h.cards:
    cards.append('%s%s' % (hand.idxr(r), suits[s]))

  return ''.join(cards)

def hands2pql(hands, f):
  for i in xrange(len(hands)):
    f.write("""
select avg(riverEquity(p1)) as EQ%d from game='omahahi', p1='%s', p2='*';
""" % (i, hand2pql(hands[i])))

def compute_equities(hands):
  f = tempfile.NamedTemporaryFile(delete=False)
  hands2pql(hands, f)
  f.flush()
  f.close()

  res = subprocess.check_output(
      "java -cp ../p3.jar propokertools.cli.RunPQL -mt 10000 -tc 8 -c < %s" % f.name,
      shell=True)

  os.unlink(f.name)

  return parse_equities(hands, res)

def parse_equities(hands, eqs):
  r = re.compile('EQ(\d+) = (.+)')
  ret = []

  for l in eqs:
    m = r.match(l)

    if m:
      (idx, eq) = m.groups()
      eq = float(eq)

      ret.append(hands[idx], eq)

  return ret

if __name__ == '__main__':
  import regress
  import sys
  import cPickle

  print "Reading hands..."
  hands = regress.read_hands(sys.argv[1])
  print "Read %d hands" % len(hands)

  print "Computing equities..."
  eqs = compute_equities(hands)

  print "Pickling..."
  pickled = open(sys.argv[2], 'wb')
  cPickle.dump(eqs, pickled)
  pickled.close()

  print "Done!"
