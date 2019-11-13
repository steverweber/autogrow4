import __future__

import glob
import os

import rdkit
import rdkit.Chem as Chem

# Disable the unnecessary RDKit warnings
rdkit.RDLogger.DisableLog("rdApp.*")

from autogrow.docking.scoring.scoring_classes.parent_scoring_class import ParentScoring
from autogrow.docking.scoring.scoring_classes.scoring_functions.vina import VINA


class LigEfficiency(VINA):
    """
    This will Score a given ligand for its binding affinity based on VINA or
    QuickVina02 type docking.

    This inherits many functions from the vina scoring function. The only
    difference is that this scoring function uses the ligand efficiency
    instead of docking score. ligand efficiency is the docking score divided
    by the number of heavy atoms (non-hydrogens)

    Inputs:
    :param class VINA: the VINA scoring function which this class inherits
        from.
    """

    def __init__(self, vars=None, smiles_dict=None, test_boot=True):
        """
        This will take vars and a list of smiles.

        Inputs:
        :param dict vars: Dictionary of User variables
        :param dict smiles_dict: a dict of ligand info of SMILES, IDS, and
            short ID
        :param bool test_boot: used to initialize class without objects for
            testing purpose
        """

        if test_boot is False:
            self.vars = vars

            self.smiles_dict = smiles_dict

    def get_lig_efficiency_rescore_from_a_file(self, file_path, lig_info):
        """
        This function will simply add a ligand efficiency score to the end of
        the lig_info list and return said list.

        The last value of the lig_info list must be a float.


        Inputs:
        :param str file_path: the path to the file to be scored
        :param list lig_info: a list of the ligands short_id_name and
            the fitness score from the best pose.
            This would have been generated by the primary method of
            scoring/rescoring

        Returns:
        :returns: list lig_info: a list of the ligands short_id_name and
            the docking score from the best pose.
        """
        # For saftey remove Nones and empty lists
        if type(lig_info) is not type([]) or len(lig_info) == 0:
            return None

        lig_info = append_lig_effeciency(lig_info)
        if lig_info is None:
            return None
        lig_info = [str(x) for x in lig_info]

        return lig_info


# These Functions are placed outside the class for multithreading reasons.
# Multithreading doesn't like being executed within the class.

def get_number_heavy_atoms(SMILES_str):
    """
    Get the number of non Hydrogens in a SMILE


    Inputs:
    :param str SMILES_str: a str representing a molecule

    Returns:
    :returns: int num_heavy_atoms: a int of the count of heavy atoms
    """
    if SMILES_str is None:
        return None
    # easiest nearly everything should get through

    try:
        mol = Chem.MolFromSmiles(SMILES_str, sanitize=False)
    except:
        mol = None

    if mol is None:
        return None

    atom_list = mol.GetAtoms()
    num_heavy_atoms = 0
    for atom in atom_list:
        if atom.GetAtomicNum() != 1:
            num_heavy_atoms = num_heavy_atoms + 1

    return num_heavy_atoms


def append_lig_effeciency(list_of_lig_info):
    """
    Determine the ligand efficiency and append it to the end of a list which
    has the ligand information.

    Inputs:
    :param list list_of_lig_info: a list containing ligand informations with
        idx=0 as the SMILES str and idx=-1 is the docking score

    Returns:
    :returns: list list_of_lig_info: the same list as list_of_lig_info, but
        with each sublist now having the ligand efficiency score appended to the
        end.
    """

    if type(list_of_lig_info) is None:
        return None
    elif type(list_of_lig_info) == list:
        if None in list_of_lig_info:
            return None

    # Unpack ligand info
    lig_smiles_str = str(list_of_lig_info[0])
    affinity = float(list_of_lig_info[-1])

    # Get num of heavy atoms
    heavy_atom_count = get_number_heavy_atoms(lig_smiles_str)

    if heavy_atom_count is None or heavy_atom_count == 0:
        return None

    # Convert to Lig efficiency (aka affinity/heavy_atom_count )
    lig_efficieny = float(affinity) / float(heavy_atom_count)

    # Append lig_efficiency to list_of_lig_info
    list_of_lig_info.append(str(lig_efficieny))

    return list_of_lig_info


if __name__ == "__main__":
    vars = {}
    # vars["scoring_choice"] = 'VINA'
    # folder_to_search = os.sep + os.path.join("home", "jspiegel", "DataB", "jspiegel", "projects", "output_autogrow_testing", "Run_11", "generation_0", "PDBs") + os.sep
    # run_scoring_common(vars, folder_to_search)
    smile_dict = {
        "Gen_0_Mutant_5_203493": [
            "COC1OC(CO)C(O)C(O)C1n1nnc(CCO)c1-c1ccc(-c2cccs2)s1",
            "(ZINC04530731+ZINC01529972)Gen_0_Mutant_5_203493",
        ],
        "Gen_0_Cross_452996": [
            "CC(=O)OCC(O)CN=[N+]=[N-]",
            "(ZINC44117885+ZINC34601304)Gen_0_Cross_452996",
        ],
        "ZINC13526729": ["[N-]=[N+]=NCC1OC(O)CC1O", "ZINC13526729"],
    }

    print(append_lig_effeciency(smile_dict["Gen_0_Mutant_5_203493"]))
