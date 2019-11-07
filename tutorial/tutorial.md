#   Welcome to Autogrow 4.0.0

This document will break down the how to run Autogrow. It will also cover what 
dependencies are required to run Autogrow. 

##  Computer Requirements:
    Autogrow has been tested on Ubuntu 16.04 and higher, as well as MacOS 10.13: High Sierra. 
    It has been verified to work on HPC using SMP multithreading running RedHat Enterprise Server release 7.3 Maipo.

    Autogrow has not been configured for Windows OS, but a docker image capable of running on Windows can be found:
#
##  Installing AutoGrow :
    AutoGrow 4.0.0 can be install by git clone command: 
        1) cd PATH/desired_dir/
        2) git clone https://git.durrantlab.pitt.edu/jdurrant/autogrow

# 
##  Dependencies:
    Autogrow has many dependencies which may need to be installed.

### Bash:(Required)
    A modern installation of bash is required to run AutoGrow.
    Autogrow has been tested using GNU bash, version 4.4.19

### Bash Dependencies: (Required For MacOS User)
    Most Linux OS comes preinstalled with modern Bash and timeout tools used by AutoGrow.

    For MacOS users please install GNU Tools for Bash. This is required for using Timeout functions in Bash.
        This can be done by running: sudo brew install coreutils
    
### Python Installation:(Required)
    AutoGrow is primarily written in python. To run Autogrow a python interpreter and bash are required.

    A modern version of python can be installed using conda:
        https://docs.conda.io/projects/conda/en/latest/user-guide/install/
        or obtained at: [http://www.python.org/getit/](http://www.python.org/getit/).
    
    AutoGrow has been tested with python 2.7, 3.6, and 3.7
        -future support and updates will be using 3.7

    We recommend using the most current version of python available. 3.7 or newer.           
    
### MGLTools: (Optional: *must use either MGLTools, obabel, or a custom file converter/docking software)
    MGLTools citations:
        - Morris, G. M., Huey, R., Lindstrom, W., Sanner, M. F., Belew, R. K., Goodsell, D. S. and Olson, A. J. (2009) 
        Autodock4 and AutoDockTools4: automated docking with selective receptor flexiblity. J. Computational Chemistry 2009, 16: 2785-91

    MGLTools is a program by the creators of Autodock Vina. It is used by AutoGrow to convert .pdb files to .pdbqt format.
        -.pdbqt format is required by Vina type docking programs including Autodock Vina and QuickVina2
        -An alternative conversion option is obabel.
        
####    Installation:
    WARNING: MGLTools installation can be tricky!
        We recommend you DO NOT pip or conda install MGLTools as it uses an outdated python package and creates issues with enviroments.
    The best way to install this is to download the latest release of the command-line version (NOT THE GUI VERSION) of MGLTools from: 
            http://mgltools.scripps.edu/downloads . 
    Once the command-line version of MGLTools package has been downloaded follow example installation provided below, which uses a Linux system
    with the 1.5.6 version of MGLTools.
        1) Extract files by unzipping/untar the package:
            tar -xvf $PATH/mgltools_x86_64Linux2_1.5.6.tar.gz
        2) Go to the extract folder:
            cd  $PATH/mgltools_x86_64Linux2_1.5.6
        3) Run the installation script and make sure MGLToolsPckgs is unpacked:
            bash install.sh
            #if $PATH/mgltools_x86_64Linux2_1.5.6/MGLToolsPckgs/ is not a folder manually unzip/untar MGLToolsPckgs.tar.gz
            tar -xvf $PATH/mgltools_x86_64Linux2_1.5.6/MGLToolsPckgs.tar.gz

        4) Click 'OK' to the licensing agreement. Please note MGLTools is free for academic use but may require a license for commerical usage.
            -This should open automatically
        5) Find pathing for AutoGrow variable (see Additional pathing Instructions below)

####    Additional pathing Instructions:
    To use MGLTools to convert files, AutoGrow requires the path to the MGLTools directory.
        The path can be found by 
            1) going to the extract folder:
                >>> cd  $PATH/mgltools_x86_64Linux2_1.5.6
            2) use pwd function in bash
                >>> pwd
                    $PATH/mgltools_x86_64Linux2_1.5.6/
                The output string will be the absolute path to the MGLTools directory.

    The installed MGLTools directory is provided to Autogrow using the variable: --mgltools_directory
        python RunAutogrow.py .. --mgltools_directory $PATH/mgltools_x86_64Linux2_1.5.6 ...
    On Linux and MacOS machines, Autogrow will autolocate three important file paths based on mgltools_directory:
        -prepare_ligand4.py     mgltools_directory + /MGLToolsPckgs/AutoDockTools/Utilities24/prepare_ligand4.py
        -prepare_receptor4.py   mgltools_directory + /MGLToolsPckgs/AutoDockTools/Utilities24/prepare_receptor4.py
        -mgl_python             mgltools_directory + /bin/pythonsh
    If running a Windows OS (not fully supported by this version of Autogrow) please provide those pathings to AutoGrow manually:
        python RunAutogrow.py .. \
        --mgltools_directory $PATH\mgltools_win32_1.5.6\ \
        --prepare_ligand4.py $PATH\mgltools_win32_1.5.6\ \
        --prepare_receptor4.py $PATH\mgltools_win32_1.5.6\ \
        --mgl_python $PATH\mgltools_win32_1.5.6\ + $PATH\TO\pythonsh ...

    If one wants to provide a custom pathing to these location, providing these variables at the commandline will override any autolocation.

### obabel: (Optional: *must use either MGLTools, obabel, or a custom file converter/docking software)
    Openbabel citations:
        - N M O'Boyle, M Banck, C A James, C Morley, T Vandermeersch, and G R Hutchison. "Open Babel: An open chemical toolbox." J. Cheminf. (2011), 3, 33. DOI:10.1186/1758-2946-3-33
        - The Open Babel Package, version 2.3.1 http://openbabel.org (accessed Oct 2011)

    obabel is a commandline tool for cheminformatic file conversion. It is used by AutoGrow to convert .pdb files to .pdbqt format.
        -.pdbqt format is required by Vina type docking programs including Autodock Vina and QuickVina2
        -An alternative conversion option is MGLTools.
            
