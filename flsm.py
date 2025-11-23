import ipaddress
from typing import List, NamedTuple
from constants import MAX_USABLE_PREFIX
from utils.network import validate_network, calculate_subnet_bits, calculate_hosts_per_subnet
from utils.format import format_subnet_info


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

def display_subnet_info(subnet_info):
    """Format subnet information for display in a table."""
    return format_subnet_info(subnet_info, is_flsm=True)
