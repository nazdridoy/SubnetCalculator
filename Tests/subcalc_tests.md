# SubnetCalculator Main Script Tests

This document outlines test cases for the main `subcalc` executable, which integrates all the functionality of the Subnet Calculator tool.

## Overview

The SubnetCalculator main script provides:
- A command-line interface to all subnet calculation modules
- Argument parsing and validation
- Interactive and non-interactive operation modes
- Integration of all subnet calculator features

## Test Cases

### Test 1: Network Summary Display

```bash
./subcalc --network 192.168.0.0/24
```

**Expected Results:**
* Display of network information for 192.168.0.0/24
* Network address, broadcast address, netmask
* Number of total and usable addresses
* First and last usable host addresses

**Sample Output:**
```
Network Summary for 192.168.0.0/24:
Network Address:     192.168.0.0
Broadcast Address:   192.168.0.255
Netmask:             255.255.255.0
Prefix Length:       /24
Number of Addresses: 256
Usable Hosts:        254
First Usable Host:   192.168.0.1
Last Usable Host:    192.168.0.254
```

### Test 2: Help Display

```bash
./subcalc --help
```

**Expected Results:**
* Display of the help text with usage information
* List of all available options and arguments
* Examples of command usage

### Test 3: FLSM with Number of Subnets

```bash
./subcalc --network 192.168.0.0/24 --flsm 4
```

**Expected Results:**
* Creation and display of 4 equal-sized subnets
* FLSM summary information
* Table displaying subnet details

### Test 4: FLSM with Prefix Length

```bash
./subcalc --network 192.168.0.0/24 --flsm /28

```

**Expected Results:**
* Creation and display of subnets with /28 prefix for both commands
* FLSM summary information
* Table displaying subnet details

### Test 5: VLSM with Host Requirements

```bash
./subcalc --network 192.168.0.0/24 --vlsm 100 50 25 10
```

**Expected Results:**
* Creation and display of subnets sized for the specified host requirements
* Table displaying subnet details
* Proper allocation from largest to smallest

## Interactive Modes

### Test 6: Interactive FLSM

```bash
./subcalc --flsm
```

**Expected Results:**
* Interactive prompt for base network address
* Interactive prompt for subnet information
* Display of subnet calculation results

### Test 7: Interactive VLSM

```bash
./subcalc --vlsm
```

**Expected Results:**
* Interactive prompt for base network address
* Interactive prompt for host requirements
* Display of subnet calculation results

### Test 8: Interactive Conversion

```bash
./subcalc --convert
```

**Expected Results:**
* Interactive prompt for notation to convert
* Display of conversion results

## Error Handling Tests

### Test 9: Invalid Network Address

```bash
./subcalc --network 300.168.0.0/24
```

**Expected Results:**
* Error message indicating that the network address is invalid
* No further calculations performed

### Test 10: No Arguments

```bash
./subcalc
```

**Expected Results:**
* Display of help text
* Error message indicating that at least one option is required

### Test 11: Invalid FLSM Parameters

```bash
./subcalc --network 192.168.0.0/24 --flsm 1000
```

**Expected Results:**
* Error message indicating that the requested number of subnets exceeds capacity
* No subnet calculation performed

### Test 12: Invalid VLSM Parameters

```bash
./subcalc --network 192.168.0.0/24 --vlsm 300 200 100
```

**Expected Results:**
* Error message indicating that the host requirements exceed the available address space
* No subnet calculation performed

## Integration Tests

### Test 13: Combined Commands

```bash
./subcalc --network 192.168.0.0/24 --supernet 192.168.0.0/25 192.168.0.128/25
```

**Expected Results:**
* Error message or warning about conflicting commands
* Only one operation should be performed
* Clear guidance on how to use commands correctly

### Test 14: Processing Interruption

```bash
# Start a long-running command and interrupt with Ctrl+C
./subcalc --network 10.0.0.0/8 --flsm /24
```

**Expected Results:**
* Graceful handling of keyboard interruption
* Display of "Operation cancelled by user" message
* Clean exit without error traceback

## Compatibility Tests

### Test 15: Script Execution Permission

```bash
# Make the script non-executable, then try to run it
chmod -x subcalc
./subcalc --network 192.168.0.0/24
```

**Expected Results:**
* Error message about permission denied
* After restoring execution permission, the script should work again

### Test 16: Python Version Compatibility

```bash
# Run with different Python versions if available
python3.7 subcalc --network 192.168.0.0/24
python3.8 subcalc --network 192.168.0.0/24
```

**Expected Results:**
* Consistent operation across different supported Python versions
* No version-specific errors or warnings

## Test Validation Matrix

| Test Case | Command/Scenario                               | Expected Result                        |
|-----------|-----------------------------------------------|-----------------------------------------|
| Test 1    | --network 192.168.0.0/24                      | Network summary display                |
| Test 2    | --help                                         | Help text display                      |
| Test 3    | --network 192.168.0.0/24 --flsm 4             | 4 equal-sized subnets                 |
| Test 4    | --network 192.168.0.0/24 --flsm /28           | Subnets with /28 prefix               |

| Test 5    | --network 192.168.0.0/24 --vlsm 100 50 25 10  | Subnets for host requirements         |
| Test 6    | --flsm (interactive)                           | Interactive FLSM calculation          |
| Test 7    | --vlsm (interactive)                           | Interactive VLSM calculation          |
| Test 8    | --convert (interactive)                        | Interactive notation conversion       |
| Test 9    | --network 300.168.0.0/24                      | Invalid network error                 |
| Test 10   | (no arguments)                                 | Help display with error               |
| Test 11   | --network 192.168.0.0/24 --flsm 1000          | Invalid FLSM parameters error         |
| Test 12   | --network 192.168.0.0/24 --vlsm 300 200 100   | Invalid VLSM parameters error         |
| Test 13   | --network 192.168.0.0/24 --supernet ...       | Command conflict handling             |
| Test 14   | (keyboard interruption)                        | Graceful interruption handling        |
| Test 15   | (execution permission)                         | Permission handling                   |
| Test 16   | (Python version compatibility)                 | Consistent cross-version operation    | 