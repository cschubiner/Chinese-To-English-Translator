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

# Extract phrase
phrase = str(sys.argv[1])
words = phrase.split()
targetTense = int(sys.argv[2])

# Convert based on tense
result = []
if targetTense == Tense.Future:
  result.append("will")
for word in words:
  try:
    if en.is_verb(word):
      if targetTense == Tense.Past:
        result.append(en.verb.past(word))
      else:
        result.append(en.verb.present(word))
    else:
      result.append(word)
  except:
    result.append(word)

# Return result
retVal = (' ').join(result)
print (retVal)