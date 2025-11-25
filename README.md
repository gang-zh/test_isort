# test_isort

The output after running `python test_isort_context.py` under airflow/ repo.

```
================================================================================
ISORT PROJECT CONTEXT TEST
================================================================================

================================================================================
TEST 1: NO PROJECT CONTEXT
================================================================================
Running from /tmp (no config files, no project detection)
--------------------------------------------------------------------------------
import ast
import datetime
import logging
from time import sleep

import requests
from airflow.models import BaseOperator
from google.auth.transport.requests import Request
from google.oauth2 import id_token
from moloco.utils.datadog_timer import report_datadog_metric
from moloco.utils.env import Env, get_env


✓ 'airflow' is sorted alphabetically with other THIRDPARTY imports

================================================================================
TEST 2: WITH PROJECT CONTEXT (from your project)
================================================================================
Running from /Users/gang.zhang/repos/airflow (detects pyproject.toml)
--------------------------------------------------------------------------------
import ast
import datetime
import logging
from time import sleep

import requests
from google.auth.transport.requests import Request
from google.oauth2 import id_token
from moloco.utils.datadog_timer import report_datadog_metric
from moloco.utils.env import Env, get_env

from airflow.models import BaseOperator


✓ 'airflow' is separated after FIRSTPARTY imports

================================================================================
TEST 3: EXPLICIT src_paths (simulating project context)
================================================================================
Running from /tmp but with --src flag pointing to your project
--------------------------------------------------------------------------------
import ast
import datetime
import logging
from time import sleep

import requests
from google.auth.transport.requests import Request
from google.oauth2 import id_token
from moloco.utils.datadog_timer import report_datadog_metric
from moloco.utils.env import Env, get_env

from airflow.models import BaseOperator


✓ Same behavior as Test 2 - src_paths is the key!

================================================================================
SUMMARY: WHAT IS PROJECT CONTEXT?
================================================================================

Project context = isort automatically detecting:
  1. Your project root (where pyproject.toml, setup.cfg, etc. are found)
  2. Setting 'src_paths' to include the project root
  3. Using this to categorize imports:
     - Modules under src_paths → FIRSTPARTY
     - Other modules → THIRDPARTY

When isort runs from /Users/gang.zhang/repos/airflow:
  - It finds pyproject.toml
  - Sets src_paths = ["/Users/gang.zhang/repos/airflow/src", "/Users/gang.zhang/repos/airflow"]
  - This affects how imports are grouped and ordered

The effect: 'airflow' import gets separated because isort applies different
sorting rules when it knows about your project structure.
    

================================================================================
HOW TO TEST YOURSELF:
================================================================================

# 1. Test without context
cd /tmp
echo 'from airflow import X\nfrom moloco import Y' > test.py
isort --stdout test.py --profile black

# 2. Test with context (from your project)
cd /Users/gang.zhang/repos/airflow
isort --stdout test.py --profile black

# 3. Check what isort detected
isort --show-config dags/moloco/operators/taskfnt.py | grep src_paths
    ```
