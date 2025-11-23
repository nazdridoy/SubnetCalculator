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

"""Variable Length Subnet Mask (VLSM) calculator module.

This module provides functionality for creating optimally-sized subnets based on
specific host requirements. Subnets are allocated in descending order of size.

Classes:
    VLSMSubnetInfo: NamedTuple containing subnet details (subnet, needed_hosts, total_hosts).

Functions:
    get_subnet_info: Calculate VLSM subnets based on host requirements.
    display_subnet_info: Format subnet information for table display.
    run_vlsm_tool: Interactive CLI tool for VLSM subnet calculation.
"""
import ipaddress
from typing import List, NamedTuple
from utils.network import validate_network, calculate_required_prefix_length
from utils.format import format_subnet_info, print_table


class VLSMSubnetInfo(NamedTuple):
    """Information about a variable-length subnet.
    
    Attributes:
        subnet: The IPv4 network object
        needed_hosts: Number of hosts originally requested
        total_hosts: Total number of usable host addresses in the subnet
    """
    subnet: ipaddress.IPv4Network
    needed_hosts: int
    total_hosts: int


def get_subnet_info(network: str, hosts_required: List[int]) -> List[VLSMSubnetInfo]:
    """Calculate VLSM subnet information based on host requirements.
    
    Args:
        network: Base network in CIDR notation (e.g., '192.168.0.0/24')
        hosts_required: List of host counts needed for each subnet
        
    Returns:
        List of VLSMSubnetInfo named tuples with subnet details
        
    Raises:
        ValueError: If network is invalid or requested hosts exceed available space
    """
    if not hosts_required:
        raise ValueError("At least one host requirement must be specified")
    
    try:
        network_address = validate_network(network)
    except ValueError as e:
        raise ValueError(str(e))

    # Calculate number of hosts per subnet
    subnets = []
    for hosts in hosts_required:
        # Find the smallest subnet that can accommodate the required hosts
        needed_subnet_size = hosts + 2  # +2 for network and broadcast addresses
        if needed_subnet_size > network_address.num_addresses:
            raise ValueError(f"The HostID is too small for the number of hosts specified ({needed_subnet_size - 2}). Reduce the NetID bits, then retry!")
        
        subnet_prefix = calculate_required_prefix_length(hosts)
        total_hosts = 2 ** (32 - subnet_prefix) - 2  # subtract 2 for network and broadcast addresses
        
        # Additional check for minimum subnet prefix to handle oversized requests
        if total_hosts < hosts:
            raise ValueError(f"The HostID is too small for the number of hosts specified ({hosts}). Reduce the NetID bits, then retry!")
        
        subnets.append((hosts, subnet_prefix, total_hosts + 2))  # adding 2 back to match the original total hosts
    
    # Sort subnets by size in descending order
    subnets.sort(key=lambda x: x[1])

    # Check if all required subnets fit within the base subnet
    total_needed_addresses = sum(2 ** (32 - prefix) for _, prefix, _ in subnets)
    if total_needed_addresses > network_address.num_addresses:
        raise ValueError("The total number of required hosts exceeds the capacity of the base subnet. Reduce the number of hosts or use a larger base subnet.")
    
    # Allocate subnets
    allocated_subnets = []
    current_base = network_address.network_address
    for hosts, prefix, total_hosts in subnets:
        subnet = ipaddress.ip_network(f"{current_base}/{prefix}", strict=False)
        allocated_subnets.append(VLSMSubnetInfo(subnet=subnet, needed_hosts=hosts, total_hosts=total_hosts - 2))
        current_base = subnet.network_address + subnet.num_addresses
    
    return allocated_subnets

def display_subnet_info(subnet_info):
    return format_subnet_info(subnet_info, is_flsm=False)


def run_vlsm_tool(network=None, hosts_input=None):
    """Run the Variable Length Subnet Mask calculator tool.
    
    Interactive CLI tool for VLSM subnet calculation. Can be called
    programmatically with parameters or run interactively.
    
    Args:
        network: Optional base network in CIDR notation.
        hosts_input: Optional host requirements as string, list, or None for interactive.
    """
    try:
        if network is None:
            network = input("Enter the base subnet address (e.g., 192.168.0.0/24): ")
        
        # Handle different input types for hosts_input
        if hosts_input is None:
            # Interactive mode
            hosts_input = input("Enter the number of hosts required for each subnet (comma or space separated, e.g., 50 25 10): ")
            hosts_required = [int(h.strip()) for h in hosts_input.replace(',', ' ').split() if h.strip()]
        elif isinstance(hosts_input, list):
            # Already parsed by argparse
            hosts_required = [int(h) for h in hosts_input]
        elif isinstance(hosts_input, str):
            # String input - parse it
            hosts_required = [int(h.strip()) for h in hosts_input.replace(',', ' ').split() if h.strip()]
        else:
            print(f"Error: Invalid hosts_input type: {type(hosts_input)}")
            return
        
        # Validate hosts
        if not hosts_required:
            print("Error: No valid host requirements provided.")
            return
        if any(h <= 0 for h in hosts_required):
            print("Error: All host requirements must be greater than 0.")
            return
        
        try:
            subnets = get_subnet_info(network, hosts_required)
            
            if not subnets:
                print("No subnets created.")
                return
            
            # Display summary
            network_obj = ipaddress.ip_network(network, strict=False)
            print(f"\nVLSM Summary:")
            print(f"Base Network:         {network_obj}")
            print(f"Number of Subnets:    {len(subnets)}")
            print(f"Total Hosts Needed:   {sum(hosts_required)}")
            print(f"Total Hosts Allocated: {sum(s.total_hosts for s in subnets)}")
            print()
            
        except ValueError as e:
            print(e)
            return
        
        # Generate the table data
        table_data = [
            ["Subnet", "Subnet Mask", "Network ID", "Broadcast ID", "First Host IP", "Last Host IP", "Needed Hosts", "Total Hosts"]
        ]
        
        for subnet_info in subnets:
            table_data.append(display_subnet_info(subnet_info))
        
        print_table(table_data)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return

