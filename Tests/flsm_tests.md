# Fixed Length Subnet Mask (FLSM) Tests

This document outlines test cases for the flsm.py module, which handles Fixed Length Subnet Mask (FLSM) calculations.

## Overview

The FLSM tool provides functionality to:
- Create equal-sized subnets from a parent network
- Calculate subnet information based on number of subnets needed
- Calculate subnet information based on a specific prefix length

## Test Cases

### Test 1: FLSM by Number of Subnets

```bash
./subcalc --network 192.168.0.0/24 --flsm 4
```

**Expected Results:**
* Creation of 4 equal-sized subnets
* Each subnet having a /26 prefix (64 addresses each)
* Proper subnet boundaries and address ranges

**Sample Output:**
```

FLSM Summary:
Base Network:         192.168.0.0/24
Subnet Bits:          2
New Prefix Length:    /26
Subnet Mask:          255.255.255.192
Hosts per Subnet:     62
Requested Subnets:    4
Actual Subnets:       4
Unused Subnets:       0

+----------+------------------+-----------------+---------------+---------------+---------------+---------------+-------+
| Subnet   | CIDR Notation    | Subnet Mask     | Network ID    | Broadcast ID  | First Host IP | Last Host IP  | Hosts |
+----------+------------------+-----------------+---------------+---------------+---------------+---------------+-------+
| Subnet 1 | 192.168.0.0/26   | 255.255.255.192 | 192.168.0.0   | 192.168.0.63  | 192.168.0.1   | 192.168.0.62  | 62    |
+----------+------------------+-----------------+---------------+---------------+---------------+---------------+-------+
| Subnet 2 | 192.168.0.64/26  | 255.255.255.192 | 192.168.0.64  | 192.168.0.127 | 192.168.0.65  | 192.168.0.126 | 62    |
+----------+------------------+-----------------+---------------+---------------+---------------+---------------+-------+
| Subnet 3 | 192.168.0.128/26 | 255.255.255.192 | 192.168.0.128 | 192.168.0.191 | 192.168.0.129 | 192.168.0.190 | 62    |
+----------+------------------+-----------------+---------------+---------------+---------------+---------------+-------+
| Subnet 4 | 192.168.0.192/26 | 255.255.255.192 | 192.168.0.192 | 192.168.0.255 | 192.168.0.193 | 192.168.0.254 | 62    |
+----------+------------------+-----------------+---------------+---------------+---------------+---------------+-------+

```

### Test 2: FLSM by Prefix Length

```bash
./subcalc --network 192.168.0.0/24 --flsm /28
```

**Expected Results:**
* Creation of subnets with /28 prefix (16 addresses each)
* All possible subnets within the parent network
* Proper subnet boundaries and address ranges

**Sample Output:**
```

FLSM Summary:
Base Network:         192.168.0.0/24
Subnet Bits:          4
New Prefix Length:    /28
Subnet Mask:          255.255.255.240
Hosts per Subnet:     14
Specified Prefix:     /28
Maximum Subnets:      16
Created Subnets:      16

+-----------+------------------+-----------------+---------------+---------------+---------------+---------------+-------+
| Subnet    | CIDR Notation    | Subnet Mask     | Network ID    | Broadcast ID  | First Host IP | Last Host IP  | Hosts |
+-----------+------------------+-----------------+---------------+---------------+---------------+---------------+-------+
| Subnet 1  | 192.168.0.0/28   | 255.255.255.240 | 192.168.0.0   | 192.168.0.15  | 192.168.0.1   | 192.168.0.14  | 14    |
+-----------+------------------+-----------------+---------------+---------------+---------------+---------------+-------+
| Subnet 2  | 192.168.0.16/28  | 255.255.255.240 | 192.168.0.16  | 192.168.0.31  | 192.168.0.17  | 192.168.0.30  | 14    |
+-----------+------------------+-----------------+---------------+---------------+---------------+---------------+-------+
| Subnet 3  | 192.168.0.32/28  | 255.255.255.240 | 192.168.0.32  | 192.168.0.47  | 192.168.0.33  | 192.168.0.46  | 14    |
+-----------+------------------+-----------------+---------------+---------------+---------------+---------------+-------+
...........												...........										   ...........
| Subnet 13 | 192.168.0.192/28 | 255.255.255.240 | 192.168.0.192 | 192.168.0.207 | 192.168.0.193 | 192.168.0.206 | 14    |
+-----------+------------------+-----------------+---------------+---------------+---------------+---------------+-------+
| Subnet 14 | 192.168.0.208/28 | 255.255.255.240 | 192.168.0.208 | 192.168.0.223 | 192.168.0.209 | 192.168.0.222 | 14    |
+-----------+------------------+-----------------+---------------+---------------+---------------+---------------+-------+
| Subnet 15 | 192.168.0.224/28 | 255.255.255.240 | 192.168.0.224 | 192.168.0.239 | 192.168.0.225 | 192.168.0.238 | 14    |
+-----------+------------------+-----------------+---------------+---------------+---------------+---------------+-------+
| Subnet 16 | 192.168.0.240/28 | 255.255.255.240 | 192.168.0.240 | 192.168.0.255 | 192.168.0.241 | 192.168.0.254 | 14    |
+-----------+------------------+-----------------+---------------+---------------+---------------+---------------+-------+

```

