from ccdc.search import SMARTSSubstructure, SubstructureSearch
from collections import Counter

def searcher(smarts_string, number=100000):
    """search the CSD for structures containing a given smarts string. Uses sustructure_search.settings to specifiy search criteria.
    Default number of retieved structures = 100000"""
    
    substructure = SMARTSSubstructure(smarts_string)
    substructure_search = SubstructureSearch()
    substructure_search.add_substructure(substructure)
    substructure_search.settings.has_3d_coordinates = True
    substructure_search.settings.max_r_factor = 7.5
    substructure_search.settings.no_disorder = True
    substructure_search.settings.no_errors = True
    #substructure_search.settings.no_ions = True
    #substructure_search.settings.no_metals = True
    #substructure_search.settings.only_organic = True
    substructure_search.settings.max_hit_structures = number
    substructure_search.settings.max_hits_per_structure = 1
    substructure_search.settings.must_not_have_elements = ['B', 'Si', 'Ge', 'As', 'Sb', 'Te', 'At']
    hits = substructure_search.search()
    return hits

def remove_empty_crystals(crystal_object):
    """check if crystal structure has atomic co-oridinates - some are blank. Return None if so"""
   
    try:
        mol = crystal_object.molecule
    except TypeError:
        return None
    
def check_z_prime_value(crystal_object):
    """often crystal structures can have many components that are all the same molecule. This causes some problems in the functional group
    and H-bond detection. Return None if this is the case"""
    
    if len(crystal_object.molecule.components) > 1:
        smiles = set([i.smiles for i in crystal_object.molecule.components])
        if len(smiles) == 1:
            return None

def remove_intra(crystal_object):
    """check if structure contains an intrmolecular H-bond. If so return None"""
    
    hbonds = crystal_object.hbonds(intermolecular="intra", distance_range=(-5.0, 1.0), angle_tolerance=100.0, path_length_range=(3, 999))
    if len(hbonds) > 0:
        return None

def get_hbonds(crystal_object):
    """get the atom labels of the atoms involved in every H-bond in the crystal and return as a list. This functional can be modified 
    to change the definition of a H-bond, using the distance_range and angle_tolerance params, for future tests""" 
    
    h_bonds = []
    hbonds = crystal_object.hbonds(intermolecular="inter", distance_range=(-5.0, 0.0), angle_tolerance=110.00)
    #remove the ccdc label stuff
    for bond in hbonds:
        x = str(bond).replace("HBond(Atom(", "")
        x1 = x.replace("Atom","")
        x2 = x1.replace("(","")
        x3 = x2.replace(")","")
        h_bonds.append(x3.split("-"))
    return h_bonds

def get_functional_groups_in_structure(crystal_object):
    """Searches through the crystal structure for every substructure defined by a smarts-string in smarts-pattern.txt. Returns
    the number of each functional groups detected, a dictionary mapping each atom label to a smarts string, and a list of the 
    heavy atoms found in the crystal structure"""
    
    smarts_tuples = get_smarts_tuples()
    atoms_to_functional_group = {}
    fgs_in_mol = []
    atoms_in_smarts = []
    for smarts in smarts_tuples:
        #substructure search with smarts string
        smartsSubstructureSearch = search.SMARTSSubstructure(str(s_tuple.smarts))
        searcher = search.SubstructureSearch()
        searcher.add_substructure(smartsSubstructureSearch)
        hit = searcher.search(crystal_object)
        if hit:
            # get the atom labels for each instance of the smarts hit
            for h in hit:
                atoms_in_each_smarts = s_tuple.heavy_atoms.split(",")
                atoms_in_smarts.extend(atoms_in_each_smarts)
                fgs_in_mol.append(s_tuple.functional_Group)
                atom_list = h.match_atoms()
                #get rid of ccdc labels
                for atom in atom_list:
                    x = str(atom).replace("Atom","")
                    x1 = x.replace("(","")
                    x2 = x1.replace(")","")
                    atoms_to_functional_group.update({x2: s_tuple.functional_Group})            
    return dict(Counter(fgs_in_mol)), atoms_to_functional_group, atoms_in_smarts

