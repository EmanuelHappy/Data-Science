import argparse
import os

parser = argparse.ArgumentParser(description="""This script creates a new sqlite database,
                                                based on text_blob scores of each youtube comment.""")

parser.add_argument("--src", dest="src", type=str, default="/../../../scratch/manoelribeiro/helpers/text_dict.sqlite",
                    help="Source folder of the comments.")

parser.add_argument("--dst", dest="dst", type=str, default="./../sentiment/text_blob/data/",
                    help="Where to save the output files.")

parser.add_argument("--pgm", dest="program", type=str, default="blobtext.py",
                    help="Where to save the output files.")

parser.add_argument("--init", dest="init", type=int, default="0",
                    help="Comment where the analysis begin at each split.")

parser.add_argument("--end", dest="end", type=int, default="-1",
                    help="Finish the program when reaches end.")

parser.add_argument("--loop", dest="loop", type=int, default="1",
                    help="Number of times the code will be executed")

parser.add_argument("--j", dest="j", type=int, default="1",
                    help="Split where the analysis begin.")


args = parser.parse_args()


os.system('echo "Starting Program"')

init = args.init 
end = args.end
diff = args.end - args.init 

for i in range(args.j, args.loop):
    
    cmd = f"python {args.program} --dst {args.dst} --j {i} --end {end}"
    os.system(f'echo {cmd}')
    os.system(cmd)
