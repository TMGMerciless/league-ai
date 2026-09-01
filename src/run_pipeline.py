from src.data_ingest import main as ingest_data
from src.normalize_champions import main as normalize_champions


def main():
    print("Starting League AI data pipeline...")

    ingest_data()
    normalize_champions()

    print("League AI data pipeline complete.")


if __name__ == "__main__":
    main()
