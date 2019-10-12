import argparse
import os

parser = argparse.ArgumentParser(description="""This script creates a new sqlite database,
                                                based on empath scores of each youtube comment.""")

parser.add_argument("--src", dest="src", type=str, default="/../../../scratch/manoelribeiro/helpers/text_dict.sqlite",
                    help="Source folder of the comments.")

parser.add_argument("--dst", dest="dst", type=str, default="perspective_value.sqlite",
                    help="Where to save the output files.")

parser.add_argument("--pgm", dest="program", type=str, default="blobtext.py",
                    help="Where to save the output files.")

parser.add_argument("--init", dest="init", type=int, default="2015",
                    help="Comment where the analysis begin.")

parser.add_argument("--end", dest="end", type=int, default="2020",
                    help="Comment where the analysis end.")

parser.add_argument("--j", dest="j", type=int, default="1",
                    help="Commit at some number of iterations.")

parser.add_argument("--year", dest="y", type=int, default="2018",
                    help="Comment where the analysis end.")
parser.add_argument("--epoch", dest="ep", type=int, default="1",
                    help="Comment where the analysis end.")
parser.add_argument("--loop", dest="loop", type=int, default="10",
                    help="Comment where the analysis end.")
parser.add_argument("--new", dest="new", type=int, default="1",
                    help="Comment where the analysis end.")
parser.add_argument("--cat", dest="cat", type=str, default="Intellectual\ Dark\ Web",
                    help="Comment where the analysis end.")


args = parser.parse_args()


os.system('echo "Starting Program"')

init = args.init 
end = args.end
diff = args.end - args.init 

for i in [2015, 2017, 2018, 2019]:
    if i < args.y or i>args.end:
        continue
    print(i)
    if args.new>0:
        cmd = f"python finetuning_only.py --year {i} --epoch 0 --cat {args.cat}"
        os.system(f'echo {cmd}')
        os.system( cmd )
    for j in range(20):
        print(j)
        cmd = f"python finetuning_only.py --year {i} --epoch {args.ep + j} --loop {args.loop} --cat {args.cat}"
        os.system(f'echo {cmd}')
        os.system( cmd )
        print(j)
        cmd = f"python finetuning_only.py --year {i} --epoch {args.ep + j} --loop {args.loop} --cat {args.cat}"
        os.system(f'echo {cmd}')
        os.system( cmd )
    cmd = f"python finetuning_only.py --year {i} --epoch {args.ep + 9 } --loop {args.loop} --cat {args.cat}"
    os.system(f'echo {cmd}')
    os.system( cmd )



