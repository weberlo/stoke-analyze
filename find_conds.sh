#!/usr/bin/env bash

set -e

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "${script_dir}"

>main.log
global_swap_mass="0"
rotate_mass="0"
cost="correctness"
distance="affine"
# distance="hamming"
beta="0.3"
instr_num="5"

archive_dir="archive/tc_restrict_num/2-4-21/binary_affine"

for distance in affine hamming; do
for beta in 0.1 0.3; do
for instr_num in 5 8 16; do
  echo "${archive_dir}/dist_${distance}_gsm_${global_swap_mass}_rm_${rotate_mass}_cost_${cost}_beta_${beta}_inum_${instr_num}"
  cat ${archive_dir}/*/dist_${distance}_gsm_${global_swap_mass}_rm_${rotate_mass}_cost_${cost}_beta_${beta}_inum_${instr_num}.log \
    | egrep '^set.*%' \
    | wc -l
  # cat ${archive_dir}/*/dist_${distance}_gsm_${global_swap_mass}_rm_${rotate_mass}_cost_${cost}_beta_${beta}_inum_${instr_num}.log \
  #   | egrep '^set.*%' -C 1 \
  #   | head -n 20
done
done
done
