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

"""IP address validation utilities.

Provides functions for validating and analyzing IPv4 addresses,
including class determination and type identification.

Functions:
    validate_ip: Validate IPv4 address and return detailed information.
"""
import ipaddress
from typing import Dict, Any
from constants import (
    CLASS_A_START, CLASS_A_END,
    CLASS_B_START, CLASS_B_END,
    CLASS_C_START, CLASS_C_END,
    CLASS_D_START, CLASS_D_END,
    CLASS_E_START, CLASS_E_END,
    LOOPBACK
)
from utils.binary import int_to_binary


def validate_ip(ip_address: str) -> Dict[str, Any]:
    """
    Validate if a string is a valid IPv4 address
    Returns a dictionary with validation status and details
    
    Args:
        ip_address: IP address to validate
        
    Returns:
        Dictionary with validation results and IP information
    """
    result: Dict[str, Any] = {"valid": False, "error": None, "binary": None, "class": None, "type": None}
    
    try:
        # Try to create an IPv4Address object
        ip = ipaddress.IPv4Address(ip_address)
        result["valid"] = True
        
        # Get binary representation
        binary = int_to_binary(int(ip), 32)
        result["binary"] = ".".join(binary[i:i+8] for i in range(0, 32, 8))
        
        # Get hex representation
        result["hex"] = format(int(ip), '08X')
        
        # Get decimal representation
        result["decimal"] = int(ip)
        
        # Get octet values
        octets = ip_address.split('.')
        result["octets"] = " | ".join(octets)
        
        # Determine IP class
        first_octet = int(ip_address.split('.')[0])
        if CLASS_A_START <= first_octet <= CLASS_A_END:
            result["class"] = f"Class A ({CLASS_A_START}-{CLASS_A_END})"
        elif CLASS_B_START <= first_octet <= CLASS_B_END:
            result["class"] = f"Class B ({CLASS_B_START}-{CLASS_B_END})"
        elif CLASS_C_START <= first_octet <= CLASS_C_END:
            result["class"] = f"Class C ({CLASS_C_START}-{CLASS_C_END})"
        elif CLASS_D_START <= first_octet <= CLASS_D_END:
            result["class"] = f"Class D (Multicast) ({CLASS_D_START}-{CLASS_D_END})"
        elif CLASS_E_START <= first_octet <= CLASS_E_END:
            result["class"] = f"Class E (Reserved) ({CLASS_E_START}-{CLASS_E_END})"
        elif first_octet == LOOPBACK:
            result["class"] = f"Loopback ({LOOPBACK})"
        
        # Set default values for range_info and comm_type
        result["range_info"] = "No specific range information available"
        result["comm_type"] = "Address is unicast (host to host communication)"
        
        # Determine IP type
        if ip.is_loopback:
            result["type"] = "Loopback Address"
            result["range_info"] = "Address is in the loopback range 127.0.0.0/8"
        elif ip.is_private:
            result["type"] = "Private Address"
            # Add RFC1918 information
            if first_octet == 10:
                result["range_info"] = "Address is in the private range 10.0.0.0/8 (RFC1918)"
            elif first_octet == 172 and 16 <= int(octets[1]) <= 31:
                result["range_info"] = "Address is in the private range 172.16.0.0/12 (RFC1918)"
            elif first_octet == 192 and int(octets[1]) == 168:
                result["range_info"] = "Address is in the private range 192.168.0.0/16 (RFC1918)"
        elif ip.is_multicast:
            result["type"] = "Multicast Address"
            result["range_info"] = "Address is used for multicast (one to many) communication"
            result["comm_type"] = "Address is multicast (one to many communication)"
        elif ip.is_reserved:
            result["type"] = "Reserved Address"
            result["range_info"] = "Address is reserved for special use"
        elif ip.is_link_local:
            result["type"] = "Link Local Address"
            result["range_info"] = "Address is in the link-local range 169.254.0.0/16"
        else:
            result["type"] = "Public Address"
            result["range_info"] = "Address is publicly routable on the internet"
            
    except ValueError as e:
        result["error"] = str(e)
    
    return result 