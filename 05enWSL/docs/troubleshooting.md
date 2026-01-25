# Troubleshooting Guide

> Week 5 - NETWORKING class - ASE, Informatics
>
> by ing. dr. Antonio Clim

## Docker Issues

In previous cohorts, roughly 70% of issues came from Docker not running or ports being in use. Check those first before diving deeper.


### Docker Desktop Not Running

**Symptoms:**
- `docker info` returns an error
- Scripts fail with "Cannot connect to Docker daemon"

**Solutions:**
1. Start Docker Desktop from the Start menu (Windows) or Applications (macOS)
2. Wait 30-60 seconds for Docker to fully initialise
3. Verify with `docker info`

### WSL2 Backend Not Enabled (Windows)

**Symptoms:**
- Docker runs but containers are slow
- Network connectivity issues between containers

**Solutions:**
1. Open Docker Desktop settings
2. Go to General tab
3. Enable "Use the WSL 2 based engine"
4. Apply and restart Docker

### Port Already in Use

**Symptoms:**
- Container fails to start
- Error: "bind: address already in use"

**Solutions:**
```powershell
# Find process using the port
netstat -ano | findstr :9999

# Kill the process (Windows)
taskkill /PID <process_id> /F

# Or change the port in docker-compose.yml
```

### Container Creation Fails

**Symptoms:**
- `docker compose up` fails
- Image build errors

**Solutions:**
```powershell
# Rebuild without cache
python scripts/start_lab.py --rebuild

# Or manually
docker compose build --no-cache
docker compose up -d
```

## Network Connectivity Issues

### Containers Cannot Communicate

**Symptoms:**
- Ping between containers fails
- Applications cannot connect

**Solutions:**
1. Verify containers are on the same network:
   ```powershell
   docker network inspect week5_labnet
   ```

2. Check container IP addresses:
   ```powershell
   docker exec week5_python ip addr
   ```

3. Verify firewall isn't blocking:
   ```powershell
   # Windows Firewall may block Docker traffic
   # Try temporarily disabling or adding rules
   ```

### DNS Resolution Fails

**Symptoms:**
- Cannot resolve hostnames
- `ping google.com` fails from container

**Solutions:**
1. Check DNS configuration:
   ```bash
   docker exec week5_python cat /etc/resolv.conf
   ```

2. Try using IP addresses directly
3. Verify host machine has internet connectivity

### Cannot Access Container from Host

**Symptoms:**
- `localhost:9999` doesn't respond
- Port mapping appears correct

**Solutions:**
1. Verify port mapping:
   ```powershell
   docker ps
   # Check PORTS column
   ```

2. Test from inside container first:
   ```bash
   docker exec week5_python curl localhost:9999
   ```

3. Check if service is listening:
   ```bash
   docker exec week5_udp-server netstat -ulnp
   ```

## Python/Exercise Issues

### Module Import Errors

**Symptoms:**
- `ModuleNotFoundError: No module named 'src'`
- Import failures in exercises

**Solutions:**
1. Ensure you're running from the correct directory:
   ```powershell
   cd WEEK5_WSLkit
   ```

2. Run exercises through Docker:
   ```powershell
   docker exec week5_python python /app/src/exercises/ex_5_01_cidr_flsm.py --help
   ```

3. Check PYTHONPATH:
   ```bash
   docker exec week5_python echo $PYTHONPATH
   # Should include /app
   ```

### Exercise Output Missing Colours

**Symptoms:**
- Output shows escape codes like `[32m`
- Formatting appears broken

**Solutions:**
1. Use a terminal that supports ANSI colours
2. Run with `--json` flag for clean output
3. On Windows, use Windows Terminal instead of CMD

### Invalid IP Address Errors

**Symptoms:**
- `ValueError: invalid IP address`
- Exercises reject valid-looking addresses

**Solutions:**
1. Verify address format:
   - Include prefix for CIDR: `192.168.1.1/24`
   - Use network address for FLSM: `192.168.1.0/24`

2. Check for typos and extra spaces

3. Ensure IPv4 octets are 0-255

## Subnetting Calculation Errors

### VLSM Allocation Fails with "Insufficient Space"

**Symptoms:**
- `ValueError: Insufficient space for X hosts`
- VLSM allocation does not complete

