#!/usr/bin/env python3
"""
Homework 5.1: Subnet Design for an Organisation
================================================
Computer Networks - Week 5 (WSL Environment)
ASE Bucharest, CSIE | by ing. dr. Antonio Clim

Objectives:
- Design a subnetting scheme using VLSM for variable-sized departments
- Calculate network addresses, broadcast addresses and usable host ranges
- Document IP allocation plans with clear justification
- Apply subnet masks to optimise address space utilisation

Prerequisites:
- Understanding of CIDR notation and subnet masks
- Familiarity with binary-to-decimal IP conversions
- Week 5 exercises completed (ex_5_01, ex_5_02)

Level: Intermediate (⭐⭐)
Estimated time: 60-90 minutes

Pair Programming Notes:
- Driver: Implement calculation functions and main logic
- Navigator: Verify calculations manually, check edge cases
- Swap after: Completing the subnet allocation function

Submission:
- Complete all TODO sections
- Run the verification tests
- Save your subnet plan as JSON output
"""

from __future__ import annotations

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import ipaddress
import json
import sys
from dataclasses import dataclass, asdict
from typing import List, Optional


# ═══════════════════════════════════════════════════════════════════════════════
# DATA_STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class Department:
    """Represents a department requiring IP addresses."""
    name: str
    required_hosts: int
    description: str


@dataclass
class SubnetAllocation:
    """Represents an allocated subnet for a department."""
    department: str
    network_address: str
    broadcast_address: str
    subnet_mask: str
    prefix_length: int
    usable_hosts: int
    first_usable: str
    last_usable: str
    utilisation_percent: float


# ═══════════════════════════════════════════════════════════════════════════════
# ORGANISATION_REQUIREMENTS
# ═══════════════════════════════════════════════════════════════════════════════
# Your organisation has been allocated: 192.168.100.0/24
# You must subnet this for the following departments:

ORGANISATION_BLOCK = "192.168.100.0/24"

DEPARTMENTS = [
    Department("Engineering", 50, "Development workstations and servers"),
    Department("Sales", 25, "Sales team laptops and phones"),
    Department("HR", 10, "Human resources department"),
    Department("Management", 5, "Executive offices"),
    Department("IT_Infrastructure", 12, "Servers, switches, APs"),
    Department("Guest_WiFi", 30, "Visitor wireless access"),
]


# ═══════════════════════════════════════════════════════════════════════════════
# PREDICTION_PROMPT
# ═══════════════════════════════════════════════════════════════════════════════
def prompt_prediction(question: str) -> str:
    """
    Ask student to predict outcome before execution.
    
    Implements Brown & Wilson Principle 4: Predictions.
    """
    print(f"\n💭 PREDICTION: {question}")
    print("   (Think about your answer before pressing Enter)")
    prediction = input("   Your prediction: ")
    return prediction


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def calculate_required_prefix(hosts_needed: int) -> int:
    """
    Calculate the prefix length needed to accommodate a number of hosts.
    
    Remember: Usable hosts = 2^(32-prefix) - 2 (network and broadcast)
    
    Args:
        hosts_needed: Number of usable host addresses required
        
    Returns:
        CIDR prefix length (e.g., 26 for /26)
        
    Example:
        >>> calculate_required_prefix(50)
        26  # /26 gives 62 usable hosts
    """
    # TODO: Implement this function
    # Hint: You need 2^n >= hosts_needed + 2
    # Then prefix = 32 - n
    
    # ─── YOUR CODE HERE ───
    import math
    # We need 2^n >= hosts_needed + 2
    n = math.ceil(math.log2(hosts_needed + 2))
    return 32 - n
    # ─── END YOUR CODE ───


