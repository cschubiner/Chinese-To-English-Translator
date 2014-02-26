import math, collections

class StupidBackoffLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.bigramCounts = collections.defaultdict(lambda: 0)
    self.unigramCounts = collections.defaultdict(lambda: 0)
    self.bigramTotal = 0
    self.unigramTotal = 0

    self.startTok = '<s>'
    self.endTok = '<\s>'

    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model.
        Compute any counts or other corpus statistics in this function.
    """
    # TODO your code here
    # Tip: To get words from the corpus, try
    #    for sentence in corpus.corpus:
    #       for datum in sentence.data:
    #         word = datum.word
    for sentence in corpus.corpus:
      for i in range(1, len(sentence.data)):
        token1 = sentence.data[i-1].word if i > 0 else self.startTok
        token2 = sentence.data[i].word if i < len(sentence.data) else self.endTok
        key = (token1, token2)

        self.bigramCounts[key] = self.bigramCounts[key] + 1
        self.bigramTotal += 1

        self.unigramCounts[token2] = self.unigramCounts[token2] + 1
        self.unigramTotal += 1

      # Handle edge case for first unigram count
      fToken = sentence.data[0].word
      self.unigramCounts[fToken] = self.unigramCounts[fToken] + 1
      self.unigramTotal += 1

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the
        sentence using your language model. Use whatever data you computed in train() here.
    """
    # TODO your code here
    score = 0.0
    for i in range(1, len(sentence)):
      token1 = sentence[i-1] if i > 0 else self.startTok
      token2 = sentence[i] if i < len(sentence) else self.endTok
      bigram = (token1, token2)

      count = self.bigramCounts[bigram]
      if count > 0:
        # Stick with unsmoothed bigram cost if bigram count > 0
        score += math.log(count)
        score -= math.log(self.unigramCounts[token1])
      else:
        # Smoothing unigram cost
        count = self.unigramCounts[token2]
        numerator = count + 1
        denominator = self.unigramTotal + len(self.unigramCounts)

        score += math.log(float(0.4))
        score += math.log(numerator)
        score -= math.log(denominator)

    return score
