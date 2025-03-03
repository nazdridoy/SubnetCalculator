import ipaddress

def get_subnet_info(network, num_subnets):
    """
    Calculate subnet information using Fixed Length Subnet Mask.
    All subnets will have the same size, based on the number of subnets required.
    
    Args:
        network: Base network in CIDR notation (e.g., '192.168.0.0/24')
        num_subnets: Number of subnets to create
        
    Returns:
        List of subnet information tuples (subnet, index, total_hosts)
    """
    try:
        network_address = ipaddress.ip_network(network, strict=False)
    except ValueError:
        raise ValueError("Invalid base subnet address. Please provide a valid subnet in CIDR notation.")
    
    # Calculate required bits for the specified number of subnets
    subnet_bits = (num_subnets - 1).bit_length()
    orig_prefix_len = network_address.prefixlen
    new_prefix_len = orig_prefix_len + subnet_bits
    
    if new_prefix_len > 30:  # Allowing /30 as the smallest subnet (2 usable hosts)
        raise ValueError(f"Cannot create {num_subnets} subnets. The resulting prefix length would be /{new_prefix_len}, which is too small.")
    
    # Number of hosts per subnet
    hosts_per_subnet = 2 ** (32 - new_prefix_len) - 2  # subtract 2 for network and broadcast addresses
    
    # Create the subnets
    allocated_subnets = []
    actual_subnets = list(network_address.subnets(new_prefix=new_prefix_len))
    
    # Only return the number of subnets requested
    for i in range(min(num_subnets, len(actual_subnets))):
        subnet = actual_subnets[i]
        allocated_subnets.append((subnet, i+1, hosts_per_subnet))
    
    return allocated_subnets

def display_subnet_info(subnet_info):
    """Format subnet information for display in a table."""
    subnet, index, total_hosts = subnet_info
    return [
        f"Subnet {index}",
        f"{subnet.netmask}",
        f"{subnet.network_address}",
        f"{subnet.broadcast_address}",
        f"{subnet.network_address + 1}",
        f"{subnet.broadcast_address - 1}",
        f"{total_hosts}"
    ]

# We'll use the print_table function from vlsm.py, so no need to reimplement it here 