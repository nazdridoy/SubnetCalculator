# SubnetCalculator - Advanced IP Networking Toolkit

![SubnetCalculator](https://img.shields.io/badge/Networking%20Tool-IPv4%20Subnetting-brightgreen)

## Introduction

SubnetCalculator (`subcalc`) is a comprehensive command-line toolkit for IP network management, subnet planning, and addressing tasks. Designed for network engineers, administrators, cybersecurity professionals, cloud architects, and IT students, this powerful utility simplifies complex IPv4 addressing calculations through an intuitive interface with zero external dependencies.

> "Master the art of IP subnet planning, CIDR aggregation, and network architecture with precision and ease"

## Key Capabilities

### Subnet Planning and Design

- **Variable Length Subnet Mask (VLSM)**: Efficiently allocate network space by creating optimally-sized subnets based on specific host requirements
- **Fixed Length Subnet Mask (FLSM)**: Create equal-sized subnets by either specifying the number of required subnets or a target prefix length
- **Visual Subnet Tables**: View comprehensive tables showing all relevant subnet information including network ID, broadcast address, usable ranges, and host capacities

### Network Information Analysis

- **Detailed Network Summaries**: Quick analysis of IP network properties including network address, broadcast address, usable host range, and address count
- **IP Validation and Classification**: Identify IP address types (private, public, loopback, multicast), validate format, and view binary/hex representations
- **Address Space Utilization**: Calculate exact address space usage and identify available address ranges
- **RFC 1918 Private Network Support**: Full support for private addressing standards

### Network Format Conversion

- **Multi-format Notation Support**: Seamlessly convert between different IP notation formats:
  - CIDR notation (e.g., /24)
  - Subnet masks (e.g., 255.255.255.0)
  - Wildcard masks (e.g., 0.0.0.255)
- **Visualization in Binary and Hexadecimal**: View network addresses in multiple formats for deeper understanding
- **Classful to Classless Conversion**: Convert between traditional class-based and modern prefix-length notations

### Advanced IP Utilities

- **Network Membership Testing**: Check if specific IP addresses belong to a given subnet with detailed position information
- **Range Analysis**: Analyze IP address ranges and calculate optimal CIDR block representations
- **Host Position Calculation**: Determine exact position of hosts within networks for address planning

### Route Summarization and Supernetting

- **CIDR Aggregation**: Combine multiple subnets into efficient summary routes to minimize routing table entries
- **Optimal Block Detection**: Automatically find the smallest common supernet that covers multiple networks
- **Common Prefix Analysis**: Identify shared network prefixes and calculate address space efficiency
- **Route Table Optimization**: Calculate the minimum set of prefixes for route advertisement

### Flexible Usage Options

- **Interactive Mode**: User-friendly command prompts with input validation for exploratory work
- **Command-line Mode**: Full scriptability for automation and integration with other tools
- **Command History and Editing**: Enhanced interactive experience with history recall and line editing

## Technical Specifications

- **Platforms**: Cross-platform compatibility (runs anywhere Python is installed)
- **Dependencies**: Zero external dependencies - just pure Python 3.6+
- **Installation**: Simple git clone with no compilation required
- **License**: MIT License - Free to use, modify, and distribute

## Use Cases

### Network Design and Implementation

- Plan efficient IP address allocation for new networks
- Subdivide existing networks to accommodate growth
- Create hierarchical addressing schemes for enterprise networks
- Design campus networks with optimal addressing hierarchy

### Network Troubleshooting

- Quickly validate if IP addresses belong to expected subnets
- Analyze address ranges to identify configuration issues
- Convert between notation formats for cross-platform compatibility
- Debug IP addressing conflicts in seconds

### Education and Training

- Learn subnet calculation concepts through interactive examples
- Visualize subnet divisions and addressing patterns
- Practice network planning exercises with immediate feedback
- Master CCNA/CCNP IP addressing concepts

### Network Security

- Analyze network boundaries for security zone planning
- Verify network segmentation for access control implementation
- Map IP ranges for firewall rule development
- Plan DMZ and perimeter network addressing

### Routing Optimization

- Aggregate routes to improve routing table efficiency
- Identify summary routes for border gateway configurations
- Analyze route overlaps and optimize path advertisements
- Minimize route advertisements in OSPF/BGP deployments

## Related Concepts

The SubnetCalculator tool aligns with the following networking concepts and protocols:

- IPv4 Addressing and Subnetting
- Subnet Masking and Wildcard Masks
- CIDR (Classless Inter-Domain Routing) Notation
- Network Segmentation and VLANs
- IP Route Summarization
- Hierarchical Network Design (Core/Distribution/Access)
- Address Space Management (IPAM)
- BGP Route Aggregation
- Network Address Translation (NAT)
- Data Center IP Address Planning

---

*Keywords: subnet calculator, IP addressing, VLSM, FLSM, CIDR, network planning, route aggregation, network utility, IPv4 subnetting, network engineering, networking tool* 