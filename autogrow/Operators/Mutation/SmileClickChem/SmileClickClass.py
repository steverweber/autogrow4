# SMILECLICK Class
import __future__ 

import sys
import random
import os
import json
import copy

import rdkit
import rdkit.Chem
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdFMCS
#Disable the unnecessary RDKit warnings
rdkit.RDLogger.DisableLog('rdApp.*')

import autogrow.Operators.ConvertFiles.gypsum_dl.gypsum_dl.MolObjectHandling as MOH
import autogrow.Operators.Filter.ExecuteFilters as Filter


class SmilesClickChem(object):
    """
    This class will take a molecule and Mutate it by reacting it.
    """
    def __init__(self, rxn_library_variables, list_of_already_made_smiles, Filter_Object_Dict):
        """
        init for SmilesClickChem.
        This will set up all the reaction and functional dictionaries required to Mutate a molecular

        :param list rxn_library_variables: a list of user variables which define the Rxn_library, rxn_library_file,     
                        complimentary_mol_directory, and function_group_library. 
                        ie. rxn_library_variables = [vars['Rxn_library'], vars['rxn_library_file'], vars['function_group_library'],vars['complimentary_mol_directory']]
        :param list list_of_already_made_smiles: a list of lists. Each sublist contains info about a smiles made in this generation via mutation
                        ie.[['O=C([O-])', '(Gen_3_Mutant_37_747+ZINC51)Gen_4_Mutant_15_52']]
        :param dict Filter_Object_Dict: a dictionary of all filter objects which are to be applied to the newly created ligands.        
        """
        # Unpackage the rxn_library_variables

        Rxn_library = rxn_library_variables[0]
        rxn_library_file = rxn_library_variables[1]
        function_group_library = rxn_library_variables[2]
        Complimentary_mol_dir = rxn_library_variables[3]
        self.reaction_dict = self.retrieve_reaction_dict(Rxn_library, rxn_library_file) # Retrieve the dictionary containing all the possible ClickChem Reactions
        self.list_of_reaction_names = list(self.reaction_dict.keys())

        self.functional_group_dict = self.retrieve_functional_group_dict(Rxn_library, function_group_library)
        self.complimentary_mol_dict = self.retrieve_complimentary_dictionary(Rxn_library, Complimentary_mol_dir)    


        # List of already predicted smiles
        self.list_of_already_made_smiles = [x[0] for x in list_of_already_made_smiles]
        # Dictionary containing all Filter class objects to be impossed on the ligand
        self.Filter_Object_Dict = Filter_Object_Dict
    #

    def update_list_of_already_made_smiles(self,list_of_already_made_smiles):
        """
        This updates the list of Smiles which have been made in this generation via mutation.
        :param list list_of_already_made_smiles: a list of lists. Each sublist contains info about a smiles made in this generation via mutation
                        ie.[['O=C([O-])', '(Gen_3_Mutant_37_747+ZINC51)Gen_4_Mutant_15_52']]
        """
        list_of_already_made_smiles = [x[0] for x in list_of_already_made_smiles]
        self.list_of_already_made_smiles.extend(list_of_already_made_smiles)
        
    def rxn_lib_format_json_dict_of_dict(self, old_dict):
        """
        json dictionaries  import as type unicode. This script converts all the keys and items to strings, with a few specific exceptions.
        It takes both the functional group dictionary and the reaction library. 
        
        The reaction library is a dictionary of dictionary and has a few exceptions which are not intended to be strings.
            ie. the num_reactants which converts to interger and functional_groups which convert to a list of strings. 

        The functional_group_dictionary is simply a dictionary with all items and keys needing to be strings.

        :param dic old_dict: a dictionary of the the reaction library or functional groups. This is what is importated from the .json file.
        returns:
        :returns: dic new_dict: a dictionary of the the reaction library or functional groups where the unicode type items have been replaced with
                        the proper python data types.
        """
        new_dict = {}
        for rxn_key in old_dict.keys():
            rxn_dic_old = old_dict[rxn_key]
            key_str = str(rxn_key)
            
            # For reaction libraries
            if type(rxn_dic_old) == dict:
                new_sub_dict = {}
                for key in rxn_dic_old.keys():
                    sub_key_str = str(key)
                    item = rxn_dic_old[key]

                    if sub_key_str == "num_reactants":
                        item = int(item)
                    elif  sub_key_str == "functional_groups":
                        new_list = []
                        for i in item:
                            i_str = str(i)
                            new_list.append(i_str)

                        item = new_list
                    else:
                        item = str(item)
                    
                    new_sub_dict[sub_key_str] = item
                new_dict[key_str] = new_sub_dict

            # For functional groups
            else:
                item = old_dict[rxn_key]
                new_dict[key_str] = str(item)
        
        return new_dict
    #

    def retrieve_reaction_dict(self, Rxn_library, rxn_library_file):
        """
        This is where all the chemical reactions for SmartClickChem are retrieved. If you want to add more just add 
        a Custom set of reactions please add a folder to PATH/autogrow/Operators/Mutation/SmileClickChem/Reaction_libraries/
        They should be formatted as a dictionary of dictionary using the same format as :
            os.path.join(pwd,"Reaction_libraries","ClickChem","ClickChem_rxn_library.json")

        The reactions are written as SMARTS-reaction strings. 
        
        This dictionary uses the reaction name as the key and the Reaction Smarts as the value.
        
        Inputs:
        :param str Rxn_library: A string defining the choice of the reaction library. ClickChem uses the set of reactions from Autogrow 3.1.2
                                Custom means you've defined a path to a Custom library in vars['rxn_library_file']
        :param str rxn_library_file: a PATH to a Custom reaction library file formated in a dictionary of dictionaries.
                            in a .json file.
                            This will be a blank string if one choses a predefined rxn_library option. 
        Return:
        :returns: dict reaction_dict: A dictionary containing all the reactions for ClickChemistry and all the information
                                    required to run the reaction
        """

        # Get the JSON file to import the proper reaction library
        pwd = os.path.dirname(__file__)
        if rxn_library_file == "":

            if Rxn_library == "ClickChem":
                rxn_library_file = os.path.join(pwd,"Reaction_libraries","ClickChem","ClickChem_rxn_library.json")
            elif Rxn_library == "Robust_Rxns":
                rxn_library_file = os.path.join(pwd, "Reaction_libraries", "Robust_Rxns", "Robust_Rxns_rxn_library.json")
            elif Rxn_library == "All_Rxns":
                rxn_library_file = os.path.join(pwd, "Reaction_libraries", "All_Rxns", "All_Rxns_rxn_library.json")
            elif Rxn_library == "Custom":
                if os.path.exists(rxn_library_file) == False:
                    raise Exception("Custom rxn_library_file cannot be found. Please check the path: ", rxn_library_file)
            else:
                raise Exception("Rxn_library is not incorporated into SMILESCLICKCHEM.py")


            # Import the proper reaction library JSON file 
            try:   
                with open(rxn_library_file, 'r') as rxn_file:
                    reaction_dict_raw = json.load(rxn_file)
            except:
                raise Exception("rxn_library_file json file not able to be imported. Check that the Rxn_library is formated correctly")

        elif type(rxn_library_file) == str:
            if os.path.exists(rxn_library_file) == False:
                raise Exception("Custom specified rxn_library_file directory can not be found")
            
            if os.path.isfile(rxn_library_file) == False:
                raise Exception("Custom specified rxn_library_file is not a file")

            try:
                extension = os.path.splitext(rxn_library_file)[1]
            except:
                raise Exception("Custom specified rxn_library_file is not .json file. It must be a .json dictionary")
                    
            if extension != ".json":
                raise Exception("Custom specified rxn_library_file is not .json file. It must be a .json dictionary")
                    
            # Import the proper reaction library JSON file 
            try:   
                with open(rxn_library_file, 'r') as rxn_file:
                    reaction_dict_raw = json.load(rxn_file)
            except:
                raise Exception("Custom specified rxn_library_file json file not able to be imported. Check that the Rxn_library is formated correctly")
        
        
        else:
            raise Exception("Custom specified rxn_library_file directory can not be found")
                
        # Convert the reaction_dict_raw from unicode to the proper 
        reaction_dict = self.rxn_lib_format_json_dict_of_dict(reaction_dict_raw)

        return reaction_dict
    #

    def retrieve_functional_group_dict(self, Rxn_library, function_group_library):
        """
        This retrieves a dictionary of all functional groups required for the respective reactions.
        This dictionary will be used to identify possible reactions.

        This is where all the functional groups which will be used in the SmartClickChem reactions are retrieved. 
        If you want to add more just add a Custom set of reactions please add a folder to PATH/autogrow/Operators/Mutation/SmileClickChem/Reaction_libraries/
        They should be formatted as a dictionary of dictionary using the same format as :
            os.path.join(pwd,"Reaction_libraries","ClickChem","ClickChem_functional_groups.json")

        IF YOU CHOSE TO DO A Custom REACTION SET YOU MUST PROVIDE A DICTIONARY OF ALL FUNCTIONAL GROUPS IT WILL REACT.
        IF YOU FORGET TO ADD A FUNCTIONAL GROUP TO YOUR Custom DICTIONARY, THE REACTION MAY NEVER BE UTILIZED.

        Please note if your functional groups involve stereochemistry notations such as '\' please replace with '\\'
            -all functional groups should be formated as SMARTS

        Inputs:
        :param str Rxn_library: A string defining the choice of the reaction library. ClickChem uses the set of reactions from Autogrow 3.1.2
                                Custom means you've defined a path to a Custom library in vars['function_group_library']
        :param str function_group_library: a PATH to a Custom functional group dictionary in a .json file.
                            This will be a blank string if one choses a predefined functional groups option. 
        Return:
        :returns: dict functional_group_dict: A dictionary containing all SMARTS for identifying 
                                                the functional groups for ClickChemistry 
        """

        # Get the JSON file to import the proper reaction library
        pwd = os.path.dirname(__file__)

        if function_group_library == "":

            if Rxn_library == "ClickChem":
                function_group_library = os.path.join(pwd,"Reaction_libraries","ClickChem","ClickChem_functional_groups.json")
            elif Rxn_library == "Robust_Rxns":
                function_group_library =  os.path.join(pwd,"Reaction_libraries","Robust_Rxns","Robust_Rxns_functional_groups.json")
            elif Rxn_library == "All_Rxns":
                function_group_library =  os.path.join(pwd,"Reaction_libraries","All_Rxns","All_Rxns_functional_groups.json")
            elif Rxn_library == "Custom":
                if os.path.exists(function_group_library) == False:
                    raise Exception("Custom function_group_library cannot be found. Please check the path: ", function_group_library)
            else:
                raise Exception("Rxn_library is not incorporated into SMILESCLICKCHEM.py")
            
            # Import the proper function_group_library JSON file 
            try:   
                with open(function_group_library, 'r') as func_dict_file:
                    functional_group_dict_raw = json.load(func_dict_file)
            except:
                raise Exception("function_group_library json file not able to be imported. Check that the Rxn_library is formated correctly")


        elif type(function_group_library) == str:

            if os.path.exists(function_group_library) == False:
                raise Exception("Custom specified function_group_library directory can not be found")
            
            if os.path.isfile(function_group_library) == False:
                raise Exception("Custom specified function_group_library is not a file")

            try:
                extension = os.path.splitext(function_group_library)[1]
            except:
                raise Exception("Custom specified function_group_library is not .json file. It must be a .json dictionary")

            if extension != ".json":
                raise Exception("Custom specified function_group_library is not .json file. It must be a .json dictionary")
                    
            # Import the proper function_group_library JSON file 
            try:   
                with open(function_group_library, 'r') as func_dict_file:
                    functional_group_dict_raw = json.load(func_dict_file)
            except:
                raise Exception("function_group_library json file not able to be imported. Check that the Rxn_library is formated correctly")
        else:
            raise Exception("Custom specified function_group_library directory can not be found")
                
        # Convert the reaction_dict_raw from unicode to the proper 
        functional_group_dict = self.rxn_lib_format_json_dict_of_dict(functional_group_dict_raw)

        return functional_group_dict
    #

    def rand_key_list(self, dictionary):
        """
        Get a random ordered list of all the keys from  a dictionary.
   
        Input:
        :param dict dictionary: any dictionary
        Return:
        :returns: list keys: a randomly ordered list containing all the keys from the dictionary
        """
        keys = list(dictionary.keys()) # List of keys
        random.shuffle(keys)
        return keys
    #

    def retrieve_complimentary_dictionary(self, Rxn_library, Complimentary_mol_dir):
        """
        Based on user controled variables, this definition will retrieve a dictionary of molecules
        seperated into classes by their functional groups.
        The sorting of a .smi file into this should be handled in the user parameter testing 
        when autogrow is initailly started.
                
        Inputs:
        :param str Rxn_library: A string defining the choice of the reaction library. ClickChem uses the set of reactions from Autogrow 3.1.2
                            Custom means you've defined a path to a Custom library in vars['Complimentary_mol_dir']
        :param dict Complimentary_mol_dir: the path to the Complimentary_mol_dir directory. It may be an empty string in which
                        case the Complimentary_mol_dir directory will default to those of the Rxn_library

        Return:
        :returns: dict complimentary_mols_dict: a dictionary of complimentary molecules
        """
        script_dir = os.path.dirname(os.path.realpath(__file__))

        if Complimentary_mol_dir == "":            
            if Rxn_library == "ClickChem":
                Complimentary_mol_dir = os.path.join(script_dir,"Reaction_libraries","ClickChem","complimentary_mol_dir")
            elif Rxn_library == "Robust_Rxns":
                Complimentary_mol_dir =  os.path.join(script_dir,"Reaction_libraries","Robust_Rxns","complimentary_mol_dir")
            elif Rxn_library == "All_Rxns":
                Complimentary_mol_dir =  os.path.join(script_dir,"Reaction_libraries","All_Rxns","complimentary_mol_dir")
            elif Rxn_library == "Custom":
                if os.path.isdir(Complimentary_mol_dir) == False:
                    raise Exception("Custom Complimentary_mol_dir cannot be found. Please check the path: ", Complimentary_mol_dir)
            else:
                raise Exception("Rxn_library is not incorporated into SMILESCLICKCHEM.py")
            
        else:
            if os.path.isdir(Complimentary_mol_dir) == False:
                raise Exception("Complimentary_mol_dir is not a directory. It must be a directory with .smi files containing SMILES specified by functional groups.\
                    These .smi files must be named the same as the files in the Complimentary_mol_dir.")

        # Make a list of all the functional groups. These will be the name of the .smi folders already seperated by group.
        functional_groups = (self.functional_group_dict.keys())

        missing_smi_files = []
        complimentary_mols_dict = {}             
        for group in functional_groups:
            filepath = "{}{}{}.smi".format(Complimentary_mol_dir,os.sep, group)

            if os.path.isfile(filepath) == True:
                complimentary_mols_dict[group] = filepath

            else:
                missing_smi_files.append(filepath)
                print("Could not find the following .smi file for complimentary molecules for Mutation: {}".format(filepath))
                
        if len(missing_smi_files) != 0:     
            raise Exception("The following .smi file for complimentary molecules for Mutation is missing: ",missing_smi_files)
                  
        return complimentary_mols_dict          
    #

    def make_reactant_order_list(self, substructure_search_result, has_substructure_matches_count):
        """
        make an ordered list of reactants which composed of 0 and 1.
        This list will be used (in later steps) to determine which reactant is the ligand and which 
        requires a complimentary molecule.

        Input:
        :param list substructure_search_result: list composed of 0 and 1. 1 for if it has the substructure 0 for not
        :param int has_substructure_matches_count: how many substructure matches there are
        Return:
        :returns: list reactant_order_list: an ordered list of reactants which composed of 0 and 1.
        """      
        # for mols w atleast 1 substructure
        if has_substructure_matches_count == 1:
            reactant_order_list = substructure_search_result
        elif has_substructure_matches_count > 1:
            # if more than 1 reactant is found in the ligand than we need to randomly
            # pick 1 to be the molecule in the reaction and the other(s) to be 
            # mols chosen from the complimentary molecule dictionary

            # create a list to be used to determine which reactants need complimentary mol
            # and which will use the Ligand
            reactant_order_list = []
            
            chosen_as_mol_num = random.randint(0,has_substructure_matches_count-1)
            counter_of_matches = 0
            for i in range(0,len(substructure_search_result)):
                if substructure_search_result[i] == 1 and counter_of_matches == chosen_as_mol_num:
                    reactant_order_list.append(1)
                    counter_of_matches = counter_of_matches+1
                elif substructure_search_result[i] == 1 and counter_of_matches != chosen_as_mol_num:
                    reactant_order_list.append(0)
                    counter_of_matches = counter_of_matches+1
                else:
                    reactant_order_list.append(0)
        return reactant_order_list
    #

    def get_random_complimentary_mol(self, functional_group):
        """
        This function will get a dictionary of complimentary mols 

        Input:
        :param str functional_group: the functional group of the needed complimentary molecule for the reaction

        Return:
        :returns: list random_comp_mol: list with the SMILES string and name of molecule for the randomly chosen comp mol
        """
        infile = self.complimentary_mol_dict[functional_group]

        with open(infile, 'r') as f:
            random_comp_mol_line = random.choice(f.readlines())
            random_comp_mol_line = random_comp_mol_line.replace("\n","").replace("\t"," ")
            for i in range(10): random_comp_mol_line.replace("  "," ")
            parts = random_comp_mol_line.split(" ")     # split line into parts seperated by 4-spaces

            smile_list = parts[0]
            zinc_name_list = parts[1]
            random_comp_mol = [smile_list, zinc_name_list]

        return random_comp_mol
    #

    def determine_functional_groups_in_mol(self, mol_deprotanated, mol_reprotanated):
        """
        This function will take a molecule and find which functional groups it has. This will save time for picking reactions, particularly as
        reaction lists become larger.

        Inputs: 
        :param rdkit.Chem.rdchem.Mol mol_deprotanated: an rdkit molecule which has been sanitized and deprotanated
        :param rdkit.Chem.rdchem.Mol mol_reprotanated: an rdkit molecule which has been sanitized and fully protanated
        Returns:
        :returns: list list_subs_within_mol: a list of the name of every functional group found within the molecule.
                                            these will be used later to filter for reactions.
        """
        list_subs_within_mol = []
        functional_group_dict = self.functional_group_dict

        for key in list(functional_group_dict.keys()):
            substructure = Chem.MolFromSmarts(functional_group_dict[key])
            if mol_reprotanated.HasSubstructMatch(substructure):
                list_subs_within_mol.append(key)
            else:
                if mol_deprotanated.HasSubstructMatch(substructure):
                    list_subs_within_mol.append(key)
                else:
                    continue
        return list_subs_within_mol
    #
            
    def run_Smile_Click(self, Ligand_smiles_string):
        """
        This will take the shuffled list of reaction names (self.shuffled_reaction_list) and test the Ligand to see if it is 
        capable of being used in the reaction. If the ligand is unable to be used in the reaction, then we move on to the
        next reaction in the list. If none work, we return a  None.

        Input:
        :param str Ligand_smiles_string: SMILES string of a molecule to be reacted

        Returns:
        :returns: list product_info: list containing the reaction product, the id_number of the reaction as found in the reaction_dict
                                    and the id for the complimentary mol (None if it was a single reactant reaction)
                                        [reaction_product_smilestring, reaction_id_number, zinc_database_comp_mol_name]  
                            returns None if all reactions failed or input failed to convert to a sanitizable rdkit mol
        """
        try:
            mol = Chem.MolFromSmiles(Ligand_smiles_string, sanitize = False) # This is the input molecule which serves as the parent molecule
        except:
            # mol object failed to initialize
            return None

        # try sanitizing, which is necessary later
        mol = MOH.check_sanitization(mol)
        if mol is None:
            return None

        # Is important for some functional groups while being deprotanated are useful for other reaction
        mol_reprotanated = copy.deepcopy(mol)
        mol_reprotanated = MOH.try_reprotanation(mol_reprotanated)
        if mol_reprotanated is None:
            return None

        mol_deprotanated = copy.deepcopy(mol)
        mol_deprotanated = MOH.try_deprotanation(mol_deprotanated)
        if mol_deprotanated is None:
            return None

        # Determine which functional groups are within a ligand
        list_subs_within_mol = self.determine_functional_groups_in_mol(mol_deprotanated, mol_reprotanated)
        if len(list_subs_within_mol) == 0:
            print("{} had no functional groups to react with.".format(Ligand_smiles_string))
            return None

        shuffled_reaction_list = self.rand_key_list(self.reaction_dict)  # Randomize the order of the list of reactions
        
        tries = 0
        is_rxn_complete = False
        # go through all possible rxns in dicitonary of rxns using the random order of rxns
        # loop ends when a rxn is successful or when it runs out of reactions
        while tries < len(shuffled_reaction_list) and is_rxn_complete is False: 
            reaction_name = shuffled_reaction_list[tries]
            a_reaction_dict = self.reaction_dict[reaction_name]
                
            fun_groups_in_rxn = a_reaction_dict["functional_groups"]
            contains_group = None
            for i in range(0,len(fun_groups_in_rxn)):
                if fun_groups_in_rxn[i] in list_subs_within_mol:
                    contains_group = i
                    # The number i which contains_group is now equal to will be used to 
                    # remember the placement of the molecule later in the reaction.
                    break
                else:
                    continue

            if contains_group == None:
                # Reaction doesn't contain a functional group found in the reactant molecule.
                # So lets move on to the next molecule
                tries = tries +1
                continue
            else:

                # Determine whether to react using the protanated or deprotanated form of the ligand
                substructure = Chem.MolFromSmarts(self.functional_group_dict[fun_groups_in_rxn[i]])
                if mol_deprotanated.HasSubstructMatch(substructure)==True:
                    mol_to_use = copy.deepcopy(mol_deprotanated)
                else:
                    mol_to_use = copy.deepcopy(mol_reprotanated)
                substructure = None

            rxn = AllChem.ReactionFromSmarts(str(a_reaction_dict['reaction_string']))
            rxn.Initialize()   
            
            # if the reaction requires only a single reactant we will attempt to run the reaction
            if a_reaction_dict['num_reactants'] == 1:
                # "Try reaction"
                zinc_database_comp_mol_name = None
                comp_mol_ID = None
                try: 
                    # if reaction works keep it
                    reaction_products_list = [x[0] for x in rxn.RunReactants((mol_to_use,))]

                    # randomly shuffle the lists of products so that we don't bias a single product type
                    # ie ClickChem Reactions 5_Alkyne_and_Azide produces two products: a 1,5 isomer and a 1,4 isomer; 
                    #  This will shuffle the list and try each option
                    random.shuffle(reaction_products_list)

                    if reaction_products_list is () or reaction_products_list is [] or len(reaction_products_list)==0:
                        # if reaction fails then lets move on to the next reaction
                        tries = tries + 1
                    else:
                        is_rxn_complete = False
                        for reaction_product in reaction_products_list:
                            # Filter and check the product is valid
                            reaction_product_smilestring = self.check_if_product_is_good(reaction_product)
                            if reaction_product_smilestring is None:
                                is_rxn_complete = False
                            else:
                                # REACTION WORKED!
                                is_rxn_complete = True 
                                break
                        if reaction_product_smilestring != None and is_rxn_complete == True:
                            # REACTION WORKED!
                            break
                        else:
                            tries = tries + 1
                            
                #
                except:
                    # if reaction fails then lets move on to the next reaction  
                    mol_to_use = None
                    tries = tries +1
                    break
                #
            #
            else:                
                # for each functional group in the reaction, test 
                # if the ligand has that as a substructure
                
                list_reactant_mols = [] 
                comp_mol_ID = []   
                for i in range(0,len(fun_groups_in_rxn)):
                    if i == contains_group:
                        # This is where the molecule goes
                        list_reactant_mols.append(mol_to_use)

                    else:
                        # for reactants which need to be taken from the complimentary dictionary
                        # Find the reactants functional group
                        functional_group_name = str(a_reaction_dict['functional_groups'][i])

                        # Determine whether to react using the protanated or deprotanated form of the ligand
                        substructure = Chem.MolFromSmarts(self.functional_group_dict[fun_groups_in_rxn[i]])

                        # lets give up to 100 tries to find a comp molecule which is viable
                        for find_mol_tries in range(0,100):

                            # find that group in the complimentary dictionary
                            # comp_molecule = ["cccc", "ZINC123"]
                            comp_molecule = self.get_random_complimentary_mol(functional_group_name)

                            # zinc_database name 
                            zinc_database_comp_mol_name = comp_molecule[1]

                            # Smiles String of complimentary molecule
                            comp_smiles_string = comp_molecule[0]

                            # check this is a santizable molecule
                            comp_mol = Chem.MolFromSmiles(comp_smiles_string, sanitize = False) 
                            # try sanitizing, which is necessary later
                            comp_mol = MOH.check_sanitization(comp_mol)

                            # Try with deprotanated molecule rdkit to recognize for the reaction
                            comp_mol = MOH.try_deprotanation(comp_mol)
                            if comp_mol == None:
                                continue

                            if comp_mol.HasSubstructMatch(substructure)==True:
                                comp_mol = comp_mol
                                # append to ordered list
                                list_reactant_mols.append(comp_mol)
                                comp_mol_ID.append(zinc_database_comp_mol_name)
                                break
                            
                            else:
                                # Try with deprotanated molecule rdkit to recognize for the reaction
                                comp_mol = MOH.try_deprotanation(comp_mol)
                                if comp_mol == None:
                                    continue

                                if comp_mol.HasSubstructMatch(substructure)==True:
                                    comp_mol = comp_mol
                                    # append to ordered list
                                    list_reactant_mols.append(comp_mol)
                                    comp_mol_ID.append(zinc_database_comp_mol_name)
                                    break
                                else:
                                    comp_mol = None
                                    continue
               
                ####### 
                # we will make a tuple of the molecules as rdkit mol objects
                # 1st we generate a list of reactant mol objects
                # then we convert to tuple

                # convert list to tuple
                tuple_reactant_mols = tuple(list_reactant_mols)
                
                ####### 
                # Run the reaction:
                # We use a try/except statement incase an error occurs
                # and rdkit is unable to complete the reaction. without this
                # a failure to complete the reaction would result in the
                # terminating.
                # 
                # 
                # Try to run reaction
                try:
                    # if reaction works keep it
                    reaction_products_list = [x[0] for x in rxn.RunReactants(tuple_reactant_mols)]

                    # randomly shuffle the lists of products so that we don't bias a single product type
                    # ie ClickChem Reactions 5_Alkyne_and_Azide produces two products: a 1,5 isomer and a 1,4 isomer; 
                    #  This will shuffle the list and try each option
                    random.shuffle(reaction_products_list)

                except:
                    reaction_product = None
                    tries = tries +1
                    continue

                if reaction_products_list is () or reaction_products_list is [] or len(reaction_products_list)==0:
                    reaction_id_number = a_reaction_dict['RXN_NUM'] 
                    tries = tries +1
                    continue
                else:
                    is_rxn_complete = False
                    for reaction_product in reaction_products_list:
                        # Filter and check the product is valid
                        reaction_product_smilestring = self.check_if_product_is_good(reaction_product)
                        if reaction_product_smilestring is None:
                            is_rxn_complete = False
                        else:
                            # REACTION WORKED!
                            is_rxn_complete = True 
                            break
                    if reaction_product_smilestring != None and is_rxn_complete == True:
                        # REACTION WORKED!
                        break
                    else:
                        tries = tries + 1
        #
            #
        #end of the big while loop (while tries < len(shuffled_reaction_list) and is_rxn_complete is False)
        #

        # check that a reaction was sucessful
        if is_rxn_complete is True:
            reaction_product = MOH.check_sanitization(reaction_product)
            if reaction_product is None:
                return None

            reaction_product_smilestring = Chem.MolToSmiles(reaction_product, isomericSmiles=True)
            reaction_id_number = a_reaction_dict['RXN_NUM']

            # RETURNS THE NEW PRODUCTS SMILESTRING,
            # THE REACTION ID NUMBER (SO ONE CAN TRACK THE MOLS LINEAGE) 
            # THE COMP_MOL ZINC DATABASE ID NUMBER (IF IT WAS A RXN WITH ONLY 1 REACTANT THIS IS None)
            if comp_mol_ID == None:
                zinc_database_comp_mol_names = None
            elif len(comp_mol_ID) == 1:
                zinc_database_comp_mol_names = comp_mol_ID[0]
            else:
                zinc_database_comp_mol_names = "+".join(comp_mol_ID)
            product_info = [reaction_product_smilestring, reaction_id_number, zinc_database_comp_mol_names]
            return product_info
        else:     
            return None
        #
    #
    def check_if_product_is_good(self, reaction_product):
        """
        This function will test whether the product passes all of the requirements:
            1) Mol sanitizes
            2) It isn't in the self.list_of_already_made_smiles
            3) It passes Filterization
        Returns the smile if it passes; returns None if it fails.
        """
        reaction_product = MOH.check_sanitization(reaction_product)
        if reaction_product is None:
            return None

        # Remove any fragments incase 1 made it through
        reaction_product = MOH.handle_frag_check(reaction_product)
        if reaction_product is None:
            return None

        # Make sure there are no unassigned atoms which made it through 
        # These are very unlikely but possible
        reaction_product = MOH.check_for_unassigned_atom(reaction_product)
        if reaction_product is None:
            return None

        reaction_product = MOH.try_reprotanation(reaction_product)
        if reaction_product is None:
            return None

        #Remove H's
        reaction_product = MOH.try_deprotanation(reaction_product)
        if reaction_product is None:
            return None

        reaction_product = MOH.check_sanitization(reaction_product)
        if reaction_product is None:
            return None

        # Check if product SMILE has been made before
        reaction_product_smilestring = Chem.MolToSmiles(reaction_product, isomericSmiles=True)
        if reaction_product_smilestring in self.list_of_already_made_smiles:
            return None

        # Run through filters
        pass_or_not = Filter.run_filter_on_just_smiles(reaction_product_smilestring, self.Filter_Object_Dict)
        if pass_or_not == False:
            return None
        else:
            return reaction_product_smilestring

# 