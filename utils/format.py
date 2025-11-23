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

"""Formatting utilities for console output.

Provides functions for formatting and displaying subnet information in tables.

Functions:
    print_table: Print a nicely formatted table from list of lists.
    format_subnet_info: Format subnet information for display.
"""

def print_table(data):
    """Print a nicely formatted table from a list of lists.
    
    The first row is treated as the header row.
    
    Args:
        data: A list of lists representing table rows and columns.
    """
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

def format_subnet_info(subnet_info, is_flsm=True):
    """Format subnet information for display.
    
    Args:
        subnet_info: A NamedTuple containing subnet information.
        is_flsm: If True, format for FLSM display; if False, format for VLSM display.
    
    Returns:
        A list of formatted strings representing subnet information for table display.
    """
    if is_flsm:
        subnet, index, total_hosts = subnet_info
        return [
            f"Subnet {index}",
            f"{subnet}",
            f"{subnet.netmask}",
            f"{subnet.network_address}",
            f"{subnet.broadcast_address}",
            f"{subnet.network_address + 1}",
            f"{subnet.broadcast_address - 1}",
            f"{total_hosts}"
        ]
    else:  # VLSM format
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