####    Installation:
    Quick install (Linux/Mac OS) - An easy installation on Linux machines is:
        sudo apt-get install openbabel
        sudo apt-get update

    Full instructions for obabel installation can be found on their site: https://openbabel.org/docs/dev/Installation/install.html
    AutoGrow 4.0.0 has been tested with obabel version 2.4.1
            
            
####    Additional pathing Instructions:
    To use obabel to convert files, AutoGrow requires the path to the obabel executable. 
    Once installed the path to the obabel executable can be found by running:
        >>> which obabel
            $PATH/obabel
    This path should be provided to AutoGrow using the --obabel_path variable:
        python RunAutogrow.py .. --obabel_path $PATH/obabel ...

    
### Python APIs: (Required)
    AutoGrow requires multiple python API libraries to function. 
        
####    Pythonic APIs: (APIs which automatically come installed with python)
    Most of the required python API libraries come preinstalled in most python installations.
        The following APIs should not require additional installations:
            __future__ ,  math,  shutil, ,  textwrap,  collections,  string,  multiprocessing,  gzip,  
            time,  copy,  json,  itertools,  subprocess,  platform,  os,  warnings,  operator,  
            webbrowser,  pickle,  importlib,  unittest,  sys,  glob,  datetime,  io,  random ,  argparse
####    Python APIs requiring installation: 
    The following libraries need to be installed into the enviroment for AutoGrow to run. Most can be installed via conda or pip.

#####       Mandatory installations:
    RDKit: Cheminformatic library
        RDKit can be downloaded via conda/pip. To install using conda use the command:
            conda install -c rdkit rdkit   
        We use the following RDKit sublibraries in AutoGrow:
            import rdkit
            from rdkit import RDLogger, Chem, DataStructs
            from rdkit.Chem import MolSurf, Crippen, rdFMCS, Descriptors, AllChem, FilterCatalog,  Lipinski, rdDepictor
            from rdkit.Chem.Draw import PrepareMolForDrawing, rdMolDraw2D
            from rdkit.Chem.rdMolDescriptors import GetMorganFingerprint
            from rdkit.Chem.FilterCatalog import FilterCatalogParams
            from rdkit.Chem.rdchem import BondStereo

    NumPy: mathematical functions
        NumPy can be downloaded via conda/pip. It can be conda installed using the command:
            conda install -c anaconda numpy
        AutoGrow has been tested using numpy version 1.15.0
        
    SciPy: mathematical functions
        SciPy can be downloaded via conda/pip. It can be conda installed using the command:
            conda install -c anaconda scipy
        AutoGrow has been tested using scipy version 1.1.0

    Matplotlib: python graphing tool
        Matplotlib can be downloaded via conda/pip. It can be conda installed using the command:
            conda install matplotlib
        AutoGrow has been tested using Matplotlib version 3.0.2

    func_timeout: a pythonic timeout tool
        func_timeout can be downloaded via pip. It can be pip installed using the command:
            pip install func-timeout
        AutoGrow has been tested using func_timeout version 4.3.5

#####       Optional installations: The following APIs are only required for users using mpi multithreading.
    mpi4py: mpi multithreading python library

        This may require a preinstallation of mpich which can be installed by running:
            sudo apt install mpich
            
        mpi4py can be downloaded via conda/pip. It can be conda installed using the command:
            conda install -c anaconda mpi4py

    AutoGrow has been tested using mpi4py version 3.0.1
    
    AutoGrow reqires mpi4py version 2.1.0 and higher. To check version:
        1) open a python window.
        2) enter into the window:
            >>> import mpi4py
            >>> mpi4py.__version__
                3.0.1

### MPI dependencies:
    To run jobs in mpi mode we require an additional installation of the python library mpi4py,
    as well as an MPI-enabled computer environment. OpenMPI was used by the authors. 

    OpenMPI installation instructions can be found: http://lsi.ugr.es/jmantas/pdp/ayuda/datos/instalaciones/Install_OpenMPI_en.pdf
        Quick setup installation can be done by running in a bash terminal:
            sudo apt-get install openmpi-bin openmpi-common openssh-client openssh-server libopenmpi1.3 libopenmpi-dbg libopenmpi-dev

    Establishing a fully MPI-enabled computer network is complicated and should only be attempted by qualified technicians. 
        -The authors used an Intel’s Omni-Path communication architecture that was established by experts at the University of Pittsburgh’s Center for Research Computing 
        -Authors DO NOT RECOMMEND ATTEMPTING THIS ON YOUR OWN.
### Pre-Installed Dependencies:
    AutoGrow 4.0.0 comes with several dependencies which are preinstalled, requiring no additional effort by the user.
    These softwares are licensed to be freely redistributed and should run without problems. 
    Maintaining AutoGrow is work and we will do our best to keep AutoGrow current as these dependencies advance, but 
    we appreciate any messages on how to keep it current. If a dependency updates please feel free to contact us and we will do our best to make our code future-compatible.
    
