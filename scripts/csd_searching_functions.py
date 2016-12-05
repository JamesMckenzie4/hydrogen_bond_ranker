from ccdc.search import SMARTSSubstructure, SubstructureSearch

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
  
