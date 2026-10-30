import argparse
import pandas as pd

def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", default="output/charts.csv")
    parser.add_argument("-o", "--output", default="output/charts_clean.csv")
    args = parser.parse_args()

    raw = pd.read_csv(args.input, dtype=str)
    df = clean(raw)

if __name__ == "__main__":
    main()