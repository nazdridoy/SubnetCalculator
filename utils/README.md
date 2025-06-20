# Subnet Calculator Utilities

This directory contains utility modules that provide common functionality used throughout the Subnet Calculator tool.

## Module Structure

- `__init__.py`: Package initialization file
- `binary.py`: Functions for binary representation and manipulation of IP addresses
- `conversion.py`: IP notation conversion utilities (CIDR, subnet mask, wildcard mask)
- `format.py`: Formatting utilities for console output and data display
- `network.py`: Network calculation utilities
- `validation.py`: IP address validation utilities

## Module Details

### binary.py

Functions for working with binary representations of IP addresses.

- `get_binary_ip(network)`: Convert network address to binary string representation
- `format_binary_ip(binary_str)`: Format a 32-bit binary string with dots for readability
- `ip_to_binary_visual(network)`: Create a visual binary representation of a network with network/host bit separation
- `create_prefix_mask(prefix_len, total_len=32)`: Create a visual mask showing network vs host parts
- `create_prefix_binary_mask(network_obj)`: Create a visual mask showing network vs host parts with actual binary values

### conversion.py

Utilities for converting between different IP notation formats.

- `cidr_to_subnet_mask(prefix_length)`: Convert CIDR prefix length to subnet mask
- `subnet_mask_to_cidr(subnet_mask)`: Convert subnet mask to CIDR prefix length
- `subnet_mask_to_wildcard(subnet_mask)`: Convert subnet mask to wildcard mask
- `wildcard_to_subnet_mask(wildcard_mask)`: Convert wildcard mask to subnet mask
- `cidr_to_wildcard(prefix_length)`: Convert CIDR prefix length to wildcard mask
- `wildcard_to_cidr(wildcard_mask)`: Convert wildcard mask to CIDR prefix length
- `detect_notation_type(input_str)`: Detect if input is CIDR, subnet mask, or wildcard mask
- `convert_notation(input_str)`: Convert between CIDR, subnet mask, and wildcard mask notations

### format.py

Utilities for console output formatting.

- `print_table(data)`: Print a nicely formatted table from a list of lists
- `format_subnet_info(subnet_info, is_flsm=True)`: Format subnet information for display

### network.py

Core network calculation utilities.

- `validate_network(network)`: Validate if a string is a valid network in CIDR notation
- `calculate_hosts_per_subnet(prefix_length)`: Calculate the number of usable hosts for a given prefix length
- `calculate_required_prefix_length(hosts_required)`: Calculate the prefix length required to accommodate a number of hosts
- `display_network_summary(network)`: Generate summary information about a network
- `check_ip_in_network(ip_address, network)`: Check if an IP address belongs to a network
- `get_common_prefix(networks)`: Find common prefix among a list of networks
- `calculate_subnet_bits(num_subnets)`: Calculate the number of subnet bits required for a given number of subnets

### validation.py

IP address validation utilities.

- `validate_ip(ip_address)`: Validate if a string is a valid IPv4 address and provide detailed information 