def get_subnet_details(network: ipaddress.IPv4Network) -> dict:
    """
    Extract all relevant details from an IPv4Network object.
    
    Args:
        network: An ipaddress.IPv4Network object
        
    Returns:
        Dictionary with network details
    """
    hosts = list(network.hosts())
    return {
        "network_address": str(network.network_address),
        "broadcast_address": str(network.broadcast_address),
        "subnet_mask": str(network.netmask),
        "prefix_length": network.prefixlen,
        "total_addresses": network.num_addresses,
        "usable_hosts": len(hosts),
        "first_usable": str(hosts[0]) if hosts else None,
        "last_usable": str(hosts[-1]) if hosts else None,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ALLOCATION_FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════
def allocate_subnets(
    base_network: str,
    departments: List[Department]
) -> List[SubnetAllocation]:
    """
    Allocate subnets to departments using VLSM.
    
    VLSM Strategy:
    1. Sort departments by size (largest first) - this minimises waste
    2. For each department, calculate the smallest subnet that fits
    3. Allocate from the available address space
    4. Track remaining space for next allocation
    
    Args:
        base_network: The organisation's allocated block (e.g., "192.168.100.0/24")
        departments: List of Department objects with requirements
        
    Returns:
        List of SubnetAllocation objects
        
    Raises:
        ValueError: If departments cannot fit in the allocated space
    """
    allocations = []
    
    # Parse the base network
    parent = ipaddress.IPv4Network(base_network, strict=True)
    available_networks = [parent]
    
    # Sort departments by required hosts (descending) for best VLSM
    sorted_depts = sorted(departments, key=lambda d: d.required_hosts, reverse=True)
    
    print(f"\n📊 Allocation Order (largest first):")
    for i, dept in enumerate(sorted_depts, 1):
        print(f"   {i}. {dept.name}: {dept.required_hosts} hosts")
    print()
    
    # TODO: Implement the allocation loop
    # For each department:
    # 1. Calculate the required prefix length
    # 2. Find a suitable network from available_networks
    # 3. Create the SubnetAllocation
    # 4. Update available_networks with remaining space
    
    # ─── YOUR CODE HERE ───
    for dept in sorted_depts:
        # Step 1: Calculate required prefix
        required_prefix = calculate_required_prefix(dept.required_hosts)
        
        if required_prefix is None:
            raise ValueError(f"Could not calculate prefix for {dept.name}")
        
        # Step 2: Find suitable network
        # Hint: Use ipaddress.IPv4Network.subnets(new_prefix=required_prefix)
        # You need to find a network in available_networks that can be split
        
        allocated = None
        new_available = []
        
        for net in available_networks:
            if allocated is None and net.prefixlen <= required_prefix:
                # This network can accommodate the department
                # Split it and take the first subnet
                subnets = list(net.subnets(new_prefix=required_prefix))
                allocated = subnets[0]
                # Add remaining subnets back to available
                new_available.extend(subnets[1:])
            else:
                new_available.append(net)
        
        if allocated is None:
            raise ValueError(f"No space for {dept.name} ({dept.required_hosts} hosts)")
        
        available_networks = new_available
        
        # Step 3: Create SubnetAllocation
        details = get_subnet_details(allocated)
        utilisation = (dept.required_hosts / details["usable_hosts"]) * 100
        
        allocation = SubnetAllocation(
            department=dept.name,
            network_address=details["network_address"],
            broadcast_address=details["broadcast_address"],
            subnet_mask=details["subnet_mask"],
            prefix_length=details["prefix_length"],
            usable_hosts=details["usable_hosts"],
            first_usable=details["first_usable"],
            last_usable=details["last_usable"],
            utilisation_percent=round(utilisation, 1)
        )
        allocations.append(allocation)
    # ─── END YOUR CODE ───
    
    return allocations


# ═══════════════════════════════════════════════════════════════════════════════
# DISPLAY_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def display_allocation_table(allocations: List[SubnetAllocation]) -> None:
    """Display allocations in a formatted table."""
    print("\n" + "=" * 90)
    print("SUBNET ALLOCATION PLAN")
    print("=" * 90)
    print(f"{'Department':<18} {'Network':<18} {'Mask':<15} {'Usable':<8} {'Range':<30} {'Util%':<6}")
    print("-" * 90)
    
    for alloc in allocations:
        range_str = f"{alloc.first_usable} - {alloc.last_usable}"
        print(f"{alloc.department:<18} {alloc.network_address:<18} {alloc.subnet_mask:<15} "
              f"{alloc.usable_hosts:<8} {range_str:<30} {alloc.utilisation_percent:<6}")
    
    print("=" * 90)


def export_to_json(allocations: List[SubnetAllocation], filename: str) -> None:
    """Export allocation plan to JSON file."""
    data = {
        "organisation_block": ORGANISATION_BLOCK,
        "allocations": [asdict(a) for a in allocations]
    }
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"\n📁 Allocation plan saved to: {filename}")


