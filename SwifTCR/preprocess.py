


def prepare(sequence_list,  min_len, max_len):
    from more_itertools import flatten

    sequence_list = flatten(sequence_list)
    
    if not isinstance(min_len, int) or min_len < 2:
        min_len = 2

    if not isinstance(max_len, int):
        return filter(lambda s: isinstance(s, str) and len(s) >= min_len, sequence_list)
    elif max_len <= min_len:
        return filter(lambda s: isinstance(s, str) and len(s) == min_len, sequence_list)
    else:
        return filter(lambda s: isinstance(s, str) and len(s) >= min_len and len(s) <= max_len, sequence_list)



def read_mixcr_cdr3(mixcr_file, colname='aaSeqCDR3', delim='\t'):
    import pandas as pd
    import os
    
    if os.path.exists(mixcr_file) and os.path.isfile(mixcr_file):
        df = pd.read_csv(mixcr_file, header=0, sep=delim)
        if colname in df.columns:
            return df[colname].tolist()
    
    return []


def cluster_mixcr_cdr3(input_data):
    import os

    if isinstance(input_data, str):
        if os.path.isfile(input_data):
            input_data = [input_data]
        elif os.path.isdir(input_data):
            input_data = [os.path.join(input_data, file) for file in os.listdir(input_data)]

    if isinstance(input_data, list):
        return [read_mixcr_cdr3(file_path) for file_path in input_data]
    
    return []