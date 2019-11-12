"""VandeWaterbeemdFilter Filter
This runs a VandeWaterbeemdFilter filter for drugs which are likely
to be blood brain barrier permeable.
VandeWaterbeemdFilter filter filters molecules for Molecular weight (MW),
and Polar Sureface Area (PSA).

To pass the VandeWaterbeemdFilter filter a ligand must have:
    Molecular Weight: max 450 dalton
    Polar Sureface Area: max 90 A^2

If you use the Van de Waterbeemd Filter please cite:
Van de Waterbeemd, Han: et al
Estimation of Dlood-Brain Barrier Crossing of Drugs 
Using Molecular Size and Shape, and H-Bonding Descriptors.
Journal of Drug Targeting (1998), 6(2), 151-165.
"""
import __future__

import rdkit
import rdkit.Chem as Chem
import rdkit.Chem.MolSurf as MolSurf
import rdkit.Chem.Descriptors as Descriptors
#Disable the unnecessary RDKit warnings
rdkit.RDLogger.DisableLog('rdApp.*')

from autogrow.operators.filter.filter_classes.parent_filter_class import ParentFilter


class VandeWaterbeemdFilter(ParentFilter):
    """
    This runs a VandeWaterbeemdFilter filter for drugs which are likely
    to be blood brain barrier permeable.
    VandeWaterbeemdFilter filter filters molecules for Molecular weight (MW),
    and Polar Sureface Area (PSA).

    To pass the VandeWaterbeemdFilter filter a ligand must have:
        Molecular Weight: max 450 dalton
        Polar Sureface Area: max 90 A^2

    If you use the Van de Waterbeemd Filter please cite:
    Van de Waterbeemd, Han: et al
    Estimation of Dlood-Brain Barrier Crossing of Drugs 
    Using Molecular Size and Shape, and H-Bonding Descriptors.
    Journal of Drug Targeting (1998), 6(2), 151-165.

    Inputs:
    :param class ParentFilter: a parent class to initialize off
    Returns:
    :returns: bool bool: True if the mol passes the filter; False if it fails the filter
    """
    def run_filter(self, mol):
        """
        This runs a VandeWaterbeemdFilter filter for drugs which are likely
        to be blood brain barrier permeable.
        VandeWaterbeemdFilter filter filters molecules for Molecular weight (MW),
        and Polar Sureface Area (PSA).

        To pass the VandeWaterbeemdFilter filter a ligand must have:
            Molecular Weight: max 450 dalton
            Polar Sureface Area: max 90 A^2

        Inputs:
        :param rdkit.Chem.rdchem.Mol object mol: An rdkit mol object to be tested if it passes the filters
        Returns:
        :returns: bool bool: True if the mol passes the filter; False if it fails the filter
        """
        ExactMWt = Descriptors.ExactMolWt(mol)
        if ExactMWt > 450:
            return False
        PSA = MolSurf.TPSA(mol)
        if PSA > 90:
            return False
        else:
            return True
    #
#