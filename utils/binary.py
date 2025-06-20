"""
Binary representation utilities for IP addresses.
"""
import ipaddress

def get_binary_ip(network):
    """
    Convert network address to binary string representation
    
    Args:
        network: Network in CIDR notation (e.g., '192.168.0.0/24')
        
    Returns:
        32-bit binary string representation or None if invalid
    """
    try:
        net_obj = ipaddress.ip_network(network, strict=False)
        ip_int = int(net_obj.network_address)
        return bin(ip_int)[2:].zfill(32)
    except ValueError:
        return None

def format_binary_ip(binary_str):
    """
    Format a 32-bit binary string with dots for readability
    
    Args:
        binary_str: A 32-bit binary string
        
    Returns:
        Formatted string with dots between octets (e.g., '11000000.10101000.00000001.00000000')
    """
    return '.'.join(binary_str[i:i+8] for i in range(0, 32, 8))

def ip_to_binary_visual(network):
    """
    Create a visual binary representation of a network, showing
    the network bits and host bits
    
    Args:
        network: Network in CIDR notation (e.g., '192.168.0.0/24')
        
    Returns:
        Formatted binary string with visual separation of network and host bits
    """
    try:
        net_obj = ipaddress.ip_network(network, strict=False)
        binary = get_binary_ip(network)
        prefix_len = net_obj.prefixlen
        
        # Format as 8-bit octets
        formatted = []
        for i in range(0, 32, 8):
            octet = binary[i:i+8]
            # Determine which bits are network vs. host bits in this octet
            if prefix_len >= 8:
                # All bits in this octet are network bits
                formatted.append(octet)
                prefix_len -= 8
            elif prefix_len > 0:
                # Some bits in this octet are network bits
                net_part = octet[:prefix_len]
                host_part = octet[prefix_len:]
                formatted.append(f"{net_part}|{host_part}")
                prefix_len = 0
            else:
                # All bits in this octet are host bits
                formatted.append(octet)
        
        return '.'.join(formatted)
    except ValueError:
        return "Invalid network"

def create_prefix_mask(prefix_len, total_len=32):
    """
    Create a visual mask showing network (1) vs host (.) parts
    
    Args:
        prefix_len: Length of the network prefix
        total_len: Total length of the address (default: 32 for IPv4)
        
    Returns:
        Visual representation of network prefix mask (e.g., '11111111.11111111.11111111..........')
    """
    # Create a string of 1s for network bits and dots for host bits
    mask = '1' * prefix_len + '.' * (total_len - prefix_len)
    
    # Insert dots every 8 bits for readability
    return '.'.join(mask[i:i+8] for i in range(0, total_len, 8))

def create_prefix_binary_mask(network_obj):
    """
    Create a visual mask showing network vs host parts with actual binary values
    Network bits are shown as 1s, host bits show the actual binary value
    
    Args:
        network_obj: IPv4Network object
        
    Returns:
        Visual representation of network prefix with actual binary values
    """
    prefix_len = network_obj.prefixlen
    binary = get_binary_ip(str(network_obj))
    
    if not binary:
        return create_prefix_mask(prefix_len)  # Fallback to simple mask
    
    # Format with 1s for network part, actual binary for host part
    formatted = []
    for i in range(0, 32, 8):
        octet = binary[i:i+8]
        # Determine how many bits in this octet are network bits
        if prefix_len >= 8:
            # All bits in this octet are network bits, mark with 1s
            formatted.append('1' * 8)
            prefix_len -= 8
        elif prefix_len > 0:
            # Some bits in this octet are network bits
            net_part = '1' * prefix_len
            # Use actual binary for host part
            host_part = octet[prefix_len:]
            formatted.append(f"{net_part}{host_part}")
            prefix_len = 0
        else:
            # All bits in this octet are host bits, use actual binary
            formatted.append(octet)
    
    return '.'.join(formatted) 