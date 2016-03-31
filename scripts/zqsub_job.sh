# Script to CV-evaluate very last experiments, https://github.com/abojchevski/nala/issues/58

# qsub -m aes -M i@juanmi.rocks -t 1-5 zqsub_job.sh

let cv_fold=$SGE_TASK_ID-1

python='/mnt/home/cejuela/anaconda3/latest/bin/python'
trainscript='/mnt/home/cejuela/nala/nala/scripts/train.py'
outputdir='/mnt/home/cejuela/tmp/models/'

# FINAL EXPERIMENTS

time $python $trainscript --training_corpus nala_training_2 --cv_n 5 --cv_fold 2 --pruner parts --labeler BIEO --model_name_suffix "TEST" --output_folder $outputdir

# BASELINE 430489.1-5:1 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus nala_training --cv_n 5 --cv_fold $cv_fold --pruner parts --labeler BIEO --model_name_suffix "BASELINE" --output_folder /mnt/home/cejuela/tmp/models/

# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------

# The next runs _do_ have the window features on

# 423093.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus nala_training --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_NL --word_embeddings --we_additive 2 --we_multiplicative 3 --elastic_net --model_name_suffix "all3_baseline_new_we" --output_folder /mnt/home/cejuela/tmp/models/
# 423094.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus IDP4+_training --delete_subclasses "1,2" --cv_n 5 --cv_fold $cv_fold --pruner parts --model_name_suffix "st_baseline_new_we" --output_folder /mnt/home/cejuela/tmp/models/
# 423095.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus IDP4+_training --delete_subclasses "1,2" --cv_n 5 --cv_fold $cv_fold --pruner parts --elastic_net --model_name_suffix "st_elasticnet_new_we" --output_folder /mnt/home/cejuela/tmp/models/


# all3 model, baseline vs elastic net
# P:0.8920	R:0.8806	F:0.8863	1 and P:0.8270	R:0.8596	F:0.8430	2 - 422030.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus nala_training --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_NL --word_embeddings --we_additive 2 --we_multiplicative 3 --model_name_suffix "all3_baseline" --output_folder /mnt/home/cejuela/tmp/models/
# WINS P:0.9090	R:0.8878	F:0.8983	1 and P:0.7773	R:0.8688	F:0.8205	2 - 422031.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus nala_training --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_NL --word_embeddings --we_additive 2 --we_multiplicative 3 --elastic_net --model_name_suffix "all3_elasticnet" --output_folder /mnt/home/cejuela/tmp/models/

# st model, baseline vs elastic net
# 422032.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus IDP4+_training --delete_subclasses "1,2" --cv_n 5 --cv_fold $cv_fold --pruner parts --model_name_suffix "st_baseline" --output_folder /mnt/home/cejuela/tmp/models/
# REPEATED :-( 422033.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus IDP4+_training --delete_subclasses "1,2" --cv_n 5 --cv_fold $cv_fold --pruner parts --model_name_suffix "st_elasticnet" --output_folder /mnt/home/cejuela/tmp/models/


# test we params in st model
# 421906.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus IDP4+_training --delete_subclasses "1,2" --cv_n 5 --cv_fold $cv_fold --pruner parts --word_embeddings --we_additive 4 --we_multiplicative 4
# 421907.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus IDP4+_training --delete_subclasses "1,2" --cv_n 5 --cv_fold $cv_fold --pruner parts --word_embeddings --we_additive 3 --we_multiplicative 3
# 421908.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus IDP4+_training --delete_subclasses "1,2" --cv_n 5 --cv_fold $cv_fold --pruner parts --word_embeddings --we_additive 2 --we_multiplicative 3
# 421909.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus IDP4+_training --delete_subclasses "1,2" --cv_n 5 --cv_fold $cv_fold --pruner parts --word_embeddings --we_additive 2 --we_multiplicative 2
# 421910.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus IDP4+_training --delete_subclasses "1,2" --cv_n 5 --cv_fold $cv_fold --pruner parts --word_embeddings --we_additive 1 --we_multiplicative 2
# 421911.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus IDP4+_training --delete_subclasses "1,2" --cv_n 5 --cv_fold $cv_fold --pruner parts --word_embeddings --we_additive 0 --we_multiplicative 1
# 421912.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus IDP4+_training --delete_subclasses "1,2" --cv_n 5 --cv_fold $cv_fold --pruner parts --word_embeddings --we_additive 0 --we_multiplicative 0
# WINS P:0.9194	R:0.8991	F:0.9092	0 - 421913.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus IDP4+_training --delete_subclasses "1,2" --cv_n 5 --cv_fold $cv_fold --pruner parts


