#!/usr/bin/env python3
from utils.conversion import convert_notation

def run_conversion_tool(input_str=None):
    """Run the notation conversion tool interactively or with provided input"""
    try:
        if input_str is None:
            input_str = input("Enter a notation to convert (CIDR prefix, subnet mask, or wildcard mask): ")
        
        result = convert_notation(input_str)
        
        if "error" in result:
            print(f"\nError: {result['error']}")
            return
        
        print(f"\nConversion Results for {input_str} ({result['notation_type']}):")
        print(f"CIDR Notation:      {result['cidr']}")
        print(f"Subnet Mask:        {result['subnet_mask']}")
        print(f"Wildcard Mask:      {result['wildcard_mask']}")
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return 