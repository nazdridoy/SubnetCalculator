#!/usr/bin/env python3
"""Supernetting and CIDR aggregation module.

This module provides functionality for network aggregation, supernetting, and
route summarization. Supports both efficient multi-block aggregation and
single supernet calculation.

Functions:
    aggregate_networks: Aggregate networks into efficient CIDR blocks.
    find_supernet: Find the smallest common supernet for all networks.
    check_network_overlap: Check if networks overlap.
    calculate_unique_addresses: Calculate total unique addresses across networks.
    run_supernet_tool: Interactive supernetting tool (CLI entry point).
    
Private Helper Functions:
    _display_input_networks: Display input network list.
    _display_efficient_aggregation: Display multi-block aggregation results.
    _display_single_supernet: Display single supernet summary.
    _display_common_prefix_analysis: Display common prefix analysis.
"""
import ipaddress
from typing import List, Tuple, Optional
from constants import LARGE_NETWORK_THRESHOLD
from utils.binary import get_binary_ip, format_binary_ip, ip_to_binary_visual, create_prefix_binary_mask
from utils.network import get_common_prefix

def aggregate_networks(networks):
    """
    Aggregate a list of networks into the most efficient CIDR blocks.
    Returns a list of supernets that cover all input networks with minimal waste.
    """
    if not networks:
        return []
    
    # Parse and validate all networks
    valid_networks = []
    for net in networks:
        try:
            network = ipaddress.ip_network(net, strict=False)
            valid_networks.append(network)
        except ValueError:
            continue
    
    if not valid_networks:
        return []
    
    # Sort networks by network address
    valid_networks.sort(key=lambda x: int(x.network_address))
    
    # Group adjacent networks that can be aggregated
    supernets = []
    i = 0
    while i < len(valid_networks):
        current = valid_networks[i]
        
        # Find networks that can be aggregated with the current one
        j = i + 1
        while j < len(valid_networks):
            # Try to aggregate the current network with the next one
            aggregate = ipaddress.collapse_addresses([current, valid_networks[j]])
            try:
                # If we get a single network after aggregation, it's efficient
                aggregate_list = list(aggregate)
                if len(aggregate_list) == 1:
                    current = aggregate_list[0]
                    j += 1
                else:
                    break
            except Exception:
                break
        
        supernets.append(current)
        i = j
    
    return supernets

def find_supernet(networks):
    """
    Find the smallest common supernet that contains all networks.
    This might be inefficient in terms of address space but guarantees one single block.
    """
    if not networks:
        return None
    
    # Find the smallest and largest IP in all networks
    min_ip = None
    max_ip = None
    
    for net_str in networks:
        try:
            net = ipaddress.ip_network(net_str, strict=False)
            if min_ip is None or int(net.network_address) < int(min_ip):
                min_ip = net.network_address
            if max_ip is None or int(net.broadcast_address) > int(max_ip):
                max_ip = net.broadcast_address
        except ValueError:
            continue
    
    if min_ip is None or max_ip is None:
        return None
    
    # Convert to integers for bit manipulation
    start_int = int(min_ip)
    end_int = int(max_ip)
    
    # Find the number of bits required to represent the range
    mask_bits = 32
    for i in range(32):
        mask = (1 << i) - 1
        if (start_int & ~mask) == (end_int & ~mask):
            mask_bits = 32 - i
            break
    
    # Apply the mask to get the network address
    network_int = start_int & (~((1 << (32 - mask_bits)) - 1))
    network = ipaddress.IPv4Address(network_int)
    
    # Return the supernet in CIDR notation
    return f"{network}/{mask_bits}"

