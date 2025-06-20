# Subnet Calculator (subcalc)

Powerful CLI toolkit for IP networking calculations, subnet/supernet planning, and CIDR address management. Master IPv4 subnetting, VLSM/FLSM calculations, and route aggregation with ease. Simplifying complex network tasks for engineers, administrators, and students.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-any-green.svg)](https://github.com/nazdridoy/SubnetCalculator)

## Features

- **Network Information**: Display detailed information about any IP network
- **VLSM Calculation**: Create optimally-sized subnets based on specific host requirements
- **FLSM Calculation**: Create equal-sized subnets based on either:
  - Number of required subnets
  - Specific prefix length
- **Notation Conversion**: Easily convert between:
  - CIDR notation (e.g., /24)
  - Subnet masks (e.g., 255.255.255.0)
  - Wildcard masks (e.g., 0.0.0.255)
- **IP Address Utilities**: Tools for IP address analysis:
  - IP validation and classification
  - Check if an IP is within a subnet
  - Analyze IP address ranges
- **Supernetting/CIDR Aggregation**: Efficient route summarization:
  - Aggregate multiple networks into optimal CIDR blocks
  - Find the smallest common supernet
  - Analyze common network prefixes
- **Interactive Mode**: User-friendly interactive input with command history and editing
- **Command-line Mode**: Scriptable operation for automation

![SubnetCalculator screenshot showing example output of subnet calculation results](https://github.com/user-attachments/assets/3058ced6-a0dc-45fa-ae99-1912a8890e4c)

## Installation

### Clone the repository
```bash
git clone https://github.com/nazdridoy/SubnetCalculator.git
cd SubnetCalculator
```

### Make the script executable
```bash
chmod +x subcalc
```

## Usage

### Network Summary
Display detailed information about a network:
```bash
./subcalc --network 192.168.0.0/24
```

### FLSM Subnet Calculation
Create equal-sized subnets in two ways:

1. By number of subnets:
```bash
./subcalc --network 192.168.0.0/24 --flsm 8
```

2. By specific prefix length:
```bash
./subcalc --network 192.168.0.0/24 --flsm /28
```

### VLSM Subnet Calculation
Create optimally-sized subnets based on host requirements:
```bash
./subcalc --network 192.168.0.0/24 --vlsm 50 30 10 5
```

### Interactive Mode
Run the tool interactively:
```bash
./subcalc --flsm     # For FLSM calculation
./subcalc --vlsm     # For VLSM calculation
```

### Notation Conversion
Convert between CIDR, subnet mask, and wildcard mask notations:

```bash
./subcalc --convert /24               # Convert from CIDR notation
./subcalc --convert 255.255.255.0     # Convert from subnet mask notation
./subcalc --convert 0.0.0.255         # Convert from wildcard mask notation
./subcalc --convert                   # Run in interactive mode
```

### IP Address Utilities

#### Validate an IP Address
Validate an IP address and display information about it:

```bash
./subcalc --validate 192.168.1.1      # Validate a specific IP
./subcalc --validate                  # Run in interactive mode
```

#### Check if an IP is within a Network
Check if an IP address belongs to a specified network:

```bash
./subcalc --check-ip 192.168.1.5 192.168.1.0/24  # Check IP in network
./subcalc --check-ip 10.0.0.1                    # Prompt for network
./subcalc --check-ip                             # Fully interactive mode
```

#### Analyze IP Address Range
Calculate information about an IP address range:

```bash
./subcalc --range 192.168.1.10 192.168.1.20  # Analyze specific range
./subcalc --range 10.0.0.1                   # Prompt for end IP
./subcalc --range                            # Fully interactive mode
```

### Supernetting/CIDR Aggregation
Aggregate multiple subnets into optimal summary routes:

```bash
# Find efficient summary routes for multiple networks
./subcalc --supernet 192.168.1.0/24 192.168.2.0/24 192.168.3.0/24

# Run in interactive mode
./subcalc --supernet
```

## Command-line Arguments

```
usage: subcalc [-h] [--network NETWORK] [--vlsm [VLSM ...]] [--flsm [FLSM]] [--convert [CONVERT]]
               [--validate [VALIDATE]] [--check-ip [CHECK_IP ...]] [--range [RANGE ...]]
               [--supernet [SUPERNET ...]]

Subnet Calculator Tool - Calculate and display subnet information

options:
  -h, --help            show this help message and exit
  --network NETWORK     Base network address in CIDR notation (e.g., 192.168.0.0/24)
  --vlsm [VLSM ...]     Run Variable Length Subnet Mask calculator with specified host requirements (e.g., --vlsm 20 40 80)
  --flsm [FLSM]         Run Fixed Length Subnet Mask calculator with either number of subnets (e.g., --flsm 4) or target prefix length
                        (e.g., --flsm /28)
  --convert [CONVERT]   Convert between CIDR notation, subnet masks, and wildcard masks (e.g., --convert /24 or --convert
                        255.255.255.0)
  --validate [VALIDATE]
                        Validate an IP address and show its properties (e.g., --validate 192.168.1.1)
  --check-ip [CHECK_IP ...]
                        Check if an IP address is in a network (e.g., --check-ip 192.168.1.5 192.168.1.0/24)
  --range [RANGE ...]   Analyze an IP address range (e.g., --range 192.168.1.10 192.168.1.20)
  --supernet [SUPERNET ...]
                        Find optimal summary routes for multiple subnets (e.g., --supernet 192.168.1.0/24 192.168.2.0/24)

Examples:
  ./subcalc --network 192.168.0.0/24                    # Display network summary
  ./subcalc --network 192.168.0.0/24 --flsm 16          # Create 16 equal-sized subnets
  ./subcalc --network 192.168.0.0/24 --flsm /28         # Create subnets with prefix /28
  ./subcalc --network 192.168.0.0/24 --vlsm 20 40 50    # Create subnets with specified host capacities
  ./subcalc --flsm                                      # Run FLSM in interactive mode
  ./subcalc --vlsm                                      # Run VLSM in interactive mode
  ./subcalc --convert /24                               # Convert between CIDR, subnet mask, and wildcard mask
  ./subcalc --convert 255.255.255.0                     # Convert between notations using subnet mask
  ./subcalc --convert                                   # Run conversion tool in interactive mode
  ./subcalc --validate 192.168.1.5                      # Validate an IP address and display information
  ./subcalc --check-ip 192.168.1.5 192.168.1.0/24       # Check if an IP address is in a network
  ./subcalc --range 192.168.1.10 192.168.1.20           # Analyze an IP address range
  ./subcalc --supernet 192.168.1.0/24 192.168.2.0/24    # Find optimal summary routes for multiple subnets
  ./subcalc --supernet                                  # Run supernetting tool in interactive mode
```

## Example Outputs

### Network Summary
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

### FLSM Output
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

...
```

### VLSM Output
```
+------------------+-----------------+---------------+---------------+---------------+---------------+--------------+-------------+
| Subnet           | Subnet Mask     | Network ID    | Broadcast ID  | First Host IP | Last Host IP  | Needed Hosts | Total Hosts |
+------------------+-----------------+---------------+---------------+---------------+---------------+--------------+-------------+
| 192.168.0.0/25   | 255.255.255.128 | 192.168.0.0   | 192.168.0.127 | 192.168.0.1   | 192.168.0.126 | 100          | 126         |
+------------------+-----------------+---------------+---------------+---------------+---------------+--------------+-------------+
| 192.168.0.128/26 | 255.255.255.192 | 192.168.0.128 | 192.168.0.191 | 192.168.0.129 | 192.168.0.190 | 50           | 62          |
+------------------+-----------------+---------------+---------------+---------------+---------------+--------------+-------------+
| 192.168.0.192/27 | 255.255.255.224 | 192.168.0.192 | 192.168.0.223 | 192.168.0.193 | 192.168.0.222 | 25           | 30          |
+------------------+-----------------+---------------+---------------+---------------+---------------+--------------+-------------+
| 192.168.0.224/28 | 255.255.255.240 | 192.168.0.224 | 192.168.0.239 | 192.168.0.225 | 192.168.0.238 | 10           | 14          |
+------------------+-----------------+---------------+---------------+---------------+---------------+--------------+-------------+

...
```

### Notation Conversion Output
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

### IP Validation Output
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

### IP Network Membership Check Output
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

### IP Range Analysis Output
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

### Supernetting Output
```

Supernetting Results:
Input Networks (3):
  1. 192.168.1.0/24 (256 addresses)
     Binary: 11000000.10101000.00000001.00000000
     Prefix: 11111111.11111111.11111111.00000000
  2. 192.168.2.0/24 (256 addresses)
     Binary: 11000000.10101000.00000010.00000000
     Prefix: 11111111.11111111.11111111.00000000
  3. 192.168.3.0/24 (256 addresses)
     Binary: 11000000.10101000.00000011.00000000
     Prefix: 11111111.11111111.11111111.00000000

1. Efficient Aggregation (Multiple Blocks)
   Result: 2 CIDR block(s)
     Block 1: 192.168.1.0/24 (256 addresses)
            Binary: 11000000.10101000.00000001.00000000
            Prefix: 11111111.11111111.11111111.00000000
     Block 2: 192.168.2.0/23 (512 addresses)
            Binary: 11000000.10101000.0000001|0.00000000
            Prefix: 11111111.11111111.11111110.00000000
   Total Addresses: 768

2. Single Supernet (Summary Route)
   Result: 192.168.0.0/22 (1024 addresses)
          Binary: 11000000.10101000.000000|00.00000000
          Prefix: 11111111.11111111.11111100.00000000
   Address Waste: 256 addresses (25.0%)

3. Common Prefix Analysis
   Common Prefix: 22 bits
   Common Network: 192.168.0.0/22
   Prefix Mask:  NNNNNNNN.NNNNNNNN.NNNNNNHH.HHHHHHHH
                 N = Network bits (match), H = Host bits (vary)
   Binary Form:  11000000.10101000.00000000.00000000
   Address Range: 192.168.0.0 - 192.168.3.255
   Total Range:   1024 addresses

```

## Author

[nazdridoy](https://github.com/nazdridoy)

## Contributing

Contributions, issues, and feature requests are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
