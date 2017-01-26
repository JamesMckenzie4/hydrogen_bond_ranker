import os
from collections import namedtuple
from path_definition import scripts_dir

def get_smarts_tuples():
    """opens smarts-patterns.txt and creates a named tuple for each functional group containing all H-bonding paramater information,
    heavy atom count etc. Returns a list of named tuples"""
    
    os.chdir(scripts_dir)
    os.chdir("../smarts_patterns")
    named_tuple_list = []
    open_file = open("smarts_patterns.txt", "r")
    smarts_named_tuple = namedtuple("SMARTS",'functional_Group smarts Type alpha alpha_stdev beta beta_stdev heavy_atoms number_of_donor_sites number_of_acceptor_sites acceptor_heavy_atom donor_heavy_atom')
    data = [i.split() for i in open_file.readlines()]
    for i in data:
        if "Functional_Group" in i:
            continue
        try:
            n_tup = smarts_named_tuple(i[0], i[1], i[2], i[3], i[4],
                                       i[5], i[6], i[7], i[8], i[9],
                                       i[10], i[11])
            named_tuple_list.append(n_tup)
        except IndexError:
            continue
    return named_tuple_list