# BASELINE all3 - 421901.1-5 - time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus nala_training --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_NL --ps_random "0.0" --word_embeddings --we_additive 2 --we_multiplicative 3 --output_folder /mnt/home/cejuela/nala/nala/tmp/models
# 421904.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus nala_training --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_NL --ps_random "0.0" --word_embeddings --we_additive 2 --we_multiplicative 3 --elastic_net --output_folder /mnt/home/cejuela/nala/nala/tmp/models_alt


# This tests feature.possible_states=BOOL, hard-coded change -- compare it agains the same line below
# 421797.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus nala_training --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_ST --ps_NL --ps_random "0.0" --word_embeddings --we_additive 2 --we_multiplicative 3


# Test deletion of 0 class in all3 model
# 421771.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus nala_training --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_NL --ps_random "0.0" --delete_subclasses "0"
# WINS by FAR - 421772.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus nala_training --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_NL --ps_random "0.0"


# https://github.com/abojchevski/nala/issues/21

# 421785.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus nala_training --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_ST --ps_NL --ps_random "0.0" --word_embeddings --we_additive 1 --we_multiplicative 16
# 421786.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus nala_training --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_ST --ps_NL --ps_random "0.0" --word_embeddings --we_additive 16 --we_multiplicative 16
# P:0.8860	R:0.8832	F:0.8846	1 and P:0.8015	R:0.9013	F:0.8485	2 - 421787.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus nala_training --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_ST --ps_NL --ps_random "0.0" --word_embeddings --we_additive 4 --we_multiplicative 4
# 421789.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus nala_training --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_ST --ps_NL --ps_random "0.0" --word_embeddings --we_additive 3 --we_multiplicative 4
# 421790.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus nala_training --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_ST --ps_NL --ps_random "0.0" --word_embeddings --we_additive 2 --we_multiplicative 4
# 421791.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus nala_training --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_ST --ps_NL --ps_random "0.0" --word_embeddings --we_additive 4 --we_multiplicative 3
# 421792.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus nala_training --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_ST --ps_NL --ps_random "0.0" --word_embeddings --we_additive 3 --we_multiplicative 3

# WINS P:0.8831	R:0.8840	F:0.8836	1 and P:0.8189	R:0.9004	F:0.8577	2  - 421773.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus nala_training --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_ST --ps_NL --ps_random "0.0" --word_embeddings --we_additive 2 --we_multiplicative 3
# 421774.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus nala_training --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_ST --ps_NL --ps_random "0.0" --word_embeddings --we_additive 1 --we_multiplicative 3
# 421775.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus nala_training --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_ST --ps_NL --ps_random "0.0" --word_embeddings --we_additive 0 --we_multiplicative 3
# 421776.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus nala_training --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_ST --ps_NL --ps_random "0.0" --word_embeddings --we_additive -1 --we_multiplicative 3
# 421777.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus nala_training --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_ST --ps_NL --ps_random "0.0" --word_embeddings --we_additive -2 --we_multiplicative 3
# 421778.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus nala_training --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_ST --ps_NL --ps_random "0.0" --word_embeddings --we_additive -1 --we_multiplicative 2
# 421779.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus nala_training --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_ST --ps_NL --ps_random "0.0" --word_embeddings --we_additive -2 --we_multiplicative 2
# 421781.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus nala_training --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_ST --ps_NL --ps_random "0.0" --word_embeddings --we_additive -1 --we_multiplicative 1
# 421782.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus nala_training --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_ST --ps_NL --ps_random "0.0" --word_embeddings --we_additive -2 --we_multiplicative 1

