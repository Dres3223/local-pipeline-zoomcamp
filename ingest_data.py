import sys
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm


def main():

    user = "root"
    password = "root"
    host = "pgdatabase"
    port = 5432
    db = "ny_taxi"
    table_name = "yellow_taxi_data"

    prefix = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/"
    file_url = prefix + "yellow_tripdata_2021-01.csv.gz"

    dtype = {
        "VendorID": "Int64",
        "passenger_count": "Int64",
        "trip_distance": "float64",
        "RatecodeID": "Int64",
        "store_and_fwd_flag": "string",
        "PULocationID": "Int64",
        "DOLocationID": "Int64",
        "payment_type": "Int64",
        "fare_amount": "float64",
        "extra": "float64",
        "mta_tax": "float64",
        "tip_amount": "float64",
        "tolls_amount": "float64",
        "improvement_surcharge": "float64",
        "total_amount": "float64",
        "congestion_surcharge": "float64"
    }

    parse_dates = [
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime"
    ]

    engine = create_engine(
        f"postgresql+psycopg://{user}:{password}@{host}:{port}/{db}"
    )

    print("Creating iterator...")

    df_iter = pd.read_csv(
        file_url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=100000
    )

    first_chunk = next(df_iter)

    print("Creating table...")

    first_chunk.head(0).to_sql(
        name=table_name,
        con=engine,
        if_exists="replace"
    )

    print("Inserting first chunk...")
    first_chunk.to_sql(
        name=table_name,
        con=engine,
        if_exists="append"
    )

    for df_chunk in tqdm(df_iter):
        df_chunk.to_sql(
            name=table_name,
            con=engine,
            if_exists="append"
        )

    print("Ingestion complete!")


if __name__ == "__main__":
    main()
