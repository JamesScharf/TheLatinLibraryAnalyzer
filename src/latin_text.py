from collections import defaultdict
from typing import DefaultDict, Dict, List, Set
from statistics import mean


class LatinText(object):
    def __init__(self, filename: str, stanza_nlp):
        self.filename: str = filename
        self.text: str = None
        self.nlp = stanza_nlp
        self.annot_tokens = None
        self.load_file()

    def load_file(self):
        f = open(self.filename, "r")
        self.text = f.read()
        f.close()
        self.preprocess_text()

    def preprocess_text(self):
        self.doc = self.nlp(self.text)

    def annotated_tokens(self) -> List[str]:
        if self.annot_tokens == None:
            self.annot_tokens = [
                word for sent in self.doc.sentences for word in sent.words
            ]

        return self.annot_tokens

    def lemmatized_sentences(self) -> List[List[str]]:
        lem_sents: List[List[str]] = [[w.lemma for w in s] for s in self.doc.sentences]
        return lem_sents

    def percent_duplicate_tokens(self) -> float:
        # figure out how repetitive this text is by unique_tokens/all tokens

        annot_tokens = self.annotated_tokens()

        all_tokens = [w.text for w in annot_tokens]
        vocab = set(all_tokens)

        return len(vocab) / len(all_tokens)

    def num_lemmas(self) -> int:

        annot_tokens = self.annotated_tokens()
        all_lemmas = [w.lemma for w in annot_tokens]

        return len(all_lemmas)

    def percent_duplicate_lemmas(self) -> float:

        annot_tokens = self.annotated_tokens()
        all_lemmas = [w.lemma for w in annot_tokens]
        lemma_vocab = set(all_lemmas)

        return len(lemma_vocab) / len(all_lemmas)

    def average_forms_per_lemma(self) -> float:
        # for each lemma, count how many derivations there are in the text

        annot_tokens = self.annotated_tokens()
        lemma_derivs: DefaultDict[str, Set[str]] = defaultdict(set)

        for w in annot_tokens:
            w_txt = w.text
            w_lemma = w.lemma
            lemma_derivs[w_lemma].add(w_txt)

        num = sum([len(lemmas) for lemmas in lemma_derivs.values()])
        denom = len(lemma_derivs)
        m = num / denom
        return m

    def average_sentence_length(self) -> float:
        sentence_lengths: List[int] = []
        for s in self.doc.sentences:
            sent_len = len([w for w in s.words])
            sentence_lengths.append(sent_len)

        return mean(sentence_lengths)

    def num_unique_ft_clusters(self) -> int:
        # check how many different paradigm clusters are present
        annot_tokens = self.annotated_tokens()
        unique_clusters = set([w.feats for w in annot_tokens])
        return len(unique_clusters)

    def percent_duplicate_ft_clusters(self) -> float:
        # figure out how often ft clusters commonly occur
        annot_tokens = self.annotated_tokens()
        ft_clusters = [w.feats for w in annot_tokens]
        unique_clusters = set(ft_clusters)

        return len(unique_clusters) / len(ft_clusters)