**Solutions:**
1. Verify total requirements fit in available space:
   ```bash
   # For each requirement, calculate addresses needed
   # 60 hosts needs /26 = 64 addresses
   # 20 hosts needs /27 = 32 addresses
   # Sum must be <= available addresses
   ```

2. Check that no single requirement exceeds available space

3. Remember: VLSM sorts largest-first internally, so order of input doesn't matter

### Network Address vs Host Address Confusion

**Symptoms:**
- "Address X is the network address"
- Cannot use certain IP for hosts

**Solutions:**
1. Network address has all host bits = 0
   - For 192.168.1.0/24, the .0 is the network address
   - For 192.168.1.64/26, the .64 is the network address

2. Use the `analyse` command to check:
   ```bash
   docker exec week5_python python /app/src/exercises/ex_5_01_cidr_flsm.py analyse 192.168.1.64/26
   # Check "Address Type" field
   ```

### Wrong Broadcast Address Calculated

**Symptoms:**
- Expected .255 but got different value
- Broadcast calculations don't match

**Solutions:**
1. Broadcast is NOT always .255 - it depends on prefix:
   - /24 → broadcast is .255 (last octet all 1s)
   - /26 → broadcast is .63, .127, .191, or .255
   - /27 → broadcast is .31, .63, .95, .127, etc.

2. Formula: Broadcast = Network + Block Size - 1
   ```
   192.168.1.64/26
   Block size = 64
   Broadcast = 64 + 64 - 1 = 127 → 192.168.1.127
   ```

3. Verify with the tool:
   ```bash
   docker exec week5_python python /app/src/exercises/ex_5_01_cidr_flsm.py analyse 192.168.1.64/26 --verbose
   ```

### Subnet Boundary Miscalculation

**Symptoms:**
- FLSM subnets don't start where expected
- /20 subnet calculation seems wrong

**Solutions:**
1. Subnet boundaries must align to block size:
   - /26 (64 addresses) starts at .0, .64, .128, .192
   - /27 (32 addresses) starts at .0, .32, .64, .96...
   - /20 (4096 addresses) affects third octet!

2. For /20, third octet changes in steps of 16:
   ```
   10.0.0.0/20  → 10.0.0.0 - 10.0.15.255
   10.0.16.0/20 → 10.0.16.0 - 10.0.31.255
   ```

3. Use binary view to understand:
   ```bash
   docker exec week5_python python /app/src/exercises/ex_5_01_cidr_flsm.py analyse 172.16.45.67/20 --verbose
   ```

### Usable Hosts Calculation Wrong

**Symptoms:**
- Expected 64 hosts but got 62
- /31 shows 0 hosts (should be 2)

**Solutions:**
1. Standard formula: Usable = 2^(32-prefix) - 2
   - Subtract 2 for network and broadcast addresses
   - /26 = 64 total, 62 usable

2. Special cases:
   - /31 (RFC 3021): 2 usable hosts (point-to-point)
   - /32: 1 host (host route)

3. The tool handles these automatically - verify with:
   ```bash
   docker exec week5_python python /app/src/exercises/ex_5_01_cidr_flsm.py analyse 10.0.0.0/31
   ```

## IPv6 Common Mistakes

### Multiple :: in Address

**Symptoms:**
- `ValueError: invalid IPv6 address`
- Address like `2001:db8::1::2` rejected

**Solutions:**
1. The `::` can only appear ONCE per address
   - `::` represents one or more groups of zeros
   - Multiple `::` would be ambiguous

2. Valid: `2001:db8::1` or `2001:db8:0:0:1::2`
3. Invalid: `2001:db8::1::2`

4. If you need zeros in two places:
   ```
   Wrong:  2001:db8::85a3::7334
   Right:  2001:db8::85a3:0:0:7334
   Right:  2001:db8:0:0:0:85a3::7334
   ```

### Leading Zeros Confusion

**Symptoms:**
- Unsure if 0db8 or db8 is correct
- Address looks different after compression

**Solutions:**
1. Leading zeros CAN be omitted within each group:
   - `0db8` → `db8` ✓
   - `0001` → `1` ✓
   - `0000` → `0` ✓

2. But you cannot remove digits that matter:
   - `db80` stays `db80` (not `db8`)

