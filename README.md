# Lexicon Classifier

Source code: https://github.com/draperunner/fjlc

This package is a Python port of the Lexicon Creator and Classifier of Valerij Fredriksen and Brage Ekroll Jahren (2016).
It is compatible with Python version >= 3.

The original Java code is available here: https://github.com/freva/Masteroppgave

If using this package in your publications, please cite
> Valerij Fredriksen and Brage Ekroll Jahren. Twitter Sentiment Analysis: Exploring Automatic Creation of Sentiment Lexica. Master's thesis, 2016.

## Installation
```bash
pip install fjlc
```

## Lexicon Classifier
The `LexiconClassifier` uses the best performing lexicon of Fredriksen and Jahren. You can specify your own lexicon, see Options below.

### Usage
```python
from fjlc import LexiconClassifier
lc = LexiconClassifier()
```

You can classify a single tweet or a list of tweets:
```
>>> lc.classify("I am happy!")
'POSITIVE'
>>> lc.classify(["I am happy!", "I hate rain"])
['POSITIVE', 'NEGATIVE']
```

You can get the sentiment value of a single tweet or multiple tweets
```
>>> lc.classify("I am happy!")
5.599244615570646
>>> lc.classify(["I am happy!", "I hate rain"])
[5.599244615570646, -2.767224666516315]
```

### Options
The `LexiconClassifier` takes three options:
* `lexicon`: Path to sentiment lexicon file
* `options`: Path to options file
* `dictionary`: Path to canonical dictionary

## Lexicon Creator
### Usage
```python
from fjlc import LexiconCreator
lc = LexiconCreator()
```
Incomplete, untested.
