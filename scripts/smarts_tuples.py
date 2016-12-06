from collections import namedtuple
import os

def get_smarts_tuples():
    """opens smarts-patterns.txt and gets all the relevant information into a list of named tuples"""
    
    #go to smarts patters directory - problems on linux machine with this
    os.chdir(r"C:\Users\Helen\Documents\James\hydrogen_bonds\smarts_patterns")
    #get data into named tuples
    named_tuple_list = []
    open_file = open("smarts-pattern.txt", "r")
    smarts_named_tuple = namedtuple("SMARTS", 'functional_Group smarts Type alpha alpha_stdev beta beta_stdev heavy_atoms number_of_donor_sites number_of_acceptor_sites acceptor_heavy_atom donor_heavy_atom')
    #parse file
    data = [i.split() for i in f.readlines()]
    for i in data:
        if "Functional_Group" in i:
            continue
        try:
            y = smartsNamedTuple(i[0], i[1], i[2], i[3], i[4], i[5], i[6],
                                 i[7], i[8], i[9], i[10], i[11])
            named_tuple_list.append(y)
        except IndexError:
            continue
    return named_tuple_list