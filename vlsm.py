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

