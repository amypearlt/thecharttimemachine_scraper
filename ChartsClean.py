import argparse
from pathlib import Path
import pandas as pd

#Overrides incorrect genre columns, sourced from a manual reference of Discogs's database, which TCTM pulls their genre data from. Data imputation
GENRE_OVERRIDE = {"https://www.charttimemachine.com/?view=title&title_id=68255": ("Electronic", "House")} #1 song does not list a genre on its webpage

def parse_week(series: pd.Series) -> pd.Series:
    dates = pd.to_datetime(series.str.strip(), format="%m/%d/%y", errors="coerce")
    dates = dates.where(dates.dt.year < 2000, dates - pd.DateOffset(years=100)) #YY maps 00-68 to 2000-2068
    return dates

def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.drop(columns=["url", "song_url"], errors="ignore") #URLs are irrelevant to the data

    text_columns = df.select_dtypes(include=["object"]).columns
    for column in text_columns: #Removing leading, trailing and excess whitespace
        df[column] = df[column].str.strip().str.replace(r"\s+", " ", regex=True)
    df[text_columns] = df[text_columns].replace("", pd.NA) #Mark empty values

    df["position"] = pd.to_numeric(df["position"], errors="coerce").astype("Int64") #Type casting
    df["week"] = parse_week(df["week"])

    df = df.sort_values(["week", "position"]).reset_index(drop=True)
    return df

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", default="output/charts.csv")
    parser.add_argument("-o", "--output", default="output/charts_clean.csv")
    args = parser.parse_args()

    raw = pd.read_csv(args.input, dtype=str)
    df = clean(raw)

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.output, index=False)

if __name__ == "__main__":
    main()