# ═══════════════════════════════════════════════════════════════════════════════
# VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
def verify_allocations(allocations: List[SubnetAllocation]) -> bool:
    """
    Verify that allocations are valid and non-overlapping.
    
    Returns:
        True if all checks pass
    """
    print("\n🔍 Verification Results:")
    all_passed = True
    
    # Check 1: All departments covered
    allocated_depts = {a.department for a in allocations}
    required_depts = {d.name for d in DEPARTMENTS}
    if allocated_depts != required_depts:
        print("   ❌ Not all departments allocated")
        all_passed = False
    else:
        print("   ✅ All departments have allocations")
    
    # Check 2: No overlapping subnets
    networks = [ipaddress.IPv4Network(f"{a.network_address}/{a.prefix_length}") 
                for a in allocations]
    
    overlaps = False
    for i, net1 in enumerate(networks):
        for j, net2 in enumerate(networks):
            if i < j and net1.overlaps(net2):
                print(f"   ❌ Overlap: {net1} and {net2}")
                overlaps = True
                all_passed = False
    
    if not overlaps:
        print("   ✅ No overlapping subnets")
    
    # Check 3: All within parent block
    parent = ipaddress.IPv4Network(ORGANISATION_BLOCK)
    for alloc in allocations:
        net = ipaddress.IPv4Network(f"{alloc.network_address}/{alloc.prefix_length}")
        if not net.subnet_of(parent):
            print(f"   ❌ {alloc.department} outside parent block")
            all_passed = False
    
    if all_passed:
        print("   ✅ All subnets within organisation block")
    
    # Check 4: Sufficient hosts
    for alloc in allocations:
        dept = next(d for d in DEPARTMENTS if d.name == alloc.department)
        if alloc.usable_hosts < dept.required_hosts:
            print(f"   ❌ {alloc.department}: insufficient hosts "
                  f"({alloc.usable_hosts} < {dept.required_hosts})")
            all_passed = False
    
    if all_passed:
        print("   ✅ All departments have sufficient hosts")
    
    return all_passed


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Main entry point for Homework 5.1."""
    print("=" * 70)
    print("Homework 5.1: Subnet Design for an Organisation")
    print("Computer Networks - Week 5 | ASE Bucharest, CSIE")
    print("=" * 70)
    
    print(f"\nOrganisation Block: {ORGANISATION_BLOCK}")
    print(f"Departments to allocate: {len(DEPARTMENTS)}")
    
    # Prediction prompt
    total_hosts = sum(d.required_hosts for d in DEPARTMENTS)
    prompt_prediction(
        f"The total hosts needed is {total_hosts}. A /24 has 254 usable hosts.\n"
        "   Will all departments fit? How much address space will be wasted?"
    )
    
    try:
        # Perform allocation
        allocations = allocate_subnets(ORGANISATION_BLOCK, DEPARTMENTS)
        
        # Display results
        display_allocation_table(allocations)
        
        # Verify
        if verify_allocations(allocations):
            print("\n✅ All verification checks passed!")
            
            # Export to JSON
            export_to_json(allocations, "subnet_plan.json")
            
            # Calculate total utilisation
            total_allocated = sum(a.usable_hosts for a in allocations)
            total_required = sum(d.required_hosts for d in DEPARTMENTS)
            overall_util = (total_required / total_allocated) * 100
            
            print(f"\n📊 Summary Statistics:")
            print(f"   Total hosts required: {total_required}")
            print(f"   Total hosts allocated: {total_allocated}")
            print(f"   Overall utilisation: {overall_util:.1f}%")
            print(f"   Wasted addresses: {total_allocated - total_required}")
            
            return 0
        else:
            print("\n❌ Verification failed. Review your implementation.")
            return 1
            
    except ValueError as e:
        print(f"\n❌ Allocation failed: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
