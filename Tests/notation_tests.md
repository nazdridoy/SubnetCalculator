# Subnet Notation Conversion Tests

This document outlines test cases for the notation.py module, which handles conversions between different subnet notation formats.

## Overview

The notation conversion tool provides functionality to:
- Convert between CIDR notation (e.g., /24)
- Convert subnet masks (e.g., 255.255.255.0)
- Convert wildcard masks (e.g., 0.0.0.255)
- Display subnet information in multiple formats

## Test Cases

### Test 1: CIDR to Other Formats

```bash
./subcalc --convert /24
```

**Expected Results:**
* Conversion of CIDR notation /24 to:
  * Subnet mask: 255.255.255.0
  * Wildcard mask: 0.0.0.255
  * Binary representation: 11111111.11111111.11111111.00000000
  * Number of addresses: 256

**Sample Output:**
```
Notation Conversion Results:

CIDR Notation:      /24
Subnet Mask:        255.255.255.0
Wildcard Mask:      0.0.0.255
Binary Mask:        11111111.11111111.11111111.00000000
Hex Mask:           FFFFFF00
Network Bits:       24
Host Bits:          8
Max Addresses:      256
Usable Hosts:       254
```

### Test 2: Subnet Mask to Other Formats

```bash
./subcalc --convert 255.255.255.0
```

**Expected Results:**
* Conversion of subnet mask 255.255.255.0 to:
  * CIDR: /24
  * Wildcard mask: 0.0.0.255
  * Binary representation: 11111111.11111111.11111111.00000000
  * Number of addresses: 256

### Test 3: Wildcard Mask to Other Formats

```bash
./subcalc --convert 0.0.0.255
```

**Expected Results:**
* Conversion of wildcard mask 0.0.0.255 to:
  * CIDR: /24
  * Subnet mask: 255.255.255.0
  * Binary representation: 11111111.11111111.11111111.00000000
  * Number of addresses: 256

### Test 4: Non-Standard Subnet Mask

```bash
./subcalc --convert 255.255.255.192
```

**Expected Results:**
* Conversion of subnet mask 255.255.255.192 to:
  * CIDR: /26
  * Wildcard mask: 0.0.0.63
  * Binary representation: 11111111.11111111.11111111.11000000
  * Number of addresses: 64

### Test 5: Interactive Mode

```bash
./subcalc --convert
```

**Expected Results:**
* Interactive prompt for notation to convert
* Support for CIDR, subnet mask, or wildcard mask input
* Proper conversion based on provided input

## Edge Cases

### Test 6: Class A Subnet

```bash
./subcalc --convert /8
```

**Expected Results:**
* Conversion of CIDR notation /8 to:
  * Subnet mask: 255.0.0.0
  * Wildcard mask: 0.255.255.255
  * Binary representation: 11111111.00000000.00000000.00000000
  * Number of addresses: 16,777,216

### Test 7: Small Subnet

```bash
./subcalc --convert /30
```

**Expected Results:**
* Conversion of CIDR notation /30 to:
  * Subnet mask: 255.255.255.252
  * Wildcard mask: 0.0.0.3
  * Binary representation: 11111111.11111111.11111111.11111100
  * Number of addresses: 4

### Test 8: Non-Octet-Aligned Subnet

```bash
./subcalc --convert /19
```

**Expected Results:**
* Conversion of CIDR notation /19 to:
  * Subnet mask: 255.255.224.0
  * Wildcard mask: 0.0.31.255
  * Binary representation: 11111111.11111111.11100000.00000000
  * Number of addresses: 8,192

### Test 9: Invalid CIDR Notation

```bash
./subcalc --convert /33
```

**Expected Results:**
* Error message indicating that CIDR /33 is invalid
* Explanation that valid CIDR values are between 0 and 32

### Test 10: Invalid Subnet Mask

```bash
./subcalc --convert 255.255.255.1
```

**Expected Results:**
* Error message indicating that 255.255.255.1 is not a valid subnet mask
* Explanation that subnet masks must have contiguous 1s followed by contiguous 0s

## Test Validation Matrix

| Test Case | Input Format    | Input Value      | Expected Output      |
|-----------|----------------|------------------|---------------------|
| Test 1    | CIDR notation  | /24              | Subnet mask, wildcard|
| Test 2    | Subnet mask    | 255.255.255.0    | CIDR, wildcard      |
| Test 3    | Wildcard mask  | 0.0.0.255        | CIDR, subnet mask   |
| Test 4    | Subnet mask    | 255.255.255.192  | CIDR /26, wildcard  |
| Test 5    | Interactive    | (various inputs) | Proper conversions  |
| Test 6    | CIDR notation  | /8               | Class A conversions |
| Test 7    | CIDR notation  | /30              | Small subnet info   |
| Test 8    | CIDR notation  | /19              | Non-octet-aligned   |
| Test 9    | Invalid CIDR   | /33              | Error message       |
| Test 10   | Invalid mask   | 255.255.255.1    | Error message       | 