from SwifTCR.output import return_type
from preprocess import prepare, cluster_mixcr_cdr3
from itertools import combinations, count, groupby, repeat, starmap, chain
import operator


def hash_sort(sequences, substings_only):
    
    def skip_comb(string, full_string):
        comb = combinations(string, len(string)-1)
        comb = chain([tuple(string)], comb) if full_string else comb
        hash_comb = zip(map(hash, comb), count(-1), repeat(string))
        return hash_comb
    
    hash_key = map(lambda s: skip_comb(s, substings_only), sequences)
    return sorted(chain(*hash_key), key=lambda k:k[0]+k[1])

def hash_clsuter(sorted_keys, key_i):
    grouped = groupby(sorted_keys, key=operator.itemgetter(*key_i))
    return grouped

def deletion(hash_grouped):
    clusters, gap = [], None
    for p, c in groupby(hash_grouped, key=lambda k: k[1]):
        
        if p == -1:
            gap = set(c)
            continue
        elif gap:
            c = set(c).union(gap)
        else:
            c = set(c)
            
        if len(c)>1:
            clusters.append(c)

    return clusters

def get_clusters(string_list, minmax_size=(2, None), delete=False, mixcr=None, output=None):
    
    if mixcr:
        string_list = cluster_mixcr_cdr3(mixcr)
    
    string_list = prepare(string_list, *minmax_size)
    
    sub_keys = hash_sort(string_list, delete)
    
    if delete:
        clusters = hash_clsuter(sub_keys, [0])
        clusters = starmap(lambda h, g: deletion(g), clusters)
        clusters = chain(*clusters)
    else:
        clusters = hash_clsuter(sub_keys, [0, 1])
        clusters = starmap(lambda k, g: set(g), clusters)
        clusters = filter(lambda c: len(c)>1, clusters)
    
    clusters = [{s[-1] for s in c} for c in clusters]

    return return_type(clusters, output) if output else clusters

