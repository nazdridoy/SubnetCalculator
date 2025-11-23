"""
Network calculation utilities.
"""
import ipaddress
from typing import List, Tuple, Union, Dict, Any, Optional
from constants import POINT_TO_POINT_PREFIX, HOST_PREFIX, NETWORK_AND_BROADCAST_OVERHEAD

def validate_network(network: str) -> ipaddress.IPv4Network:
    """
    Validate if a string is a valid network in CIDR notation.
    
    Args:
        network: Network in CIDR notation (e.g., '192.168.0.0/24')
    
    Returns:
        IPv4Network object if valid
        
    Raises:
        ValueError: If the network is invalid
    """
    try:
        return ipaddress.ip_network(network, strict=False)
    except ValueError:
        raise ValueError("Invalid network address. Please provide a valid network in CIDR notation.")

def calculate_hosts_per_subnet(prefix_length: int) -> int:
    """
    Calculate the number of usable hosts for a given prefix length.
    
    Args:
        prefix_length: CIDR prefix length
        
    Returns:
        Number of usable hosts (excluding network and broadcast addresses)
    """
    if prefix_length >= POINT_TO_POINT_PREFIX:
        # Special case for /31 networks (RFC 3021) and /32 (single host)
        return 2 if prefix_length == POINT_TO_POINT_PREFIX else 1
    return 2 ** (32 - prefix_length) - NETWORK_AND_BROADCAST_OVERHEAD

def calculate_required_prefix_length(hosts_required: int) -> int:
    """
    Calculate the prefix length required to accommodate a given number of hosts.
    
    Args:
        hosts_required: Number of hosts required
        
    Returns:
        Required prefix length
    """
    # Add 2 for network and broadcast addresses
    needed_subnet_size = hosts_required + NETWORK_AND_BROADCAST_OVERHEAD
    
    # Calculate required prefix length
    return 32 - (needed_subnet_size - 1).bit_length()

def display_network_summary(network: str) -> Dict[str, Any]:
    """
    Generate summary information about a network.
    
    Args:
        network: Network in CIDR notation
        
    Returns:
        Dictionary with network summary information
    """
    try:
        network_obj = ipaddress.ip_network(network, strict=False)
        summary = {
            "network": str(network_obj),
            "network_address": str(network_obj.network_address),
            "broadcast_address": str(network_obj.broadcast_address),
            "netmask": str(network_obj.netmask),
            "prefix_length": f"/{network_obj.prefixlen}",
            "num_addresses": network_obj.num_addresses,
            "usable_hosts": network_obj.num_addresses - NETWORK_AND_BROADCAST_OVERHEAD if network_obj.prefixlen < POINT_TO_POINT_PREFIX else network_obj.num_addresses,
            "first_usable": str(network_obj.network_address + 1) if network_obj.prefixlen < POINT_TO_POINT_PREFIX else str(network_obj.network_address),
            "last_usable": str(network_obj.broadcast_address - 1) if network_obj.prefixlen < POINT_TO_POINT_PREFIX else str(network_obj.broadcast_address) if network_obj.prefixlen == POINT_TO_POINT_PREFIX else str(network_obj.network_address)
        }
        return summary
    except ValueError as e:
        return {"error": str(e)}

def check_ip_in_network(ip_address: str, network: str) -> Dict[str, Any]:
    """
    Check if an IP address belongs to a network.
    
    Args:
        ip_address: IP address to check
        network: Network in CIDR notation
        
    Returns:
        Dictionary with result and network details
    """
    result = {"in_network": False, "error": None, "details": None}
    
    try:
        # Create IP and network objects
        ip = ipaddress.IPv4Address(ip_address)
        net = ipaddress.ip_network(network, strict=False)
        
        # Check if IP is in the network
        result["in_network"] = ip in net
        
        # Add details about the network
        result["details"] = display_network_summary(network)
        
        # Add host position details if IP is in network
        if result["in_network"]:
            # Calculate host number (position) in the network
            host_position = int(ip) - int(net.network_address)
            result["details"]["host_position"] = host_position
            result["details"]["host_position_from_end"] = net.num_addresses - host_position - 1
            
    except ValueError as e:
        result["error"] = str(e)
    
    return result

def get_common_prefix(networks: List[str]) -> Tuple[Optional[str], int]:
    """
    Find common prefix among a list of networks.
    
    Args:
        networks: List of networks in CIDR notation
        
    Returns:
        Tuple of (common_network, prefix_length)
    """
    from utils.binary import get_binary_ip
    
    if not networks:
        return None, 0
    
    # Convert all network addresses to binary
    binary_networks = []
    for net in networks:
        try:
            binary = get_binary_ip(net)
            if binary:
                binary_networks.append(binary)
        except (ValueError, TypeError):
            continue
    
    if not binary_networks:
        return None, 0
    
    # Find the common prefix length
    common_prefix = ""
    for i in range(32):
        if i >= len(binary_networks[0]):
            break
            
        bit = binary_networks[0][i]
        if all(net[i] == bit for net in binary_networks):
            common_prefix += bit
        else:
            break
    
    prefix_len = len(common_prefix)
    
    # Create a network address from the common prefix
    if prefix_len > 0:
        # Pad with zeros to get a full 32-bit address
        binary_address = common_prefix + "0" * (32 - prefix_len)
        ip_int = int(binary_address, 2)
        ip_addr = ipaddress.IPv4Address(ip_int)
        return f"{ip_addr}/{prefix_len}", prefix_len
    
    return None, 0

def calculate_subnet_bits(num_subnets: int) -> int:
    """
    Calculate the number of subnet bits required for a given number of subnets.
    
    Args:
        num_subnets: Number of subnets required
        
    Returns:
        Required number of subnet bits
    """
    return (num_subnets - 1).bit_length() 