import logging
from pathlib import Path

import hydra
from hydra.utils import instantiate
from omegaconf import DictConfig, OmegaConf

logger = logging.getLogger(__name__)


@hydra.main(config_path="config", config_name="config", version_base="1.2")
def main(config: DictConfig):
    logger.info(OmegaConf.to_yaml(config))

    output_path = Path(config.output_directory)

    relevance_dataset = instantiate(config.relevance_dataset)
    relevance_df = relevance_dataset.load()
    relevance_df.to_parquet(output_path / "relevance.parquet")

    query_ids = relevance_df.query_id.unique()
    click_dataset = instantiate(config.click_dataset, filter_query_ids=query_ids)
    df = click_dataset.load()
    df.to_parquet(output_path / "clicks.parquet")


if __name__ == "__main__":
    main()