#### Preinstalled software:
##### Docking programs:
    AutoGrow 4.0.0 comes preinstalled with two docking programs:
        -Autodock Vina 1.1.2 (packaged with executables for Linux, MacOS, and Windows)
            -Version:   1.1.2
            -Location:  $PATH/autogrow4/autogrow/Docking/Docking_Executables/Vina/
            -Citation:  Trott, O., & Olson, A. J. (2010). AutoDock Vina: improving the speed and accuracy of docking with a new scoring function, efficient optimization, and multithreading. Journal of computational chemistry, 31(2), 455–461. doi:10.1002/jcc.21334
            -License:   Apache version 2

        -QuickVina2.1 (compatible with Linux OS)
            -Version:   2.1
            -Location:  $PATH/autogrow4/autogrow/Docking/Docking_Executables/QVina02/
            -Citation:  Amr Alhossary, Stephanus Daniel Handoko, Yuguang Mu, and Chee-Keong Kwoh. Bioinformatics (2015) 31 (13): 2214-2216. [DOI:10.1093/bioinformatics/btv082](https://doi.org/10.1093/bioinformatics/btv082)
            -License:   Apache version 2

    These softwares can be found within the directory $PATH/autogrow4/autogrow/Docking/Docking_Executables/


    AutoGrow allows users to provide custom docking software. 
    This could be as simple as using a different version of Autodock Vina:
        Example: python RunAutogrow.py ... --docking_executable $PATH/TO/Autodock_Vina_version_X_executable
    Or
    A slightly more involved incorporation of a completely new docking software type:
        Details for custom docking suites are provided below in the section "Providing Custom options"

##### Scoring/Rescoring programs:
    NNScore 1 and NNScore 2 are free and open-source programs that are distributed with AutoGrow.
    Both NNScore1 and NNScore2 reassess ligand docking. They were trained using Autodock Vina 1.1.2 so
    to use these programs we require the docking be performed using Autodock Vina 1.1.2.
    
    AutoGrow allows users to provide custom Scoring/Rescoring software. 
        Details for custom Scoring/Rescoring suites are provided below in the section "Providing Custom options"

    -NNScore 1: 
        -Version:   1.1
        -Location:  $PATH/autogrow4/autogrow/Docking/Scoring/NNScore_exe/nnscore1/
        -Citation:  NNScore: A Neural-Network-Based Scoring Function for the Characterization of Protein-Ligand Complexes. Jacob D. Durrant, J. Andrew McCammon. Journal of Chemical Information and Modeling, 2010, 50 (10), pp 1865-1871.
        -License:   GNU General Public version 3
    -NNScore 2: 
        -Version:   2.02
        -Location:  $PATH/autogrow4/autogrow/Docking/Scoring/NNScore_exe/nnscore2/
        -Citation:  NNScore 2.0: A Neural-Network Receptor–Ligand Scoring Function. Jacob D. Durrant, Andrew McCammon. Journal of Chemical Information and Modeling, 2011, 51 (11), pp 2897-2903.
        -License:   GNU General Public version 3

##### SMILES Conversion to 3D and protanation adjustments:
    AutoGrow 4.0.0 performs most of its ligand handling using 2D SMILES. 
    AutoGrow 4.0.0 uses the free and open-source program Gypsum-DL to convert from SMILES to 3D SDF format.
    Gypsum_dl is prepackaged in AutoGrow 4.0.0. Gypsum_dl also prepackages two software packages: MolVS and Dimorphite-DL.

    -Gypsum_dl: 
        -Version:   1.1.1
        -Location:  $PATH/autogrow4/autogrow/Operators/ConvertFiles/gypsum_dl/
        -Citation:  Ropp PJ, Spiegel JO, Walker JL, Green H, Morales GA, Milliken KA, Ringe JJ, Durrant JD. Gypsum-DL: An Open-Source Program for Preparing Small-Molecule Libraries for Structure-Based Virtual Screening. J Cheminform. 11(1):34, 2019. [PMID: 31127411] [doi: 10.1186/s13321-019-0358-3]
        -License:   Apache version 2.0
    -Dimorphite_dl: 
        -Version:   1.2.2
        -Location:  $PATH/autogrow4/autogrow/Operators/ConvertFiles/gypsum_dl/gypsum_dl/Steps/SMILES/dimorphite_dl
        -Citation:  Ropp PJ, Kaminsky JC, Yablonski S, Durrant JD (2019) Dimorphite-DL: An open-source program for enumerating the ionization states of drug-like small molecules. J Cheminform 11:14. doi:10.1186/s13321-019-0336-9.
        -License:   Apache version 2.0
    -MolVS: 
        -Version:   v0.1.1 2019 release
        -Location:  $PATH/autogrow4/autogrow/Operators/ConvertFiles/gypsum_dl/gypsum_dl/molvs
        -Citation:  https://molvs.readthedocs.io; Take from https://github.com/mcs07/MolVS
        -License:   MIT License

#
## Running AutoGrow:
    AutoGrow 4.0.0 is run using the python script RunAutogrow.py located in the top directory of the download AutoGrow project.
    Autogrow is a commandline operated python program. It has two options for job submission:
     1) commandline submission: executing directly from the commandline.
         Example:
             cd $PATH/autogrow/

             python RunAutogrow.py \
                 --filename_of_receptor $PATH/autogrow4/autogrow/tutorial/PARP/4r6e_removed_smallmol_aligned_Hs.pdb \
                 --center_x -70.76 --center_y  21.82 --center_z 28.33 \
                 --size_x 25.0 --size_y 16.0 --size_z 25.0 \
                 --source_compound_file $PATH/autogrow4/autogrow/source_compounds/naphthalene_smiles.smi \
                 --root_output_folder $PATH/output_directory/ \
                 --number_of_mutants_first_generation 50 \
                 --number_of_crossovers_first_generation 50 \
                 --number_of_mutants 50 \
                 --number_of_crossovers 50 \
                 --top_mols_to_seed_next_generation 50 \
                 --number_elitism_advance_from_previous_gen 50 \
                 --number_elitism_advance_from_previous_gen_first_generation 10 \
                 --diversity_mols_to_seed_first_generation 10 \
                 --diversity_seed_depreciation_per_gen 10 \
                 --num_generations 5 \
                 --mgltools_directory $PATH/mgltools_x86_64Linux2_1.5.6/ \
                 --number_of_processors -1 \
                 --scoring_choice VINA \
                 --Lipinski_Lenient \
                 --start_a_new_run \
                 --rxn_library ClickChem \
                 --selector_choice Rank_Selector \
                 --dock_choice VinaDocking \
                 --max_variants_per_compound 5 \
                 --redock_elite_from_previous_gen False \
                 --generate_plot True \
                 --reduce_files_sizes True \
                 --use_docked_source_compounds True \
                 >  $PATH/OUTPUT/text_file.txt 2>  $PATH/OUTPUT/text_errormessage_file.txt
     2) json file submission: store variables for AutoGrow in a .json file
         Example:
             cd $PATH/autogrow/   
             python RunAutogrow.py -j $PATH/json_file_with_variable.json

     Examples of the json files can be found in the tutorial folder.
