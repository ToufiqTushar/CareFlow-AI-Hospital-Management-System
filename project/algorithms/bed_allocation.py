
def allocate_bed(priority, beds):
    """
    Allocate bed based on priority level.
    Returns (ward_name, bed_index) or None if no bed available.
    
    beds structure:
    {
        "ICU": [False, True, False],  # False=available, True=occupied
        "Ward": [False, False, False, False]
    }
    """
    
    if priority == "RED":
        allocation_order = ["ICU", "Ward"]
    elif priority == "YELLOW":
        allocation_order = ["Ward", "ICU"]
    elif priority == "GREEN":
        allocation_order = ["Ward"]
    else: 
        allocation_order = ["Ward"]
    
    for ward in allocation_order:
        if ward not in beds:
            continue
            
        for bed_index, occupied in enumerate(beds[ward]):
            if not occupied:  # Bed is available
                return (ward, bed_index)
    
    return None  # No beds available

def release_bed(ward, bed_index, beds):
    """Release a bed when patient leaves"""
    if ward in beds and 0 <= bed_index < len(beds[ward]):
        beds[ward][bed_index] = False
        return True
    return False

def get_bed_status(beds):
    """Get current bed occupancy statistics"""
    status = {}
    for ward, bed_list in beds.items():
        total = len(bed_list)
        occupied = sum(bed_list)
        available = total - occupied
        status[ward] = {
            "total": total,
            "occupied": occupied,
            "available": available,
            "occupancy_rate": (occupied / total * 100) if total > 0 else 0
        }
    return status