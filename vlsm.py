import ipaddress
from utils.network import validate_network, calculate_required_prefix_length
from utils.format import format_subnet_info, print_table

def get_subnet_info(network, hosts_required):
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
        allocated_subnets.append((subnet, hosts, total_hosts - 2))  # subtracting 2 to show the usable hosts
        current_base = subnet.network_address + subnet.num_addresses
    
    return allocated_subnets

def display_subnet_info(subnet_info):
    return format_subnet_info(subnet_info, is_flsm=False)

