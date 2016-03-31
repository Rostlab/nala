import glob
import sys
from nalaf.learning.evaluators import Evaluations, Evaluation

folder = sys.argv[1]
jobid = sys.argv[2]

def n(col):
    return int(col)


counts = [0] * 4
for i in range(0, 4):
    counts[i] = ([0] * 5)

# Output looks like this:
# #class	tp	fp	fn	fp_ov	fn_ov	match	P	R	F	match	P	R	F
# 0	138	21	30	13	15	e	0.8679	0.8214	0.8440	o	0.9540	0.9171	0.9352
# 1	31	62	78	52	45	e	0.3333	0.2844	0.3069	o	0.9275	0.7950	0.8562
# 2	6	15	17	9	8	e	0.2857	0.2609	0.2727	o	0.7931	0.7188	0.7541
# TOTAL	175	98	125	74	68	e	0.6410	0.5833	0.6108	o	0.9296	0.8476	0.8867

for fn in glob.glob(folder + "/*o{}.*".format(jobid)):
    with open(fn) as f:
        valid = False
        for line in f.readlines():
            if line[0] in '012' or line.startswith("TOTAL"):
                c = line.split()
                if len(c) == 14 and c[6] == 'e' and c[10] == 'o':
                    valid = True

                    subclass = c[0]
                    subclass = 3 if subclass == "TOTAL" else int(subclass)

                    # tp = n(c[1])
                    # fp = n(c[2])
                    # fn = n(c[3])
                    # fpo = n(c[4])
                    # fno = n(c[5])
                    for i in range(0, 5):
                        counts[subclass][i] += n(c[i+1])

        print(fn, valid)

evaluations = Evaluations()
for subclass, c in enumerate(counts):
    subclass = "TOTAL" if subclass == 3 else subclass
    evaluations.add(Evaluation(str(subclass), *c))

print(evaluations)
