from path_definition import scripts_dir
from smarts_tuples import get_smarts_tuples
import os, glob

class AcceptorCompetitionData(object):
    """Class to parse dataframe files and get competition data. Method to write to file for analysis of competition
    data"""
    
    def __init__(self, data_frame_path):
        
        self.data_frame_path = data_frame_path
        self.competition_tuples = []
        
    def competition_data(self):
        """parse dataframe and return competition data"""
        
        donor_functional_groups = [i.functional_Group for i in get_smarts_tuples()
                                   if i.Type == "Donor"] 
        os.chdir(self.data_frame_path)
        competition_data = []
        for tsv in glob.glob("*.tsv"):
            if tsv.replace(".tsv", "") in donor_functional_groups:
                continue
            with open(tsv, "r") as open_file:
                open_file_lines = open_file.readlines()
                for i in open_file_lines:
                    if i == "REFCODE\win\lose\n":
                        continue
                    elif i.split("\t")[1] in donor_functional_groups or i.split("\t")[2] in donor_functional_groups:
                        continue
                    elif i.split("\t")[1] == "Water" or i.split("\t")[2] == "Water":
                        continue
                    else:
                        competition_data.append((i.split("\t")[0], i.split("\t")[1], i.split("\t")[2].replace("\n","")))
        self.competition_tuples = list(set([tuple(sorted(i)) for i in competition_data]))
        return list(set([tuple(sorted(i)) for i in competition_data]))
                        
    def write_to_file(self):
        """write comeptition tuples to file"""
        
        #check first if self.competition_tuples has been set
        if len(self.competition_tuples) == 0:
            return None
        else:
            os.chdir(scripts_dir)
            os.chdir("../competition_data")
            write_file = open("acceptor_competition_data.txt", "w")
            for i in self.competition_tuples:
                write_file.write(i[0].strip("'") + "," + i[1].strip("'") + 
                                 "," + i[2].strip("'") + "\n")
            write_file.close()