
# tmVar 3366cc
# dir=`mktemp -d` && python scripts/tag_tmvar.py SETH,Var120,nala_test $dir predict && python scripts/tag_tmvar.py SETH,Var120,nala_test $dir evaluate
A = set([

])

# SETH ffcc00
# dir=`mktemp -d` && python scripts/SETH.py SETH nala_random $dir && python scripts/SETH.py check_performance nala_random $dir/SETH/nala_random
B = set([

])

# nala 669933
# python nala/learning/train.py --model_path_1 nala/data/nala_BIEO_del_None_471433.bin --we --test_corpus nala_random
C = set([

])

# ------------------------------------------------

def print_sets(A, B, C, mapper_f=(lambda x: x[:-2]), filter_f=(lambda _: True)):
    A = set(map(mapper_f, (filter(filter_f, A))))
    B = set(map(mapper_f, (filter(filter_f, B))))
    C = set(map(mapper_f, (filter(filter_f, C))))

    A_SIZE = len(A)
    B_SIZE = len(B)
    C_SIZE = len(C)

    AiB_SIZE = len(A.intersection(B))
    AiC_SIZE = len(A.intersection(C))
    BiC_SIZE = len(B.intersection(C))

    AiBiC_SIZE = len(A.intersection(B).intersection(C))

    # ------------------------------------------------

    print("A_SIZE: ", A_SIZE)
    print("B_SIZE: ", B_SIZE)
    print("C_SIZE: ", C_SIZE)
    print("AiB_SIZE: ", AiB_SIZE)
    print("AiC_SIZE: ", AiC_SIZE)
    print("BiC_SIZE: ", BiC_SIZE)
    print("AiBiC_SIZE: ", AiBiC_SIZE)
    print()

# ------------------------------------------------

print_sets(A, B, C)  # all
print_sets(A, B, C, filter_f=(lambda x: x.endswith('0')))  # ST
print_sets(A, B, C, filter_f=(lambda x: x.endswith('1')))  # NL
