# Week 6: Troubleshooting Guide

> NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

## Before You Debug: The Prediction Method

I recommend writing your prediction on paper before running any command — it forces clarity.

Before examining troubleshooting, answer these three questions:

1. **What did I expect to happen?**
2. **What actually happened?**
3. **What's the difference?**

This simple framework prevents wasted time fixing the wrong problem.

---

## Docker Issues

### Docker Desktop Not Starting

**Symptoms:** Docker commands hang or fail with connection errors.

**Diagnostic questions:**
- Is Docker Desktop running? (Check system tray)
- Is WSL2 integration enabled?

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

---

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

**Diagnostic checklist:**
- [ ] Is the controller process running?
- [ ] Is port 6633 listening?
- [ ] Is the switch configured with correct controller IP?

**Solutions:**
1. Verify controller is running:
   ```bash
   ss -ltn | grep 6633
   ```
2. Check OVS configuration:
   ```bash
   ovs-vsctl show
   # Look for "is_connected: true"
   ```
3. Verify controller IP in topology matches actual controller
4. Check firewall rules aren't blocking port 6633

### Ping Very Slow or Timing Out

**Symptoms:** First pings take several seconds, subsequent pings fail.

💭 **Prediction check:** How many flow rules do you expect to see?

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

---

## NAT Issues

### NAT Not Translating Packets

**Symptoms:** Private hosts cannot reach public hosts.

💭 **Prediction check:** What source IP should the public host see?

**Diagnostic decision tree:**
```
Is IP forwarding enabled?
├── No → Enable it (see below)
└── Yes → Is MASQUERADE rule present?
    ├── No → Add the rule (see below)
    └── Yes → Are FORWARD rules correct?
        ├── No → Add FORWARD rules
        └── Yes → Check routing on private hosts
```

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

### Return Traffic Not Working

**Symptoms:** Outbound packets leave but responses don't arrive.

⚠️ **Common misconception:** "NAT is stateless." Actually, NAT requires the conntrack table to work.

**Solutions:**
1. Check conntrack entry exists:
   ```bash
   conntrack -L | grep <destination_ip>
   ```
2. Verify FORWARD rule for ESTABLISHED,RELATED:
   ```bash
   iptables -L FORWARD -n -v | grep ESTABLISHED
   ```

---

## SDN Issues

### Controller Not Receiving Packet-In Events

**Symptoms:** Flow table shows only table-miss rule, no traffic-specific flows.

💭 **Prediction check:** After a ping, how many new flows should appear?

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
   python3 src/exercises/ex_6_02_sdn_topology.py --cli --install-flows
   ```
3. Or install older os-ken version:
   ```bash
   pip install "os-ken<4.0.0"
   ```

### Flows Not Matching Traffic

**Symptoms:** Flow exists but traffic isn't matching it.

⚠️ **Common misconception:** "Higher priority number = less important." In OpenFlow, **higher priority = more important**.

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

### Traffic Blocked Unexpectedly

**Symptoms:** Ping or connection fails when it should work.

**Diagnostic steps:**
1. List all flows sorted by priority:
   ```bash
   ovs-ofctl -O OpenFlow13 dump-flows s1 --rsort=priority
   ```
2. Find which rule matches your traffic (check from highest priority down)
3. Look for drop rules that might be matching

---

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

---

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

---

## Quick Diagnostic Commands

| Issue | Command | What to look for |
|-------|---------|------------------|
| Docker running? | `docker info` | No errors |
| IP forwarding? | `sysctl net.ipv4.ip_forward` | Value = 1 |
| NAT rules? | `iptables -t nat -L -n` | MASQUERADE rule present |
| Conntrack? | `conntrack -L` | Entries for your connections |
| Controller up? | `ss -ltn \| grep 6633` | LISTEN state |
| Switch connected? | `ovs-vsctl show` | is_connected: true |
| Flows installed? | `ovs-ofctl dump-flows s1` | Your expected rules |

---

## Getting Help

If you encounter issues not covered here:

1. Check the error message carefully — it often tells you exactly what's wrong
2. Consult `docs/misconceptions.md` — you might have a wrong assumption
3. Review the logs:
   ```bash
   docker compose logs
   journalctl -u openvswitch-switch
   ```
4. Ask during laboratory hours with:
   - The exact error message
   - What you expected vs what happened
   - What you've already tried

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
