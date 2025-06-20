#!/usr/bin/env python3
import ipaddress

def validate_ip(ip_address):
    """
    Validate if a string is a valid IPv4 address
    Returns a dictionary with validation status and details
    """
    result = {"valid": False, "error": None, "binary": None, "class": None, "type": None}
    
    try:
        # Try to create an IPv4Address object
        ip = ipaddress.IPv4Address(ip_address)
        result["valid"] = True
        
        # Get binary representation
        binary = bin(int(ip))[2:].zfill(32)
        result["binary"] = ".".join(binary[i:i+8] for i in range(0, 32, 8))
        
        # Determine IP class
        first_octet = int(ip_address.split('.')[0])
        if 1 <= first_octet <= 126:
            result["class"] = "A"
        elif 128 <= first_octet <= 191:
            result["class"] = "B"
        elif 192 <= first_octet <= 223:
            result["class"] = "C"
        elif 224 <= first_octet <= 239:
            result["class"] = "D (Multicast)"
        elif 240 <= first_octet <= 255:
            result["class"] = "E (Reserved)"
        
        # Determine IP type
        if ip.is_private:
            result["type"] = "Private"
        elif ip.is_loopback:
            result["type"] = "Loopback"
        elif ip.is_multicast:
            result["type"] = "Multicast"
        elif ip.is_reserved:
            result["type"] = "Reserved"
        elif ip.is_link_local:
            result["type"] = "Link Local"
        else:
            result["type"] = "Public"
            
    except ValueError as e:
        result["error"] = str(e)
    
    return result

def is_ip_in_network(ip_address, network):
    """
    Check if an IP address belongs to a network
    Returns a dictionary with the result and details
    """
    result = {"in_network": False, "error": None, "details": None}
    
    try:
        # Create IP and network objects
        ip = ipaddress.IPv4Address(ip_address)
        net = ipaddress.IPv4Network(network, strict=False)
        
        # Check if IP is in the network
        result["in_network"] = ip in net
        
        # Add details about the network
        result["details"] = {
            "network_address": str(net.network_address),
            "broadcast_address": str(net.broadcast_address),
            "netmask": str(net.netmask),
            "prefix_length": f"/{net.prefixlen}",
            "total_addresses": net.num_addresses,
            "first_usable": str(net.network_address + 1),
            "last_usable": str(net.broadcast_address - 1)
        }
        
        # Add host position details if IP is in network
        if result["in_network"]:
            # Calculate host number (position) in the network
            host_position = int(ip) - int(net.network_address)
            result["details"]["host_position"] = host_position
            result["details"]["host_position_from_end"] = net.num_addresses - host_position - 1
            
    except ValueError as e:
        result["error"] = str(e)
    
    return result

def calculate_ip_range(start_ip, end_ip):
    """
    Calculate information about an IP range specified by start and end addresses
    Returns summary information and the networks that encompass the range
    """
    result = {"valid": False, "error": None, "summary": None, "networks": []}
    
    try:
        # Create IP objects
        start = ipaddress.IPv4Address(start_ip)
        end = ipaddress.IPv4Address(end_ip)
        
        # Ensure start is before end
        if start > end:
            start, end = end, start
            
        # Calculate summary information
        result["valid"] = True
        result["summary"] = {
            "start_ip": str(start),
            "end_ip": str(end),
            "total_addresses": int(end) - int(start) + 1
        }
        
        # Find the networks that exactly encompass this range (CIDR blocks)
        networks = list(ipaddress.summarize_address_range(start, end))
        
        # Add information about each network
        for net in networks:
            result["networks"].append({
                "network": str(net),
                "network_address": str(net.network_address),
                "broadcast_address": str(net.broadcast_address),
                "netmask": str(net.netmask),
                "prefix_length": f"/{net.prefixlen}",
                "num_addresses": net.num_addresses
            })
            
    except ValueError as e:
        result["error"] = str(e)
    
    return result

def run_ip_validation_tool(ip_address=None):
    """Run the IP address validation tool interactively or with provided input"""
    try:
        if ip_address is None:
            ip_address = input("Enter an IP address to validate: ")
        
        result = validate_ip(ip_address)
        
        if result["error"]:
            print(f"\nError: {result['error']}")
            return
        
        print(f"\nIP Validation Results for {ip_address}:")
        print(f"Valid IPv4:         {result['valid']}")
        print(f"Binary:             {result['binary']}")
        print(f"IP Class:           {result['class']}")
        print(f"IP Type:            {result['type']}")
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return

def run_ip_in_network_tool(ip_address=None, network=None):
    """Run the tool to check if an IP belongs to a network, interactively or with provided input"""
    try:
        if ip_address is None:
            ip_address = input("Enter an IP address to check: ")
        
        if network is None:
            network = input("Enter a network in CIDR notation (e.g., 192.168.1.0/24): ")
        
        result = is_ip_in_network(ip_address, network)
        
        if result["error"]:
            print(f"\nError: {result['error']}")
            return
        
        details = result["details"]
        print(f"\nIP Network Membership Check:")
        print(f"IP Address:         {ip_address}")
        print(f"Network:            {network}")
        print(f"Is IP in Network:   {result['in_network']}")
        print()
        print(f"Network Details:")
        print(f"Network Address:    {details['network_address']}")
        print(f"Broadcast Address:  {details['broadcast_address']}")
        print(f"Subnet Mask:        {details['netmask']}")
        print(f"Prefix Length:      {details['prefix_length']}")
        print(f"Total Addresses:    {details['total_addresses']}")
        print(f"First Usable Host:  {details['first_usable']}")
        print(f"Last Usable Host:   {details['last_usable']}")
        
        if result["in_network"]:
            print()
            print(f"Host Position Details:")
            print(f"Position in Network: {details['host_position']} (starting from 0)")
            print(f"Position from End:   {details['host_position_from_end']} (to broadcast)")
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return

def run_ip_range_tool(start_ip=None, end_ip=None):
    """Run the IP range calculation tool interactively or with provided input"""
    try:
        if start_ip is None:
            start_ip = input("Enter the starting IP address: ")
        
        if end_ip is None:
            end_ip = input("Enter the ending IP address: ")
        
        result = calculate_ip_range(start_ip, end_ip)
        
        if result["error"]:
            print(f"\nError: {result['error']}")
            return
        
        summary = result["summary"]
        networks = result["networks"]
        
        print(f"\nIP Range Analysis:")
        print(f"Start IP:           {summary['start_ip']}")
        print(f"End IP:             {summary['end_ip']}")
        print(f"Total Addresses:    {summary['total_addresses']}")
        
        print(f"\nOptimal CIDR Block Representation:")
        if networks:
            for i, net in enumerate(networks, 1):
                print(f"  Block {i}: {net['network']} ({net['num_addresses']} addresses)")
        else:
            print("  No networks found")
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return 