### Test 3: Class B Network with FLSM

```bash
./subcalc --network 172.16.0.0/16 --flsm 8
```

**Expected Results:**
* Creation of 8 equal-sized subnets
* Each subnet having a /19 prefix (8,192 addresses each)
* Proper subnet boundaries and address ranges

### Test 4: Small Network with Many Subnets

```bash
./subcalc --network 192.168.0.0/24 --flsm 64
```

**Expected Results:**
* Creation of 64 equal-sized subnets
* Each subnet having a /30 prefix (4 addresses each, 2 usable)
* Proper subnet boundaries and address ranges

### Test 5: Subnet Request Exceeding Capacity

```bash
./subcalc --network 192.168.0.0/24 --flsm 1000
```

**Expected Results:**
* Error message indicating that the requested number of subnets exceeds capacity
* The error should explain that creating 1000 subnets would result in a prefix length greater than /30

### Test 6: Interactive Mode

```bash
./subcalc --flsm
```

**Expected Results:**
* Interactive prompt for base network address
* Interactive prompt for subnet information (number or prefix)
* Proper calculation based on provided information

## Edge Cases

### Test 7: Large Network with Small Subnets

```bash
./subcalc --network 10.0.0.0/8 --flsm /24
```

**Expected Results:**
* Creation of many /24 subnets (65,536 subnets)
* Proper subnet boundaries and address ranges
* Efficient display handling of large number of subnets

### Test 8: Requesting Smaller Prefix than Original

```bash
./subcalc --network 192.168.0.0/24 --flsm /16
```

**Expected Results:**
* Error message indicating that the new prefix must be larger than the original prefix
* Clear explanation that /16 cannot be used for a /24 network

### Test 9: Maximum Allowed Prefix Length

```bash
./subcalc --network 192.168.0.0/24 --flsm /30
```

**Expected Results:**
* Creation of subnets with /30 prefix (4 addresses each)
* All possible subnets within the parent network
* Proper subnet boundaries and address ranges

### Test 10: Invalid Network Address

```bash
./subcalc --network 300.168.0.0/24 --flsm 4
```

**Expected Results:**
* Error message indicating that the network address is invalid
* No subnet calculation performed

## Test Validation Matrix

| Test Case | Description              | Expected Result                     | 
|-----------|--------------------------|-------------------------------------|
| Test 1    | Basic FLSM by count      | 4 equal /26 subnets                 |
| Test 2    | FLSM by prefix           | 16 equal /28 subnets                |
| Test 3    | Class B network          | 8 equal /19 subnets                 |
| Test 4    | Small subnets            | 64 equal /30 subnets                |
| Test 5    | Exceeding capacity       | Error message                       |
| Test 6    | Interactive mode         | Interactive prompts and calculation |
| Test 7    | Large network            | Many /24 subnets (65,536)           |
| Test 8    | Invalid prefix           | Error message                       |
| Test 9    | Maximum prefix           | Multiple /30 subnets                |
| Test 10   | Invalid network          | Error message                       | 