#!/bin/bash
#SBATCH --job-name=Tournement_k_vary_Run_0
#SBATCH --output=/bgfs/jdurrant/jspiegel/Luxury_Run/Tournement_k_vary/Tournement_k_vary_Run_0.conf.out
#SBATCH --time=47:55:00
#SBATCH --nodes=5
#SBATCH --ntasks-per-node=28
#SBATCH --cluster=mpi
#SBATCH --partition=opa
#SBATCH --mail-type BEGIN,END,FAIL,ARRAY_TASKS  
#SBATCH --mail-user jako134j@gmail.com                                   

## Define the environment
#py2.7 settings 
module purge
module load mgltools
module load gcc/8.2.0
# module load python/anaconda2.7-2018.12_westpa

#py3.6 settings 
# module purge
# module load mgltools
# module load gcc/8.2.0
# module load python/anaconda3.7-2018.12_westpa
source activate py37

highest_folder="/bgfs/jdurrant/jspiegel/Luxury_Run/Tournement_k_vary/"
mkdir $highest_folder

# run precache
mpirun -n 1 ~/miniconda3/envs/py37/bin/python -m mpi4py /bgfs/jdurrant/jspiegel/autogrow4/RunAutogrow.py -c

average_time=0
for i in 4
do
    outfolder_k_dir=$highest_folder"k_00$i/"
    mkdir $outfolder_k_dir
    outfolder_four=$highest_folder"Run_1/"
    mkdir $outfolder_four
    
    echo "START Autogrow 4.0 Run number $i  STABILITY RUN USING with Tournement_QVINA2_3"
    start_time="$(date +%s%N | cut -b1-13)"
    date +%s%N | cut -b1-13

    mpirun -n $SLURM_NTASKS \
    ~/miniconda3/envs/py37/bin/python -m mpi4py /bgfs/jdurrant/jspiegel/autogrow4/RunAutogrow.py \
        --filename_of_receptor /bgfs/jdurrant/jspiegel/autogrow4/tutorial/PARP/4r6e_removed_smallmol_aligned_Hs.pdb \
        --center_x -70.76 --center_y  21.82 --center_z 28.33 \
        --size_x 25.0 --size_y 16.0 --size_z 25.0 \
        --source_compound_file /bgfs/jdurrant/jspiegel/autogrow4/source_compounds/PARP_docked_ranked_ZINC_fragments.smi \
        --root_output_folder $outfolder_four \
        --number_of_mutants_first_generation 250 \
        --number_of_crossovers_first_generation 250 \
        --number_to_advance_from_previous_gen_first_generation 100 \
        --number_of_mutants 250 \
        --number_of_crossovers 250 \
        --number_to_advance_from_previous_gen 100 \
        --top_mols_to_seed_next_generation_first_generation 50 \
        --top_mols_to_seed_next_generation 50 \
        --diversity_mols_to_seed_first_generation 50 \
        --diversity_seed_depreciation_per_gen 0 \
        --num_generations 15 \
        --mgltools_directory $MGLTOOLS_HOME/ \
        --number_of_processors -1 \
        --dock_choice QuickVina2Docking \
        --scoring_choice VINA \
        --selector_choice Tournement_Selector \
        --tourn_size 0.0$i \
        --Lipinski_Strict \
        --Ghose \
        --PAINS_Filter \
        --reduce_files_sizes True \
        --max_variants_per_compound 3 \
        --redock_advance_from_previous_gen False \
        --filter_source_compounds False \
        --use_docked_source_compounds True \
        --rxn_library All_Rxns \
        --generate_plot True \
        --multithread_mode mpi \
        >>  $outfolder_four"test_output_$i.txt" 2>>  $outfolder_four"test_error_$i.txt"

done