# P:0.8824	R:0.8777	F:0.8800 - 421719.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus nala_training --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_ST --ps_NL --ps_random "0.0" --word_embeddings --we_additive 2 --we_multiplicative 2
# P:0.8793	R:0.8757	F:0.8775	1 - 421718.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus nala_training --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_ST --ps_NL --ps_random "0.0" --word_embeddings --we_additive 1 --we_multiplicative 2
# 421717.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus nala_training --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_ST --ps_NL --ps_random "0.0" --word_embeddings --we_additive 0 --we_multiplicative 2
# 421716.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus nala_training --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_ST --ps_NL --ps_random "0.0" --word_embeddings --we_additive 2 --we_multiplicative 1
# 421715.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus nala_training --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_ST --ps_NL --ps_random "0.0" --word_embeddings --we_additive 1 --we_multiplicative 1
# P:0.8832	R:0.8710	F:0.8771	1 - 421714.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus nala_training --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_ST --ps_NL --ps_random "0.0" --word_embeddings --we_additive 0 --we_multiplicative 1
# P:0.8806	R:0.8779	F:0.8792	1 - 421713.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus nala_training --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_ST --ps_NL --ps_random "0.0" --word_embeddings --we_additive 0 --we_multiplicative 0
# P:0.8819	R:0.8614	F:0.8715 - 421712.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus nala_training --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_ST --ps_NL --ps_random "0.0"



# The next runs do not have the window features on

# 421706.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus nala_training --cv_n 5 --cv_fold $cv_fold --pruner parts --ps_random "0.0"
# 421705.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus nala_training --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_random "0.0"
# 421704.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus nala_training --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_ST --ps_random "0.0"
# WINS P:0.8817	R:0.8696	F:0.8756	1 and P:0.8086	R:0.8961	F:0.8501	2 but very close to ST and NL too -- 421703.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus nala_training --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_NL --ps_random "0.0"
# 421702.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus nala_training --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_ST --ps_NL --ps_random "0.0"

# WINS P:0.8288	R:0.7225	F:0.7720 -- 421701.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus IDP4+_training --cv_n 5 --cv_fold $cv_fold --pruner parts --ps_random "0.0"
# 421699.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus IDP4+_training --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_random "0.0"
# 421698.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus IDP4+_training --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_ST --ps_random "0.0"
# 421696.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus IDP4+_training --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_NL --ps_random "0.0"
# 421695.1-5 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus IDP4+_training --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_ST --ps_NL --ps_random "0.0"

# WINS P:0.9372	R:0.8535	F:0.8934 -- 10 421693.1-5:1 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus nala_training --delete_subclasses "1,2" --cv_n 5 --cv_fold $cv_fold --pruner parts --ps_random "0.0"
# 9 421692.1-5:1 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus nala_training --delete_subclasses "1,2" --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_random "0.0"
# 8 421691.1-5:1 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus nala_training --delete_subclasses "1,2" --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_ST --ps_random "0.0"
# 7 421690.1-5:1 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus nala_training --delete_subclasses "1,2" --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_NL --ps_random "0.0"
# 6 421689.1-5:1 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus nala_training --delete_subclasses "1,2" --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_ST --ps_NL --ps_random "0.0"

# WINS P:0.9060	R:0.9135	F:0.9097 -- 5 421686.1-5:1 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus IDP4+_training --delete_subclasses "1,2" --cv_n 5 --cv_fold $cv_fold --pruner parts --ps_random "0.0"
# 4 421685.1-5:1 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus IDP4+_training --delete_subclasses "1,2" --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_random "0.0"
# 3 421684.1-5:1 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus IDP4+_training --delete_subclasses "1,2" --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_ST --ps_random "0.0"
# 2 421683.1-5:1 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus IDP4+_training --delete_subclasses "1,2" --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_NL --ps_random "0.0"
# 1 421682.1-5:1 time /mnt/home/cejuela/anaconda3/latest/bin/python /mnt/home/cejuela/nala/nala/scripts/train.py --training_corpus IDP4+_training --delete_subclasses "1,2" --cv_n 5 --cv_fold $cv_fold --pruner sentences --ps_ST --ps_NL --ps_random "0.0"
