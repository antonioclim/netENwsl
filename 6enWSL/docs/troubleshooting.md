# Week 6: Troubleshooting Guide

> NETWORKING class - ASE, Informatics | by Revolvix

## Docker Issues

### Docker Desktop Not Starting

**Symptoms:** Docker commands hang or fail with connection errors.

**Solutions:**
1. Ensure Docker Desktop is running (check system tray)
2. Restart Docker Desktop
3. Check WSL2 integration is enabled:
   - Docker Desktop → Settings → Resources → WSL Integration
   - Enable integration with your Ubuntu distribution

### Privileged Container Errors

**Symptoms:** Container fails to start with permission errors.

**Solutions:**
1. Ensure Docker Desktop is configured for privileged containers
2. On Windows, restart Docker Desktop with administrator privileges
3. Verify in docker-compose.yml that `privileged: true` is set

### Network Mode Host Not Working

**Symptoms:** Containers can't access host network or Mininet fails.

**Solutions:**
1. On Docker Desktop for Windows/Mac, host networking is limited
2. Use the provided Docker container which is configured correctly
3. For full functionality, use native Linux or a Linux VM

## Mininet Issues

### "File exists" Error on Startup

**Symptoms:** Mininet fails to start with messages about existing interfaces.

**Solutions:**
```bash
# Clean up Mininet state
sudo mn -c

# If that fails, manually remove interfaces
sudo ip link delete s1-eth1 2>/dev/null
sudo ip link delete s1-eth2 2>/dev/null

# Kill any orphaned processes
sudo pkill -9 ovs
sudo pkill -9 controller
```

### "OVS switch failed to connect"

**Symptoms:** SDN topology shows switches but controller connection fails.

**Solutions:**
1. Verify controller is running:
   ```bash
   ss -ltn | grep 6633
   ```
2. Check OVS configuration:
   ```bash
   ovs-vsctl show
   ```
3. Verify controller IP in topology matches actual controller
4. Check firewall rules aren't blocking port 6633

### Ping Very Slow or Timing Out

**Symptoms:** First pings take several seconds, subsequent pings fail.

**Solutions:**
1. For SDN topology, check flow rules are installed:
   ```bash
   ovs-ofctl -O OpenFlow13 dump-flows s1
   ```
2. Ensure ARP is working (flows should exist for ARP)
3. Check that controller is processing packet-in events
4. Try using `--install-flows` flag for static flows

### "mn: command not found"

**Symptoms:** Mininet is not installed.

**Solutions:**
```bash
# Install Mininet
sudo apt-get update
sudo apt-get install -y mininet openvswitch-switch

# Verify installation
mn --version
```

## NAT Issues

### NAT Not Translating Packets

**Symptoms:** Private hosts cannot reach public hosts.

**Solutions:**
1. Verify IP forwarding is enabled:
   ```bash
   sysctl net.ipv4.ip_forward
   # If 0, enable it:
   sudo sysctl -w net.ipv4.ip_forward=1
   ```

2. Check MASQUERADE rule exists:
   ```bash
   iptables -t nat -L -n -v | grep MASQUERADE
   ```

3. Verify routing on private hosts:
   ```bash
   ip route
   # Should have default via NAT router
   ```

4. Check interface names match iptables rules

### Conntrack Table Full

**Symptoms:** New connections fail, existing connections work.

**Solutions:**
```bash
# Check current connections
conntrack -C

# Increase conntrack limit
sudo sysctl -w net.netfilter.nf_conntrack_max=131072
```

## SDN Issues

### Controller Not Receiving Packet-In Events

**Symptoms:** Flow table shows only table-miss rule, no traffic-specific flows.

**Solutions:**
1. Verify switch is connected to controller:
   ```bash
   ovs-vsctl show
   # Look for "is_connected: true"
   ```

2. Check OpenFlow version matches:
   ```bash
   ovs-vsctl get bridge s1 protocols
   # Should show OpenFlow13
   ```

3. Ensure table-miss rule sends to controller:
   ```bash
   ovs-ofctl -O OpenFlow13 dump-flows s1
   # Should have: actions=CONTROLLER
   ```

### os-ken / osken-manager Not Found

**Symptoms:** `osken-manager: command not found`

**Solutions:**
1. os-ken 4.0.0+ removed CLI tools
2. Use static flow installation instead:
   ```bash
   python3 topo_sdn.py --cli --install-flows
   ```
3. Or install older os-ken version:
   ```bash
   pip install "os-ken<4.0.0"
   ```

### Flows Not Matching Traffic

**Symptoms:** Flow exists but traffic isn't matching it.

**Solutions:**
1. Check match criteria exactly matches traffic:
   - Verify IP addresses, ports, protocols
   - Check priority (higher priority matches first)

2. Use flow statistics to debug:
   ```bash
   ovs-ofctl -O OpenFlow13 dump-flows s1 --rsort=n_packets
   ```

3. Verify packet is reaching the switch:
   ```bash
   tcpdump -i s1-eth1 -n
   ```

## WSL2 Issues

### WSL2 Performance Issues

**Symptoms:** Commands are slow, network latency is high.

**Solutions:**
1. Ensure using WSL2, not WSL1:
   ```powershell
   wsl --list --verbose
   ```

2. If using WSL1, convert:
   ```powershell
   wsl --set-version Ubuntu 2
   ```

3. Allocate more resources in `.wslconfig`:
   ```ini
   [wsl2]
   memory=8GB
   processors=4
   ```

### Network Connectivity from WSL2

**Symptoms:** Can't reach Docker containers from WSL2.

**Solutions:**
1. Use localhost instead of container IP
2. Ensure Docker Desktop WSL integration is enabled
3. Check Windows Firewall isn't blocking

## Python Issues

### Module Import Errors

**Symptoms:** `ModuleNotFoundError: No module named 'os_ken'`

**Solutions:**
```bash
pip install --break-system-packages os-ken scapy requests pyyaml docker
```

### Mininet Python API Not Found

**Symptoms:** `ModuleNotFoundError: No module named 'mininet'`

**Solutions:**
```bash
# Mininet Python API comes with Mininet installation
sudo apt-get install mininet

# The Python module is installed globally by apt, not pip
```

## Getting Help

If you encounter issues not covered here:

1. Check the error message carefully
2. Search the course forums
3. Review the logs:
   ```bash
   docker compose logs
   journalctl -u openvswitch-switch
   ```
4. Ask during laboratory hours

---

*NETWORKING class - ASE, Informatics | by Revolvix*
