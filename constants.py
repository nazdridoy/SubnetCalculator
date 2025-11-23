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

"""Constants used across the subnet calculator.

This module defines all magic numbers and configuration values used throughout
the SubnetCalculator project, improving code readability and maintainability.

Module Constants:
    Version:
        VERSION: Current version of SubnetCalculator.
    
    IPv4 Prefix Limits:
        MIN_PREFIX_LENGTH: Minimum IPv4 prefix length (0).
        MAX_PREFIX_LENGTH: Maximum IPv4 prefix length (32).
        MAX_USABLE_PREFIX: Maximum usable prefix with hosts (/30).
        POINT_TO_POINT_PREFIX: RFC 3021 point-to-point links (/31).
        HOST_PREFIX: Single host address (/32).
    
    Performance Thresholds:
        LARGE_NETWORK_THRESHOLD: Threshold for algorithm selection.
    
    Network Calculation:
        NETWORK_AND_BROADCAST_OVERHEAD: Reserved addresses per subnet.
    
    IP Address Classes:
        CLASS_*_START/END: IPv4 address class boundaries.
        LOOPBACK: Loopback address (127).
    
    Binary Formatting:
        BITS_PER_OCTET: Bits per IPv4 octet (8).
        OCTETS_IN_IPV4: Number of octets in IPv4 (4).
        BITS_IN_IPV4: Total bits in IPv4 address (32).
"""

# Version
VERSION = "1.3.0"

# IPv4 Prefix Limits
MIN_PREFIX_LENGTH = 0
MAX_PREFIX_LENGTH = 32
MAX_USABLE_PREFIX = 30  # /30 = 4 addresses, 2 usable hosts
POINT_TO_POINT_PREFIX = 31  # RFC 3021 - point-to-point links (2 addresses, 2 usable)
HOST_PREFIX = 32  # Single host address

# Performance Thresholds
LARGE_NETWORK_THRESHOLD = 65536  # Use optimized algorithms for networks larger than this
MAX_SUBNETS_TO_CREATE = 4096  # Reasonable limit for subnet creation to prevent memory issues

# Network Calculation
NETWORK_AND_BROADCAST_OVERHEAD = 2  # Addresses reserved in subnets (network + broadcast)

# IP Address Classes (for validation and classification)
CLASS_A_START = 1
CLASS_A_END = 126
CLASS_B_START = 128
CLASS_B_END = 191
CLASS_C_START = 192
CLASS_C_END = 223
CLASS_D_START = 224  # Multicast
CLASS_D_END = 239
CLASS_E_START = 240  # Reserved
CLASS_E_END = 255
LOOPBACK = 127

# Binary Formatting
BITS_PER_OCTET = 8
OCTETS_IN_IPV4 = 4
BITS_IN_IPV4 = 32  # Total bits in an IPv4 address