3. Test compression:
   ```bash
   docker exec week5_python python /app/src/exercises/ex_5_02_vlsm_ipv6.py ipv6 2001:0db8:0000:0000:0000:0000:0000:0001
   ```

### Link-Local vs Global Address Confusion

**Symptoms:**
- Cannot reach `fe80::` address from another network
- IPv6 connectivity works locally but not remotely

**Solutions:**
1. Link-local (`fe80::/10`) addresses are NOT routable
   - Valid only on local network segment
   - Every interface has one automatically

2. Global unicast (`2000::/3`) addresses ARE routable
   - Assigned by DHCP or SLAAC
   - Required for Internet connectivity

3. Check address type:
   ```bash
   docker exec week5_python python /app/src/exercises/ex_5_02_vlsm_ipv6.py ipv6 fe80::1
   # Shows: Type = link-local
   ```

### IPv6 Subnet Size Confusion

**Symptoms:**
- Unsure what prefix to use for LANs
- Over-engineering IPv6 subnets

**Solutions:**
1. Standard LAN subnet is /64 (always!)
   - Provides 2^64 addresses per subnet
   - Required for SLAAC to work properly

2. Typical allocation:
   - ISP gives you /48 → 65,536 possible /64 subnets
   - Each LAN gets one /64

3. Don't try to "save" IPv6 addresses like IPv4
   - /64 per LAN is the standard
   - Smaller prefixes break SLAAC

## Packet Capture Issues

### tcpdump Permission Denied

**Symptoms:**
- `tcpdump: permission denied`
- Cannot capture traffic

**Solutions:**
1. Container should have NET_ADMIN capability (included in compose file)
2. If running directly, add capability:
   ```powershell
   docker run --cap-add=NET_ADMIN ...
   ```

### No Packets Captured

**Symptoms:**
- tcpdump runs but shows no output
- Capture file is empty

**Solutions:**
1. Verify interface name:
   ```bash
   docker exec week5_python ip link
   # Use correct interface (usually eth0)
   ```

2. Generate traffic while capturing:
   ```bash
   # In one terminal
   docker exec week5_python tcpdump -i eth0

   # In another terminal
   docker exec week5_python ping 10.5.0.20
   ```

3. Check filter is not too restrictive

### Wireshark Cannot Read Capture

**Symptoms:**
- Wireshark shows no packets
- File appears corrupted

**Solutions:**
1. Ensure capture completed properly (Ctrl+C to stop tcpdump)
2. Copy file from container correctly:
   ```powershell
   docker cp week5_python:/app/pcap/capture.pcap ./capture.pcap
   ```

3. Try capinfos to verify file:
   ```powershell
   capinfos capture.pcap
   ```

## Performance Issues

### Containers Start Slowly

**Symptoms:**
- `docker compose up` takes several minutes
- Timeouts during startup

**Solutions:**
1. Increase Docker Desktop resources:
   - Settings → Resources → Advanced
   - Increase memory to 4GB+
   - Increase CPUs to 2+

2. Use pre-built images when possible:
   ```powershell
   python scripts/start_lab.py
   # (without --rebuild unless necessary)
   ```

### High CPU Usage

**Symptoms:**
- System becomes slow
- Docker Desktop using excessive CPU

**Solutions:**
1. Stop unused containers:
   ```powershell
   python scripts/stop_lab.py
   ```

2. Limit container resources in docker-compose.yml:
   ```yaml
   services:
     python:
       deploy:
         resources:
           limits:
             cpus: '1.0'
             memory: 512M
   ```

## Getting Help

### Diagnostic Information

Collect this information when reporting issues:

```powershell
# Docker version
docker version

# Docker info
docker info

# Container status
docker ps -a

# Container logs
docker logs week5_python

# Network info
docker network ls
docker network inspect week5_labnet
```

### Clean Reset

If all else fails, perform a complete reset:

```powershell
# Stop everything
python scripts/stop_lab.py

# Full cleanup
python scripts/cleanup.py --full --prune

# Rebuild from scratch
python scripts/start_lab.py --rebuild
```

### Additional Resources

- See `docs/misconceptions.md` for common conceptual errors
- See `docs/glossary.md` for terminology reference
- See `docs/code_tracing.md` for algorithm understanding
