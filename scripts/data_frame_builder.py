import os, glob
from csd_searching_functions import *
from smarts_tuples import get_smarts_tuples

#get list of smarts tuples
sma_list = get_smarts_tuples()
#get current directory
cwd = os.getcwd()

for sma in sma_list:
    #Check if files are already in the database directory - allows the program to continue after a potential crash
    os.chdir("../database") 
    obtained_files = [i.replace(".tsv", "") for i in glob.glob("*.tsv")]
    if sma.functional_Group in obtained_files:
        continue
    #create write files
    data_tsv_file = open(functional_group_name + ".tsv","w")
    data_tsv_file.write("REFCODE\tH_Bonds\tFunctional_Groups\tUsed_acceptors\tUnused_acceptors" + "\n")
    #retrieve hits from the CSD
    hits = searcher(smarts, number=100000)
    if hits is None:
        continue
    #run checks on each crystal, add missing hydrogen atoms and get h-bonds
    for retrieved_structure in hits:
        crystal = retrieved_structure.crystal
        if remove_empty_crystal(crystal) == None:
            continue
        if check_z_prime_value(crystal) == None:
            continue
        if remove_riff_raff(crystal) == None:
            continue
        if remove_intra(crystal) == None:
            continue
        try:
            crystal = add_missing_H_atoms(crystal)
        except RuntimeError:
            continue
        if crystal is None:
            continue
        #get list of Hbonds
        try:
            hbond_list = get_hbonds(crystal)
            if len(hbond_list) == 0:
                continue
        except RuntimeError:
            continue
        #get all the functional groups in each crystal
        try:
            functional_group_numbers, functional_group_dictionary, atoms_in_smarts = get_functional_groups_in_structure(crystal)
        except TypeError:
            continue
        if len(atoms_in_smarts) == 0:
            continue
        ref = crystal.identifier
        #compare heavy atoms
        if compare_heavy_atoms(crystal, atoms_in_smarts) is False:
            continue
        #identify which functional groups are involved in each H-bond
        try:
            hbonds = identify_hbonds(hbond_list, functional_group_dictionary)
        except KeyError:
            continue
        #get the used and unused H-bond acceptors
        used, unused = get_unused_acceptors(functional_group_numbers, hbonds)
        #write to tsv file
        data_tsv_file.write(repr(ref) + "\t" + repr(hbonds) + "\t" + repr(functional_group_numbers) + "\t" + repr(used) +
                            "\t" + repr(unused) + "\n")
    data_tsv_file.close()