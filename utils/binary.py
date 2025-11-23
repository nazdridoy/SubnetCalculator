# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 2025 nazDridoy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""Binary representation utilities for IP addresses.

Provides functions for converting IP addresses and networks to binary format,
creating visual representations, and generating prefix masks.

Functions:
    int_to_binary: Convert integer to binary string with specified width.
    get_binary_ip: Convert network address to 32-bit binary string.
    format_binary_ip: Format binary string with dots for readability.
    ip_to_binary_visual: Create visual binary representation showing network/host bits.
    create_prefix_mask: Create visual mask showing network vs host parts.
    create_prefix_binary_mask: Create visual mask with actual binary values.
"""
import ipaddress
from constants import BITS_PER_OCTET, OCTETS_IN_IPV4, BITS_IN_IPV4


def int_to_binary(value: int, bit_width: int = BITS_IN_IPV4) -> str:
    """
    Convert an integer to a binary string with specified width.
    
    Args:
        value: Integer value to convert
        bit_width: Width of the binary string (default: 32 bits for IPv4)
        
    Returns:
        Binary string representation
    """
    return bin(value)[2:].zfill(bit_width)


def get_binary_ip(network: str) -> str:
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
        return int_to_binary(ip_int, BITS_IN_IPV4)
    except (ValueError, TypeError):
        return None


def format_binary_ip(binary_str: str) -> str:
    """
    Format a 32-bit binary string with dots for readability
    
    Args:
        binary_str: A 32-bit binary string
        
    Returns:
        Formatted string with dots between octets (e.g., '11000000.10101000.00000001.00000000')
    """
    return '.'.join(binary_str[i:i+BITS_PER_OCTET] for i in range(0, BITS_IN_IPV4, BITS_PER_OCTET))

def ip_to_binary_visual(network: str) -> str:
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
        for i in range(0, BITS_IN_IPV4, BITS_PER_OCTET):
            octet = binary[i:i+BITS_PER_OCTET]
            # Determine which bits are network vs. host bits in this octet
            if prefix_len >= BITS_PER_OCTET:
                # All bits in this octet are network bits
                formatted.append(octet)
                prefix_len -= BITS_PER_OCTET
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
    except (ValueError, TypeError):
        return "Invalid network"

def create_prefix_mask(prefix_len: int, total_len: int = BITS_IN_IPV4) -> str:
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
    return '.'.join(mask[i:i+BITS_PER_OCTET] for i in range(0, total_len, BITS_PER_OCTET))

def create_prefix_binary_mask(network_obj: ipaddress.IPv4Network) -> str:
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
    for i in range(0, BITS_IN_IPV4, BITS_PER_OCTET):
        octet = binary[i:i+BITS_PER_OCTET]
        # Determine how many bits in this octet are network bits
        if prefix_len >= BITS_PER_OCTET:
            # All bits in this octet are network bits, mark with 1s
            formatted.append('1' * BITS_PER_OCTET)
            prefix_len -= BITS_PER_OCTET
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