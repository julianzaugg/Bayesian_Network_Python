"""
An unfinished script to streamline the profiling process.
"""

import pstats
import cProfile

temp = cProfile.Profile()
temp.dump_stats("TrainExample.profile")

stats = pstats.Stats("TrainExample.profile")

# Clean up filenames for the report
stats.strip_dirs()

# Sort the statistics by the cumulative time spent in the function
stats.sort_stats("time")

stats.print_stats()

#python -m cProfile -o TrainExample.profile TrainExample.py