#
## Understanding Autogrow parameters:
    A explanation of every parameter can be retrieved by running:
        python $PATH/autogrow4/RunAutogrow.py --help
    
#
## Docker submission: For Windows users
    @@@@@@@@@JAKE Fill in with how to use once it has been included
#
## Providing Custom options:
    AutoGrow was designed to be modular. This allows for the easy swaping of code.
    AutoGrow is to be a living codebase so if you have added good custom code and would like to make it open source. please contact the authors so that we can grow the user options.

    Many of the AutoGrow functions can be supplemented with custom options. These functions include:
        1) Custom ligands filters ***
        2) Custom docking code ***
        3) Custom ligand conversion code from PDB to dockable format (ie PDBQT) ***
        4) Custom Scoring/Rescoring code ***
        5) Custom Reaction libraries
        6) Custom complimentary molecules libraries
    
    *** Indicates that when using this feature the code is automatically copied into the 
        directory that is required to house that code. This is only done once so please unittest
        the code prior to incorporating it into AutoGrow. A print message will indicate where the file is
        copied to. That file can be manually deleted or overwritten by the user.
        AutoGrow will need to be restarted after the custom files have been copied into the proper locations. After that the new script should be able intergrated into AutoGrow.
        AutoGrow ASSUMES ALL CUSTOM CODE HAS BEEN TESTED AND FUNCTIONS WITH SPECIFIED I/O 
            -ie) AutoGrow assumes that scoring favors the most negative docking score; 
                    -AutoGrow will continue to assume all custom Scoring scripts set the most fit score to the most negative for all metrics besides diversity.
                    -It also assumes in ranked .smi files that the last column is the diversity fitness
                        and assumes the second to last column to be the metric for "docking/rescored" fitness. 
                    -If a custom script scores ligands such that the most fit ligand has the highest score,
                         Autogrow may inadvertently be favoring ligands that are least fit.  

### 1) Custom ligands filters: ***
    This feature allows the user to incorporate custom python scripts for filtering ligands.
    These filters are applied to ligands after they are created by Mutation/Crossover 
    but before Gypsum_dl conversion to 3D.

    This custom code will be copied to the directory: $PATH/autogrow4/autogrow/Operators/Filter/Filter_classes/FilterClasses/
#####   Script formating:
    These filters use a class-based inheritance architecture which require:
    1) Filter must be instanced off of the ParentFilterClass located:
        - $PATH/autogrow4/autogrow/Operators/Filter/Filter_classes/ParentFilterClass.py
    2) Have a unique name: class unique_name(ParentFilter)
        -unique_name cannot be one of the predefined filters
    3) Must have at least one function called run_filter
        -run_filter takes a single variable which must be an rdkit molecule object

#####   Running custom Filters:
    Example shown is to submit multiple custom filters:
        alternative_filter [["custom_filter_1","$PATH/custom_filter_1.py"],["custom_filter_2","$PATH//custom_filter_2.py"]]
    To sumbit for a single custom filter it should be:
        alternative_filter [["custom_filter_1","$PATH/custom_filter_1.py"]]
        
    Submission through .json format: 

        {
            ... ,
            "alternative_filter": [["custom_filter_1","$PATH/custom_filter_1.py"],["custom_filter_2","$PATH/custom_filter_2.py"]]
        }

        python RunAutogrow.py -j $PATH/To/json_file_with_variable.json


    Commandline submission format: 
        python RunAutogrow.py \
            ... \
            --alternative_filter [["custom_filter_1","$PATH/custom_filter_1.py"],["custom_filter_2","$PATH/custom_filter_2.py"]]
    # 
### 2) Custom docking code: ***
    This feature allows the user to incorporate custom python scripts for docking ligands.
    Currently AutoGrow is configured to dock using Autodock Vina and QuickVina2, but AutoGrow is not limited to these docking softwares.
    A custom script can be added to run docking using virtually any software. 

    This custom code will be copied to the directory: $PATH/autogrow4/autogrow/Docking/Docking_Class/DockingClassChildren/
#####   Script formating:    
    These docking scripts use a class-based inheritance architecture which require:
    1) Docking class object must be instanced off of the ParentDocking located:
        - $PATH/autogrow4/autogrow/Docking/Docking_Class/ParentDockClass.py
    2) Have a unique name: class unique_name(ParentDocking)
        -unique_name can not be one of the predefined docking scripts (currently just VinaDocking and QuickVina2Docking)
    3) Must have atleast have three functions following the below formating:
        -def __init__(self, vars=None, receptor_file=None, test_boot=True):
            """
            get the specifications for ligand assessment/docking from vars
            load them into the self variables we will need
            and convert the receptor to the proper file format (ie pdb-> pdbqt)

            Inputs:
            :param dict vars: Dictionary of User variables
            :param str receptor_file: the path for the receptor pdb
            :param bool test_boot: used to initialize class without objects for testing purpose
            """
        
        
        -def run_dock(self, pdbqt_filename):
            """
            this function runs the docking. Returns None if it worked and the name if it failed to dock.

            Inputs:
            :param str pdbqt_filename: the pdbqt file of a ligand to dock and score    
                        if using a docking software that use a file format other than pdbqt please substitute that file here     
            Returns:
            :returns: str smile_name: name of smiles if it failed to dock
                                    returns None if it docked properly
            """


        -def rank_and_save_output_smi(self, vars, current_generation_dir, current_gen_int, smile_file, deleted_smiles_names_list):
            """
            Given a folder with PDBQT's, rank all the SMILES based on docking score (High to low).
            Then format it into a .smi file.
            Then save the file.

            Inputs:
            :param dict vars: vars needs to be threaded here because it has the paralizer object which is needed within Scoring.run_scoring_common
            :param str current_generation_dir: path of directory of current generation
            :param int current_gen_int: the interger of the current generation indexed to zero
            :param str smile_file:  File path for the file with the ligands for the generation which will be a .smi file
            :param list deleted_smiles_names_list: list of SMILES which may have failed the conversion process

            Return:
            :returns: str output_ranked_smile_file: the path of the output ranked .smi file
            """
