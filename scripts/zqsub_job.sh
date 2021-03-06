# Script to CV-evaluate very last experiments, https://github.com/abojchevski/nala/issues/58

# qsub -m aes -M i@juanmi.rocks -t 1-5 -j y zqsub_job.sh

SGE_TASK_ID=${SGE_TASK_ID-1}
let cv_fold=$SGE_TASK_ID-1
jobid=${JOB_ID-last}

python='/mnt/home/cejuela/anaconda3/latest/bin/python'
trainscript='/mnt/home/cejuela/nala/nala/scripts/train.py'
outputdir='/mnt/home/cejuela/tmp/models/'
outputdir2='/mnt/home/cejuela/tmp/zqsub/'
train="time $python $trainscript --cv_n 5 --cv_fold $cv_fold --model_name_suffix $jobid "
train_cv=$train
train_no_cv="time $python $trainscript --validation none --model_name_suffix $jobid --output_folder $outputdir "

# FINAL EXPERIMENTS
# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------

# Features: we (on/off)

# 482686.1-5 $train_cv --training_corpus nala_training --we --use_feat_windows false
# 482687.1-5 $train_cv --training_corpus nala_training --use_feat_windows false --> 0 PERFORMANCE

# Features: TokenStem + we (on/off)

# 482690.1-5 $train_cv --training_corpus nala_training --we --use_feat_windows false
# 482691.1-5 $train_cv --training_corpus nala_training --use_feat_windows false

# Features: PostProcessing + we (on/off)

# 482444.1-5 $train_cv --training_corpus nala_training --we --use_feat_windows false
# 482493.1-5 $train_cv --training_corpus nala_training --use_feat_windows false

# Features: TokenStem + PostProcessing + we (on/off)

# 479727.1-5 $train_cv --training_corpus nala_training --we --use_feat_windows false
# 479752.1-5 $train_cv --training_corpus nala_training --use_feat_windows false

# ------------------------------------------------------------------------------------------

# Iterations CV

# 471590.1-5 $train_cv --training_corpus nala_training_5 --we
# 471591.1-5 $train_cv --training_corpus nala_training_10 --we
# 471592.1-5 $train_cv --training_corpus nala_training_15 --we
# 471593.1-5 $train_cv --training_corpus nala_training_20 --we
# 471594.1-5 $train_cv --training_corpus nala_training_25 --we
# 471595.1-5 $train_cv --training_corpus nala_training_30 --we
# 471596.1-5 $train_cv --training_corpus nala_training_35 --we
# 471597.1-5 $train_cv --training_corpus nala_training_40 --we
# 471598.1-5 $train_cv --training_corpus nala_training_45 --we
# 471599.1-5 $train_cv --training_corpus nala_training_50 --we

# ------------------------------------------------------------------------------------------

# 471417.1-5 $train_cv --training_corpus nala_training
# BASELINE 471430.1-5 $train_cv --training_corpus nala_training --we
# 471431 $train_no_cv --training_corpus nala_training --we
# 471432 $train_no_cv --training_corpus nala
# 471433 $train_no_cv --training_corpus nala --we
# 471434 $train_no_cv --training_corpus tmVar_training --test_corpus tmVar_test --we

# 469533.1-5 $train_cv --training_corpus nala_training --pruner parts
# 469534.1-5 $train_cv --training_corpus nala_training --pruner parts --we
# 469535.1-5 $train_cv --training_corpus nala_training --pruner sentences --ps_ST --ps_NL --we
# 471410.1-5 $train_cv --training_corpus IDP4+_training --pruner parts --we
# 469537.1-5 $train_cv --training_corpus IDP4+_training --pruner parts --we --delete_subclasses "2"
# 469539.1-5 $train_cv --training_corpus IDP4+_training --pruner parts --we --delete_subclasses "1,2"
# 471411.1-5 $train_cv --training_corpus nala_training --pruner parts --we --delete_subclasses "1"

# ------------------------------------------------------------------------------------------

