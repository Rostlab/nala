from collections import Counter

sample = 726
c = Counter({'no': 136, 'nl': 40, 'st': 12})

def stats(counter):
    num_nl_mut = counter['nl']
    num_mut = num_nl_mut + counter['st']
    total = counter['no'] + num_mut

    ratio_nl_muts_total = num_nl_mut / total
    ratio_muts_total = num_mut / total
    ratio_nl_muts_muts = num_nl_mut / num_mut

    print('%NL/total: {} -- %muts/total: {} --  %NL/muts: {}'.format(ratio_nl_muts_total, ratio_muts_total, ratio_nl_muts_muts))

stats(c)
