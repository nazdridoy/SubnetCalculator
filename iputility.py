#!/usr/bin/env python3
"""IP address utility tools module.

Provides utilities for IP address validation, network membership checking,
and IP range analysis.

Functions:
    calculate_ip_range: Calculate information about an IP range.
    run_ip_validation_tool: Interactive IP validation tool.
    run_ip_in_network_tool: Check if IP is within a network.
    run_ip_range_tool: Analyze an IP address range.
"""
import ipaddress
from utils.validation import validate_ip
from utils.network import check_ip_in_network, display_network_summary

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
            net_summary = display_network_summary(str(net))
            if "error" not in net_summary:
                result["networks"].append({
                    "network": net_summary["network"],
                    "network_address": net_summary["network_address"],
                    "broadcast_address": net_summary["broadcast_address"],
                    "netmask": net_summary["netmask"],
                    "prefix_length": net_summary["prefix_length"],
                    "num_addresses": net_summary["num_addresses"]
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
        
        print(f"\nIP Address Analysis Results:")
        print()
        print(f"IP Address:        {ip_address}")
        print(f"Valid IPv4:         {result['valid']}")
        print(f"Address Type:      {result['type']}")
        print(f"Binary Form:       {result['binary']}")
        print(f"Hex Form:          {result['hex']}")
        print(f"Decimal Form:      {result['decimal']}")
        print(f"Octet Values:      {result['octets']}")
        print(f"Address Class:     {result['class']}")
        print()
        print(f"Network Info:")
        print(f"{result['range_info']}")
        print(f"{result['comm_type']}")
    
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
        
        result = check_ip_in_network(ip_address, network)
        
        if result["error"]:
            print(f"\nError: {result['error']}")
            return
        
        details = result["details"]
        print(f"\nIP Network Membership Check:")
        print(f"IP Address:         {ip_address}")
        print(f"Network:            {details['network']}")
        print(f"Is IP in Network:   {result['in_network']}")
        print()
        print(f"Network Details:")
        print(f"Network Address:    {details['network_address']}")
        print(f"Broadcast Address:  {details['broadcast_address']}")
        print(f"Subnet Mask:        {details['netmask']}")
        print(f"Prefix Length:      {details['prefix_length']}")
        print(f"Total Addresses:    {details['num_addresses']}")
        print(f"Usable Hosts:       {details['usable_hosts']}")
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