#####   Running custom Docking scripts:
        
    Please note using a new docking software will likely also require custom conversion script 
    and scoring scripts. Documentation for these is provided in the next two subsections. The example below ignores these extras.

    AutoGrow will need to be restarted once after this has been incorporated into the code base.

    Submission through .json format: 

        {
            ...
            "docking_executable": "$PATH/To/executable/for/custom_docking",
            "dock_choice": "Custom",
            "custom_docking_script": ["custom_docking", "$PATH/To/class_object/for/custom_docking.py"]
        }

        python RunAutogrow.py -j $PATH/To/json_file_with_variable.json


    Commandline submission format: 
        python RunAutogrow.py \
            ... \
            --docking_executable "$PATH/To/executable/for/custom_docking" \
            --dock_choice Custom \
            --alternative_filter ["custom_docking", "$PATH/To/class_object/for/custom_docking.py"]

### 3) Custom ligand conversion code from PDB to dockable format (ie PDBQT) ***
    If using a docking software other than VINA/QuickVina is being used, one may need to convert the pdb format ligands into a different format or it may take .pdb files.
    If taking a format other than .pdbqt users will need to provide a custom script to convert ligands (or simply do nothing if it takes .pdbs).

    This custom code will be copied to the directory: $PATH/autogrow4/autogrow/Docking/Docking_Class/DockingClassChildren/
#####   Script formating:    
    These conversion scripts use a class-based inheritance architecture which require:
    1) Conversion class object must be instanced off of the ParentPDBQTConverter located:
        - $PATH/autogrow4/autogrow/Docking/Docking_Class/ParentPDBQTConverter.py
    2) Have a unique name: class unique_name(ParentPDBQTConverter)
        -unique_name can not be one of the predefined docking scripts 
        Currently files named: Convert_with_MGLTOOLS.py and Convert_with_obabel.py
        Classes named obabel_Conversion and MGLTools_Conversion

    3) Must have atleast have two functions following the below formating:
            # def convert_receptor_pdb_files_to_pdbqt(self, receptor_file, mgl_python, receptor_template, number_of_processors):
            #     """
            #     Make sure a PDB file is properly formatted for conversion to pdbqt
                
            #     Inputs:
            #     :param str receptor_file:  the file path of the receptor
            #     :param str mgl_python: file path of the pythonsh file of mgl tools
            #     :param str receptor_template: the receptor4.py file path from mgl tools.
            #     :param int number_of_processors: number of processors to multithread
            #     """
            #     raise NotImplementedError("convert_receptor_pdb_files_to_pdbqt() not implemented")
            # #

            # def convert_ligand_pdb_file_to_pdbqt(self, pdb_file):
            #     """
            #     Convert the ligands of a given directory from pdb to pdbqt format
                
            #     Inputs:
            #     :param str pdb_file: the file name, a string.
            #     Returns:
            #     :returns: bool bool: True if it worked; 
            #                         False if its the gypsum param file or if it failed to make PDBQT
            #     :returns: str smile_name: name of the SMILES string from a pdb file
            #                                 None if its the param file 
            #     """
            #     raise NotImplementedError("rank_and_save_output_smi() not implemented")
            #

            
#####   Running custom conversion scripts:

    AutoGrow will need to be restarted once after this has been incorporated into the code base.

    Submission through .json format: 

        {
            ...
            "conversion_choice": "Custom",
            "custom_conversion_script": ["custom_conversion", "$PATH/To/class_object/for/custom_conversion.py"]
        }

        python RunAutogrow.py -j $PATH/To/json_file_with_variable.json

    Commandline submission format: 
        python RunAutogrow.py \
            ... \
            --conversion_choice Custom \
            --custom_conversion_script ["custom_conversion", "$PATH/To/class_object/for/custom_conversion.py"]


### 4) Custom Scoring/Rescoring code ***
    This feature allows the user to incorporate custom python scripts for scoring and rescoring ligands.
    Currently AutoGrow is configured to dock using Autodock Vina and QuickVina2 and there are two provided options to rescore a ligand
    using either NNScore 1 or NNScore 2. Additionally, ligand efficiency (dividing the score/rescore value by the number of non-Hydrogen atoms)
    can be applied with any float based scoring value.
    
    Users can incorporate custom scoring and rescoring options into AutoGrow. 
    
    This custom code will be copied to the directory: $PATH/autogrow4/autogrow/Docking/Scoring/Scoring_classes/
#####   Script formating:    
    These conversion scripts use a class-based inheritance architecture which require:
    1) Conversion class object must be instanced off of the ParentScoringClass located:
        - $PATH/autogrow4/autogrow/Docking/Scoring/Scoring_classes/ParentScoringClass.py
    2) Have a unique name: class unique_name(ParentScoringClass)
        -unique_name can not be one of the predefined docking scripts 
        Currently files named: VINA.py, NN1.py, NN2.py, and Lig_Efficiency.py
        Classes named VINA.py, NN1, NN2, and Lig_Efficiency
    3) Must have atleast have two functions following the below formating:
            # def get_name(self):
            #     """
            #     Returns the current class name.    
            #     Returns:
            #     :returns: str self.__class__.__name__: the current class name.
            #     """
            #     return self.__class__.__name__
            # #
            # def run_scoring(self, input_string):
            #     """
            #     run_scoring is needs to be implimented in each class.
            #     Inputs:
            #     :param str input_string:  A string to raise an exception
            #     """
            #     raise NotImplementedError("run_scoring() not implemented")

