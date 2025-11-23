#!/usr/bin/env python3
"""Notation conversion tool module.

Provides functionality to convert between different network notation formats:
CIDR notation, subnet masks, and wildcard masks.

Functions:
    run_conversion_tool: Interactive conversion tool (CLI entry point).
"""
from utils.conversion import convert_notation
from utils.binary import int_to_binary
import ipaddress

def run_conversion_tool(input_str=None):
    """Run the notation conversion tool interactively or with provided input"""
    try:
        if input_str is None:
            input_str = input("Enter a notation to convert (CIDR prefix, subnet mask, or wildcard mask): ")
        
        result = convert_notation(input_str)
        
        if "error" in result:
            print(f"\nError: {result['error']}")
            return
        
        # Extract prefix length for additional calculations
        prefix_length = int(result['cidr'].split('/')[-1])
        
        # Calculate binary mask representation
        subnet_mask = result['subnet_mask']
        network_obj = ipaddress.IPv4Network(f"0.0.0.0/{prefix_length}", strict=False)
        binary_mask = int_to_binary(int(network_obj.netmask), 32)
        formatted_binary = '.'.join(binary_mask[i:i+8] for i in range(0, 32, 8))
        
        # Calculate hex mask
        mask_int = int(network_obj.netmask)
        hex_mask = format(mask_int, '08X')
        
        # Calculate host and address information
        host_bits = 32 - prefix_length
        max_addresses = 2 ** host_bits
        usable_hosts = max_addresses - 2 if prefix_length < 31 else max_addresses
        
        print(f"\nNotation Conversion Results:")
        print(f"\nCIDR Notation:      {result['cidr']}")
        print(f"Subnet Mask:        {result['subnet_mask']}")
        print(f"Wildcard Mask:      {result['wildcard_mask']}")
        print(f"Binary Mask:        {formatted_binary}")
        print(f"Hex Mask:           {hex_mask}")
        print(f"Network Bits:       {prefix_length}")
        print(f"Host Bits:          {host_bits}")
        print(f"Max Addresses:      {max_addresses}")
        print(f"Usable Hosts:       {usable_hosts}")
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return 