# Expected Outputs for Week 6 Exercises

> NETWORKING class - ASE, Informatics | by Revolvix

## Exercise 1: NAT/PAT Configuration

### Expected NAT Table Output

```
Chain PREROUTING (policy ACCEPT)
target     prot opt source               destination

Chain INPUT (policy ACCEPT)
target     prot opt source               destination

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination

Chain POSTROUTING (policy ACCEPT)
target     prot opt source               destination
MASQUERADE  all  --  192.168.1.0/24       0.0.0.0/0
```

### Expected NAT Observer Output (Server Side)

```
[NAT Observer Server]
Listening on 203.0.113.2:5000
Waiting for connections...
------------------------------------------------------------
[2025-XX-XX XX:XX:XX] Connection from 203.0.113.1:50001
            Message: Hello from h1

[2025-XX-XX XX:XX:XX] Connection from 203.0.113.1:50002
            Message: Hello from h2
```

Note: Both connections appear from 203.0.113.1 (NAT public IP) with different ports.

## Exercise 2: SDN Flow Observation

### Expected Flow Table (Initial)

```
 cookie=0x0, duration=Xs, table=0, n_packets=0, n_bytes=0, priority=0 actions=CONTROLLER:65535
```

### Expected Flow Table (After Traffic)

```
 cookie=0x0, duration=Xs, table=0, n_packets=N, n_bytes=M, priority=200,icmp,in_port=1,nw_dst=10.0.6.12 actions=output:2
 cookie=0x0, duration=Xs, table=0, n_packets=N, n_bytes=M, priority=200,icmp,in_port=2,nw_dst=10.0.6.11 actions=output:1
 cookie=0x0, duration=Xs, table=0, n_packets=N, n_bytes=M, priority=250,icmp,in_port=1,nw_dst=10.0.6.13 actions=drop
 cookie=0x0, duration=Xs, table=0, n_packets=0, n_bytes=0, priority=0 actions=CONTROLLER:65535
```

### Expected Ping Results

```
# h1 → h2 (PERMIT)
PING 10.0.6.12 (10.0.6.12) 56(84) bytes of data.
64 bytes from 10.0.6.12: icmp_seq=1 ttl=64 time=X ms
64 bytes from 10.0.6.12: icmp_seq=2 ttl=64 time=X ms
--- 10.0.6.12 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss

# h1 → h3 (DROP)
PING 10.0.6.13 (10.0.6.13) 56(84) bytes of data.
--- 10.0.6.13 ping statistics ---
2 packets transmitted, 0 received, 100% packet loss
```

## Exercise 3: Policy Modification

### Expected Output After Adding ICMP Permit Rule

```
# Add rule
sh ovs-ofctl -O OpenFlow13 add-flow s1 "priority=300,icmp,nw_src=10.0.6.11,nw_dst=10.0.6.13,actions=output:3"

# Verify ping now works
h1 ping -c 2 10.0.6.13
PING 10.0.6.13 (10.0.6.13) 56(84) bytes of data.
64 bytes from 10.0.6.13: icmp_seq=1 ttl=64 time=X ms
64 bytes from 10.0.6.13: icmp_seq=2 ttl=64 time=X ms
--- 10.0.6.13 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss
```

---

*NETWORKING class - ASE, Informatics | by Revolvix*
