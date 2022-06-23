from glob import glob
from typing import *
import pandas as pd
import stanza
from tqdm import tqdm
from latin_text import LatinText


def get_filenames() -> List[str]:
    folder = "../TheLatinLibraryScraper/data/texts/"
    filenames = [fp for fp in glob(folder + "*")]
    open_files = [open(fp) for fp in filenames]
    txts = [f.read() for f in open_files]
    for f in open_files:
        f.close()

    non_empty_files = [
        fp
        for fp, txt in zip(filenames, txts)
        if len(txt) > 100 and len(txt.split(" ")) < 100000
    ]
    non_bibles = [fp for fp in non_empty_files if "bible" not in fp]
    return non_bibles


def initialize_stanza() -> Any:
    nlp = stanza.Pipeline("la")
    return nlp


def ingest_text(filename: str, nlp: Any) -> Dict[str, Union[float, int]]:
    t = LatinText(filename, nlp)
    data = {
        "filename": filename,
        "token_dupl": round(t.percent_duplicate_tokens(), 4),
        "lemmas": round(t.num_lemmas(), 4),
        "lemma_dupl": t.percent_duplicate_lemmas(),
        "avg_forms_per_lemma": round(t.average_forms_per_lemma(), 4),
        "avg_sent_len": round(t.average_sentence_length(), 4),
        "unique_ft_clusts": round(t.num_unique_ft_clusters(), 4),
        "perc_dupl_ft_clusts": round(t.percent_duplicate_ft_clusters(), 4),
    }
    t = None
    return data


def build_table():
    filenames = get_filenames()
    nlp = initialize_stanza()

    all_data: List[Dict[str, Union[float, int]]] = []
    for fp in tqdm(filenames, desc="Ingesting files:"):
        try:
            d = ingest_text(fp, nlp)
            all_data.append(d)
        except:
            print("Failure with: ", fp)

    df = pd.DataFrame(all_data)
    df.to_csv("latinlibrarystats.csv")


build_table()
