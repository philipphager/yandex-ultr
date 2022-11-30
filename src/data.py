import subprocess
from pathlib import Path
from typing import Union, Set, List

import pandas as pd
from tqdm import tqdm

QUERY_ACTION = "Q"
CLICK_ACTION = "C"


def unpack_query(session_id, time_passed, action_type, query_id, region_id, *doc_ids):
    return int(query_id), list(map(int, doc_ids))


def unpack_click(session_id, time_passed, action_type, doc_id):
    return int(doc_id)


def unpack_relevance(query_id, region_id, doc_id, relevance):
    return int(query_id), int(doc_id), int(relevance)


def count_lines(path: Path):
    return int(subprocess.check_output(["wc", "-l", path]).split()[0])


class YandexRelevanceDataset:
    def __init__(self, path: Union[Path, str]):
        self.path = Path(path)

    def load(self):
        assert self.path.exists(), f"File not found: {self.path}"
        rows = []

        with open(self.path, "r") as f:
            for line in f:
                values = line.rstrip().split("\t")
                query_id, doc_id, relevance = unpack_relevance(*values)

                row = {"query_id": query_id, "doc_id": doc_id, "relevance": relevance}
                rows.append(row)

        return pd.DataFrame(rows)


class YandexClickDataset:
    def __init__(
        self,
        path: Union[Path, str],
        filter_queries_without_relevance: bool,
        filter_query_ids: Union[Set, List] = [],
    ):
        self.path = Path(path)
        self.filter_queries_without_relevance = filter_queries_without_relevance
        self.filter_query_ids = set(filter_query_ids)

    def load(self):
        assert self.path.exists(), f"File not found: {self.path}"

        total_lines = count_lines(self.path)
        rows = []
        query_id = None

        with open(self.path, "r") as f:
            for line in tqdm(f, total=total_lines):
                values = line.rstrip().split("\t")

                if values[2] == QUERY_ACTION:
                    has_previous_query = query_id is not None
                    should_store_query = (
                        query_id in self.filter_query_ids
                        or not self.filter_queries_without_relevance
                    )

                    if has_previous_query and should_store_query:
                        click = [d in clicked_doc_ids for d in doc_ids]
                        row = {"query_id": query_id, "doc_ids": doc_ids, "click": click}
                        rows.append(row)

                    query_id, doc_ids = unpack_query(*values)
                    clicked_doc_ids = set()
                elif values[2] == CLICK_ACTION:
                    doc_id = unpack_click(*values)
                    clicked_doc_ids.add(doc_id)

        return pd.DataFrame(rows)
