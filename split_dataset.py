import pandas as pd

import os
import argparse, sys

parser = argparse.ArgumentParser()

parser.add_argument('--csv', help='CSV File', type=str)
parser.add_argument('--train', help='Train indexes', type=str)
parser.add_argument('--dev', help='Dev indexes', type=str)
parser.add_argument('--output', help='Output Dir', type=str)
parser.add_argument('--tsv', help='Generates tsv instead', action='store_true')

args = parser.parse_args()


def split_and_save():
    df = pd.read_csv(filepath_or_buffer=args.csv)

    df = df.fillna({'review': ''})
    df = df[df['rating'] != 3]

    df['sentiment'] = df['rating'].apply(lambda rating: +1 if rating > 3 else -1)

    train_arr = pd.read_json(args.train)
    dev_arr = pd.read_json(args.dev)

    df_train: pd.DataFrame = df.iloc[train_arr[0]]
    df_dev: pd.DataFrame = df.iloc[dev_arr[0]]

    if not args.tsv:
        df_train.to_csv(path_or_buf=os.path.join(args.output, 'train.csv'))
        df_dev.to_csv(path_or_buf=os.path.join(args.output, 'dev.csv'))
    else:
        df_train_tsv = pd.DataFrame({
            'id': range(len(df_train)),
            'label': df_train['sentiment'],
            'alpha':['a']*df_train.shape[0],
            'text': df_train['review'].replace(r'\n',' ', regex=True)
        })

        df_dev_tsv = pd.DataFrame({
            'id': range(len(df_dev)),
            'label': df_dev['sentiment'],
            'alpha': ['a'] * df_dev.shape[0],
            'text': df_dev['review'].replace(r'\n', ' ', regex=True)
        })

        with pd.option_context('display.max_rows', None, 'display.max_columns', 10):
            print(df_train_tsv.iloc[:25])

        # return None

        df_train_tsv.to_csv(path_or_buf=os.path.join(args.output, 'train.tsv'), sep='\t', index=False, header=False)
        df_dev_tsv.to_csv(path_or_buf=os.path.join(args.output, 'dev.tsv'), sep='\t', index=False, header=False)


if __name__ == "__main__":
    if args.csv is None or not os.path.isfile(args.csv):
        raise FileNotFoundError

    if args.output is None or not os.path.isdir(args.output):
        print("--output is not specified or invalid. Using csv dir for output")

        args.output, _ = os.path.split(args.csv)

    if args.train is None or not os.path.isfile(args.train):
        raise FileNotFoundError

    if args.dev is None or not os.path.isfile(args.dev):
        raise FileNotFoundError

    split_and_save()
