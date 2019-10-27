import __future__

import os
import glob
import sys

import numpy as np
import matplotlib as matplotlib
# matplotlib.use('agg')
import matplotlib.pyplot as plt

def get_usable_fomat(infile):
    """
    This code takes a string for an file which is formated as an .smi file.
    It opens the file and reads in the components into a usable list.

    The .smi must follow the following format for each line:
        MANDATORY INFO
            part 1 is the SMILES string
            part 2 is the SMILES name/ID

        Optional info
            part -1 (the last piece of info) is the SMILES diversity score relative to its population
            part -2 (the second to last piece of info) is the fitness metric for evaluating
                        - For default setting this is the Docking score
                        - If you add a unique scoring function Docking score should be -3 and that score function should be -2

            Any other information MUST be between part 2 and part -2 (this allows for the 
                expansion of features without disrupting the rest of the code)

    Input:
    :param str infile: the string of the PATHname of a formatted .smi file to be read into the program
    Return:
    :returns: list usable_list_of_smiles: list of SMILES and their associated information formated into a list
                                    which is usable by the rest of Autogrow
    """   
    # IMPORT SMILES FROM THE PREVIOUS GENERATION  
    usable_list_of_smiles = []
    with open(infile) as smiles_file:
        for line in smiles_file:
            line = line.replace("\n","")
            parts = line.split('\t')      # split line into parts seperated by 4-spaces

            choice_list = []
            for i in range(0,len(parts)):
                choice_list.append(parts[i])
            usable_list_of_smiles.append(choice_list)

    return usable_list_of_smiles

def get_average_score_per_gen(infolder, folder_list):
    """
    This script will get the average docking score from the ranked .smi file from each generation.

    Input:
    :param str infolder: the path of the folder which has all of the generation folders
    :param list folder_list: a list of generation folders for each generation within infolder
    Return:
    :returns: list usable_list_of_smiles: list of SMILES and their associated information formated into a list
                                    which is usable by the rest of Autogrow
    """ 

    average_affinity_dict = {}
    for gen_folder in folder_list:
        gen_folder_name = infolder + gen_folder + "/"
        ranked_file = glob.glob(gen_folder_name + "*_ranked.smi")

        for rank_file in ranked_file:
            # write as a tab delineated .smi file
            with open(rank_file, 'r') as f:
                gen_affinity_sum = float(0.0)
                num_lines_counter = float(0.0)
                for line in f:
                    line = line.replace("\n","")
                    parts = line.split('\t')      # split line into parts seperated by 4-spaces

                    choice_list = []
                    for i in range(0,len(parts)):
                        choice_list.append(parts[i])

                    
                    gen_affinity_sum = gen_affinity_sum + float(choice_list[-2])
                    num_lines_counter = num_lines_counter + float(1.0)


            gen_affinity_average = gen_affinity_sum/num_lines_counter
            
            gen_num = os.path.basename(rank_file).split("_")[1]
            gen_name = "generation_{}".format(gen_num)
            average_affinity_dict[gen_name] = gen_affinity_average

    print_gens(average_affinity_dict)
    return average_affinity_dict

def get_average_top_score_per_gen(infolder, folder_list, top_score_per_gen):
    """
    This script will get the average docking score of the top N number of ligands 
     ranked .smi file from each generation.

    Input:
    :param str infolder: the path of the folder which has all of the generation folders
    :param list folder_list: a list of generation folders for each generation within infolder
    :param int top_score_per_gen: the number of ligands to determine the average score.
                ie) if top_score_per_gen=50 it will return the average of the top 50 scores.
    Return:
    :returns: dict average_affinity_dict: dictionary of average affinity scores for top_score_per_gen number of ligands
    """ 
    average_affinity_dict = {}

    for gen_folder in folder_list:
        gen_folder_name = infolder + gen_folder + "/"
        ranked_file = glob.glob(gen_folder_name + "*_ranked.smi")

        for rank_file in ranked_file:
            # Check number of lines
            num_lines=0 
            with open(rank_file,'r') as rf:
                for line in rf:
                    num_lines=num_lines+1
       
            if num_lines >= top_score_per_gen:
                # read as a tab delineated .smi file
                with open(rank_file, 'r') as f:
                    gen_affinity_sum = float(0.0)
            
                    for i,line in enumerate(f.readlines()):
                        if i >= top_score_per_gen:
                            break
                        line = line.replace("\n","")
                        parts = line.split('\t')      # split line into parts seperated by 4-spaces

                        choice_list = []
                        for i in range(0,len(parts)):
                            choice_list.append(parts[i])

                        gen_affinity_sum = gen_affinity_sum + float(choice_list[-2])
                        
                    gen_affinity_average = gen_affinity_sum/top_score_per_gen

                    gen_num = os.path.basename(rank_file).split("_")[1]
                    gen_name = "generation_{}".format(gen_num)
                    average_affinity_dict[gen_name] = gen_affinity_average

            else:
                gen_num = os.path.basename(rank_file).split("_")[1]
                gen_name = "generation_{}".format(gen_num)
                average_affinity_dict[gen_name] = "N/A"

    print_gens(average_affinity_dict)
    return average_affinity_dict

