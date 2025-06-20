# Subnet Calculator (subcalc)

A powerful command-line subnet calculator that supports both Variable Length Subnet Mask (VLSM) and Fixed Length Subnet Mask (FLSM) calculations. Designed for network administrators, students, and anyone working with IP addressing and subnetting.

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
- **Interactive Mode**: User-friendly interactive input with command history and editing
- **Command-line Mode**: Scriptable operation for automation

![2025-03-03_10-53-01](https://github.com/user-attachments/assets/3058ced6-a0dc-45fa-ae99-1912a8890e4c)

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

## Command-line Arguments

```
usage: subcalc [-h] [--network NETWORK] [--vlsm [VLSM ...]] [--flsm [FLSM]] [--convert [CONVERT]] [--validate [VALIDATE]]
               [--check-ip [CHECK_IP ...]] [--range [RANGE ...]]

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
Requested Subnets:    3
Actual Subnets:       3
Unused Subnets:       1

+----------+------------------+-----------------+---------------+---------------+---------------+---------------+-------+
| Subnet   | CIDR Notation    | Subnet Mask     | Network ID    | Broadcast ID  | First Host IP | Last Host IP  | Hosts |
+----------+------------------+-----------------+---------------+---------------+---------------+---------------+-------+
| Subnet 1 | 192.168.0.0/26   | 255.255.255.192 | 192.168.0.0   | 192.168.0.63  | 192.168.0.1   | 192.168.0.62  | 62    |
+----------+------------------+-----------------+---------------+---------------+---------------+---------------+-------+
| Subnet 2 | 192.168.0.64/26  | 255.255.255.192 | 192.168.0.64  | 192.168.0.127 | 192.168.0.65  | 192.168.0.126 | 62    |
+----------+------------------+-----------------+---------------+---------------+---------------+---------------+-------+
| Subnet 3 | 192.168.0.128/26 | 255.255.255.192 | 192.168.0.128 | 192.168.0.191 | 192.168.0.129 | 192.168.0.190 | 62    |
+----------+------------------+-----------------+---------------+---------------+---------------+---------------+-------+

...
```

### VLSM Output
```
+------------------+-----------------+---------------+---------------+---------------+---------------+--------------+-------------+
| Subnet           | Subnet Mask     | Network ID    | Broadcast ID  | First Host IP | Last Host IP  | Needed Hosts | Total Hosts |
+------------------+-----------------+---------------+---------------+---------------+---------------+--------------+-------------+
| 192.168.0.0/26   | 255.255.255.192 | 192.168.0.0   | 192.168.0.63  | 192.168.0.1   | 192.168.0.62  | 40           | 62          |
+------------------+-----------------+---------------+---------------+---------------+---------------+--------------+-------------+
| 192.168.0.64/26  | 255.255.255.192 | 192.168.0.64  | 192.168.0.127 | 192.168.0.65  | 192.168.0.126 | 50           | 62          |
+------------------+-----------------+---------------+---------------+---------------+---------------+--------------+-------------+
| 192.168.0.128/27 | 255.255.255.224 | 192.168.0.128 | 192.168.0.159 | 192.168.0.129 | 192.168.0.158 | 20           | 30          |
+------------------+-----------------+---------------+---------------+---------------+---------------+--------------+-------------+

...
```

### Notation Conversion Output
```
Conversion Results for /24 (CIDR):
CIDR Notation:      /24
Subnet Mask:        255.255.255.0
Wildcard Mask:      0.0.0.255

Conversion Results for 255.255.255.0 (Subnet Mask):
CIDR Notation:      /24
Subnet Mask:        255.255.255.0
Wildcard Mask:      0.0.0.255

Conversion Results for 0.0.0.255 (Wildcard Mask):
CIDR Notation:      /24
Subnet Mask:        255.255.255.0
Wildcard Mask:      0.0.0.255
```

### IP Validation Output
```
IP Validation Results for 192.168.1.1:
Valid IPv4:         True
Binary:             11000000.10101000.00000001.00000001
IP Class:           C
IP Type:            Private
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
  Block 3: 192.168.1.16/29 (8 addresses)
```

## Author

[nazdridoy](https://github.com/nazdridoy)

## Contributing

Contributions, issues, and feature requests are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
