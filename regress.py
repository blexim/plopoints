#!/usr/bin/python

import hand, features
import numpy as np

def read_hands(ranking_file):
  handrankings = open(ranking_file)
  allfeatures = []

  for l in handrankings:
    l = l.strip()
    h = hand.Hand(l)
    feats = features.features(h)

    allfeatures.append(feats)

  handrankings.close()

  return allfeatures

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

def vectorize(featurelist):
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

def normalize(soln):
  maxcoeff = max(abs(x) for x in soln)
  mincoeff = min(abs(x) for x in soln if abs(x) != 0)

  return [int(x / mincoeff) - 1 for x in soln]

def print_rules(rules, revnames):
  coeffs = []

  for i in xrange(len(rules)):
    name = revnames[i]
    coeff = rules[i]

    if coeff != 0:
      coeffs.append((name, coeff))

  coeffs.sort()

  for (name, coeff) in coeffs:
    print "%s: %d" % (name, coeff)

if __name__ == '__main__':
  import sys

  print "Reading hand rankings..."
  rankings = read_hands(sys.argv[1])

  print "Vectorizing features..."
  (vects, names, revnames) = vectorize(rankings)

  print "Created %d vectors over %d features" % (len(vects), len(names))

  print "Creating matrix..."
  (A, y) = create_matrix(vects)

  print "Solving..."
  solution = solve(A, y)[0]

  rules = normalize(solution)
  print_rules(rules, revnames)


  print "Done!"
