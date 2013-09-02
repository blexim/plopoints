#!/usr/bin/python

import hand, features
import numpy as np
import random

def read_hands(ranking_file):
  handrankings = open(ranking_file)
  hands = []

  for l in handrankings:
    l = l.strip()
    h = hand.Hand(l)
    hands.append(h)

  handrankings.close()

  return hands

def feature_names(featurelist):
  names = {}
  revnames = {}

  for feats in featurelist:
    for f in feats:
      if f not in names:
        idx = len(names)
        names[f] = idx
        revnames[idx] = f

  return (names, revnames)

def vectorize(hands):
  featurelist = [features.features(h) for h in hands]

  (names, revnames) = feature_names(featurelist)
  ret = []

  for feats in featurelist:
    row = [0] * len(names)

    for f in feats:
      idx = names[f]
      row[idx] += 1

    ret.append(row)

  return (ret, names, revnames)

def create_matrix(vectors):
  A = np.vstack(vectors)
  y = np.array(range(len(vectors), 0, -1))

  return (A, y)

def solve(A, y):
  return np.linalg.lstsq(A, y)

def normalize(soln, revnames):
  maxcoeff = max(abs(x) for x in soln)
  mincoeff = min(abs(x) for x in soln if abs(x) != 0)
  ret = {}

  for i in xrange(len(soln)):
    name = revnames[i]
    x = soln[i]
    ret[name] = int(x / mincoeff)

  return ret

def eval(rules, hand):
  score = 0

  for feat in features.features(hand):
    score += rules[feat]

  return score

def print_rules(rules):
  for (name, coeff) in sorted(rules.items()):
    if coeff != 0:
      print "%s: %d" % (name, coeff)

def check(rules, hands, numtrials=100000):
  correct = 0
  incorrect = 0
  total = 0

  for i in xrange(numtrials):
    idx1 = random.randint(0, len(hands) - 1)
    idx2 = random.randint(0, len(hands) - 1)

    h1 = hands[idx1]
    h2 = hands[idx2]

    score1 = eval(rules, h1)
    score2 = eval(rules, h2)

    if h1 <= h2 and score1 >= score2:
      correct += 1
    else:
      incorrect += 1

    total += 1.0

  frac = correct / total

  return (correct, total, frac*100)

def anneal(hands, maxcoeff=50, iterations=10000):
  (_, names, revnames) = vectorize(hands)
  rules = {}
  temp = maxcoeff*2
  iternum = 0
  checktrials = 1000

  for n in names:
    rules[n] = random.randint(-maxcoeff, maxcoeff)

  bestscore = 0
  best = rules

  while temp > 0:
    if iternum % (iterations / temp) == 0:
      temp = int(temp*0.8)
      print "Temperature: %d" % temp

    newrules = {}

    for n in names:
      coeff = rules[n] + random.randint(-temp, temp)
      coeff = max(coeff, -maxcoeff)
      coeff = min(coeff, maxcoeff)

      newrules[n] = coeff

    score = check(newrules, hands, checktrials)[0]

    if score > bestscore:
      print "New best: %d" % score
      iternum = 0

      bestscore = score
      best = newrules

    rules = newrules
    iternum += 1

  return best

if __name__ == '__main__':
  import sys

  print "Reading hand rankings..."
  rankings = read_hands(sys.argv[1])

  doanneal = False

  if doanneal:
    print "Annealing..."
    rules = anneal(rankings)
  else:
    print "Vectorizing features..."
    (vects, names, revnames) = vectorize(rankings)

    print "Created %d vectors over %d features" % (len(vects), len(names))

    print "Creating matrix..."
    (A, y) = create_matrix(vects)

    print "Solving..."
    solution = solve(A, y)[0]

    rules = normalize(solution, revnames)

  print_rules(rules)

  print "Checking..."
  (correct, total, perc) = check(rules, rankings)


  print "%d/%d correct (%.02f%%)" % (correct, total, perc)

  if len(sys.argv) > 2:
    h = hand.Hand(sys.argv[2])

    print "Hand score: %d" % eval(rules, h)

  print "Done!"