def compare_heavy_atoms(crystal_object, atoms_in_smarts):
    """a function to compare the number of heavy atoms expected by smarts hits with the number of heavy atoms
    in the crystal structure, found using the API. If the numbers are the same return TRUE else False. The
    function takes the crystal object and the atoms_in_smarts list retrived from get_functional_groups()"""
    
    #get atoms in crystal object
    atoms = [str(atom.atomic_symbol) for atom in crystal_object.molecule.heavy_atoms]
    atoms_dict = dict(Counter(atoms))
    
    #count heavy atoms found in smarts strings
    oxygens = 0
    nitrogens = 0
    sulphurs = 0
    for a in atoms_in_smarts:
        if a == "None":
            continue
        if list(a)[0] == "O":
            oxygens += int(list(a)[1])
        if list(a)[0] == "N":
            nitrogens += int(list(a)[1])
        if list(a)[0] == "S":
            sulphurs += int(list(a)[1])
    #compare atoms in the crystal with atoms from the smarts strings. If they don't match return false
    try:
        if atoms_dict["O"] != oxygens:
            return False, "number of oxygens = " + repr(oxygens) + " expected " + repr(atoms_dict["O"])
    except KeyError:
        pass
    try:
        if atoms_dict["N"] != nitrogens:
            return False, "number of nitrogens = " + repr(nitrogens) + " expected " + repr(atoms_dict["N"])
    except KeyError:
        pass
    try:
        if atoms_dict["S"] != sulphurs:
            return False, "number of sulphurs = " + repr(sulphurs) +  " expected " + repr(atoms_dict["S"])
    except KeyError:
        pass
    return True

def identify_hbonds(hbond_list, atoms_to_smarts_dictionary):
    """takes the list of H-bonds in the crystal structure and the dictionary of atoms to smarts strings and works
    out which functional groups are involved in each hbond. Returns a list of tuples of structure 
    -[(donor functional group, acceptor functional group)]"""

    hbond_tuples = []
    for hbond in hbond_list:
        smarts_in_mol = []
        for atom in hbond:
            if "H" in list(atom):
                donor_smarts = atoms_to_smarts_dictionary[atom]
            else:
                smarts_in_mol.append(atoms_to_smarts_dictionary[atom])

        if smarts_in_mol.count(donor_smarts) == 2:
            #then every atom is from the same functional group
            hbond_tuples.append((donor_smarts,donor_smarts))
        else:
            #find the smarts of the functional group which is not the donor
            for smarts in smarts_in_mol:
                if smarts == donor_smarts:
                    continue
                hbond_tuples.append((donor_smarts,smarts))

    keys = Counter(hbond_tuples).keys()
    vals = Counter(hbond_tuples).values()
    h_bond_dict = {}
    for i in range(len(keys)):
        h_bond_dict.update({keys[i]: vals[i]})
    return h_bond_dict

def get_unused_acceptors(functional_group_numbers, Hbond_list):
    """compares a list of functional groups with a list of H-bonds to find out which acceptors have formed H-bonds
    and which have not"""
    
    unused_acceptors = []
    used_acceptors = []
    acceptors = [i.functional_Group for i in get_smarts_tuples() if i.Type != "Donor"]
    for functional_group in functional_group_numbers.keys():
        if functional_group not in acceptors:
            continue
        functional_group_is_used = 0
        for hbond in Hbond_list.keys():
            #print hbond
            if functional_group == hbond[1]:
                functional_group_is_used = 1
        #print functional_group_is_used
        if functional_group_is_used == 0:
            unused_acceptors.append(functional_group)
        else:
            used_acceptors.append(functional_group)
    return used_acceptors, unused_acceptors