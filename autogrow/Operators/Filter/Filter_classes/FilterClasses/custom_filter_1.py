"""Lipinski Lenient
This runs a Lenient Lipinski filter.
Lipinski filter refines for orally available drugs. 
It filters molecules by Molecular weight (MW),
the number of hydrogen donors, the number hydrogen acceptors,
and the logP value.

To pass the Lipinski filter a molecule must be
    MW: Max 500 dalton
    Number of H acceptors: Max 10
    Number of H donors: Max 5
    logP Max +5.0

If you use the Lipinski Filter please cite:
C.A. Lipinski et al.
Experimental and computational approaches to estimate 
solubility and permeability in drug discovery 
and development settings
Advanced Drug Delivery Reviews, 46 (2001), pp. 3-26
"""
import __future__

import rdkit
import rdkit.Chem as Chem
import rdkit.Chem.Lipinski as Lipinski
import rdkit.Chem.Crippen as Crippen
import rdkit.Chem.Descriptors as Descriptors

from autogrow.Operators.Filter.Filter_classes.ParentFilterClass import ParentFilter
functional_dict = {
        "1_4_dione": "[#6]-[C&R0](=[O&D1])-[C;H1,H2]-[C;H1,H2]-C(=[O&D1])-[#6]",
        "2_acetylphenol": "c(-[C&$(C-c1ccccc1)](=[O&D1])-[C&H3]):c-[O&H1]",
        "4_piperidone": "O=C1[#6&H2][#6&H2][N][#6&H2][#6&H2]1",
        "5_mem_aryl_w_NH_max2N": "[n&H1&+0&r5&!$(n[#6]=[O,S,N])&!$(n~n~n)&!$(n~n~c~n)&!$(n~c~n~n)]",
        "B_arylethylamine": "[c&H1]1:c(-[C&H2]-[C&H2]-[N&H2]):c:c:c:c:1",
        "acetohydrazide": "[N&H2]-[N&H1]-[C&H0&$(C-[#6])&R0]=[O&D1]",
        "alcohol": "[#6&$([#6]~[#6])&!$([#6]=O)][#8&H1]",
        "aldehyde": "[#6]-[C&H1&R0]=[O&D1]",
        "aldehyde_or_ketone": "[#6]-[C;H1,$([C&H0](-[#6])[#6])]=[O&D1]",
        "aldehyde_or_ketone_flexible": "[#6]-[C;H1,$([C&H0](-[#6])[#6]);!$(CC=O)]=[O&D1]",
        "aldehyde_or_ketone_restricted": "[#6][C;H1,$(C(-,:[#6])[#6])]=[O&D1]",
        "aliphatic_alkyne": "[C&H0&$(C-[#6])]#[C&H1]",
        "aliphatic_alkyne_w_aro_alkyl_group": "[C&H0&$(C-[#6])]#[C&H0&$(C-[#6])]",
        "alkene": "[#6;c,$(C(=O)O),$(C#N)][#6&H1]=[#6&H2]",
        "alkyl_halide": "[Cl,Br,I][#6&H2&$([#6]~[#6])]",
        "alkyl_halogen": "[C&A&!$(C=O)]-[*;#17,#35,#53]",
        "alkyl_halogen_or_alcohol": "[C;H1,H2;A;!$(C=O)]-[*;#17,#35,#53,O&H1]",
        "alkyne": "[C&H1]#[C&$(C-[#6])]",
        "alpha_halo_ketone": "[C&$(C(-,:[#6])[#6&!$([#6]Br)])](=[O&D1])[C&H1&$(C(-,:[#6])[#6])]Br",
        "amide": "[N&!H0&!$(N-N)&!$(N-C=N)&!$(N(-C=O)-C=O)]-[C;H1,$(C-[#6])]=[O&D1]",
        "amidine": "[#7&H2][C&$(C(=N)(-,:N)[c,#7])]=[#7&H1&D1]",
        "aminobenzenethiol": "[*;Br,I;$(*c1ccccc1)]-c:c-[S&D2]-[C&H3]",
        "anthranilic_acid": "c(-[C&$(C-c1ccccc1)](=[O&D1])-[O&H1]):c-[N&H2]",
        "aryl_aldehyde": "c-[C&H1&R0]=[O&D1]",
        "aryl_boronic_acid": "cB(-,:O)O",
        "aryl_carboxylic_acid": "[c&$(c1[c&$(c[C,S,N](=[O&D1])[*&R0])]cccc1)][C&$(C(=O)[O&H1])]",
        "aryl_halide": "[#6&H0&D3&$([#6](~[#6])~[#6])][Cl,Br,I]",
        "aryl_halide_flexible": "[c&$(c1aaccc1)][Cl,Br,I]",
        "aryl_halide_nitrogen_optional": "[Cl,Br,I][c&$(c1:[c,n]:[c,n]:[c,n]:[c,n]:[c,n]:1)]",
        "aryl_or_vinyl_halide": "[#6;$(C=C-[#6]),$(c:c)][Br,I]",
        "benzil_or_benzoin": "[C&$(C-c1ccccc1)](=[O&D1])-[C&D3&$(C-c1ccccc1)]~[O;D1,H1]",
        "beta_dicarbonyl": "[#6&!$([#6](-C=O)-C=O)]-[C&H0](=[O&D1])-[C;H1&!$(C-[*&!#6])&!$(C-C(=O)O),H2]-[C&H0&R0](=[O&D1])-[#6&!$([#6](-C=O)-C=O)]",
        "boronic_acid": "[#6&H0&D3&$([#6](~[#6])~[#6])]B(-,:O)O",
        "carboxylic_acid": "[#6]-[C&R0](=[O&D1])-[O&H1]",
        "carboxylic_acid_or_ester": "[#6]-[C&R0](=[O&D1])-[#8;H1,$(O-[C&H3])]",
        "carboxylic_acid_or_extended_esters": "[C&H0&$(C-[#6])&R0](=[O&D1])-[#8;H1,$(O-[C&H3]),$(O-[C&H2]-[C&H3])]",
        "cyclohexanone": "[C&$(C1-[C&H2]-[C&H2]-[N,C]-[C&H2]-[C&H2]-1)]=[O&D1]",
        "halide_type_1": "[Cl,Br,I][#6&$([#6]~[#6])&!$([#6](-,:[Cl,Br,I])[Cl,Br,I])&!$([#6]=O)]",
        "halide_type_2": "[#6;$([#6]=[#6]),$(c:c)][Cl,Br,I]",
        "halide_type_3": "[#6&$([#6]~[#6])&!$([#6]~[S,N,O,P])][Cl,Br,I]",
        "haloketone": "[#6]-[C&R0](=[O&D1])-[C&H1&R0](-[#6])-[*;#17,#35,#53]",
        "hydrazine": "[N&H2]-[N&!H0;$(N-[#6]),H2]",
        "imide": "[N&H1&$(N(-,:C=O)C=O)]",
        "indole": "[c&H1]1:c:c:[c&H1]:c2:[n&H1]:c:[c&H1]:c:1:2",
        "isocyanate": "[N&$(N-[#6])]=[C&$(C=O)]",
        "isothiocyanate": "[N&$(N-[#6])]=[C&$(C=S)]",
        "ketone": "[C&$(C(-,:[#6])[#6])](=[O&D1])-[C&H2&$(C(-,:[#6])[#6])&!$(C(-,:C=O)C=O)]",
        "nitrile": "[C&H0&$(C-[#6])]#[N&H0]",
        "ortho_1amine_2alcohol_arylcyclic": "[c&r6](-[O&H1]):[c&r6]-[N&H2]",
        "ortho_aminobenzaldehyde": "[N&H2&$(N-c1ccccc1)]-c:c-[C&H1]=[O&D1]",
        "ortho_aminophenol": "c(-[O&H1&$(Oc1ccccc1)]):[c&r6]-[N&H2]",
        "ortho_aminothiophenol": "[c&r6](-[S&H1]):[c&r6]-[N&H2]",
        "ortho_halo_nitrobenzene": "[c&$(c1c(-,:N(~O)~O)cccc1)][Cl,F]",
        "ortho_halo_phenol": "[*;Br,I;$(*c1ccccc1)]-c:c-[O&H1]",
        "ortho_halo_thioanizole": "[*;Br,I;$(*c1ccccc1)]-c:c-[N&H2]",
        "ortho_phenylenediamine": "[c&r6](-[N&H1&$(N-[#6])]):[c&r6]-[N&H2]",
        "para_halo_nitrobenzene": "[c&$(c1ccc(-,:N(~O)~O)cc1)][Cl,F]",
        "phenole": "[O&H1&$(Oc1ccccc1)]",
        "phenylhydrazine": "[N&H1&$(N-c1ccccc1)](-[N&H2])-c:[c&H1]",
        "phthalazinone_precursor": "[c&r6](-[C&$(C=O)]-[O&H1]):[c&r6]-[C;H1,$(C-C)]=[O&D1]",
        "primary_amine": "[N&H2&$(N-[C,N])&!$(NC=[O,S,N])&!$(N(-,:[#6])[#6])&!$(N~N~N)]",
        "primary_or_secondary_alcohol": "[C;H1&$(C(-,:[#6])[#6]),H2&$(C[#6])][O&H1]",
        "primary_or_secondary_amine": "[N&$(NC)&!$(N=*)&!$([N&-])&!$(N#*)&!$([N&D3])&!$([N&D4])&!$(N[c,O])&!$(N[C,S]=[S,O,N])]",
        "primary_or_secondary_amine_C_aryl_alkyl": "[N&$(NC)&!$(N=*)&!$([N&-])&!$(N#*)&!$([N&D3])&!$([N&D4])&!$(N[O,N])&!$(N[C,S]=[S,O,N])]",
        "primary_or_secondary_amine_aro_optional": "[N;$(NC)&!$(N=*)&!$([N&-])&!$(N#*)&!$([N&D3])&!$([N&D4])&!$(N[c,O])&!$(N[C,S]=[S,O,N]),H2&$(Nc1:[c,n]:[c,n]:[c,n]:[c,n]:[c,n]:1)]",
        "primary_or_secondary_halide": "[Cl,Br,I][C&H2&$(C-[#6])&!$(CC[I,Br])&!$(CCO[C&H3])]",
        "pyridine_pyrimidine_triazine": "[c&!$(c1ccccc1)&$(c1[n,c]c[n,c]c[n,c]1)][Cl,F]",
        "restricted_hydrazine": "[N&H2]-[N&H1&$(N-[#6])&!$(NC=[O,S,N])]",
        "sulfonamide": "[N&H1&$(N(-,:[#6])S(=O)=O)]",
        "sulfonic_acid": "[S&$(S(=O)(=O)[C,N])]Cl",
        "terminal_alkene": "[#6;c,$(C(=O)O),$(C#N)][#6](-,:[#6])=[#6&H1&$([#6][#6])]",
        "terminal_alkyne": "[C&H1&$(C#CC)]",
        "tetrazole_1": "[#7&H1]1~[#7]~[#7]~[#7]~[#6]~1",
        "tetrazole_2": "[#7]1~[#7]~[#7&H1]~[#7]~[#6]~1",
        "thioamide": "[N&H2]-C=[S&D1]"
    }


