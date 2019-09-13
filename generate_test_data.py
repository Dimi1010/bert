import pandas as pd

import os
import argparse, sys

parser = argparse.ArgumentParser()

parser.add_argument('--csv', help='CSV File', type=str)
parser.add_argument('--output', help='Output Dir', type=str)

args = parser.parse_args()


def generate_test():
    df = pd.read_csv(filepath_or_buffer=args.csv)

    df = df.fillna({'review': ''})
    df = df[df['rating'] != 3]

    df['sentiment'] = df['rating'].apply(lambda rating: +1 if rating > 3 else -1)

    df_test_tsv = pd.DataFrame({
        'id': range(len(df)),
        'label': df['sentiment'],
        'alpha':['a']*df.shape[0],
        'text': df['review'].replace(r'\n',' ', regex=True)
    })

    with pd.option_context('display.max_rows', None, 'display.max_columns', 10):
        print(df_test_tsv.iloc[:25])

    df_test_tsv.to_csv(path_or_buf=os.path.join(args.output, 'test.tsv'), sep='\t', index=False, header=False)


if __name__ == "__main__":
    if args.csv is None or not os.path.isfile(args.csv):
        raise FileNotFoundError

    if args.output is None or not os.path.isdir(args.output):
        print("--output is not specified or invalid. Using csv dir for output")

        args.output, _ = os.path.split(args.csv)

    generate_test()
