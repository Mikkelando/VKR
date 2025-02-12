# algorithm.py

"""
This script replicates the behavior of algorithm.gms in GAMS:
It imports the optimization logic from 'optimization_loop' and passes
a list of coalition-changing times (akin to %coalitions_t_sequence% in GAMS).
"""

from algorithm.optimization_loop import run_optimization

def main(coalitions_t_sequence):
    """
    Launch the optimization logic with the given coalition-changing times.
    Equivalent to:
    $batinclude "algorithm/optimization_loop" %coalitions_t_sequence%
    in GAMS.
    """
    print("Launching optimization with the following coalition times:", coalitions_t_sequence)
    run_optimization(coalitions_t_sequence)

if __name__ == "__main__":
    # Example usage:
    # In a production setting, you could parse these from command-line arguments
    # or configuration files.
    example_coalitions_t_sequence = [2025, 2030, 2035, 2040]  # Example times
    main(example_coalitions_t_sequence)
