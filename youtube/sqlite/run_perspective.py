import argparse
import os

parser = argparse.ArgumentParser(description="""This script creates a new sqlite database,
                                                based on empath scores of each youtube comment.""")

parser.add_argument("--src", dest="src", type=str, default="/../../../scratch/manoelribeiro/helpers/text_dict.sqlite",
                    help="Source folder of the comments.")

parser.add_argument("--dst", dest="dst", type=str, default="perspective_value.sqlite",
                    help="Where to save the output files.")

parser.add_argument("--pgm", dest="program", type=str, default="perspective_values.py",
                    help="Where to save the output files.")

parser.add_argument("--init", dest="init", type=int, default="0",
                    help="Comment where the analysis begin.")

parser.add_argument("--end", dest="end", type=int, default="-1",
                    help="Comment where the analysis end.")

parser.add_argument("--loop", dest="loop", type=int, default="1",
                    help="Number of times the system will be called to run the code.")

parser.add_argument("--loop2", dest="loop2", type=int, default="1",
                    help="Number of loops that perspective will execute the code."
                         "Correct: (end-init) / loop2 == 10000")

args = parser.parse_args()


os.system('echo "Starting Program"')

init = args.init 
end = args.end
diff = args.end - args.init 

for i in range(args.loop):
    cmd = f"python {args.program} --src {args.src} --dst {args.dst} --init {init} --end {end} --loop {args.loop2}"
    os.system(f'echo {cmd}')
    os.system(cmd)
    
    init += diff
    end += diff

