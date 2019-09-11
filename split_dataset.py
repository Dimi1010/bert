import pandas as pd

import os
import argparse, sys

parser = argparse.ArgumentParser()

parser.add_argument('--csv', help='CSV File', type=str)
parser.add_argument('--train', help='Train indexes', type=str)
parser.add_argument('--test', help='Test indexes', type=str)
parser.add_argument('--tsv', help='Generates tsv instead', action='store_true')

args = parser.parse_args()


def split_and_save():
    df = pd.read_csv(filepath_or_buffer=args.csv)

    df = df.fillna({'review': ''})
    df = df[df['rating'] != 3]

    df['sentiment'] = df['rating'].apply(lambda rating: +1 if rating > 3 else -1)

    train_arr = pd.read_json(args.train)
    test_arr = pd.read_json(args.test)

    df_train: pd.DataFrame = df.iloc[train_arr[0]]
    df_test: pd.DataFrame = df.iloc[test_arr[0]]

    # with pd.option_context('display.max_rows', None, 'display.max_columns', 10):
    #    print(df_train.iloc[:5])
    #
    # return None

    path, _ = os.path.split(args.csv)

    if not args.tsv:
        df_train.to_csv(path_or_buf=os.path.join(path, 'train.csv'))
        df_test.to_csv(path_or_buf=os.path.join(path, 'test.csv'))
    else:
        df_train_tsv = pd.DataFrame({
            'id': range(len(df_train)),
            'label': df_train['sentiment'],
            'alpha':['a']*df_train.shape[0],
            'text': df_train['review'].replace(r'\n',' ', regex=True)
        })

        df_test_tsv = pd.DataFrame({
            'id': range(len(df_test)),
            'label': df_test['sentiment'],
            'alpha': ['a'] * df_test.shape[0],
            'text': df_test['review'].replace(r'\n', ' ', regex=True)
        })

        with pd.option_context('display.max_rows', None, 'display.max_columns', 10):
            print(df_train_tsv.iloc[:25])

        # return None

        df_train_tsv.to_csv(path_or_buf=os.path.join(path, 'train.tsv'), sep='\t', index=False, header=False)
        df_test_tsv.to_csv(path_or_buf=os.path.join(path, 'dev.tsv'), sep='\t', index=False, header=False)


if __name__ == "__main__":
    if args.csv is None or not os.path.isfile(args.csv):
        raise FileNotFoundError

    if args.train is None or not os.path.isfile(args.train):
        raise FileNotFoundError

    if args.test is None or not os.path.isfile(args.test):
        raise FileNotFoundError

    split_and_save()