#####   Running custom scoring/rescoring scripts:
        
    AutoGrow will need to be restarted once after this has been incorporated into the code base.

    Submission through .json format: 

        {
            ...
            "scoring_choice": "Custom",
            "custom_scoring_script": ["custom_scoring_name", "$PATH/To/class_object/for/custom_scoring.py"]
        }

        python RunAutogrow.py -j $PATH/To/json_file_with_variable.json

    Commandline submission format: 
        python RunAutogrow.py \
            ... \
            --conversion_choice Custom \
            --custom_conversion_script ["custom_scoring_name", "$PATH/To/class_object/for/custom_scoring.py"]

    # 
### 5) Custom Reaction libraries

    AutoGrow assumes all custom scripts have been unittested by its creators. Please ensure all
    reactions and libraries are accurate before using this option.
    
    Unlike the other custom options, reaction libraries are stored in human readable json dictionaries;
        all other custom options use inherited class scripts. 
    These json files do not need to be incorporated into AutoGrow and thus require no restarting or copying of files.

    Reaction Libraries are stored in .json files and are dictionaries of dictionaries.
    The outer dictionary uses the reaction's name as the key and the subdictionary contiaining all information
    about the reaction as the item. 

    If using this you will need three pieces of information each explained below:
        
#####    Three requirments for custom Reaction libraries:
######   1) Reaction library .json file: Contains reactions and all reaction information
 

    Each subdictionary must contain the following information:
        "reaction_name": "Name of the reaction",
        "example_rxn_product": "SMILES of Product using example example_rxn_reactants", 
        "example_rxn_reactants": ["SMILES of example reactant_1"], # if two or more reactants in reaction ["SMILES of example reactant_1","SMILES of example reactant_2",...]
        "functional_groups": ["functional group name reactant_1"], # if two or more reactants in reaction ["functional group name reactant_1","functional group name reactant_2",...]
        "group_smarts": ["functional_group SMARTS reactant_1"],# if two or more reactants in reaction ["functional_group SMARTS reactant_1","functional_group SMARTS reactant_2",...]
        "num_reactants": 1, # (int) if 2 or more reactants change accordingly
        "reaction_string": "reaction string ie reactant_1_smart.reactant_2_smart>>product_SMART", # This uses Daylights SMARTS reaction notation
        "RXN_NUM": 3 # (int) a unique reaction number. This is used in naming products of mutation: ie ) a ligand named Gen_1_Mutant_72_867328 is a ligand from generation 1 created by the 72 reaction in a reaction library

    An example libraries can be found: 

        autogrow4/autogrow/Operators/Mutation/SmileClickChem/SmileClickChem/Reaction_libraries/All_Rxns/All_Rxns_rxn_library.json
        autogrow4/autogrow/Operators/Mutation/SmileClickChem/SmileClickChem/Reaction_libraries/ClickChem/ClickChem_rxn_library.json
        autogrow4/autogrow/Operators/Mutation/SmileClickChem/SmileClickChem/Reaction_libraries/Robust_Rxns/Robust_Rxns_rxn_library.json            
    
    Reaction libraries identify ligands capable of reacting in a given reaction using the information
    found in the subdictionary's items "functional_groups" and "group_smarts". 

######   2) Functional group library .json file: simple json diction containing each functional group and its SMARTS definition.
    Functional group library are simple dictionaries of the functional groups used by a reaction library.
    Every moiety used by the reaction library must have an entry in the Functional group library.
    
    Functional group library are formated as such:
        {
            "Acid_Anhydride_Noncyclic": "[*]C(=O)-[O;R0]-C(=O)[*]",
            "Alcohol": "[#6&$([CR0,R1X3,R1X4])&!$([#6](=,-[OR0,SR0])[OR0])]-[OR0;H1,-]",
            "Alkene": "[CR0;X3,X2H1,X1H2]=[CR0;X3,X2H1,X1H2]",
            "Alkyne": "[CR0;X2,X1H1]#[CR0;X2,X1H1]",
            "Amine_2R":  "[#7;$([#7;H3+,H2R0X1]-[#6]),$([#7&!H3;H1R1X3](:,-[#6R1]):,-[#6R1,#7R1]),$([#7&!H3;H2]-[#6]),$([#7&!H3;H0R1X2](:,-[#6R1;X3H1]):,-[#6R1X3H1]),$([#7&!H3;H0R1X2](:,-[#6R1;X3]):,-[#7R1X3]),$([#7&!H3;H1R0X3](-[#6])-[#6R0])]", 
            "Azide_1R": "[*;#6]-[$(N=[N+]=[N-]),$([N-][N+]#N)]",
            "Carbonochloridate": "Cl[C;X3](=O)-O[*]",
            "Carboxylate": "[*;!O]-[$([CR0;X3](=[OR0&D1])[OR0&H1]),$([CR0;X3](=[OR0&D1])[OR0-])]",
            "Epoxide": "[CR1;H2,H1X4,H0X4]1O[CR1;H2,H1X4,H0X4]1",
            "Ester": "[*;#6]C(=O)-O[*]",
            "Halide": "[Cl,Br,I][$([CX4,c]),$([#6X3]=[O,S])]",
            "Isocyanate": "[#6]N=C=O",
            "Isothiocyanate": "[#6]N=C=S",
            "Primary_Amine_1R": "[#7;$([H3+]),$([H2R0;!+])]-[#6]",
            "Sulfonyl_Azide": "[*]S(=O)(=O)-[$(N=[N+]=[N-]),$([N-][N+]#N)]",
            "Thio_Acid": "[C]-[$([CX3R0]([S;H1,X1])=[OX1]),$([CX3R0]([O;H1,X1])=[SX1])]",
            "Thiol_1R": "[#6&$([CR0,R1X3,R1X4])&!$([#6](=,-[OR0,SR0])[SR0])]-[SR0;H1,-]"
        }
    Examples can be found: 

        autogrow4/autogrow/Operators/Mutation/SmileClickChem/SmileClickChem/Reaction_libraries/All_Rxns/All_Rxns_functional_groups.json
        autogrow4/autogrow/Operators/Mutation/SmileClickChem/SmileClickChem/Reaction_libraries/ClickChem/ClickChem_functional_groups.json
        autogrow4/autogrow/Operators/Mutation/SmileClickChem/SmileClickChem/Reaction_libraries/Robust_Rxns/Robust_Rxns_functional_groups.json

    The SMARTS strings provided in this file should also be present in each subdirctionary of the Reaction library .json file
    that references that functional group, 
    placing the name of the group in the list of functional group names of reactants found under subdictionary key "functional_groups" 
            and 
    placing the SMARTS string of the group in the list of functional group SMARTS of reactants found under subdictionary key "group_smarts" 


