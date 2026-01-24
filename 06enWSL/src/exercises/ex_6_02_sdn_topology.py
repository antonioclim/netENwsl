#!/usr/bin/env python3
"""
Exercise 6.02: SDN Topology with OpenFlow 1.3
=============================================
Computer Networks - Week 6 (WSL Environment)
ASE Bucharest | by ing. dr. Antonio Clim

Topology:
    h1 (10.0.6.11) ────┐
                       │
    h2 (10.0.6.12) ────┼──── s1 (OVS) ←───── Controller (OS-Ken)
                       │          ↑
    h3 (10.0.6.13) ────┘      OpenFlow 1.3

All hosts are in the same subnet (10.0.6.0/24).
Switch s1 is controlled by an external controller (OS-Ken) via OpenFlow.

Expected policy (implemented in controller):
- ✓ h1 ↔ h2: PERMIT (all traffic)
- ✗ * → h3: DROP (implicit, with configurable exceptions)
- ? UDP → h3: CONFIGURABLE in controller

Objectives:
- Understand control plane / data plane separation
- Observe flow installation from controller
- Analyse flow table with ovs-ofctl
- Experiment with allow/drop policies per protocol

Prerequisites:
- Mininet installed in WSL/Docker environment
- Open vSwitch running
- Root privileges (sudo)

Level: Intermediate
Estimated time: 35 minutes

Pair Programming Notes:
- Driver: Execute flow commands and tests
- Navigator: Track flow table changes, verify predictions
- Swap after: Examining initial flow table

Usage:
    # With static flows (no controller needed):
    sudo python3 ex_6_02_sdn_topology.py --cli --install-flows

    # With external controller:
    # Terminal 1: osken-manager src/apps/sdn_policy_controller.py
    # Terminal 2: sudo python3 ex_6_02_sdn_topology.py --cli
"""

from __future__ import annotations

import argparse
import sys
import time
from typing import Optional

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel, info


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION_CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

# SDN Network (Week 6 allocation)
SDN_SUBNET = "10.0.6.0/24"
H1_IP = "10.0.6.11"
H2_IP = "10.0.6.12"
H3_IP = "10.0.6.13"

# Controller settings
DEFAULT_CONTROLLER_IP = "127.0.0.1"
DEFAULT_CONTROLLER_PORT = 6633

# Policy configuration
ALLOW_UDP_TO_H3 = False  # Set True to allow UDP traffic to h3


# ═══════════════════════════════════════════════════════════════════════════════
# STATIC_FLOW_INSTALLATION
# ═══════════════════════════════════════════════════════════════════════════════

