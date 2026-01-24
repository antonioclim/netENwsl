# Expected Outputs

> Week 5 Laboratory - NETWORKING class - ASE, Informatics
>
> by Revolvix

## Exercise 1: CIDR Analysis

### Input
```
python src/exercises/ex_5_01_cidr_flsm.py analyse 192.168.10.14/26
```

### Expected Output
```
═══════════════════════════════════════════════════
  IPv4 CIDR Analysis
═══════════════════════════════════════════════════

  Input:                       192.168.10.14/26
  IP Address:                  192.168.10.14
  Address Type:                HOST

  Network Address:             192.168.10.0/26
  Subnet Mask:                 255.255.255.192
  Wildcard Mask:               0.0.0.63
  Broadcast Address:           192.168.10.63

  Total Addresses:             64
  Usable Hosts:                62
  First Host:                  192.168.10.1
  Last Host:                   192.168.10.62

  Private Address:             Yes
```

## Exercise 2: FLSM Subnetting

### Input
```
python src/exercises/ex_5_01_cidr_flsm.py flsm 192.168.100.0/24 4
```

### Expected Output
```
════════════════════════════════════════════════════════════════
  FLSM Subnetting (Fixed Length Subnet Mask)
════════════════════════════════════════════════════════════════

  Base Network:                192.168.100.0/24
  Number of Subnets:           4
  Borrowed Bits:               2
  New Prefix:                  /26
  Increment:                   64 addresses

────────────────────────────────────────────────────────────────
  No.  Subnet               Broadcast          Hosts      Range
────────────────────────────────────────────────────────────────
    1. 192.168.100.0/26     192.168.100.63     62         192.168.100.1..192.168.100.62
    2. 192.168.100.64/26    192.168.100.127    62         192.168.100.65..192.168.100.126
    3. 192.168.100.128/26   192.168.100.191    62         192.168.100.129..192.168.100.190
    4. 192.168.100.192/26   192.168.100.255    62         192.168.100.193..192.168.100.254
────────────────────────────────────────────────────────────────

  Total Usable Hosts: 248
```

## Exercise 3: VLSM Allocation

### Input
```
python src/exercises/ex_5_02_vlsm_ipv6.py vlsm 172.16.0.0/24 60 20 10 2
```

### Expected Output
```
══════════════════════════════════════════════════════════════════════
  VLSM Allocation (Variable Length Subnet Mask)
══════════════════════════════════════════════════════════════════════

  Available Network:           172.16.0.0/24
  Total Addresses:             256
  Host Requirements:           60, 20, 10, 2

──────────────────────────────────────────────────────────────────────
  VLSM Algorithm:
──────────────────────────────────────────────────────────────────────
  1. Sort requirements in descending order
  2. For each requirement, calculate minimum prefix needed
  3. Align start address to block boundary
  4. Allocate and advance cursor

──────────────────────────────────────────────────────────────────────
    #  Required   Prefix  Subnet               Gateway          Efficiency
──────────────────────────────────────────────────────────────────────
    1        60  /26     172.16.0.0/26        172.16.0.1        96.8%
    2        20  /27     172.16.0.64/27       172.16.0.65       66.7%
    3        10  /28     172.16.0.96/28       172.16.0.97       71.4%
    4         2  /30     172.16.0.112/30      172.16.0.113      100.0%
──────────────────────────────────────────────────────────────────────

  Summary:
    Total hosts required:     92
    Total hosts allocated:    108
    Overall efficiency:       85.2%
    Remaining free addresses: 140
    First free address:       172.16.0.116
```

## Exercise 4: IPv6 Operations

### Input
```
python src/exercises/ex_5_02_vlsm_ipv6.py ipv6 2001:0db8:0000:0000:0000:0000:0000:0001
```

### Expected Output
```
════════════════════════════════════════════════════════════════
  IPv6 Address Analysis
════════════════════════════════════════════════════════════════

  Input:                       2001:0db8:0000:0000:0000:0000:0000:0001
  Full Form:                   2001:0db8:0000:0000:0000:0000:0000:0001
  Compressed Form:             2001:db8::1

  Address Type:                global-unicast
  Scope:                       global

────────────────────────────────────────────────────────────────
  IPv6 Compression Rules:
────────────────────────────────────────────────────────────────
  1. Remove leading zeros from each group
  2. Use :: for the longest sequence of zeros
  3. :: can only be used once
```

## Docker Container Tests

### Container IP Verification
```bash
docker exec week5_python ip addr show eth0
```

### Expected Output
```
X: eth0@ifY: <BROADCAST,MULTICAST,UP,LOWER_UP> ...
    link/ether XX:XX:XX:XX:XX:XX brd ff:ff:ff:ff:ff:ff
    inet 10.5.0.10/24 brd 10.5.0.255 scope global eth0
       valid_lft forever preferred_lft forever
```

### UDP Echo Test
```bash
docker exec week5_python python /app/src/apps/udp_echo.py client --host 10.5.0.20 --port 9999 --count 1
```

### Expected Output
```
[INFO] Starting UDP Echo client
[INFO] Sending to 10.5.0.20:9999
[INFO] Sent: Hello from UDP client
[INFO] Received echo: Hello from UDP client
```