def print_gens(average_affinity_dict):
    """
    This prints out the average scores for each generation

    Input:
    :param dict average_affinity_dict: dictionary of average affinity scores for top_score_per_gen number of ligands
    """ 
    print("generation_number              average affinity score")
    affinity_keys = list(average_affinity_dict.keys())
    affinity_keys.sort(key=lambda x: int(x.split('_')[1]))
    for gen in affinity_keys:
        print(gen,"                  ",average_affinity_dict[gen])

def make_graph(dictionary):
    """
    Because some generations may not have 50 ligands this basically checks to see if 
    theres enough ligands and prepares lists to be plotted
    
    Input:
    :param dict dictionary: dictionary of average affinity scores for top_score_per_gen number of ligands
    Return:
    :returns: list list_generations: list of ints for each generation to be plotted.
        if a generation lacks ligands to generate the average it will return "N/A"
    :returns: list list_of_scores: list of averages for each generation; 
        if a generation lacks ligands to generate the average it will return "N/A"
    """ 
    list_generations = []
    list_of_gen_names = []
    list_of_scores = []
    #print(dictionary)

    for key in dictionary.keys():
        #print(key)
        list_of_gen_names.append(key)    

        score = dictionary[key]
        list_of_scores.append(score)

        gen = key.replace("generation_","")

        gen = int(gen)
        list_generations.append(gen)
        list_of_gen_names.append(key)    

    enough=True
    for i in list_of_scores:
        if i is "N/A":
            enough=False
            return None, None
    else:
        return list_generations, list_of_scores

