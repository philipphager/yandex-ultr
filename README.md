# Yandex Relevance Prediction Parser
Parse and preprocess the Yandex relevance prediction dataset from the 2012 edition of the Web Search Click Data (WSCD) workshop series.

## Setup
1. Create conda environment: `conda env create -f environment.yaml`
2. Activate environment: `conda activate yandex-ultr`
3. Update configurations under: `config/config.yaml`
4. Run parser using: `python main.py`

## Statistics
Statistics for the subset of queries that also have relevance annotations:

### Click dataset
- \# of search queries: 37,469,405
- \# of unique search queries: 4,991
- \# of unique documents: 296,607
- \# of documents per query (min | median | max): 10 | 10 | 10

### Relevance dataset
- \# of unique queries: 4,991
- \# of unique documents: 39,949
- \# of documents per query (min | median | max): 1 | 7 | 90
