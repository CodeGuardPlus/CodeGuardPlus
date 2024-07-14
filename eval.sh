MODEL_DIR=$1
OUTPUT_NAME=$2
EVAL_TYPE=$3
DECODING=$4

# Check whether there are enough arguments
if [ $# -lt 4 ]; then
    echo "Usage: $0 MODEL_DIR OUTPUT_NAME EVAL_TYPE DECODING"
    exit 1
fi

# Running generation
echo "Running generation using $DECODING decoding."
COMMAND="python generate.py --model_type lm --model_dir $MODEL_DIR --output_name $OUTPUT_NAME --eval_type $EVAL_TYPE"
case "$DECODING" in
    nucleus)
        COMMAND+=" --do_sample --num_gen 10"
        ;;
    beam)
        COMMAND+=" --do_sample --num_beams 25 --num_gen 10"
        ;;
    cbs)
        COMMAND+=" --do_sample --num_beams 25 --num_gen 10 --use_pos_constraints --use_neg_constraints"
        ;;
    *)
        echo "Invalid DECODING method specified."
        continue
        ;;
esac

echo "Executing command: $COMMAND"
eval $COMMAND

# CodeQL evaluation
echo "Running CodeQL evaluation."
COMMAND="python codeql_eval.py --output_dir experiments/$OUTPUT_NAME --category $EVAL_TYPE"
echo "Executing command: $COMMAND"
eval $COMMAND

# SonarQube evaluation
echo "Running SonarQube evaluation."
COMMAND="python sonar_eval.py"
echo "Executing command: $COMMAND"
eval $COMMAND

# Functional correctness evaluation
echo "Running functional correctness evaluation."
COMMAND="python correctness_eval.py --paths experiments/$OUTPUT_NAME --do_eval --num_seeds 1"
echo "Executing command: $COMMAND"
eval $COMMAND

# Displaying results
echo "Results for $OUTPUT_NAME:"
COMMAND="python correctness_eval.py --paths experiments/$OUTPUT_NAME --do_print --num_seeds 1"
echo "Executing command: $COMMAND"
eval $COMMAND