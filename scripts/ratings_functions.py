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