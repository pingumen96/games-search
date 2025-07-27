"""
Test runner for all unit tests.
"""
import unittest
import sys
import os

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def run_all_tests():
    """Discover and run all tests"""
    # Discover tests in the tests directory
    loader = unittest.TestLoader()
    test_suite = loader.discover('tests', pattern='test_*.py')

    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # Return exit code based on test results
    return 0 if result.wasSuccessful() else 1


def run_specific_test(test_module):
    """Run a specific test module"""
    try:
        suite = unittest.TestLoader().loadTestsFromName(f'tests.{test_module}')
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        return 0 if result.wasSuccessful() else 1
    except Exception as e:
        print(f"Error running test {test_module}: {e}")
        return 1


if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Run specific test module
        test_module = sys.argv[1]
        exit_code = run_specific_test(test_module)
    else:
        # Run all tests
        print("Running all tests...")
        exit_code = run_all_tests()

    sys.exit(exit_code)
