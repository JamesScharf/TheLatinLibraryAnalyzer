# TheLatinLibraryAnalyzer

The following project was an attempt to describe, in quantitative terms, which text in [The Latin Library](https://www.thelatinlibrary.com/) is the "easiest."

## Motivation

A beginner in the Latin language understandably wants to read authentic texts as soon as possible. The traditional texts that one might start with are surprisingly difficult. Personally, I found that my (extremely) rusty skills were simply inadaquate for translating something like Caesar's Gallic Wars.

This raises the question: Which text *should* a beginner translate first? I sought to answer this question in a quantitative, yet totally unscientific way.

## Methods/Tools

I constructed several distinct measures which could, individually, be indicative of a text's difficulty:
1. Token duplication percentage: A higher rate of duplication means that a user can memorize fewer words.
2. Lemma duplication percentage: Similar to method #1, but perhaps more appropriate for such a morphologically rich language as Latin.
3. Average forms per lemma: For each lemma, count how many derivations there are and take the average. A text with many derivations of a lemma requires that the learner have a larger personal inventory of grammatical structures.
4. Average sentence length
5. Feature cluster duplication: A text with high duplication of any given morphological cluster means that the user can memorize fewer morphological features and still translate a text.

I should be _stressed_ that these measures are **not at all** disjoint.

I used the wonderful [Stanza](https://stanfordnlp.github.io/stanza/) toolkit to obtain morphological features and token lemmas.

To combine all of these methods, I [scaled](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html) the data and then added them together with subjective weights to create an "ease index". A higher ease index score *should* mean that a text is easier to translate.

You can see this list in the analysis.ipynb Jupyter Notebook.

## Data

The project assumes that you have downloaded my other repo, TheLatinLibraryScraper, and placed it in the same parent directory as the TheLatinLibraryAnalyzer. The scraper is unfortunately imperfect; it scraped several webpages that serve as hubs for multiple texts by the same author.