def check_network_overlap(networks: List[str]) -> Tuple[bool, int]:
    """
    Check if networks overlap and calculate the amount of overlap.
    Uses optimized algorithm based on network size.
    
    Args:
        networks: List of networks in CIDR notation
        
    Returns:
        Tuple of (has_overlap, overlap_addresses)
    """
    if not networks or len(networks) < 2:
        return False, 0
    
    # Convert to network objects
    valid_networks = []
    for net in networks:
        try:
            network = ipaddress.ip_network(net, strict=False)
            valid_networks.append(network)
        except (ValueError, TypeError):
            continue
    
    if not valid_networks or len(valid_networks) < 2:
        return False, 0
    
    # For small to medium networks, use direct IP counting
    if all(net.num_addresses <= LARGE_NETWORK_THRESHOLD for net in valid_networks):
        # Count unique IPs
        unique_ips = set()
        for net in valid_networks:
            for ip in net:
                unique_ips.add(ip)
        
        # Calculate overlap
        total_size = sum(net.num_addresses for net in valid_networks)
        unique_size = len(unique_ips)
        overlap = total_size - unique_size
        
        return overlap > 0, overlap
    else:
        # For large networks, use mathematical overlap detection
        # Sort networks by network address for efficient comparison
        sorted_networks = sorted(valid_networks, key=lambda x: int(x.network_address))
        
        has_overlap = False
        for i in range(len(sorted_networks) - 1):
            current = sorted_networks[i]
            next_net = sorted_networks[i + 1]
            
            # Check if current network's broadcast overlaps with next network's start
            if int(current.broadcast_address) >= int(next_net.network_address):
                has_overlap = True
                break
        
        # Also check for containment (one network inside another)
        if not has_overlap:
            for i, net1 in enumerate(sorted_networks):
                for j, net2 in enumerate(sorted_networks):
                    if i != j and (net1.subnet_of(net2) or net2.subnet_of(net1)):
                        has_overlap = True
                        break
                if has_overlap:
                    break
        
        return has_overlap, 0  # For large networks, don't calculate exact overlap

def calculate_unique_addresses(networks: List[str]) -> int:
    """
    Calculate the total number of unique addresses across all networks,
    accounting for overlaps.
    
    Args:
        networks: List of networks in CIDR notation
        
    Returns:
        Total number of unique addresses
    """
    if not networks:
        return 0
    
    # Convert to network objects
    valid_networks = []
    for net in networks:
        try:
            network = ipaddress.ip_network(net, strict=False)
            valid_networks.append(network)
        except (ValueError, TypeError):
            continue
    
    # For large networks, estimate without creating sets of all IPs
    if any(net.num_addresses > LARGE_NETWORK_THRESHOLD for net in valid_networks):
        # Sort networks by size (largest first)
        valid_networks.sort(key=lambda x: x.num_addresses, reverse=True)
        
        # Take the largest network as the base
        unique_addresses = valid_networks[0].num_addresses if valid_networks else 0
        
        # For each smaller network, add only addresses that don't overlap with larger ones
        for i in range(1, len(valid_networks)):
            current = valid_networks[i]
            overlap = False
            
            # Check if current network overlaps with any larger network
            for j in range(i):
                if current.overlaps(valid_networks[j]):
                    # If it's a subset, don't add any addresses
                    if current.subnet_of(valid_networks[j]):
                        overlap = True
                        break
            
            if not overlap:
                unique_addresses += current.num_addresses
                
        return unique_addresses
    else:
        # For smaller networks, use direct IP counting
        unique_ips = set()
        for net in valid_networks:
            for ip in net:
                unique_ips.add(ip)
        return len(unique_ips)

def _display_input_networks(networks: List[str]) -> None:
    """Display input networks with binary representations."""
    print("\nSupernetting Results:")
    print(f"Input Networks ({len(networks)}):")
    for i, net in enumerate(networks, 1):
        try:
            network = ipaddress.ip_network(net, strict=False)
            print(f"  {i}. {network} ({network.num_addresses} addresses)")
            binary = get_binary_ip(net)
            if binary:
                print(f"     Binary: {ip_to_binary_visual(net)}")
                print(f"     Prefix: {create_prefix_binary_mask(network)}")
        except (ValueError, TypeError) as e:
            print(f"  {i}. {net} (Invalid: {e})")


