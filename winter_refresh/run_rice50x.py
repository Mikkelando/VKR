#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
run_rice50x.py

Equivalent logic to run_rice50x.gms in GAMS.
"""

import time
from modules_main import handle_modules
from algorithm.optimization_loop import run_optimization  # Обновленный импорт

def main():
    # 1) Record start time (equivalent to scalar starttime; starttime = jnow)
    start_time = time.time()
    
    # 2) Default settings (mimic $setglobal)
    n = "ed57"               # Region definition
    baseline = "ssp2"        # Baseline scenario
    policy = "bau"           # Policy
    cooperation = "noncoop"  # Cooperation mode
    impact = "kalkuhl"       # Impact specification
    climate = "witchco2"     # Climate module
    savings = "fixed"        # Savings rate
    nameout = f"{baseline}_{policy}"
    datapath = f"data_{n}/"
    
    # Results path (resdir) and output_filename
    resdir = "./"
    output_filename = f"results_{nameout}"
    
    print(f"Running RICE50+ with settings:")
    print(f"  region: {n}, baseline: {baseline}, policy: {policy}, cooperation: {cooperation}")
    print(f"  impact: {impact}, climate: {climate}, savings: {savings}")
    print(f"  nameout: {nameout}, datapath: {datapath}, resdir: {resdir}")

    # Define t_vals and n_vals for compute_data
    t_vals = list(range(1, 101))  # Example time steps
    n_vals = ['region1', 'region2', 'region3']  # Example regions

    # 3) Model definition through phases
    handle_modules(phase="conf", arg2=None, cooperation=cooperation, baseline=baseline, t_vals=t_vals, n_vals=n_vals)
    handle_modules(phase="sets", arg2=None, cooperation=cooperation, baseline=baseline, t_vals=t_vals, n_vals=n_vals)
    handle_modules(phase="include_data", arg2=None, cooperation=cooperation, baseline=baseline, t_vals=t_vals, n_vals=n_vals)
    handle_modules(phase="compute_data", arg2=None, cooperation=cooperation, baseline=baseline, t_vals=t_vals, n_vals=n_vals)
    handle_modules(phase="declare_vars", arg2=None, cooperation=cooperation, baseline=baseline, t_vals=t_vals, n_vals=n_vals)
    handle_modules(phase="compute_vars", arg2=None, cooperation=cooperation, baseline=baseline, t_vals=t_vals, n_vals=n_vals)

    # 4) Execution: run 'algorithm'
    run_optimization()

    # 5) Reporting
    handle_modules(phase="report", arg2=None, cooperation=cooperation, baseline=baseline, t_vals=t_vals, n_vals=n_vals)

    # 6) Time elapsed
    elapsed = time.time() - start_time
    
    # Placeholder for quick analysis
    tatm2100 = 2.5  # Example placeholder
    world_damfrac2100 = 0.03
    gdp2100 = 1.2e5

    print("\nQuick Analysis Values:")
    print(f"  tatm2100: {tatm2100}")
    print(f"  gdp2100: {gdp2100}")
    print(f"  world_damfrac2100: {world_damfrac2100}")
    print(f"  elapsed time (sec): {elapsed}")

    # 7) Produce results
    results_file = f"{resdir}/{output_filename}.json"
    print(f"\nSaving results to: {results_file} (example)")
    print("\nDone. RICE50+ run complete.")

if __name__ == "__main__":
    main()
