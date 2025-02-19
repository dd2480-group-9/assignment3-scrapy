from pathlib import Path
import json

# File path in the top folder (adjust as needed)
coverage_file = Path.cwd() / "coverage_report.json"

# Load existing data if the file exists
with coverage_file.open("r") as f:
    coverage_data = json.load(f)

with Path.open("diy_coverage_report.txt", "w") as f:
    f.write("Coverage report of five functions in Scrapy.\n\n")
    total_coverage_tracker = [0,0]
    for func,branches in coverage_data.items():
        f.write("-"*45 + "\n")
        f.write(f"Function: {func}\n")
        for num,branch in enumerate(branches):
            f.write(f"\tBranch {num+1:>2}: {branch}\n")
        covered_branches = branches.count(True)
        total_branches = len(branches)
        f.write(f"Function coverage: {(covered_branches / total_branches) * 100:.2f}%\n")
        f.write("-"*45 + "\n\n")
        total_coverage_tracker[0] += covered_branches
        total_coverage_tracker[1] += total_branches
    f.write(f"Total coverage: {(total_coverage_tracker[0] / total_coverage_tracker[1]) * 100:.2f}%\n\n")
    f.write("-"*45)
    
print(f"Coverage data written to diy_coverage_report.txt.")