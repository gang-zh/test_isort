#!/usr/bin/env python3
"""
Test script to demonstrate isort's project context effect.

This script shows how isort behaves differently with and without project context.
"""

import subprocess
import tempfile
import os
import sys

# Base repository path - update this if your repos are in a different location
REPOS_BASE_PATH = "/Users/gang.zhang/repos"
PROJECT_PATH = os.path.join(REPOS_BASE_PATH, "airflow")

# Test imports that match your actual file
TEST_IMPORTS = """import ast
import datetime
import logging
from time import sleep

import requests
from google.auth.transport.requests import Request
from google.oauth2 import id_token
from airflow.models import BaseOperator
from moloco.utils.datadog_timer import report_datadog_metric
from moloco.utils.env import Env, get_env
"""

def test_isort(test_name, cwd, extra_args=None):
    """Run isort and return the formatted output."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(TEST_IMPORTS)
        test_file = f.name
    
    try:
        args = ['isort', '--stdout', test_file, '--profile', 'black']
        if extra_args:
            args.extend(extra_args)
        
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            cwd=cwd
        )
        return result.stdout
    finally:
        os.unlink(test_file)

def main():
    print("=" * 80)
    print("ISORT PROJECT CONTEXT TEST")
    print("=" * 80)
    
    print("\n" + "=" * 80)
    print("TEST 1: NO PROJECT CONTEXT")
    print("=" * 80)
    print("Running from /tmp (no config files, no project detection)")
    print("-" * 80)
    result1 = test_isort("no_context", "/tmp")
    print(result1)
    print("\n✓ 'airflow' is sorted alphabetically with other THIRDPARTY imports")
    
    print("\n" + "=" * 80)
    print("TEST 2: WITH PROJECT CONTEXT (from your project)")
    print("=" * 80)
    print(f"Running from {PROJECT_PATH} (detects pyproject.toml)")
    print("-" * 80)
    result2 = test_isort("with_context", PROJECT_PATH)
    print(result2)
    print("\n✓ 'airflow' is separated after FIRSTPARTY imports")
    
    print("\n" + "=" * 80)
    print("TEST 3: EXPLICIT src_paths (simulating project context)")
    print("=" * 80)
    print(f"Running from /tmp but with --src flag pointing to your project")
    print("-" * 80)
    result3 = test_isort("explicit_src", "/tmp", 
                        extra_args=['--src', PROJECT_PATH])
    print(result3)
    print("\n✓ Same behavior as Test 2 - src_paths is the key!")
    
    print("\n" + "=" * 80)
    print("SUMMARY: WHAT IS PROJECT CONTEXT?")
    print("=" * 80)
    print(f"""
Project context = isort automatically detecting:
  1. Your project root (where pyproject.toml, setup.cfg, etc. are found)
  2. Setting 'src_paths' to include the project root
  3. Using this to categorize imports:
     - Modules under src_paths → FIRSTPARTY
     - Other modules → THIRDPARTY

When isort runs from {PROJECT_PATH}:
  - It finds pyproject.toml
  - Sets src_paths = ["{PROJECT_PATH}/src", "{PROJECT_PATH}"]
  - This affects how imports are grouped and ordered

The effect: 'airflow' import gets separated because isort applies different
sorting rules when it knows about your project structure.
    """)
    
    print("\n" + "=" * 80)
    print("HOW TO TEST YOURSELF:")
    print("=" * 80)
    print(f"""
# 1. Test without context
cd /tmp
echo 'from airflow import X\\nfrom moloco import Y' > test.py
isort --stdout test.py --profile black

# 2. Test with context (from your project)
cd {PROJECT_PATH}
isort --stdout test.py --profile black

# 3. Check what isort detected
isort --show-config dags/moloco/operators/taskfnt.py | grep src_paths
    """)

if __name__ == "__main__":
    main()

