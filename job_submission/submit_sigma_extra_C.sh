rm job_submission/*sigma_C*.stderr
rm job_submission/*sigma_C*.stdout

#test job:
#qsub -q localgrid@cream02 -o job_submission/script_sigma_test.stdout -e job_submission/script_sigma_test.stderr job_submission/script_sigma.sh

for index in `seq 0 ${1}`; do
    sed -i "s/-i [0-9]*/-i ${index}/" job_submission/script_sigma_C.sh
    qsub -q localgrid@cream02 -o job_submission/script_sigma_C${index}.stdout -e job_submission/script_sigma_C${index}.stderr job_submission/script_sigma_C.sh
done
