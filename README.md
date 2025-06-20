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

## Command-line Arguments

```
usage: subcalc [-h] [--network NETWORK] [--vlsm [VLSM ...]] [--flsm [FLSM]] [--convert [CONVERT]]

Subnet Calculator Tool - Calculate and display subnet information

options:
  -h, --help           show this help message and exit
  --network NETWORK    Base network address in CIDR notation (e.g., 192.168.0.0/24)
  --vlsm [VLSM ...]    Run Variable Length Subnet Mask calculator with specified host 
                       requirements (e.g., --vlsm 20 40 80)
  --flsm [FLSM]        Run Fixed Length Subnet Mask calculator with either number of 
                       subnets (e.g., --flsm 4) or target prefix length (e.g., --flsm /28)
  --convert [CONVERT]  Convert between CIDR notation, subnet masks, and wildcard masks (e.g., --convert
                       /24 or --convert 255.255.255.0)

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

## Author

[nazdridoy](https://github.com/nazdridoy)

## Contributing

Contributions, issues, and feature requests are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