def run_plotter(vars, dict_of_averages, outfile):
    """
    This plots the averages into a matplotlib figure. 
    It will require you to answer questions about titles and labels

    Inputs:
    :param dict vars: dict of user variables which will govern how the programs runs
    :param dict dict_of_averages: a dictionary of dictionaries containing the average of each generation for the top 50,20, 10, and 1 ligand(s)
                    and the overall average for each generation.
    :param str outfile: Path for the output file for the plot
    """
    
    average_affinity_dict = dict_of_averages["average_affinity_dict"]
    top_fifty_dict = dict_of_averages["top_fifty_dict"]
    top_twenty_dict = dict_of_averages["top_twenty_dict"]
    top_ten_dict = dict_of_averages["top_ten_dict"]
    top_one_dict = dict_of_averages["top_one_dict"]

    # print("Graphing Overall Average")
    list_generations_Average, list_of_scores_Average = make_graph(average_affinity_dict)
    # print("Graphing top_fifty_dict")
    print_fifty=True
    for key in top_fifty_dict.keys():
        if top_fifty_dict[key] == "N/A":
            print_fifty=False
    if print_fifty==True:
        list_generations_Fifty, list_of_scores_Fifty = make_graph(top_fifty_dict)
    # print("Graphing top_fifty_dict")
    print_twenty=True
    for key in top_twenty_dict.keys():
        if top_twenty_dict[key] == "N/A":
            print_twenty=False
    if print_twenty==True:
        list_generations_Twenty, list_of_scores_Twenty = make_graph(top_twenty_dict)

    # print("Graphing top_ten_dict")
    list_generations_Ten, list_of_scores_Ten = make_graph(top_ten_dict)
    # print("Graphing top_one_dict")
    list_generations_one, list_of_scores_one = make_graph(top_one_dict)
    # print("")

    ax = plt.subplot(111)

    ax.plot(list_generations_Average, list_of_scores_Average, color='b', label="Average")
    if print_fifty==True:
        ax.plot(list_generations_Fifty, list_of_scores_Fifty, color='c', label="Top 50")

    if print_twenty==True:
        ax.plot(list_generations_Twenty, list_of_scores_Twenty, color='m', label="Top 20")
    ax.plot(list_generations_Ten, list_of_scores_Ten, color='g', label="Top 10")
    ax.plot(list_generations_one, list_of_scores_one, color='r', label="Top 1")

    #Niraparib has a docking score of -10.7 
    #Olaparib has a docking score of -12.2
    ax.axhline(y=-9.3, color='maroon', linestyle=':', label="ADP-ribose")
    ax.axhline(y=-10.3, color='purple', linestyle=':', label="NAD/NADH")
    ax.axhline(y=-10.7, color='k', linestyle=':', label="Niraparib score")
    ax.axhline(y=-12.2, color='y', linestyle=':', label="Olaparib score")

    ax.set_ylim()

    receptor_name = os.path.basename(vars["filename_of_receptor"])
    scoring_type = vars["Scoring_choice"]
    docking_type = vars["Scoring_choice"]
    num_lig = int(vars["number_of_mutants"]) +  int(vars["number_of_crossovers"]) +  int(vars["number_to_advance_from_previous_gen"])
    number_of_conf_per_lig = str(vars["max_variants_per_compound"])


    # Get Customizations
    title_of_figure = '{} Scores for {} using {}'.format(scoring_type, receptor_name, docking_type)
    plt.title(title_of_figure ,fontweight='semibold')

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.274),fontsize='small')
    number_of_lig_per_gen = str(num_lig)
    
    output = str(number_of_lig_per_gen) + " lig/gen" + "\n" + str(number_of_conf_per_lig) +" conformer/lig"
    
    plt.text(5.4,-8.5, output, bbox=dict(facecolor="white", alpha=0.5),fontsize='small')

    # legend1 = plt.legend([lines[i].get_label()  for i in range(0,lines_leg)],loc='center left', bbox_to_anchor=(1, 0.274),fontsize='small')
    # legend2 = plt.legend([output],loc='center left', bbox_to_anchor=(1, 0.774),fontsize='small')
    # # help(plt.legend)
    # ax.add_artist(legend1)
    # ax.add_artist(legend2)

    ax.set_ylim()



    if "VINA" in str(scoring_type):
        y_label = 'Docking Affinity (kcal/mol)'
    else: 
        y_label = 'Fitness Score'


    plt.ylabel(y_label,fontweight='semibold')
    
    plt.xlabel("Generation Number",fontweight='semibold')

    plt.savefig(outfile,bbox_inches='tight',dpi=1000)


def print_data_table(infolder, folder_list):
    """
    This function takes a folder of an Autogrow Run and a list of all folders within the infolder, and finds the average of each generation,
    the average of the top 50,20, 10, and 1 ligand(s) in each generation.

    It prints the average docking score values in a table and returns that information as a dictionary of dictionaries.

    Inputs:
    :param str infolder: a string for the file path to a directory containing an Autogrow run.
                            ie) "PATH/Run_0/"
    :param list folder_list: a list of every generation folders within the infolder

    Returns
    :returns: dict dict_of_averages: a dictionary of dictionaries containing the average of each generation for the top 50,20, 10, and 1 ligand(s)
                    and the overall average for each generation.

    """

    print("Overall Scoring Average for all Compounds")
    average_affinity_dict = get_average_score_per_gen(infolder, folder_list)
    print("")
    print("Average for Top Scoring Compounds")
    print("Number of top scoring compounds: ", 50)
    top_fifty_dict = get_average_top_score_per_gen(infolder, folder_list, 50)
    print("")
    print("Average for Top Scoring Compounds")
    print("Number of top scoring compounds: ", 20)
    top_twenty_dict = get_average_top_score_per_gen(infolder, folder_list, 20)
    print("") 
    print("Average for Top Scoring Compounds")
    print("Number of top scoring compounds: ", 10)
    top_ten_dict = get_average_top_score_per_gen(infolder, folder_list, 10)
    print("") 
    print("Best Score per generation")
    print("Number of top scoring compounds: ", 1)
    top_one_dict = get_average_top_score_per_gen(infolder, folder_list, 1)
    print("")
    print("")
    dict_of_averages = {}
    dict_of_averages["average_affinity_dict"] = average_affinity_dict
    dict_of_averages["top_fifty_dict"] = top_fifty_dict
    dict_of_averages["top_twenty_dict"] = top_twenty_dict
    dict_of_averages["top_ten_dict"] = top_ten_dict
    dict_of_averages["top_one_dict"] = top_one_dict



    return dict_of_averages

