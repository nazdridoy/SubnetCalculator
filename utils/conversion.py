"""IP notation conversion utilities.

Provides functions to convert between different IP network notation formats:
CIDR prefix lengths, subnet masks, and wildcard masks.

Functions:
    cidr_to_subnet_mask: Convert CIDR prefix to subnet mask.
    subnet_mask_to_cidr: Convert subnet mask to CIDR prefix.
    subnet_mask_to_wildcard: Convert subnet mask to wildcard mask.
    wildcard_to_subnet_mask: Convert wildcard mask to subnet mask.
    cidr_to_wildcard: Convert CIDR prefix to wildcard mask.
    wildcard_to_cidr: Convert wildcard mask to CIDR prefix.
    detect_notation_type: Detect notation type from input string.
    convert_notation: Convert between all notation formats.
"""
import ipaddress

def cidr_to_subnet_mask(prefix_length):
    """
    Convert CIDR prefix length to subnet mask
    
    Args:
        prefix_length: CIDR prefix length (0-32)
    
    Returns:
        Subnet mask as a string (e.g., '255.255.255.0')
    """
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
    """
    Convert subnet mask to CIDR prefix length
    
    Args:
        subnet_mask: Subnet mask as a string (e.g., '255.255.255.0')
    
    Returns:
        CIDR prefix length as an integer
    """
    try:
        # Create IPv4Network to validate the subnet mask
        network = ipaddress.IPv4Network(f"0.0.0.0/{subnet_mask}", strict=False)
        return network.prefixlen
    except ValueError as e:
        return str(e)

def subnet_mask_to_wildcard(subnet_mask):
    """
    Convert subnet mask to wildcard mask
    
    Args:
        subnet_mask: Subnet mask as a string (e.g., '255.255.255.0')
    
    Returns:
        Wildcard mask as a string (e.g., '0.0.0.255')
    """
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
    """
    Convert wildcard mask to subnet mask
    
    Args:
        wildcard_mask: Wildcard mask as a string (e.g., '0.0.0.255')
    
    Returns:
        Subnet mask as a string (e.g., '255.255.255.0')
    """
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
    """
    Convert CIDR prefix length to wildcard mask
    
    Args:
        prefix_length: CIDR prefix length (0-32)
    
    Returns:
        Wildcard mask as a string (e.g., '0.0.0.255')
    """
    try:
        subnet_mask = cidr_to_subnet_mask(prefix_length)
        return subnet_mask_to_wildcard(subnet_mask)
    except ValueError as e:
        return str(e)

def wildcard_to_cidr(wildcard_mask):
    """
    Convert wildcard mask to CIDR prefix length
    
    Args:
        wildcard_mask: Wildcard mask as a string (e.g., '0.0.0.255')
    
    Returns:
        CIDR prefix length as an integer
    """
    try:
        subnet_mask = wildcard_to_subnet_mask(wildcard_mask)
        return subnet_mask_to_cidr(subnet_mask)
    except ValueError as e:
        return str(e)

def detect_notation_type(input_str):
    """
    Detect the type of notation (CIDR, subnet mask, or wildcard mask)
    
    Args:
        input_str: Input string to detect notation type
    
    Returns:
        String indicating the detected notation type ('cidr', 'subnet', 'wildcard', or 'unknown')
    """
    input_str = input_str.strip()
    
    # Check for CIDR notation (e.g., /24)
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
    """
    Convert between CIDR, subnet mask, and wildcard mask notations
    
    Args:
        input_str: Input string in any notation format
    
    Returns:
        Dictionary with converted notation in all formats
    """
    input_str = input_str.strip()
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