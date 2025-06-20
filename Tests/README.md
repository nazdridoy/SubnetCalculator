# SubnetCalculator Test Suite

This directory contains test documentation for the SubnetCalculator tool. Each markdown file provides detailed test cases for specific components of the application.

## Test Documentation Files

### Main Components

- [**subcalc_tests.md**](subcalc_tests.md): Tests for the main executable script, including command-line argument handling, integration tests, error handling, and compatibility tests.

### Core Modules

- [**supernet_tests.md**](supernet_tests.md): Tests for supernetting and CIDR aggregation operations, including adjacent networks, non-adjacent networks, and highly disjoint networks.
- [**flsm_tests.md**](flsm_tests.md): Tests for Fixed Length Subnet Mask (FLSM) calculations, including creating subnets by count and by prefix length.
- [**vlsm_tests.md**](vlsm_tests.md): Tests for Variable Length Subnet Mask (VLSM) calculations, including optimal subnet allocation based on host requirements.

### Utility Modules

- [**notation_tests.md**](notation_tests.md): Tests for conversion between different subnet notation formats (CIDR, subnet mask, wildcard mask).
- [**iputility_tests.md**](iputility_tests.md): Tests for IP address utilities, including validation, network membership checks, and IP range analysis.

## Running Tests

The test cases documented in these files can be manually executed using the SubnetCalculator tool. Each test file includes:

1. Command-line examples
2. Expected outputs
3. Edge case tests
4. Test validation matrices

To run a specific test case, copy the command from the test file and execute it in your terminal. For example:

```bash
./subcalc --supernet 10.0.0.0/24 10.0.1.0/24
```

## Test Categories

Each test file follows a similar structure with these categories of tests:

1. **Basic Functionality Tests**: Common use cases that verify core functionality
2. **Edge Case Tests**: Tests that explore boundary conditions and unusual inputs
3. **Interactive Mode Tests**: Tests for the interactive prompts and user input
4. **Error Handling Tests**: Tests that verify proper handling of invalid inputs
5. **Validation Matrices**: Tables summarizing expected results for test cases

## Adding New Tests

When adding new features to the SubnetCalculator tool, follow these guidelines for adding test cases:

1. Identify the appropriate test file for your feature
2. Create test cases that verify correct functionality
3. Include edge cases and error conditions
4. Document expected outputs
5. Update the validation matrix

## Test Environment

All tests are designed to run on any system that supports Python 3.x and can execute the SubnetCalculator tool. 