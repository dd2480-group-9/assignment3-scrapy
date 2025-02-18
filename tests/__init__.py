"""
tests: this package contains all Scrapy unittests

see https://docs.scrapy.org/en/latest/contributing.html#running-tests
"""

import atexit
import json
import os
import socket
from pathlib import Path

# ignore system-wide proxies for tests
# which would send requests to a totally unsuspecting server
# (e.g. because urllib does not fully understand the proxy spec)
os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""
os.environ["ftp_proxy"] = ""

tests_datadir = str(Path(__file__).parent.resolve() / "sample_data")


# In some environments accessing a non-existing host doesn't raise an
# error. In such cases we're going to skip tests which rely on it.
try:
    socket.getaddrinfo("non-existing-host", 80)
    NON_EXISTING_RESOLVABLE = True
except socket.gaierror:
    NON_EXISTING_RESOLVABLE = False


def get_testdata(*paths: str) -> bytes:
    """Return test data"""
    return Path(tests_datadir, *paths).read_bytes()


# initialize coverage_data to keep track of branch coverage
coverage_data = {
    "_get_serialized_fields": [False],
    "_next_request": [False],
    "run": [False],
    "func_4": [False],
    "func_5": [False],
}


def output_coverage_data():
    # File path in the top folder (adjust as needed)
    coverage_file = Path.cwd() / "coverage_report.json"

    # Load existing data if the file exists
    if coverage_file.exists():
        try:
            with coverage_file.open("r") as f:
                previous_coverage = json.load(f)
        except json.JSONDecodeError:
            previous_coverage = {}
    else:
        previous_coverage = {}

    # Merge the new data with the existing data
    for func, branches in coverage_data.items():
        if func in previous_coverage:
            prev_branches = previous_coverage[func]
            merged = []
            for i, new_flag in enumerate(branches):
                old_flag = prev_branches[i] if i < len(prev_branches) else False
                merged.append(new_flag or old_flag)
            previous_coverage[func] = merged
        else:
            previous_coverage[func] = branches

    # Write the merged data back to the file
    with coverage_file.open("w") as f:
        json.dump(previous_coverage, f, indent=2)


# Register output_coverage_data to run when the program exits
atexit.register(output_coverage_data)
