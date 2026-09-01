from unittest.mock import patch

from src import run_pipeline

def test_pipeline_calls_ingest_and_normalize():
    with patch("src.run_pipeline.ingest_data") as mock_ingest:
        with patch(
            "src.run_pipeline.normalize_champions"
        ) as mock_normalize:

            run_pipeline.main()

            mock_ingest.assert_called_once_with()
            mock_normalize.assert_called_once_with()
