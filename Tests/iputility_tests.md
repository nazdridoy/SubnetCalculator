# IP Utility Tests

This document outlines test cases for the iputility.py module, which handles IP address validation, classification, and related operations.

## Overview

The IP Utility tool provides functionality to:
- Validate IP addresses and check their properties
- Determine if an IP address is within a specific network
- Analyze IP address ranges
- Classify IP addresses (private, public, special, etc.)

## Test Cases

### Test 1: IP Address Validation

```bash
./subcalc --validate 192.168.1.5
```

**Expected Results:**
* Confirmation that 192.168.1.1 is a valid IPv4 address
* Classification as a private IP address
* Display binary representation and other properties

**Sample Output:**
```
IP Address Analysis Results:

IP Address:        192.168.1.5
Valid IPv4:         True
Address Type:      Private Address
Binary Form:       11000000.10101000.00000001.00000101
Hex Form:          C0A80105
Decimal Form:      3232235781
Octet Values:      192 | 168 | 1 | 5
Address Class:     Class C (192-223)

Network Info:
Address is in the private range 192.168.0.0/16 (RFC1918)
Address is unicast (host to host communication)
```

### Test 2: IP Address in Network Check

```bash
./subcalc --check-ip 192.168.1.5 192.168.1.0/24
```

**Expected Results:**
* Confirmation that 192.168.1.5 is within the 192.168.1.0/24 network
* Display network information for both the IP and network

**Sample Output:**
```
IP Network Membership Check:
IP Address:         192.168.1.5
Network:            192.168.1.0/24
Is IP in Network:   True

Network Details:
Network Address:    192.168.1.0
Broadcast Address:  192.168.1.255
Subnet Mask:        255.255.255.0
Prefix Length:      /24
Total Addresses:    256
Usable Hosts:       254
First Usable Host:  192.168.1.1
Last Usable Host:   192.168.1.254

Host Position Details:
Position in Network: 5 (starting from 0)
Position from End:   250 (to broadcast)
```

### Test 3: IP Range Analysis

```bash
./subcalc --range 192.168.1.10 192.168.1.20
```

**Expected Results:**
* Analysis of the IP range from 192.168.1.10 to 192.168.1.20
* Count of addresses in the range
* Smallest common network containing both IPs

**Sample Output:**
```
IP Range Analysis:
Start IP:           192.168.1.10
End IP:             192.168.1.20
Total Addresses:    11

Optimal CIDR Block Representation:
  Block 1: 192.168.1.10/31 (2 addresses)
  Block 2: 192.168.1.12/30 (4 addresses)
  Block 3: 192.168.1.16/30 (4 addresses)
  Block 4: 192.168.1.20/32 (1 addresses)
```

### Test 4: Special IP Address Analysis

```bash
./subcalc --validate 127.0.0.1
```

**Expected Results:**
* Confirmation that 127.0.0.1 is a valid IPv4 address
* Classification as a loopback address
* Display special properties and information

### Test 5: Interactive Mode

```bash
./subcalc --validate
```

**Expected Results:**
* Interactive prompt for IP address to validate
* Complete analysis based on provided input

## Edge Cases

### Test 6: Invalid IP Address

```bash
./subcalc --validate 300.168.1.1
```

**Expected Results:**
* Error message indicating that 300.168.1.1 is not a valid IPv4 address
* Explanation that octet values must be between 0 and 255

### Test 7: Cross-Subnet IP Range

```bash
./subcalc --range 192.168.1.250 192.168.2.10
```

**Expected Results:**
* Analysis of the IP range spanning multiple subnets
* Count of addresses in the range (17)
* Identification of the smallest common network (/23)

### Test 8: IP Not in Network

```bash
./subcalc --check-ip 192.168.2.1 192.168.1.0/24
```

**Expected Results:**
* Indication that 192.168.2.1 is NOT part of the 192.168.1.0/24 network
* Suggestion of the network that the IP does belong to

### Test 9: Special Purpose IP Addresses

```bash
./subcalc --validate 224.0.0.1
```

**Expected Results:**
* Validation of the multicast address
* Classification as a multicast IP address
* Details about the purpose and scope of this special address

### Test 10: Large IP Range

```bash
./subcalc --range 10.0.0.0 10.0.255.255
```

**Expected Results:**
* Analysis of a large IP range (65,536 addresses)
* Identification of the smallest common network containing the range (/16)
* Efficient handling of the large range without excessive output

## Test Validation Matrix

| Test Case | Description              | Input                          | Expected Result                    |
|-----------|--------------------------|--------------------------------|-----------------------------------|
| Test 1    | Basic IP validation      | 192.168.1.1                    | Valid private IPv4                |
| Test 2    | IP in network            | 192.168.1.5, 192.168.1.0/24    | IP is in network                  |
| Test 3    | IP range analysis        | 192.168.1.10, 192.168.1.20     | 11 IPs, common network /27        |
| Test 4    | Special IP               | 127.0.0.1                      | Valid loopback address            |
| Test 5    | Interactive mode         | (various inputs)               | Proper validation on input        |
| Test 6    | Invalid IP               | 300.168.1.1                    | Error: invalid IP                 |
| Test 7    | Cross-subnet range       | 192.168.1.250, 192.168.2.10    | 17 IPs, common network /23        |
| Test 8    | IP not in network        | 192.168.2.1, 192.168.1.0/24    | IP is NOT in network              |
| Test 9    | Special purpose IP       | 224.0.0.1                      | Multicast address details         |
| Test 10   | Large IP range           | 10.0.0.0, 10.0.255.255         | 65,536 IPs, common network /16    | 