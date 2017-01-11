rm job_submission/*res*.stderr
rm job_submission/*res*.stdout

#test job:
#qsub -q localgrid@cream02 -o script_test.stdout -e script_test.stderr script.sh

for index in `seq 0 ${1}`; do
    sed -i "s/-i [0-9]*/-i ${index}/" job_submission/script_resolution.sh
    qsub -q localgrid@cream02 -o job_submission/script_res_${index}.stdout -e job_submission/script_res_${index}.stderr job_submission/script_resolution.sh
done