def _display_efficient_aggregation(networks: List[str]) -> None:
    """Display efficient aggregation results (multiple blocks)."""
    print("\n1. Efficient Aggregation (Multiple Blocks)")
    efficient_blocks = aggregate_networks(networks)
    if efficient_blocks:
        print(f"   Result: {len(efficient_blocks)} CIDR block(s)")
        total_addresses = sum(net.num_addresses for net in efficient_blocks)
        for i, net in enumerate(efficient_blocks, 1):
            print(f"     Block {i}: {net} ({net.num_addresses} addresses)")
            print(f"            Binary: {ip_to_binary_visual(str(net))}")
            print(f"            Prefix: {create_prefix_binary_mask(net)}")
        print(f"   Total Addresses: {total_addresses}")
    else:
        print("   No valid aggregation possible.")


def _display_single_supernet(networks: List[str], has_overlap: bool) -> None:
    """Display single supernet summary route."""
    print("\n2. Single Supernet (Summary Route)")
    single_supernet = find_supernet(networks)
    if single_supernet:
        try:
            network = ipaddress.ip_network(single_supernet, strict=False)
            
            # Calculate unique addresses across all input networks
            unique_addresses = calculate_unique_addresses(networks)
            
            # Calculate waste as the difference between supernet size and unique addresses
            waste = network.num_addresses - unique_addresses
            waste_percent = (waste / network.num_addresses) * 100 if network.num_addresses > 0 else 0
            
            print(f"   Result: {network} ({network.num_addresses} addresses)")
            print(f"          Binary: {ip_to_binary_visual(single_supernet)}")
            print(f"          Prefix: {create_prefix_binary_mask(network)}")
            
            if has_overlap:
                print(f"   Note: Calculation accounts for overlapping networks")
                
            print(f"   Address Waste: {waste} addresses ({waste_percent:.1f}%)")
        except (ValueError, TypeError):
            print(f"   Result: {single_supernet} (Could not calculate waste)")
    else:
        print("   No valid supernet possible.")


def _display_common_prefix_analysis(networks: List[str]) -> None:
    """Display common prefix analysis."""
    print("\n3. Common Prefix Analysis")
    common_network, prefix_len = get_common_prefix(networks)
    if common_network:
        print(f"   Common Prefix: {prefix_len} bits")
        print(f"   Common Network: {common_network}")
        
        # Visualize the common prefix
        binary = get_binary_ip(common_network)
        if binary:
            # Show the matching prefix pattern
            common_mask = 'N' * prefix_len + 'H' * (32 - prefix_len)  # N for network, H for host
            formatted_mask = '.'.join(common_mask[i:i+8] for i in range(0, 32, 8))
            print(f"   Prefix Mask:  {formatted_mask}")
            print(f"                 N = Network bits (match), H = Host bits (vary)")
            
            # Show the actual binary of the network with the common prefix
            actual_binary = format_binary_ip(binary)
            print(f"   Binary Form:  {actual_binary}")
            
            # Calculate base network based on prefix
            base_network = ipaddress.ip_network(f"{ipaddress.IPv4Address(int(binary[:prefix_len] + '0' * (32 - prefix_len), 2))}/{prefix_len}")
            first_address = base_network.network_address
            last_address = base_network.broadcast_address
            print(f"   Address Range: {first_address} - {last_address}")
            print(f"   Total Range:   {base_network.num_addresses} addresses")
    else:
        print("   No common prefix found.")


def run_supernet_tool(networks: Optional[List[str]] = None) -> None:
    """Run the supernetting tool interactively or with provided networks.
    
    Args:
        networks: Optional list of network strings in CIDR notation
    """
    try:
        if networks is None:
            networks_input = input("Enter a list of networks to aggregate (comma or space separated, e.g., 192.168.0.0/24 192.168.1.0/24): ")
            networks = [net.strip() for net in networks_input.replace(',', ' ').split() if net.strip()]
        
        if not networks:
            print("Error: No valid networks provided.")
            return
        
        # Display input networks
        _display_input_networks(networks)
        
        # Check for overlapping networks
        has_overlap, overlap_amount = check_network_overlap(networks)
        if has_overlap:
            print("\nNote: The provided networks have overlapping address spaces.")
            print(f"      Some addresses appear in multiple networks.")
        
        # Display results
        _display_efficient_aggregation(networks)
        _display_single_supernet(networks, has_overlap)
        _display_common_prefix_analysis(networks)
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return
    except Exception as e:
        print(f"Error: {e}")
        return 