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
  