def make_vars_dict(autogrow_output_file):

    vars={}

    list_info = ["filename_of_receptor","scoring_function","number_of_mutants","number_of_crossovers","number_to_advance_from_previous_gen","max_variants_per_compound"] 
    count_of_vars = 0
    with open(autogrow_output_file, 'r') as f:
        for line in f.readlines():
            if len(vars.keys()) == len(list_info):
                break
            for i in list_info:
                if i in line:
                    item = line.split(", ")[-1]
                    item = item.replace(")\n","")
                    if '"' in item:

                        new_item = item.replace('"',"")
                    if "'" in item:

                        new_item = item.replace("'","")
                    else:
                        try:
                            new_item = int(item)
                        except:
                            new_item = str(item)
                        
                    vars[i] = new_item
    return vars
# Run Everything
def run_a_single_folder(vars,infolder,outfile, all_folders_list):
    folder_list = []
    for folder in all_folders_list:
        print(folder)
        if folder!="Data" and len(folder.split('_'))==2:
            folder_list.append(folder)

    folder_list.sort(key=lambda x: int(x.split('_')[1]))
    print(folder_list)
    dict_of_averages = print_data_table(infolder, folder_list)
    run_plotter(vars,dict_of_averages, outfile)

def run_everything(infolder, autogrow_output_file,outfile):

    vars = make_vars_dict(autogrow_output_file)
    
    for v in vars.keys():
        if "num" in v or "max_var" in v:
            if type(vars[v])!=int:
                vars[v] = int(vars[v].split(" ")[1].strip())

    print("")
    print(infolder)
    print("")
     
    all_folders_list = [f for f in sorted(os.listdir(infolder)) if os.path.isdir(infolder+f)]
    right_level = False
    for i in all_folders_list:
        if "generation_" in os.path.basename(os.path.dirname(i)):
            right_level = True
            break
    
    if right_level == False:
        topfolder_list = [x for x in all_folders_list if "__pycache__" not in x]
        all_folders_list = []
        for topfolder in topfolder_list:
            tempfolder = "{}/{}/".format(infolder,topfolder)
            all_folders_list = [f for f in sorted(os.listdir(tempfolder)) if os.path.isdir(tempfolder+f)]
            right_level = False
            for i in all_folders_list:
                if "generation_" in os.path.basename(os.path.dirname(i)):
                    right_level = True
                    break
            if right_level ==False:
                print("THIS IS THE WRONG LEVEL TO WORK AT!!!!!!!!!!!!")
            run_a_single_folder(vars,tempfolder,outfile, all_folders_list)

    else:
        run_a_single_folder(vars,infolder,outfile, all_folders_list)

 

if __name__ == "__main__":
    
    #
    # SPECIFY WHICH RUN NUMBER
    infolder = "/home/jspiegel/DataB/jspiegel/projects/Autogrow_output/Run_0/"

    # infolder = sys.argv[1]
    # try: 
    #     autogrow_output_file = sys.argv[2]
    # except:
    #     autogrow_output_file = infolder + "/test_output.txt"

    infolder = "/home/jacob/Desktop/PARP_AUTOGROW_DATA/new_data/"
    topfolder = "/home/jacob/Desktop/PARP_AUTOGROW_DATA/new_data/Run_0/"
        

    topfolder = sys.argv[1]
    for infolder in glob.glob(topfolder):
        autogrow_output_file = infolder + "/test_output.txt"
        outfile = infolder + "/data_histogram.png"
        print(topfolder)
        print(infolder)
        print(outfile)

        print(infolder)
        run_everything(infolder, autogrow_output_file, outfile)
        print("FINISHED {}".format(infolder))

    print("finished")