# 467068.1-5 $train_cv --labeler BIEO --we --training_corpus nala_training --pruner parts
# 467069.1-5 $train_cv --labeler BIEO --we --training_corpus nala_training --pruner parts --delete_subclasses "0"
# 467070.1-5 $train_cv --labeler BIEO --we --training_corpus nala_training --pruner parts --delete_subclasses "0,2"
# 467071.1-5 $train_cv --labeler BIEO --we --training_corpus nala_training --pruner parts --delete_subclasses "1,2"
# 467072.1-5 $train_cv --labeler BIEO --we --training_corpus nala_training --pruner parts --delete_subclasses "1"
#
# 467073.1-5 $train_cv --labeler BIEO --we --training_corpus nala_training --pruner sentences
# 467074.1-5 $train_cv --labeler BIEO --we --training_corpus nala_training --pruner sentences --delete_subclasses "0"
# 467075.1-5 $train_cv --labeler BIEO --we --training_corpus nala_training --pruner sentences --delete_subclasses "0,2"
# 467076.1-5 $train_cv --labeler BIEO --we --training_corpus nala_training --pruner sentences --delete_subclasses "1,2"
# 467077.1-5 $train_cv --labeler BIEO --we --training_corpus nala_training --pruner sentences --delete_subclasses "1"
#
# 467078.1-5 $train_cv --labeler BIEO --we --training_corpus nala_training --pruner sentences --ps_ST --ps_NL
# 467079.1-5 $train_cv --labeler BIEO --we --training_corpus nala_training --pruner sentences --ps_ST --ps_NL --delete_subclasses "0"
# 467080.1-5 $train_cv --labeler BIEO --we --training_corpus nala_training --pruner sentences --ps_ST --ps_NL --delete_subclasses "0,2"
# 467081.1-5 $train_cv --labeler BIEO --we --training_corpus nala_training --pruner sentences --ps_ST --ps_NL --delete_subclasses "1,2"
# 467082.1-5 $train_cv --labeler BIEO --we --training_corpus nala_training --pruner sentences --ps_ST --ps_NL --delete_subclasses "1"
#
# 467083.1-5 $train_cv --labeler BIEO --we --training_corpus IDP4+_training --pruner parts
# 467084.1-5 $train_cv --labeler BIEO --we --training_corpus IDP4+_training --pruner parts --delete_subclasses "0"
# 467085.1-5 $train_cv --labeler BIEO --we --training_corpus IDP4+_training --pruner parts --delete_subclasses "0,2"
# 467086.1-5 $train_cv --labeler BIEO --we --training_corpus IDP4+_training --pruner parts --delete_subclasses "1,2"
# 467087.1-5 $train_cv --labeler BIEO --we --training_corpus IDP4+_training --pruner parts --delete_subclasses "1"
#
# 467088.1-5 $train_cv --labeler BIEO --we --training_corpus IDP4+_training --pruner sentences
# 467089.1-5 $train_cv --labeler BIEO --we --training_corpus IDP4+_training --pruner sentences --delete_subclasses "0"
# 467090.1-5 $train_cv --labeler BIEO --we --training_corpus IDP4+_training --pruner sentences --delete_subclasses "0,2"
# 467091.1-5 $train_cv --labeler BIEO --we --training_corpus IDP4+_training --pruner sentences --delete_subclasses "1,2"
# 467092.1-5 $train_cv --labeler BIEO --we --training_corpus IDP4+_training --pruner sentences --delete_subclasses "1"
#
# 467093.1-5 $train_cv --labeler BIEO --we --training_corpus IDP4+_training --pruner sentences --ps_ST --ps_NL
# 467094.1-5 $train_cv --labeler BIEO --we --training_corpus IDP4+_training --pruner sentences --ps_ST --ps_NL --delete_subclasses "0"
# 467095.1-5 $train_cv --labeler BIEO --we --training_corpus IDP4+_training --pruner sentences --ps_ST --ps_NL --delete_subclasses "0,2"
# 467096.1-5 $train_cv --labeler BIEO --we --training_corpus IDP4+_training --pruner sentences --ps_ST --ps_NL --delete_subclasses "1,2"
# 467097.1-5 $train_cv --labeler BIEO --we --training_corpus IDP4+_training --pruner sentences --ps_ST --ps_NL --delete_subclasses "1"


# ------------------------------------------------------------------------------------------

# FINAL MODELS

# Includes PP improvements and can be tested directly against alex winner
# FINAL BASELINE 466739.1-5 $train_cv --training_corpus nala_training --pruner parts --labeler BIEO --word_embeddings --we_additive 0 --we_multiplicative 1
# 466740.1-5 $train_cv --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 0 --we_multiplicative 1
# 466741.1-5 $train_cv --training_corpus tmVar_training --pruner parts --labeler BIEO --word_embeddings --we_additive 0 --we_multiplicative 1
# 466742.1-5 $train_cv --training_corpus tmVar_training --pruner parts --labeler IO --word_embeddings --we_additive 0 --we_multiplicative 1

