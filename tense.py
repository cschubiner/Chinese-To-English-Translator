#!/usr/bin/python
import en
import sys

#print("Printing past tense of give")
#print(en.verb.past("give"))
#print(en.verb.present("give"))

# Enum class to track Chinese tense
def enum(**enums):
  return type('Enum', (), enums)
Tense = enum(Past=1, Present=2, Future=3)

## Main script ##
if len(sys.argv) != 3:
  print 'must have two arguments'
  sys.exit()

# Extract word
word = sys.argv[1]
targetTense = int(sys.argv[2])

# Convert based on tense
if targetTense == Tense.Past:
  print (en.verb.past(word))
elif targetTense == Tense.Future:
  print ("will " + en.verb.present(word))
else:
  print (en.verb.present(word))