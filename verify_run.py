"""
Simple runner to execute the built-in verification test.

Usage:
  python verify_run.py

This will invoke the inference_engine's verification function which prints a
hard-coded test case and the diagnostic results to the console for grading and
validation purposes.
"""

from inference_engine import run_verification


if __name__ == "__main__":
    run_verification()