######   3) Directory of complimentary molecule libraries: directory of .smi files
    Any reaction containing more than one reactant will require a complimentary molecule to suppliment the reaction.
    For this reason we require a directory populated with .smi files containing small molecules that match each functional group.

    The name of each .smi file should be the name of the functional group (the keys of the Functional group library .json file) +.smi
        Example the .smi file for the functional group "Acid_Anhydride_Noncyclic" should be $PATH/complimentary_mol_directory/Acid_Anhydride_Noncyclic.smi

    THERE MUST BE ONE ENTRY PER FUNCTIONAL GROUP. NAMES ARE CAP SENSITIVE.

####    Important formating notes about the .smi file for complimentary_mol_directory:
        1) No headers are allowed in the file.                 
        2) .smi files can be either tab or 4-space delineated. 
        3) The only columns are the 1st two columns.
            Column 1: SMILES string
            Column 2: ligand name/identifier (1 WORD, NO SPACES)
    
    We strongly recommend thoroughly checking that each molecule in each library matches the intended functional group.
    If a ligand does not match the inteded functional group the reaction will fail and it will slow the process of mutant creation.

    
####    Running Custom reactions:

    Running a custom reaction library requires 4 parameters to be set:
        rxn_library, rxn_library_file, function_group_library, complimentary_mol_directory

    Submission through .json format: 

        {
            ...
            "rxn_library": "Custom",
            "rxn_library_file": "$PATH/To/rxn_library_file.json",
            "function_group_library": "$PATH/To/function_group_library.json",
            "complimentary_mol_directory": "$PATH/To/complimentary_mol_directory/",
        }

        python RunAutogrow.py -j $PATH/To/json_file_with_variable.json

    Commandline submission format: 
        python RunAutogrow.py \
            ... \
            --rxn_library Custom \
            --rxn_library_file $PATH/To/rxn_library_file.json \
            --function_group_library $PATH/To/function_group_library.json \
            --complimentary_mol_directory $PATH/To/complimentary_mol_directory/ 
    # 
### 6) Custom Complimentary molecule libraries for Mutation:
    One can provide custom libraries of molecules to suppliment reactions by using the --complimentary_mol_directory option.

    This can be used in conjunction with any of the predefined reactions sets (ie ClickChem, Robust_Rxns, All_Rxns), but this requires that
    all functional groups used by those reaction libraries have a .smi file contained within the custom complimentary_mol_directory
    
        
    We strongly recommend thoroughly checking that each molecule in each library matches the intended functional group.
    If a ligand does not match the inteded functional group the reaction will fail and it will slow the process of mutant creation.

    THERE MUST BE ONE ENTRY PER FUNCTIONAL GROUP. NAMES ARE CAP SENSITIVE.

####    Important formating notes about the .smi file for complimentary_mol_directory:
    1) No headers are allowed in the file.                 
    2) .smi files can be either tab or 4-space delineated. 
    3) The only columns are the 1st two columns.
        Column 1: SMILES string
        Column 2: ligand name/identifier (1 WORD, NO SPACES)

####    Running Custom reactions:

    Submission through .json format: 

        {
            ...
            "complimentary_mol_directory": "$PATH/To/complimentary_mol_directory/",
        }

        python RunAutogrow.py -j $PATH/To/json_file_with_variable.json

    Commandline submission format: 
        python RunAutogrow.py \
            ... \
            --complimentary_mol_directory $PATH/To/complimentary_mol_directory/ 
# 

## Prepping Receptor:
    Autogrow takes a single .pdb file for the receptor. Although not required we recommend doing some preparation
    to the receptor file prior to submitting to Autogrow. 
### 1) Remove all ligands, water, or non-protein atoms. This can be done in a PDB viewer such as Pymol or VMD.
    - If drugs are already bound to target pocket, one may want to use that ligand to define the pocket prior to removing it.
### 2) Remove chains not being tested. 
    -ie. Many protein structures contains multiple protein chains and even multiple proteins. 
    We recommend removing all chains you are not explicitly testing.
    This can be done in a PDB viewer such as Pymol or VMD.
### 3) Adjust protonation of the receptor to the appropriate pH. Crystal structures are often not at biologically relavent pH.
    More accurate scoring requires proper protonation. This can be done using the program PDB2PQR. This can be accessed via 
    the webserver http://nbcr-222.ucsd.edu/pdb2pqr_2.0.0/
    -If you use the PDB2PQR to protonate the receptor, you will need to convert it back to pdb.
        -To convert back we recommend obabel.
        obabel:
            # Installation instructions for obabel are provided in the Dependencies section.

            # Convert PQR to PDB via obabel
            obabel -ipqr PATH/PQR_FILE.pqr -opdb -O PATH/PDB_OUTPUT_FILE.pdb

