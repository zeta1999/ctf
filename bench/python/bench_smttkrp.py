import ctf
import os
import argparse
import time
import sbench_args as sargs
import numpy as np

def run_bench(num_iter, s_start, s_end, mult, R, sp):
    wrld = ctf.comm()
    s = s_start
    nnz = s_start*s_start*s_start
    agg_s = []
    agg_avg_times = []
    agg_min_times = []
    agg_max_times = []
    agg_min_95 = []
    agg_max_95 = []
    while s<=s_end:
        agg_s.append(s)
        T = ctf.tensor((s,s,s),sp=sp)
        T.fill_sp_random(-1.,1.,float(nnz)/float(s*s*s))
        if ctf.comm().rank() == 0:
            print("T sp =",T.sp,"nnz_tot =",T.nnz_tot,"sp_frac is",float(nnz)/float(s*s*s))
        U = ctf.random.random((s,R))
        V = ctf.random.random((s,R))
        W = ctf.random.random((s,R))
        te1 = 0.
        te2 = 0.
        te3 = 0.
        avg_times = []
        for i in range(num_iter):
            t0 = time.time()
            U = ctf.einsum("ijk,jr,kr->ir",T,V,W)
            t1 = time.time()
            ite1 = t1 - t0
            te1 += ite1

            t0 = time.time()
            V = ctf.einsum("ijk,ir,kr->jr",T,U,W)
            t1 = time.time()
            ite2 = t1 - t0
            te2 += ite2

            t0 = time.time()
            W = ctf.einsum("ijk,ir,jr->kr",T,U,V)
            t1 = time.time()
            ite3 = t1 - t0
            te3 += ite3
            if ctf.comm().rank() == 0:
                print(ite1,ite2,ite3,"avg:",(ite1+ite2+ite3)/3.)
            avg_times.append((ite1+ite2+ite3)/3.)
        if ctf.comm().rank() == 0:
            print("Completed",num_iter,"iterations, took",te1/num_iter,te2/num_iter,te3/num_iter,"seconds on average for 3 variants.")
            avg_time = (te1+te2+te3)/(3*num_iter)
            agg_avg_times.append(avg_time)
            print("MTTKRP took",avg_times,"seconds on average across variants with s =",s,"nnz =",nnz,"sp",sp)
            min_time = np.min(avg_times)
            max_time = np.max(avg_times)
            agg_min_times.append(min_time)
            agg_max_times.append(max_time)
            print("min/max interval is [",min_time,",",max_time,"]")
            stddev = np.std(avg_times)
            min_95 = (te1+te2+te3)/(3*num_iter)-2*stddev
            max_95 = (te1+te2+te3)/(3*num_iter)+2*stddev
            agg_min_95.append(min_95)
            agg_max_95.append(max_95)
            print("95% confidence interval is [",min_95,",",max_95,"]")
        s = int(s*mult)
    if ctf.comm().rank() == 0:
        print("s min_time min_95 avg_time max_95 max_time")
        for i in range(len(agg_s)):
            print(agg_s[i], agg_min_times[i], agg_min_95[i], agg_avg_times[i], agg_max_95[i], agg_max_times[i])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    sargs.add_arguments(parser)
    args, _ = parser.parse_known_args()

    num_iter = args.num_iter
    s_start = args.s_start
    s_end = args.s_end
    mult = args.mult
    R = args.R
    sp = args.sp

    if ctf.comm().rank() == 0:
        print("num_iter is",num_iter,"s_start is",s_start,"s_end is",s_end,"mult is",mult,"R is",R,"sp is",sp)
    run_bench(num_iter, s_start, s_end, mult, R, sp)

