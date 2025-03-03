import ipaddress

def get_subnet_info(network, hosts_required):
    try:
        network_address = ipaddress.ip_network(network, strict=False)
    except ValueError:
        raise ValueError("Invalid base subnet address. Please provide a valid subnet in CIDR notation.")

    # Calculate number of hosts per subnet
    subnets = []
    for hosts in hosts_required:
        # Find the smallest subnet that can accommodate the required hosts
        needed_subnet_size = hosts + 2  # +2 for network and broadcast addresses
        if needed_subnet_size > network_address.num_addresses:
            raise ValueError(f"The HostID is too small for the number of hosts specified ({needed_subnet_size - 2}). Reduce the NetID bits, then retry!")
        
        subnet_prefix = 32 - (needed_subnet_size - 1).bit_length()
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
    subnet, needed_hosts, total_hosts = subnet_info
    return [
        f"{subnet}",
        f"{subnet.netmask}",
        f"{subnet.network_address}",
        f"{subnet.broadcast_address}",
        f"{subnet.network_address + 1}",
        f"{subnet.broadcast_address - 1}",
        f"{needed_hosts}",
        f"{total_hosts}"
    ]

def print_table(data):
    # Calculate the width of each column
    col_widths = [max(len(str(item)) for item in col) for col in zip(*data)]
    
    # Create a horizontal line
    def print_horizontal_line():
        line = "+"
        for width in col_widths:
            line += "-" * (width + 2) + "+"
        print(line)
    
    # Print the table
    def print_row(row):
        line = "|"
        for i, item in enumerate(row):
            line += " " + str(item).ljust(col_widths[i]) + " |"
        print(line)

    print_horizontal_line()
    for row in data:
        print_row(row)
        print_horizontal_line()