class custom_filter_1(ParentFilter):
    """
    limit to 250kda
    must have atleast 1 substructure match

    Inputs:
    :param class ParentFilter: a parent class to initialize off
    """        
    def run_filter(self, mol):
        """
        This runs the Lenient Lipinski filter.
        Lipinski filter refines for orally available drugs. 
        It filters molecules by Molecular weight (MW),
        the number of hydrogen donors, the number hydrogen acceptors,
        and the logP value.
        
        This is a Lenient Lipinski which means a ligand 
        is allowed one violation exception to 
        the Lipinski Rule of 5 restraints.

        To pass the Lipinski filter a molecule must be
            MW: Max 500 dalton
            Number of H acceptors: Max 10
            Number of H donors: Max 5
            logP Max +5.0
            
        Inputs:
        :param rdkit.Chem.rdchem.Mol object mol: An rdkit mol object to be tested if it passes the filters
        Returns:
        :returns: bool bool: True if the mol passes the filter; False if it fails the filter
        """    
        print("F1")
        ExactMWt = Descriptors.ExactMolWt(mol)
        if ExactMWt > 150:
            return False
        for fun_group in functional_dict.keys():
            if mol.HasSubstructMatch(Chem.MolFromSmarts(functional_dict[fun_group])) == True:
                return True

        return False
    #
#