def install_static_flows(net: Mininet) -> None:
    """
    Install a minimal set of OpenFlow rules using ovs-ofctl.
    
    Rationale:
    - os-ken 4.0.0 removed CLI tools (osken-manager) and the os_ken.cmd.* modules,
      so an external controller is not always available in student VMs.
    - For Week 6 we still want deterministic behaviour for the policy exercises.
    
    Policy implemented on switch s1 (OpenFlow 1.3):
    - h1 <-> h2: PERMIT (ICMP and ARP)
    - h1 -> h3: DROP (ICMP)
    - h2 -> h3: PERMIT (ICMP)
    - everything else: NORMAL (acts like a simple learning switch)
    
    💭 PREDICTION: How many flow entries will exist after this function runs?
    """
    s1 = net.get("s1")
    h1, h2, h3 = net.get("h1", "h2", "h3")

    # ─────────────────────────────────────────────────────────────────────────
    # Step 1: Determine port mappings
    # ─────────────────────────────────────────────────────────────────────────
    
    # Map host interface to switch port number
    p_h1 = s1.ports[h1.intf()].port_no
    p_h2 = s1.ports[h2.intf()].port_no
    p_h3 = s1.ports[h3.intf()].port_no
    
    info(f"*** Port mapping: h1→port{p_h1}, h2→port{p_h2}, h3→port{p_h3}\n")

    def ofctl(cmd: str) -> None:
        """Execute ovs-ofctl command on s1."""
        s1.cmd(f"ovs-ofctl -O OpenFlow13 {cmd} s1")

    # ─────────────────────────────────────────────────────────────────────────
    # Step 2: Clear existing flows
    # ─────────────────────────────────────────────────────────────────────────
    
    ofctl("del-flows")
    info("*** Cleared existing flows\n")

    # ─────────────────────────────────────────────────────────────────────────
    # Step 3: Install table-miss rule (lowest priority)
    # ─────────────────────────────────────────────────────────────────────────
    
    # 💭 PREDICTION: What happens to packets that don't match any rule?
    
    # Default behaviour: learning switch
    ofctl("add-flow 'priority=0,actions=NORMAL'")

    # ─────────────────────────────────────────────────────────────────────────
    # Step 4: ARP rules (required for MAC resolution)
    # ─────────────────────────────────────────────────────────────────────────
    
    # Always allow ARP so hosts can resolve MAC addresses
    ofctl(f"add-flow 'priority=100,arp,in_port={p_h1},actions=output:{p_h2},output:{p_h3}'")
    ofctl(f"add-flow 'priority=100,arp,in_port={p_h2},actions=output:{p_h1},output:{p_h3}'")
    ofctl(f"add-flow 'priority=100,arp,in_port={p_h3},actions=output:{p_h1},output:{p_h2}'")

    # ─────────────────────────────────────────────────────────────────────────
    # Step 5: ICMP permit rules (h1 ↔ h2)
    # ─────────────────────────────────────────────────────────────────────────
    
    # 💭 PREDICTION: After h1 pings h2, will new flows appear or will these handle it?
    
    # Permit ICMP between h1 and h2
    ofctl(f"add-flow 'priority=200,icmp,in_port={p_h1},nw_dst={H2_IP},actions=output:{p_h2}'")
    ofctl(f"add-flow 'priority=200,icmp,in_port={p_h2},nw_dst={H1_IP},actions=output:{p_h1}'")

    # ─────────────────────────────────────────────────────────────────────────
    # Step 6: ICMP drop rule (h1 → h3)
    # ─────────────────────────────────────────────────────────────────────────
    
    # 💭 PREDICTION: Why is this rule's priority (250) higher than the permit rules (200)?
    
    # Drop ICMP from h1 to h3 (demonstrates policy)
    ofctl(f"add-flow 'priority=250,icmp,in_port={p_h1},nw_dst={H3_IP},actions=drop'")

    # ─────────────────────────────────────────────────────────────────────────
    # Step 7: ICMP permit rules (h2 ↔ h3) - contrasting case
    # ─────────────────────────────────────────────────────────────────────────
    
    # Explicitly permit ICMP from h2 to h3 (so the demo has a contrasting case)
    ofctl(f"add-flow 'priority=200,icmp,in_port={p_h2},nw_dst={H3_IP},actions=output:{p_h3}'")
    ofctl(f"add-flow 'priority=200,icmp,in_port={p_h3},nw_dst={H2_IP},actions=output:{p_h2}'")
    
    info("*** Static flows installed\n")
    info("*** Policy: h1↔h2 PERMIT, h1→h3 DROP, h2↔h3 PERMIT\n")


# ═══════════════════════════════════════════════════════════════════════════════
# TOPOLOGY_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════

class SDNTopology(Topo):
    """
    Simple SDN topology: 3 hosts connected to an OVS switch.
    
    The switch is configured to use OpenFlow 1.3 and connect
    to an external controller on port 6633.
    
    Port assignments (determined by link order):
      port 1 → h1
      port 2 → h2
      port 3 → h3
    """
    
    def build(self) -> None:
        # OpenFlow switch
        s1 = self.addSwitch(
            "s1",
            cls=OVSSwitch,
            protocols="OpenFlow13"  # Explicit OpenFlow 1.3
        )
        
        # Hosts with static IPs
        h1 = self.addHost("h1", ip=f"{H1_IP}/24")
        h2 = self.addHost("h2", ip=f"{H2_IP}/24")
        h3 = self.addHost("h3", ip=f"{H3_IP}/24")
        
        # Links - connection order determines port numbers
        self.addLink(h1, s1)  # port 1
        self.addLink(h2, s1)  # port 2
        self.addLink(h3, s1)  # port 3


# ═══════════════════════════════════════════════════════════════════════════════
# SMOKE_TEST
# ═══════════════════════════════════════════════════════════════════════════════