# 466743 $train_no_cv --training_corpus nala_training --pruner parts --labeler BIEO --word_embeddings --we_additive 0 --we_multiplicative 1 --output_folder $outputdir
# 466744 $train_no_cv --training_corpus nala --pruner parts --labeler BIEO --word_embeddings --we_additive 0 --we_multiplicative 1 --output_folder $outputdir
# 466745 $train_no_cv --training_corpus IDP4+_training --pruner parts --labeler BIEO --word_embeddings --we_additive 0 --we_multiplicative 1 --output_folder $outputdir
# 466746 $train_no_cv --training_corpus IDP4+ --pruner parts --labeler BIEO --word_embeddings --we_additive 0 --we_multiplicative 1 --output_folder $outputdir
# 466747 $train_no_cv --training_corpus tmVar_training --pruner parts --labeler BIEO --word_embeddings --we_additive 0 --we_multiplicative 1 --output_folder $outputdir
# 466748 $train_no_cv --training_corpus tmVar --pruner parts --labeler BIEO --word_embeddings --we_additive 0 --we_multiplicative 1 --output_folder $outputdir

# ------------------------------------------------------------------------------------------

# FINAL BASELINE

# branch with new PP juanmi improvements
# $train_cv --training_corpus nala_training --pruner parts --labeler BIEO --word_embeddings --we_additive 0 --we_multiplicative 1

# branch with and/or splitting but also accepting SS cases
# 466728.1-5 $train_cv --training_corpus nala_training --pruner parts --labeler BIEO --word_embeddings --we_additive 0 --we_multiplicative 1

# ------------------------------------------------------------------------------------------

## Alex experiments

# develop -> new code
# 466713.1-5 $train_cv --training_corpus nala_training --pruner parts --labeler BIEO --word_embeddings --we_additive 0 --we_multiplicative 1

# feature_rule_0 -> no rule at all
# 466706.1-5 $train_cv --training_corpus nala_training --pruner parts --labeler BIEO --word_embeddings --we_additive 0 --we_multiplicative 1

# feature_rule_1 -> old code
# (old BASLINE) $train_cv --training_corpus nala_training --pruner parts --labeler BIEO --word_embeddings --we_additive 0 --we_multiplicative 1

# ------------------------------------------------------------------------------------------

# without extra post-processing rules
# 466606.1-5 $train_cv --training_corpus tmVar_training --pruner parts --labeler BIEO --word_embeddings --we_additive 0 --we_multiplicative 1

# 466277.1-5 $train_cv --training_corpus tmVar_training --pruner parts --labeler IO --word_embeddings --we_additive 0 --we_multiplicative 1
# 466278.1-5 $train_cv --training_corpus tmVar_training --pruner parts --labeler BIO --word_embeddings --we_additive 0 --we_multiplicative 1
# 466280.1-5 $train_cv --training_corpus tmVar_training --pruner parts --labeler BIEO --word_embeddings --we_additive 0 --we_multiplicative 1

# 466268.1-5 $train_cv --training_corpus nala_training --pruner parts --labeler BIO --word_embeddings --we_additive 0 --we_multiplicative 1

# 464639.1-5 $train_cv --training_corpus nala_training --pruner parts --labeler BIEO --word_embeddings --we_additive 0 --we_multiplicative 1

# These runs have the new post-processing rules hard-coded commented out
# 464620.1-5 $train_cv --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 0 --we_multiplicative 1
# 464621.1-5 $train_cv --training_corpus nala_training --pruner parts --labeler BIEO --word_embeddings --we_additive 0 --we_multiplicative 1

# ------------------------------------------------------------------------------------------

# BASELINE 464576.1-5 $train_cv --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 0 --we_multiplicative 1
# 464577.1-5 $train_cv --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 0 --we_multiplicative 1 --nl --nl_threshold 0

# 464587 $train_no_cv --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 0 --we_multiplicative 1 --output_folder $outputdir
# 464588 $train_no_cv --training_corpus nala --pruner parts --labeler IO --word_embeddings --we_additive 0 --we_multiplicative 1 --output_folder $outputdir
# 464589 $train_no_cv --training_corpus IDP4+_training --pruner parts --labeler IO --word_embeddings --we_additive 0 --we_multiplicative 1 --output_folder $outputdir
# 464590 $train_no_cv --training_corpus IDP4+ --pruner parts --labeler IO --word_embeddings --we_additive 0 --we_multiplicative 1 --output_folder $outputdir
# 464591 $train_no_cv --training_corpus tmVar_training --pruner parts --labeler IO --word_embeddings --we_additive 0 --we_multiplicative 1 --output_folder $outputdir
# 464592 $train_no_cv --training_corpus tmVar --pruner parts --labeler IO --word_embeddings --we_additive 0 --we_multiplicative 1 --output_folder $outputdir

