import pandas as pd
from Bio import SeqIO
import glob
import re


def logfile(*args):
    if args[1]['rc'] != 'ok':
        with open('logfile.csv', 'a+') as f:
            line = str('\n' + f'{args[0]}, {args[1]["validation"]}')
            f.write(line)
    else:
        with open('logfile.csv', 'a+') as f:
            line = str('\n' + f'{args[0]}, success')
            f.write(line)


def check_file(fname):
    d = {}
    if 'collated' in fname[0]:
        d.update(collated=True)
    else:
        d.update(collated=False)
    try:
        for i in fname[0]:
            if re.search("\.csv$", i, flags=re.IGNORECASE):
                d["csv"] = i
            elif re.search("\.fa$", i, flags=re.IGNORECASE):
                d["fa"] = i
            else:
                pass
    except IndexError:
        print("File Error")
    return d


def read_files(args):
    data = check_file(args)
    if data['collated']:

        x = (pd.read_csv(data['csv'], index_col=0))
        x.rename({'CollectionDate': 'covv_collection_date'}, axis=1, inplace=True)
        x['covv_collection_date'] = pd.to_datetime(x['covv_collection_date'])
        x['covv_collection_date'] = x['covv_collection_date'].astype(str)
        x = (x.fillna('')).replace("NaT", '')
        d = x.apply(lambda x: x.to_dict(), axis=1)

    else:
        try:
            seq = {k.id: str(k.seq) for k in SeqIO.parse(data["fa"], "fasta")}

            df = pd.read_csv(data["csv"])
            df['covv_collection_date'] = pd.to_datetime(df['covv_collection_date'])
            df['covv_collection_date'] = df['covv_collection_date'].astype(str)

            metadata = df.apply(lambda x: x.to_dict(), axis=1)
            # noinspection PyStatementEffect
            {
                i.update({"covv_sequence": seq[k] for k in i.values() if k in seq})
                for i in metadata
            }

        except KeyError:
            print(f'{data["error"]} not found')

        except TypeError:
            print('file not found')

    return metadata


def collate_fa(kwargs):
    if kwargs['sub']:
        for file in glob.iglob('{}/**/*'.format(kwargs['fa'])):
            with open('collated_fasta', 'a+') as f:
                seq = {k.id: str(k.seq) for k in SeqIO.parse(file, "fasta")}
                f.write('\n' + seq)
    else:
        for file in glob.iglob('{}/*'.format(kwargs['fa'])):
            with open('collated_fasta.fa', 'a+') as f:
                seq = {k.id: str(k.seq) for k in SeqIO.parse(file, "fasta")}
                f.write('\n' + seq)

    seq = {k.id: str(k.seq) for k in SeqIO.parse('collated_fasta.fa', "fasta")}

    df = pd.read_csv(kwargs["csv"])
    df['covv_collection_date'] = pd.to_datetime(df['covv_collection_date'])
    df['covv_collection_date'] = df['covv_collection_date'].astype(str)

    metadata = df.apply(lambda x: x.to_dict(), axis=1)
    # noinspection PyStatementEffect
    {
        i.update({"covv_sequence": seq[k] for k in i.values() if k in seq})
        for i in metadata
    }
    return metadata
