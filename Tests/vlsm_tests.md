# Variable Length Subnet Mask (VLSM) Tests

This document outlines test cases for the vlsm.py module, which handles Variable Length Subnet Mask (VLSM) calculations.

## Overview

The VLSM tool provides functionality to:
- Create differently-sized subnets from a parent network
- Allocate subnet sizes based on specific host requirements
- Optimize address space usage with variable-length prefixes

## Test Cases

### Test 1: Basic VLSM Allocation

```bash
./subcalc --network 192.168.0.0/24 --vlsm 100 50 25 10
```

**Expected Results:**
* Creation of 4 subnets with varying sizes based on host requirements
* Efficient allocation from largest to smallest requirement
* No address space wasted between subnets

**Sample Output:**
```
+----------+----------------+--------------+---------------+---------------+---------------+--------------+------------+
| Subnet   | Subnet Mask    | Network ID   | Broadcast ID  | First Host IP | Last Host IP  | Needed Hosts | Total Hosts|
+----------+----------------+--------------+---------------+---------------+---------------+--------------+------------+
| Subnet 1 | 255.255.255.128| 192.168.0.0  | 192.168.0.127 | 192.168.0.1   | 192.168.0.126 | 100          | 126        |
| Subnet 2 | 255.255.255.192| 192.168.0.128| 192.168.0.191 | 192.168.0.129 | 192.168.0.190 | 50           | 62         |
| Subnet 3 | 255.255.255.224| 192.168.0.192| 192.168.0.223 | 192.168.0.193 | 192.168.0.222 | 25           | 30         |
| Subnet 4 | 255.255.255.240| 192.168.0.224| 192.168.0.239 | 192.168.0.225 | 192.168.0.238 | 10           | 14         |
+----------+----------------+--------------+---------------+---------------+---------------+--------------+------------+
```

### Test 2: Large Host Requirements

```bash
./subcalc --network 10.0.0.0/16 --vlsm 16000 8000 4000 1000 500
```

**Expected Results:**
* Creation of 5 subnets with varying sizes based on large host requirements
* Proper allocation from largest to smallest requirement
* Appropriate subnet masks for each requirement

### Test 3: Many Small Subnets

```bash
./subcalc --network 192.168.0.0/24 --vlsm 10 10 10 10 10 10 10 5 5 5 2 2 2 2
```

**Expected Results:**
* Creation of many small subnets with different requirements
* Efficient allocation despite having many subnets
* Proper boundaries between each subnet

### Test 4: Requirements Exceeding Capacity

```bash
./subcalc --network 192.168.0.0/24 --vlsm 100 100 100
```

**Expected Results:**
* Error message indicating that the host requirements exceed the available address space
* Clear explanation that 300+ hosts cannot fit in a /24 network (which has 254 usable hosts)

### Test 5: Interactive Mode

```bash
./subcalc --vlsm
```

**Expected Results:**
* Interactive prompt for base network address
* Interactive prompt for host requirements
* Proper calculation based on provided information

## Edge Cases

### Test 6: Single Large Subnet

```bash
./subcalc --network 192.168.0.0/24 --vlsm 200
```

**Expected Results:**
* Creation of a single subnet that uses most of the address space
* Proper subnet mask and address range for the requirement

### Test 7: Maximum Utilization

```bash
./subcalc --network 192.168.0.0/24 --vlsm 125 60 30 10 5 2
```

**Expected Results:**
* Creation of subnets that utilize almost all available address space
* Efficient allocation with minimal waste

### Test 8: Exact Requirements

```bash
./subcalc --network 192.168.0.0/23 --vlsm 126 126 126 126
```

**Expected Results:**
* Creation of 4 subnets that exactly fit the requirements
* Each subnet should be exactly a /25 (126 usable hosts)
* No address space wasted

### Test 9: Very Small Requirements

```bash
./subcalc --network 192.168.0.0/24 --vlsm 2 2 2 2 2 2 2 2
```

**Expected Results:**
* Creation of many /30 subnets (smallest practical subnet with 2 usable hosts)
* Proper allocation and addressing

### Test 10: Invalid Network Address

```bash
./subcalc --network 300.168.0.0/24 --vlsm 100 50 25
```

**Expected Results:**
* Error message indicating that the network address is invalid
* No subnet calculation performed

## Test Validation Matrix

| Test Case | Description            | Expected Result                     | 
|-----------|------------------------|-------------------------------------|
| Test 1    | Basic VLSM allocation  | 4 subnets with varying sizes        |
| Test 2    | Large requirements     | Proper allocation of large subnets  |
| Test 3    | Many small subnets     | Efficient allocation of many subnets|
| Test 4    | Exceeding capacity     | Error message                       |
| Test 5    | Interactive mode       | Interactive prompts and calculation |
| Test 6    | Single large subnet    | One subnet using most space         |
| Test 7    | Maximum utilization    | Minimal wasted space                |
| Test 8    | Exact requirements     | All subnets exactly match needs     |
| Test 9    | Very small requirements| Many /30 subnets                    |
| Test 10   | Invalid network        | Error message                       | 