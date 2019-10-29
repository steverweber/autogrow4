import os

file_path = "/bgfs/jdurrant/jspiegel/autogrow4/submit_PARP_SMP_run.sh"
out_folder = "/bgfs/jdurrant/jspiegel/test_autogrow/"

if os.path.exists(out_folder) == False:
    os.mkdir(out_folder)


for x in range(0,10):
    print("")
    printout = ""
    with open(file_path, 'r') as f:
        for line in f.readlines():
            if "#SBATCH --job-name=" in line:
                parts = line.split("_Run_")
                line = parts[0]+"_Run_"+str(x) + "\n"
            elif "#SBATCH --output=" in line:
                parts = line.split("_Run_")
                line = parts[0] + "_Run_" + str(x) + ".conf.out\n"
            # elif "highest_folder=" in line:

            #     line = 'highest_folder={}/bgfs/jdurrant/jspiegel/output_crc/BenchMarking_small_4/Run_{}/{}\n'.format('"',str(x),'"')
            elif "for i in " in line:
                parts = line.split("i in ")
                line = parts[0] + "i in " + str(x) + "\n"

            printout = printout + line
    new_file = out_folder + "submit_SMP_Run_{}.sh".format(str(x))
        
    with open(new_file, 'w') as f:
        f.write(printout)

    
    command = "sbatch {}".format(new_file)
    print("Submittings run numbers: {}".format(x))
    print("\t"+command)

    os.system(command)