# 464596 $train_no_cv --training_corpus tmVar_training --pruner parts --labeler IO --word_embeddings --we_additive 0 --we_multiplicative 1 --output_folder $outputdir --test_corpus tmVar_test
# 464618 $train_no_cv --training_corpus tmVar_training --pruner parts --labeler BIEO --word_embeddings --we_additive 0 --we_multiplicative 1 --output_folder $outputdir --test_corpus tmVar_test


# ------------------------------------------------------------------------------------------

# $train --training_corpus nala_training --pruner parts --labeler IO
# 455859.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --nl --nl_threshold 0
# 455860.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --nl --nl_threshold 1
# 455861.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --nl --nl_threshold 2
# 455862.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --nl --nl_threshold 3
# 455863.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --nl --nl_threshold 4
# 455864.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --nl --nl_threshold 5
# 455865.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --nl --nl_threshold 6
# 455866.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --nl --nl_threshold 7
# 455867.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --nl --nl_threshold 8
# 455868.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --nl --nl_threshold 9
# 455869.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --nl --nl_threshold 10

# 455870.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --nl --nl_threshold 4 --nl_window

# 456048.1-5 $train --training_corpus nala_training --pruner parts --labeler IO
# 456049.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --nl --nl_threshold 0
# 456050.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --nl --nl_threshold 0 --nl_window


# ------------------------------------------------------------------------------------------

# as=('0' '0.1' '0.5' '1' '2' '3')
# #ms=('1' '1.1' '1.5' '2' '3' '4')
# ms=('2' '3' '4')
# cv_folds=('0' '1' '2' '3' '4')

# 455886.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 0 --we_multiplicative 1.0 --we_model_location /mnt/project/pubseq/nala/backup_we/300_10_0_5_False.model

# $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 0.1 --we_multiplicative 1.0
# $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 0.5 --we_multiplicative 1.0
# $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 1.0 --we_multiplicative 1.0
# $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 2.0 --we_multiplicative 1.0
# $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 3.0 --we_multiplicative 1.0
# $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 0.1 --we_multiplicative 1.1
# $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 0.5 --we_multiplicative 1.1
# $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 1.0 --we_multiplicative 1.1

# 455774.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 2.0 --we_multiplicative 1.1
# 455775.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 3.0 --we_multiplicative 1.1
# 455777.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 0.1 --we_multiplicative 1.5
# 455778.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 0.5 --we_multiplicative 1.5
# 455779.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 1.0 --we_multiplicative 1.5
# 455780.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 2.0 --we_multiplicative 1.5
# 455781.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 3.0 --we_multiplicative 1.5


# 455758.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 0 --we_multiplicative 0
# 455759.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 0 --we_multiplicative 1.0
# 455760.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 0 --we_multiplicative 1.1
# 455761.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 0 --we_multiplicative 1.5
#
# 455762.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 0 --we_multiplicative 2
# 450502.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 0.1 --we_multiplicative 2
# 450503.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 0.5 --we_multiplicative 2
# 450850.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 1.0 --we_multiplicative 2
# 450455.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 2.0 --we_multiplicative 2
# 450810.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 3.0 --we_multiplicative 2
#
# 455763.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 0 --we_multiplicative 3
# 450812.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 0.1 --we_multiplicative 3
# 450459.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 0.5 --we_multiplicative 3
# 450460.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 1.0 --we_multiplicative 3
# 450461.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 2.0 --we_multiplicative 3
# 450462.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 3.0 --we_multiplicative 3
#
# 455764.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 0 --we_multiplicative 4
# 450814.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 0.1 --we_multiplicative 4
# 450465.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 0.5 --we_multiplicative 4
# 450815.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 1.0 --we_multiplicative 4
# 450467.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 2.0 --we_multiplicative 4
# 450468.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 3.0 --we_multiplicative 4
#
# 455765.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 0 --we_multiplicative 5
# 455766.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 0 --we_multiplicative 6
# 455767.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 0 --we_multiplicative 7
# 455768.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive 0 --we_multiplicative 10

#
# for a in "${as[@]}"
# do
#   for m in "${ms[@]}"
#   do
#     jobid="we_${a}_${m}"
#     for cv_fold in "${cv_folds[@]}"
#     do
#       echo "$jobid - $cv_fold"
#       common=" --cv_n 5 --cv_fold $cv_fold --model_name_suffix $jobid"
#       train="time $python $trainscript $common "
#       $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --we_additive $a --we_multiplicative $m &> "$outputdir2/wesearch_o${jobid}.${cv_fold}"
#     done
#   done
# done

# ---

