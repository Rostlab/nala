import glob
import sys
from nalaf.learning.evaluators import Evaluations, Evaluation, MentionLevelEvaluator, EvaluationWithStandardError

folder = sys.argv[1]
jobid = sys.argv[2]

def n(cols, index, typ=int):
    return typ(cols[index])

labels = {'0', '1', '2', MentionLevelEvaluator.TOTAL_LABEL}
first_letter_labels = {label[0] for label in labels}

counts = {label: {key: 0 for key in ['tp', 'fp', 'fn', 'fp_ov', 'fn_ov']} for label in labels}

precomputed_SEs = {label: {match: {key: [] for key in ['precision_SE', 'recall_SE', 'f_measure_SE']} for match in ['exact', 'overlapping']} for label in labels}

# Old version, output looks like this:

# #class	tp	fp	fn	fp_ov	fn_ov	match	P	R	F	match	P	R	F
# 0	138	21	30	13	15	e	0.8679	0.8214	0.8440	o	0.9540	0.9171	0.9352
# 1	31	62	78	52	45	e	0.3333	0.2844	0.3069	o	0.9275	0.7950	0.8562
# 2	6	15	17	9	8	e	0.2857	0.2609	0.2727	o	0.7931	0.7188	0.7541
# TOTAL	175	98	125	74	68	e	0.6410	0.5833	0.6108	o	0.9296	0.8476	0.8867

# New version, output looks like this:

# # class	tp	fp	fn	fp_ov	fn_ov	match	P	P_SE	R	R_SE	F	F_SE	match	P	P_SE	R	R_SE	F	F_SE
# 0	46	16	15	12	13	e	0.7419	0.0072	0.7541	0.0074	0.7480	0.0053	o	0.9467	0.0063	0.9726	0.0021	0.9595	0.0027
# 1	2	8	20	6	6	e	0.2000	0.0147	0.0909	0.0066	0.1250	0.0367	o	0.8750	0.0143	0.5000	0.0125	0.6364	0.0086
# 2	3	0	2	0	0	e	1.0000	0.0000	0.6000	0.0211	0.7500	0.0133	o	1.0000	0.0000	0.6000	0.0216	0.7500	0.0137
# TOTAL	51	24	37	18	19	e	0.6800	0.0069	0.5795	0.0070	0.6258	0.0060	o	0.9362	0.0043	0.8302	0.0060	0.8800	0.0046


for fn in glob.glob(folder + "/*o{}.*".format(jobid)):
    with open(fn) as f:
        valid_file = False
        for line in f.readlines():
            valid_line = False

            if line[0] in first_letter_labels:
                c = line.split()

                if len(c) == 20 and c[6] == 'e' and c[13] == 'o':
                    is_new_version = True
                    valid_line = True

                elif len(c) == 14 and c[6] == 'e' and c[10] == 'o':
                    is_new_version = False
                    valid_line = True

                if valid_line:
                    valid_file = True
                    label = c[0]

                    counts[label]['tp'] += n(c, 1)
                    counts[label]['fp'] += n(c, 2)
                    counts[label]['fn'] += n(c, 3)
                    counts[label]['fp_ov'] += n(c, 4)
                    counts[label]['fn_ov'] += n(c, 5)

                    if is_new_version:
                        precomputed_SEs[label]['exact']['precision_SE'].append(n(c, 8, float))
                        precomputed_SEs[label]['exact']['recall_SE'].append(n(c, 10, float))
                        precomputed_SEs[label]['exact']['f_measure_SE'].append(n(c, 12, float))
                        # ---
                        precomputed_SEs[label]['overlapping']['precision_SE'].append(n(c, 15, float))
                        precomputed_SEs[label]['overlapping']['recall_SE'].append(n(c, 17, float))
                        precomputed_SEs[label]['overlapping']['f_measure_SE'].append(n(c, 19, float))

        print(fn, valid_file)


if is_new_version:
    for label in labels:
        for match, values in precomputed_SEs[label].items():
            for count in values.keys():
                array = precomputed_SEs[label][match][count]
                precomputed_SEs[label][match][count] = sum(array) / len(array)

evaluations = Evaluations()
for label, c in counts.items():
    if is_new_version:
        evaluations.add(EvaluationWithStandardError(str(label), {None: c}, precomputed_SEs=precomputed_SEs[label]))

    else:
        evaluations.add(Evaluation(str(label), c['tp'], c['fp'], c['fn'], c['fp_ov'], c['fn_ov']))

print(evaluations)
