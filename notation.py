#!/usr/bin/env python3
import ipaddress

def cidr_to_subnet_mask(prefix_length):
    """Convert CIDR prefix length to subnet mask"""
    try:
        prefix_length = int(prefix_length)
        if prefix_length < 0 or prefix_length > 32:
            raise ValueError("Prefix length must be between 0 and 32")
        
        # Create a network with this prefix length
        network = ipaddress.IPv4Network(f"0.0.0.0/{prefix_length}", strict=False)
        return str(network.netmask)
    except ValueError as e:
        return str(e)

def subnet_mask_to_cidr(subnet_mask):
    """Convert subnet mask to CIDR prefix length"""
    try:
        # Create IPv4Network to validate the subnet mask
        network = ipaddress.IPv4Network(f"0.0.0.0/{subnet_mask}", strict=False)
        return network.prefixlen
    except ValueError as e:
        return str(e)

def subnet_mask_to_wildcard(subnet_mask):
    """Convert subnet mask to wildcard mask"""
    try:
        # Create IPv4Network to validate the subnet mask
        network = ipaddress.IPv4Network(f"0.0.0.0/{subnet_mask}", strict=False)
        mask_int = int(network.netmask)
        wildcard_int = ~mask_int & 0xFFFFFFFF  # Bitwise NOT and mask to 32 bits
        
        # Convert to dotted decimal notation
        octets = []
        for i in range(4):
            octet = (wildcard_int >> (24 - i * 8)) & 0xFF
            octets.append(str(octet))
        
        return ".".join(octets)
    except ValueError as e:
        return str(e)

def wildcard_to_subnet_mask(wildcard_mask):
    """Convert wildcard mask to subnet mask"""
    try:
        # Parse the wildcard mask
        octets = wildcard_mask.split('.')
        if len(octets) != 4:
            raise ValueError("Invalid wildcard mask format")
        
        # Convert to integer
        wildcard_int = 0
        for i, octet in enumerate(octets):
            wildcard_int |= (int(octet) << (24 - i * 8))
        
        # Invert to get subnet mask
        mask_int = ~wildcard_int & 0xFFFFFFFF  # Bitwise NOT and mask to 32 bits
        
        # Convert to dotted decimal notation
        mask_octets = []
        for i in range(4):
            octet = (mask_int >> (24 - i * 8)) & 0xFF
            mask_octets.append(str(octet))
        
        return ".".join(mask_octets)
    except ValueError as e:
        return str(e)

def cidr_to_wildcard(prefix_length):
    """Convert CIDR prefix length to wildcard mask"""
    try:
        subnet_mask = cidr_to_subnet_mask(prefix_length)
        return subnet_mask_to_wildcard(subnet_mask)
    except ValueError as e:
        return str(e)

def wildcard_to_cidr(wildcard_mask):
    """Convert wildcard mask to CIDR prefix length"""
    try:
        subnet_mask = wildcard_to_subnet_mask(wildcard_mask)
        return subnet_mask_to_cidr(subnet_mask)
    except ValueError as e:
        return str(e)

def detect_notation_type(input_str):
    """Detect the type of notation (CIDR, subnet mask, or wildcard mask)"""
    input_str = input_str.strip()
    
    # Check for CIDR notation
    if input_str.startswith('/'):
        return "cidr"
    
    # Check for just a number (interpreted as CIDR prefix length)
    if input_str.isdigit():
        return "cidr"
    
    # Otherwise, it's either a subnet mask or wildcard mask
    # We need to test if each octet is a valid number
    octets = input_str.split('.')
    if len(octets) != 4:
        return "unknown"
    
    try:
        oct_values = [int(oct) for oct in octets]
        
        # Subnet masks typically have high values (255, 254, 252, etc.)
        # Wildcard masks typically have the inverse pattern
        if all(oct in [0, 128, 192, 224, 240, 248, 252, 254, 255] for oct in oct_values):
            if oct_values[0] >= oct_values[1] >= oct_values[2] >= oct_values[3]:
                return "subnet"
        
        # Check for typical wildcard mask pattern
        inverse_values = [255 - oct for oct in oct_values]
        if all(inv in [0, 128, 192, 224, 240, 248, 252, 254, 255] for inv in inverse_values):
            if inverse_values[0] >= inverse_values[1] >= inverse_values[2] >= inverse_values[3]:
                return "wildcard"
    
    except ValueError:
        return "unknown"
    
    return "unknown"

def convert_notation(input_str):
    """Convert between CIDR, subnet mask, and wildcard mask notations"""
    notation_type = detect_notation_type(input_str)
    
    if notation_type == "unknown":
        return {
            "error": "Unknown notation format. Please provide a valid CIDR prefix, subnet mask, or wildcard mask."
        }
    
    result = {}
    
    # Process CIDR notation
    if notation_type == "cidr":
        prefix_length = input_str.strip('/')
        result["notation_type"] = "CIDR"
        result["cidr"] = f"/{prefix_length}"
        result["subnet_mask"] = cidr_to_subnet_mask(prefix_length)
        result["wildcard_mask"] = cidr_to_wildcard(prefix_length)
    
    # Process subnet mask notation
    elif notation_type == "subnet":
        result["notation_type"] = "Subnet Mask"
        result["subnet_mask"] = input_str
        prefix_length = subnet_mask_to_cidr(input_str)
        result["cidr"] = f"/{prefix_length}"
        result["wildcard_mask"] = subnet_mask_to_wildcard(input_str)
    
    # Process wildcard mask notation
    elif notation_type == "wildcard":
        result["notation_type"] = "Wildcard Mask"
        result["wildcard_mask"] = input_str
        result["subnet_mask"] = wildcard_to_subnet_mask(input_str)
        prefix_length = subnet_mask_to_cidr(result["subnet_mask"])
        result["cidr"] = f"/{prefix_length}"
    
    return result

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