# 450064.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings
# 450067.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --word_embeddings --elastic_net

# ---

# ST
# (BASELINE) $train --training_corpus nala_training --pruner parts --labeler BIEO --output_folder $outputdir
# 446478.1-5 $train --training_corpus nala_training --pruner parts --labeler IO --output_folder $outputdir

# all3
# 446477.1-5 $train --training_corpus nala_training --pruner sentences --ps_ST --ps_NL --labeler BIO --output_folder $outputdir

# ---

# Question elastic net

# 446460.1-5 $train --training_corpus nala_training --pruner sentences --ps_ST --ps_NL --labeler BIO --elastic_net --output_folder $outputdir

# ---

# Question IO labeler

# Deleting class 0, all suck
# 432102.1-5 $train --training_corpus nala_training --delete_subclasses "0" --pruner sentences --ps_ST --ps_NL --labeler IO
# 432103.1-5 $train --training_corpus nala_training --delete_subclasses "0" --pruner sentences --labeler IO
# 432104.1-5 $train --training_corpus nala_training --delete_subclasses "0" --pruner parts --labeler IO
#
# 432105.1-5 $train --training_corpus nala_training --pruner sentences --ps_ST --ps_NL --labeler IO
# 432106.1-5 $train --training_corpus nala_training --pruner sentences --labeler IO
# 432107.1-5 $train --training_corpus nala_training --pruner parts --labeler IO
#
# # Question BIO labeler
#
# 432108.1-5 $train --training_corpus nala_training --delete_subclasses "0" --pruner sentences --ps_ST --ps_NL --labeler BIO
# 432109.1-5 $train --training_corpus nala_training --delete_subclasses "0" --pruner sentences --labeler BIO
# 432110.1-5 $train --training_corpus nala_training --delete_subclasses "0" --pruner parts --labeler BIO
#
# 432111.1-5 $train --training_corpus nala_training --pruner sentences --ps_ST --ps_NL --labeler BIO
# 432112.1-5 $train --training_corpus nala_training --pruner sentences --labeler BIO
# 432113.1-5 $train --training_corpus nala_training --pruner parts --labeler BIO
#
# # ---
#
# # Question combination of training data, del classes, and pruning --> IDP4+_training
#
# 446459.1-5 $train --training_corpus IDP4+_training --delete_subclasses "1,2" --pruner sentences --ps_ST --ps_NL
# 446458.1-5 $train --training_corpus IDP4+_training --delete_subclasses "1,2" --pruner parts
# 446456.1-5 $train --training_corpus IDP4+_training --delete_subclasses "0" --pruner sentences --ps_ST --ps_NL
# 446455.1-5 $train --training_corpus IDP4+_training --delete_subclasses "0" --pruner parts
# 446454.1-5 $train --training_corpus IDP4+_training --pruner sentences --ps_ST --ps_NL
# 446453.1-5 $train --training_corpus IDP4+_training --pruner parts
#
# # ---
#
# # Question combination of training data, del classes, and pruning --> nala_training
#
# 432131.1-5 $train --training_corpus nala_training --delete_subclasses "1,2" --pruner sentences --ps_ST --ps_NL
# 432132.1-5 $train --training_corpus nala_training --delete_subclasses "1,2" --pruner sentences --ps_NL
# 432133.1-5 $train --training_corpus nala_training --delete_subclasses "1,2" --pruner sentences --ps_ST
# 432134.1-5 $train --training_corpus nala_training --delete_subclasses "1,2" --pruner sentences
# 432135.1-5 $train --training_corpus nala_training --delete_subclasses "1,2" --pruner parts
#
# 432136.1-5 $train --training_corpus nala_training --delete_subclasses "0" --pruner sentences --ps_ST --ps_NL
# 432137.1-5 $train --training_corpus nala_training --delete_subclasses "0" --pruner sentences --ps_NL
# 432138.1-5 $train --training_corpus nala_training --delete_subclasses "0" --pruner sentences --ps_ST
# 432139.1-5 $train --training_corpus nala_training --delete_subclasses "0" --pruner sentences
# 432140.1-5 $train --training_corpus nala_training --delete_subclasses "0" --pruner parts
#
# 432141.1-5 $train --training_corpus nala_training --pruner sentences --ps_ST --ps_NL
# 432142.1-5 $train --training_corpus nala_training --pruner sentences --ps_NL
# 432143.1-5 $train --training_corpus nala_training --pruner sentences --ps_ST
# 432144.1-5 $train --training_corpus nala_training --pruner sentences
# this is the baseline, so no run $train --training_corpus nala_training --pruner parts


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