### 4) Determine and define the binding pocket:
    Docking software such as Vina and QuickVina require 6 float parameters to define a binding pocket:
        coordinates: The center of the pocket location in x,y,z axis
            center_x,center_y,center_z
        dimensions: The distance from the center of the pocket which will be considered part of the pocket in x,y,z axis
            size_x, size_y, size_z

    Autogrow requires all 6 parameters to run the docking portion of the code.
    
    To determine these we recommend using the python API library scoria:
        Citation Scoria: Ropp, P., Friedman, A., & Durrant, J. D. (2017). Scoria: a Python module for manipulating 3D molecular data. Journal of cheminformatics, 9(1), 52. doi:10.1186/s13321-017-0237-8

        Installation of Scoria:
            Scoria can be installed either by pip installation or manual download. 
            We recommend pip installation:
                pip install scoria
            Details for downloading the program can be found:
                -Download scoria from https://durrantlab.pitt.edu/scoria/
        Once Scoria is installed:
        1) Manually inspect the pocket of your protein in a protein visualizer such as Pymol, Chimera, or VMD.
            -Pick out 3 to 6 residues which will be used to define the protein pocket.
            - For the AutoGrow 4.0.0 publication we used Chain A of the PARP-1 catayltic domain xray structure 4r6e.
                The selected residues used to define the pocket were:
                        763, 872, 888, 907, 988

        2) Determine the geometric center of the pocket with Scoria's get_geometric_center function in python.
            In a python terminal or in a jupyter notebook environment: 
                # Import the scoria API
                >> import scoria
                >> 
                # define your protein pdb file
                # The protein pdb file used for the publication can be found at: $PATH/autogrow4/autogrow/tutorial/PARP/4r6e_removed_smallmol_aligned_Hs.pdb
                >> pdb_file = "$PATH/OF/PDB_FILE.pdb"

                # create a scoria mol object from the protein pdb file
                >> mol = scoria.Molecule(pdb_file)

                # select which residues are going to be used to define pocket with resseq (the residue number)
                >> sel = mol.select_atoms({"resseq":[763, 872, 888, 907, 988]})
                
                # get geometric center of the protein pocket
                >> geometric_center = mol.get_geometric_center(sel)
                >> print(geometric_center)
                array([-70.75619481,  21.815     ,  28.32835065])
                

            From this you can set 
            "center_x" = -70.756,"center_y" =21.815 ,"center_z"= 28.328
        3) Determine the dimensions of the pocket with Scoria's bounding_box function in python.

            in python: 
                # Import the scoria API
                >> import scoria
                >> 
                # define the protein molecule from the PDB file
                >> mol = scoria.Molecule("PATH/OF/PDB_FILE.pdb")

                # select which residues are going to be used to define pocket with resseq (the residue number)
                >> sel = mol.select_atoms({"resseq":[763, 872, 888, 907, 988]})
                
                # get the dimensions of the box that encompasses the protein pocket
                >> bounding_box = mol.get_bounding_box(sel)
                >> mol.get_bounding_box(sel)
                array([[-83.764,  15.015,  15.305],
                    [-60.814,  29.578,  36.727]])

            From this we need to take the difference from the 1st and 2nd coordinate for x,y,z:
            1st box coordinate:
                x_1st = -83.764,  y_1st = 15.015, z_1st = 15.305
            2nd box coordinate:
                x_2nd = -60.814,  y_2nd = 29.578, z_2nd = 36.727
            Absolute value of diff from 1st and 2nd:
                "size_x" = 22.950,"size_y" = 14.563,"size_z"= 21.422

            We suggest rounding these up to ensure the entire pocket is included:

                "size_x" = 25.00,"size_y" = 16.00,"size_z"= 25.00

#
## Other Factors for consideration prior to running Autogrow:
### Processors and multiprocessing style:
    Autogrow is recommended to be run on a larger computer or a cluster but it can be run on a local computer such as a laptop or PC.
####    -If running on a laptop or PC: 
    We recommend lowering some factors of Autogrow to lower the computational overhead for smaller machines.
        -lower the population size and number of generations. This will mean a less intense search of chemistry space
            but will make run times more reasonable.
        
        - lower the max_variation to 1. This means for every ligand created by Autogrow we will only create 1 conformer and thus only dock once per ligand.
            -This of course means a trade-off of getting more useful information for each ligand for computational efficiency.
        
    We also recommend considering how long you can allow the computer to run. If you need to continually use the computer while running Autogrow then you want to fix the number_of_processors to leave several available to perform other activities.
        -if you can leave the computer to run undisturbed for an extended period we recommend setting number_of_processors=-1 which will use all available Processors.
####    -If running on a larger super computer:
    We recommend fixing the number_of_processors to however many processors you will be dedicating to Autogrow.
        - if number_of_processors=-1 than all available processors will be occupied to run Autogrow.

####    -If running on a cluster:
    We recommend setting the number_of_processors=-1 and defining the number of processors in an SBATCH type submission script.

### Webserver:@@@@@@@@@JAKE NOT IMPLIMENTED
    If you struggle to have enough computational power to sucessfully run Autogrow, try using our free webserver at:
        @@@@@@@@@JAKE INSERT BIOTITE WEBSERVER


#
##  Multiprocessing/MPI/Parallelization/Parallelizer:
    Autogrow uses the Parallelizer.py script from Gypsum-DL (autogrow/Operators/ConvertFiles/gypsum_dl/gypsum_dl/Parallelizer.py).
    This script creates a Parallelizer class object which can divide jobs in three manners:
        1) Serial: run all jobs 1 at a time
        2) Multiprocessing: dynamically allocated distribution of jobs across multiple cpus on the same device
        3) MPI: static allocation of jobs across many cpus across multiple machines.

###  *** Important notes when running on clusters using SLURM ***
    1) Multiprocessing: When running Autogrow in Multiprocessing mode using SLURM, one should
        1st run the cache_prerun option on a single processor. 
            srun -n 1 python RunAutogrow.py -c
            *** USE srun or mpirun for the cache_prerun. This limits the prerun to a 
            single processor thus preventing errors caused by race conditions when creating pycache files. ***

        then run the simulation as intended.
            python RunAutogrow.py -j custom_parameters.json
            *** Do not use srun or mpirun for the production run. cpu/job distribution is handled internally. 
            Using srun or mpirun can cause errors with the mpi4py universe. ***


    2) MPI: When running Autogrow in mpi mode using SLURM, one should:
        1st run the cache_prerun option on a single processor. 
            srun -n 1 python RunAutogrow.py -c
            *** USE srun or mpirun for the cache_prerun. This limits the prerun to a 
            single processor thus preventing errors caused by race conditions when creating pycache files. ***

        then run the simulation as intended.
            python RunAutogrow.py -j custom_parameters.json
            *** Do not use srun or mpirun for the production run. cpu/job distribution is handled internally. 
            Using srun or mpirun can cause errors with the mpi4py universe. ***