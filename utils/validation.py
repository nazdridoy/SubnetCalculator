"""
IP address validation utilities.
"""
import ipaddress

def validate_ip(ip_address):
    """
    Validate if a string is a valid IPv4 address
    Returns a dictionary with validation status and details
    
    Args:
        ip_address: IP address to validate
        
    Returns:
        Dictionary with validation results and IP information
    """
    result = {"valid": False, "error": None, "binary": None, "class": None, "type": None}
    
    try:
        # Try to create an IPv4Address object
        ip = ipaddress.IPv4Address(ip_address)
        result["valid"] = True
        
        # Get binary representation
        binary = bin(int(ip))[2:].zfill(32)
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
        if 1 <= first_octet <= 126:
            result["class"] = "Class A (1-126)"
        elif 128 <= first_octet <= 191:
            result["class"] = "Class B (128-191)"
        elif 192 <= first_octet <= 223:
            result["class"] = "Class C (192-223)"
        elif 224 <= first_octet <= 239:
            result["class"] = "Class D (Multicast) (224-239)"
        elif 240 <= first_octet <= 255:
            result["class"] = "Class E (Reserved) (240-255)"
        elif first_octet == 127:
            result["class"] = "Loopback (127)"
        
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