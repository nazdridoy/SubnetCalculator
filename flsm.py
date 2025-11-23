# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 2025 nazDridoy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""Fixed Length Subnet Mask (FLSM) calculator module.

This module provides functionality for calculating equal-sized subnets from a base network.
Supports calculation by number of subnets or by target prefix length.

Classes:
    SubnetInfo: NamedTuple containing subnet details (subnet, index, total_hosts).

Functions:
    get_subnet_info: Calculate subnets by number of subnets required.
    get_subnet_info_by_prefix: Calculate subnets by target prefix length.
    parse_subnet_input: Parse user input for subnet/prefix specification.
    display_summary: Display FLSM calculation summary.
    display_subnet_info: Format subnet information for table display.
    run_flsm_tool: Interactive CLI tool for FLSM subnet calculation.
"""
import ipaddress
from typing import List, NamedTuple
from constants import MAX_USABLE_PREFIX
from utils.network import validate_network, calculate_subnet_bits, calculate_hosts_per_subnet
from utils.format import format_subnet_info, print_table


class SubnetInfo(NamedTuple):
    """Information about a fixed-length subnet.
    
    Attributes:
        subnet: The IPv4 network object
        index: Subnet number (1-indexed)
        total_hosts: Total number of usable host addresses
    """
    subnet: ipaddress.IPv4Network
    index: int
    total_hosts: int

def get_subnet_info(network: str, num_subnets: int) -> List[SubnetInfo]:
    """
    Calculate subnet information using Fixed Length Subnet Mask.
    All subnets will have the same size, based on the number of subnets required.
    
    Args:
        network: Base network in CIDR notation (e.g., '192.168.0.0/24')
        num_subnets: Number of subnets to create
        
    Returns:
        List of SubnetInfo named tuples containing subnet details
        
    Raises:
        ValueError: If network is invalid or resulting subnets would be too small
    """
    try:
        network_address = validate_network(network)
    except ValueError as e:
        raise ValueError(str(e))
    
    # Calculate required bits for the specified number of subnets
    subnet_bits = calculate_subnet_bits(num_subnets)
    orig_prefix_len = network_address.prefixlen
    new_prefix_len = orig_prefix_len + subnet_bits
    
    if new_prefix_len > MAX_USABLE_PREFIX:
        raise ValueError(
            f"Cannot create {num_subnets} subnets. The resulting prefix length "
            f"would be /{new_prefix_len}, which exceeds the maximum usable prefix /{MAX_USABLE_PREFIX}."
        )
    
    # Number of hosts per subnet
    hosts_per_subnet = calculate_hosts_per_subnet(new_prefix_len)
    
    # Create the subnets
    allocated_subnets = []
    actual_subnets = list(network_address.subnets(new_prefix=new_prefix_len))
    
    # Only return the number of subnets requested
    for i in range(min(num_subnets, len(actual_subnets))):
        subnet = actual_subnets[i]
        allocated_subnets.append(SubnetInfo(subnet=subnet, index=i+1, total_hosts=hosts_per_subnet))
    
    return allocated_subnets

def get_subnet_info_by_prefix(network: str, new_prefix: int) -> List[SubnetInfo]:
    """
    Calculate subnet information using Fixed Length Subnet Mask with a specified prefix length.
    
    Args:
        network: Base network in CIDR notation (e.g., '192.168.0.0/24')
        new_prefix: The new prefix length to use for subnets (e.g., 28)
        
    Returns:
        List of SubnetInfo named tuples containing subnet details
        
    Raises:
        ValueError: If network is invalid, new prefix is invalid, or prefix is too small
    """
    try:
        network_address = validate_network(network)
    except ValueError as e:
        raise ValueError(str(e))
    
    # Validate the new prefix
    orig_prefix_len = network_address.prefixlen
    if new_prefix <= orig_prefix_len:
        raise ValueError(
            f"New prefix /{new_prefix} must be larger than the original prefix /{orig_prefix_len}"
        )
    
    if new_prefix > MAX_USABLE_PREFIX:
        raise ValueError(
            f"Prefix /{new_prefix} is too small. The smallest supported prefix is /{MAX_USABLE_PREFIX}."
        )
    
    # Number of hosts per subnet
    hosts_per_subnet = calculate_hosts_per_subnet(new_prefix)
    
    # Create the subnets
    allocated_subnets = []
    actual_subnets = list(network_address.subnets(new_prefix=new_prefix))
    
    # Calculate total possible subnets with this prefix
    subnet_bits = new_prefix - orig_prefix_len
    max_possible_subnets = 2 ** subnet_bits
    
    # Return all possible subnets
    for i, subnet in enumerate(actual_subnets):
        allocated_subnets.append(SubnetInfo(subnet=subnet, index=i+1, total_hosts=hosts_per_subnet))
    
    return allocated_subnets

def parse_subnet_input(subnet_input):
    """Parse subnet input to determine if it's a number of subnets or prefix length.
    
    Args:
        subnet_input: String or int representing either number of subnets or prefix length.
        
    Returns:
        Tuple of (by_prefix: bool, value: int) or (None, None) if invalid.
    """
    if isinstance(subnet_input, str) and subnet_input.startswith('/'):
        try:
            prefix_length = int(subnet_input[1:])
            return True, prefix_length
        except (ValueError, IndexError):
            print("Invalid prefix length. Please provide a number after the '/' prefix.")
            return None, None
    else:
        try:
            num_subnets = int(subnet_input)
            if num_subnets <= 0:
                print("Number of subnets must be greater than 0.")
                return None, None
            return False, num_subnets
        except ValueError:
            print("Invalid input. Please provide either a number of subnets or a prefix length (e.g., 16 or /28).")
            return None, None


def display_summary(network_obj, subnet_obj, subnets, by_prefix, value):
    """Display FLSM calculation summary.
    
    Args:
        network_obj: Base network object.
        subnet_obj: First subnet object.
        subnets: List of all SubnetInfo tuples.
        by_prefix: Whether calculation was by prefix or by number.
        value: Either prefix_length or num_subnets.
    """
    subnet_bits = subnet_obj.prefixlen - network_obj.prefixlen
    actual_subnets = len(subnets)
    hosts_per_subnet = subnets[0].total_hosts
    max_subnets = 2 ** subnet_bits
    
    print("\nFLSM Summary:")
    print(f"Base Network:         {network_obj}")
    print(f"Subnet Bits:          {subnet_bits}")
    print(f"New Prefix Length:    /{subnet_obj.prefixlen}")
    print(f"Subnet Mask:          {subnet_obj.netmask}")
    print(f"Hosts per Subnet:     {hosts_per_subnet}")
    
    if by_prefix:
        print(f"Specified Prefix:     /{value}")
        print(f"Maximum Subnets:      {max_subnets}")
        print(f"Created Subnets:      {actual_subnets}")
    else:
        unused_subnets = max_subnets - value
        print(f"Requested Subnets:    {value}")
        print(f"Actual Subnets:       {actual_subnets}")
        print(f"Unused Subnets:       {unused_subnets}")
    print()


def display_subnet_info(subnet_info):
    """Format subnet information for display in a table.
    
    Args:
        subnet_info: SubnetInfo NamedTuple containing subnet details.
        
    Returns:
        List of formatted strings for table display.
    """
    return format_subnet_info(subnet_info, is_flsm=True)


def run_flsm_tool(network=None, subnet_input=None):
    """Run the Fixed Length Subnet Mask calculator tool.
    
    Interactive CLI tool for FLSM subnet calculation. Can be called
    programmatically with parameters or run interactively.
    
    Args:
        network: Optional base network in CIDR notation.
        subnet_input: Optional number of subnets or prefix length (e.g., 4 or '/26').
    """
    try:
        if network is None:
            network = input("Enter the base subnet address (e.g., 192.168.0.0/24): ")
        
        if subnet_input is None:
            subnet_input = input("Enter the number of subnets to create OR prefix length (e.g., 16 or /28): ")
        
        # Parse input
        by_prefix, value = parse_subnet_input(subnet_input)
        if value is None:
            return
        
        try:
            # Get subnets based on either number of subnets or prefix length
            if by_prefix:
                subnets = get_subnet_info_by_prefix(network, value)
            else:
                subnets = get_subnet_info(network, value)
            
            if not subnets:
                print("No subnets created.")
                return
            
            # Display summary
            network_obj = ipaddress.ip_network(network, strict=False)
            subnet_obj = subnets[0].subnet
            display_summary(network_obj, subnet_obj, subnets, by_prefix, value)
            
        except ValueError as e:
            print(e)
            return
        
        # Generate the table data
        table_data = [
            ["Subnet", "CIDR Notation", "Subnet Mask", "Network ID", "Broadcast ID", "First Host IP", "Last Host IP", "Hosts"]
        ]
        
        for subnet_info in subnets:
            table_data.append(display_subnet_info(subnet_info))
        
        print_table(table_data)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return