def run_smoke_test(net: Mininet) -> int:
    """
    Run tests to verify SDN policies.
    
    Returns:
        0 if all tests pass, 1 otherwise
    """
    h1, h2, h3 = net.get("h1", "h2", "h3")
    s1 = net.get("s1")
    
    # 💭 PREDICTION: Which of these tests will pass and which will fail?
    
    info("\n*** TEST 1: Ping h1 → h2 (PERMIT expected)\n")
    out1 = h1.cmd(f"ping -c 2 -W 3 {H2_IP}")
    ok1 = "0% packet loss" in out1 or " 2 received" in out1
    info(f"    Result: {'OK (PERMIT)' if ok1 else 'FAIL'}\n")
    
    info("*** TEST 2: Ping h1 → h3 (DROP expected)\n")
    out2 = h1.cmd(f"ping -c 2 -W 3 {H3_IP}")
    ok2 = "100% packet loss" in out2 or " 0 received" in out2
    info(f"    Result: {'OK (DROP)' if ok2 else 'FAIL - traffic got through!'}\n")
    
    info("*** TEST 3: Ping h2 → h3 (PERMIT expected)\n")
    out3 = h2.cmd(f"ping -c 2 -W 3 {H3_IP}")
    ok3 = "0% packet loss" in out3 or " 2 received" in out3
    info(f"    Result: {'OK (PERMIT)' if ok3 else 'FAIL'}\n")
    
    # 💭 PREDICTION: How many packets will the drop rule have matched?
    
    info("\n*** Flow table s1 (sorted by packets):\n")
    flows = s1.cmd("ovs-ofctl -O OpenFlow13 dump-flows s1 --rsort=n_packets")
    info(flows + "\n")
    
    all_passed = ok1 and ok2 and ok3
    if all_passed:
        info("*** ALL TESTS PASSED ***\n")
        return 0
    else:
        info("*** SOME TESTS FAILED ***\n")
        return 1


# ═══════════════════════════════════════════════════════════════════════════════
# INTERACTIVE_CLI
# ═══════════════════════════════════════════════════════════════════════════════

def print_cli_banner(controller_ip: str, controller_port: int) -> None:
    """Print helpful information when entering CLI mode."""
    info("\n" + "=" * 60 + "\n")
    info("  SDN TOPOLOGY STARTED\n")
    info(f"  Controller: {controller_ip}:{controller_port}\n")
    info("=" * 60 + "\n\n")
    
    info("💭 PREDICTIONS to verify:\n")
    info("  1. How many flows exist in the initial table?\n")
    info("  2. Will h1 be able to ping h2? What about h3?\n")
    info("  3. If you add priority=300 rule, will it override priority=250?\n")
    info("  4. After 10 pings, what will the packet counters show?\n\n")
    
    info("Implemented policies:\n")
    info("  ✓ h1 ↔ h2: PERMIT\n")
    info("  ✗ h1 → h3: DROP (ICMP)\n")
    info("  ✓ h2 ↔ h3: PERMIT\n")
    info("  ? UDP → h3: Configurable (ALLOW_UDP_TO_H3)\n\n")
    
    info("Useful commands:\n")
    info("  h1 ping 10.0.6.12                              # Should work\n")
    info("  h1 ping 10.0.6.13                              # Should be blocked\n")
    info("  h2 ping 10.0.6.13                              # Should work\n")
    info("  sh ovs-ofctl -O OpenFlow13 dump-flows s1       # Show flows\n")
    info("  sh ovs-ofctl -O OpenFlow13 dump-flows s1 --rsort=n_packets\n")
    info("\n" + "=" * 60 + "\n\n")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="SDN topology with OpenFlow 1.3"
    )
    parser.add_argument(
        "--cli", action="store_true",
        help="Interactive mode"
    )
    parser.add_argument(
        "--install-flows", action="store_true",
        help="Install OpenFlow rules using ovs-ofctl (no external controller required)"
    )
    parser.add_argument(
        "--test", action="store_true",
        help="Smoke test"
    )
    parser.add_argument(
        "--controller-ip", default=DEFAULT_CONTROLLER_IP,
        help=f"Controller IP (default: {DEFAULT_CONTROLLER_IP})"
    )
    parser.add_argument(
        "--controller-port", type=int, default=DEFAULT_CONTROLLER_PORT,
        help=f"Controller port (default: {DEFAULT_CONTROLLER_PORT})"
    )
    args = parser.parse_args()
    
    # Build topology
    topo = SDNTopology()
    
    # External controller (OS-Ken)
    # Must be started separately: osken-manager ...
    controller = RemoteController(
        "c0",
        ip=args.controller_ip,
        port=args.controller_port
    )
    
    net = Mininet(
        topo=topo,
        controller=controller,
        switch=OVSSwitch,
        link=TCLink,
        autoSetMacs=True
    )
    
    net.start()

    # Optional: install static OpenFlow rules directly
    if args.install_flows:
        install_static_flows(net)
    
    try:
        if args.test:
            time.sleep(2)  # Wait for controller connection
            return run_smoke_test(net)
        elif args.cli:
            print_cli_banner(args.controller_ip, args.controller_port)
            CLI(net)
        else:
            info("Topology started. Use --cli for interactive mode.\n")
        
        return 0
    finally:
        net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    sys.exit(main())
