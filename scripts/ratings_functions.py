from path_definition import scripts_dir

def get_acceptor_competitions():
    """Parse data-frame files and get the competition data for acceptor ratings - write the data to file for analysis"""
    
    #get donor functional group tuples
    donor_functional_groups = [i.functional_Group for i in get_smarts_tuples() if i.Type == "Donor"]
    #change directory to database file
    os.chdir(scripts_dir)
    os.chdir("../database")
    #get competition data
    competition_data = []
    for tsv in glob.glob("*.tsv"):
        if tsv.replace(".tsv", "") in donor_functional_groups:
            continue
        open_file_lines = open(tsv, "r").readlines()
        for i in open_file_lines:
            if i == "REFCODE\win\lose\n":
                continue
            if i.split("\t")[1] in donor_functional_groups or i.split("\t")[2] in donor_functional_groups:
                continue
            else:
                comp_tuple = [(i.split("\t")[0], i.split("\t")[1], i.split("\t")[2].replace("\n",""))]
                competition_data.append(comp_tuple)
    #remove duplicate crystal structures
    new_comps = list(set([tuple(sorted(i)) for i in competition_data]))
    #change directory to competition data
    os.chdir("../competition_data")
    write_file = open("acceptor_competition_data.txt", "w")
    for i in new_comps:
        write_file.write(str(i[0][0]) + "," + str(i[0][1]).replace("'\n", "") + "," + str(i[0][2]).replace("'\n", "") + "\n")
    write_file.close()
    
def calculate_and_track_ratings(remove_outliers=None):
    """function to calculate and track the Elos, glickos and TrueSkills for H-bond acceptors"""
    
    #functional groups to remove from analysis
    to_remove = ["Pyrrole", "Indole"] 
    
    functional_groups = [i.functional_Group for i in get_smarts_tuples() if i.Type != "Donor"]
    fg_to_beta = {i.functional_Group: i.beta for i in get_smarts_tuples() if i.Type != "Donor"}

    #get_competition_data
    os.chdir(scripts_dir)
    os.chdir("../competition_data")

    #get competition_tuples list and shuffle them
    competition_tuples = [(i.split(",")[1].strip("'").replace("'\n",""),i.split(",")[2].strip("'").replace("'\n",""))
                          for i in open("acceptor_competition_data.txt").readlines() if
                          i.split(",")[1].strip("'").replace("'\n","") in functional_groups and
                          i.split(",")[2].strip("'").replace("'\n","") in functional_groups and
                          (i.split(",")[1].strip("'").replace("'\n","") != "Pyrrole" or
                          i.split(",")[2].strip("'").replace("'\n","") != "Indole")]
    
    #shuffle the competition data
    random.shuffle(competition_tuples)
    #get functional group numbers
    fg_to_nums = {}
    for fg in functional_groups:
        count = 0
        for tup in competition_tuples:
            if tup[0] == fg or tup[1] == fg:
                count += 1
        fg_to_nums.update({fg:count})
        
    #calculate ratings

    #get a dictionary of ratings objects and tracker for each functional group
    ratings_dict_skill = {i: Rating() for i in functional_groups}
    track_skill_dict = {i: [] for i in functional_groups}

    ratings_dict_elo = {i: elo.Rating() for i in functional_groups}
    track_elo_dict = {i: [] for i in functional_groups}

    ratings_dict_gli = {i: glicko2.Rating() for i in functional_groups}
    track_gli_dict = {i: [] for i in functional_groups}

    #calculate skills and trackers
    for tup in competition_tuples:
        if tup[0] == 'Acceptor_1':
            continue
        track_skill_dict[tup[0]].append(ratings_dict_skill[tup[0]])
        track_skill_dict[tup[1]].append(ratings_dict_skill[tup[1]])
        ratings_dict_skill[tup[0]], ratings_dict_skill[tup[1]] = rate_1vs1(ratings_dict_skill[tup[0]], ratings_dict_skill[tup[1]])

        track_elo_dict[tup[0]].append(ratings_dict_elo[tup[0]])
        track_elo_dict[tup[1]].append(ratings_dict_elo[tup[1]])
        ratings_dict_elo[tup[0]], ratings_dict_elo[tup[1]] = elo.rate_1vs1(ratings_dict_elo[tup[0]], ratings_dict_elo[tup[1]])

        track_gli_dict[tup[0]].append(ratings_dict_gli[tup[0]])
        track_gli_dict[tup[1]].append(ratings_dict_gli[tup[1]])
        ratings_dict_gli[tup[0]], ratings_dict_gli[tup[1]] = glicko2.Glicko2().rate_1vs1(ratings_dict_gli[tup[0]], ratings_dict_gli[tup[1]])

    return [(track_elo_dict, ratings_dict_elo), (track_gli_dict, ratings_dict_gli), (track_skill_dict, ratings_dict_skill), (fg_to_nums, fg_to_beta)]