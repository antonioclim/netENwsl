# 🧩 Parsons Problems — Week 6

## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> Reorder the code blocks or commands to create a working solution. Some blocks may be distractors (not needed).

---

## Problem P1: Configure NAT with iptables

### Task

Arrange these commands in the correct order to configure NAT/MASQUERADE on a Linux router. The router has two interfaces:
- `eth0`: Connected to private network (192.168.1.0/24)
- `eth1`: Connected to public network (has public IP)

### Scrambled Blocks

```bash
# Block A
iptables -A FORWARD -i eth1 -o eth0 -m state --state ESTABLISHED,RELATED -j ACCEPT

# Block B
sysctl -w net.ipv4.ip_forward=1

# Block C
iptables -t nat -A POSTROUTING -o eth1 -s 192.168.1.0/24 -j MASQUERADE

# Block D
iptables -A FORWARD -i eth0 -o eth1 -j ACCEPT

# Block E (DISTRACTOR - not needed for basic NAT)
iptables -t nat -A PREROUTING -i eth1 -p tcp --dport 80 -j DNAT --to 192.168.1.10

# Block F (DISTRACTOR - wrong interface)
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
```

### Correct Order

<details>
<summary>Click to reveal</summary>

```bash
# Block B - Enable IP forwarding first
sysctl -w net.ipv4.ip_forward=1

# Block D - Allow forwarding from private to public
iptables -A FORWARD -i eth0 -o eth1 -j ACCEPT

# Block A - Allow return traffic (established connections)
iptables -A FORWARD -i eth1 -o eth0 -m state --state ESTABLISHED,RELATED -j ACCEPT

# Block C - Enable MASQUERADE on outbound interface
iptables -t nat -A POSTROUTING -o eth1 -s 192.168.1.0/24 -j MASQUERADE
```

**Why this order:**
1. IP forwarding must be enabled before the router will forward packets
2. FORWARD rules determine what traffic can pass through
3. MASQUERADE rule rewrites the source address

**Distractors:**
- Block E: DNAT rule for port forwarding — not needed for outbound NAT
- Block F: MASQUERADE on eth0 — wrong! Should be on the public interface (eth1)

</details>

---

## Problem P2: Install SDN Flow Rules

### Task

Arrange these commands to implement a policy that:
1. Allows all traffic between h1 (10.0.6.11) and h2 (10.0.6.12)
2. Blocks all traffic to h3 (10.0.6.13)
3. Has a table-miss rule that sends unknowns to the controller

### Scrambled Blocks

```bash
# Block A
ovs-ofctl -O OpenFlow13 add-flow s1 "priority=0,actions=CONTROLLER"

# Block B
ovs-ofctl -O OpenFlow13 add-flow s1 "priority=100,ip,nw_src=10.0.6.11,nw_dst=10.0.6.12,actions=output:2"

# Block C
ovs-ofctl -O OpenFlow13 add-flow s1 "priority=50,ip,nw_dst=10.0.6.13,actions=drop"

# Block D
ovs-ofctl -O OpenFlow13 add-flow s1 "priority=100,ip,nw_src=10.0.6.12,nw_dst=10.0.6.11,actions=output:1"

# Block E (DISTRACTOR - wrong priority order)
ovs-ofctl -O OpenFlow13 add-flow s1 "priority=200,ip,nw_dst=10.0.6.13,actions=drop"

# Block F
ovs-ofctl -O OpenFlow13 del-flows s1
```

### Correct Order

<details>
<summary>Click to reveal</summary>

```bash
# Block F - Clear existing flows first
ovs-ofctl -O OpenFlow13 del-flows s1

# Block A - Install table-miss rule (lowest priority)
ovs-ofctl -O OpenFlow13 add-flow s1 "priority=0,actions=CONTROLLER"

# Block C - Block traffic to h3 (medium priority)
ovs-ofctl -O OpenFlow13 add-flow s1 "priority=50,ip,nw_dst=10.0.6.13,actions=drop"

# Block B - Allow h1 → h2 (higher priority than block rule)
ovs-ofctl -O OpenFlow13 add-flow s1 "priority=100,ip,nw_src=10.0.6.11,nw_dst=10.0.6.12,actions=output:2"

# Block D - Allow h2 → h1 (bidirectional communication)
ovs-ofctl -O OpenFlow13 add-flow s1 "priority=100,ip,nw_src=10.0.6.12,nw_dst=10.0.6.11,actions=output:1"
```

**Why this order:**
1. Clear flows first to start fresh
2. Table-miss goes in as foundation (priority=0)
3. Block rule for h3 at priority=50
4. Allow rules at priority=100 (higher than block, so h1↔h2 works)

**Distractor:**
- Block E: Priority=200 for blocking h3 would override permit rules if we later wanted to allow specific traffic to h3. Using lower priority (50) for blocks allows higher-priority exceptions.

**Priority reasoning:**
- priority=0: Default/fallback
- priority=50: General block rules
- priority=100: Specific permit rules
- Higher numbers = checked first

</details>

---

## Problem P3: SDN Controller Packet-In Handler

### Task

Arrange these Python code blocks to create a basic SDN controller packet-in handler that:
1. Learns the source MAC address
2. Looks up the destination MAC
3. Either floods (unknown) or forwards (known)

### Scrambled Blocks

```python
# Block A
out_port = self.mac_to_port.get(dpid, {}).get(dst_mac, ofproto.OFPP_FLOOD)

# Block B
def on_packet_in(self, ev):
    msg = ev.msg
    datapath = msg.datapath
    ofproto = datapath.ofproto
    parser = datapath.ofproto_parser
    dpid = datapath.id
    in_port = msg.match["in_port"]

# Block C
actions = [parser.OFPActionOutput(out_port)]
out = parser.OFPPacketOut(
    datapath=datapath,
    buffer_id=ofproto.OFP_NO_BUFFER,
    in_port=in_port,
    actions=actions,
    data=msg.data
)
datapath.send_msg(out)

# Block D
pkt = packet.Packet(msg.data)
eth = pkt.get_protocols(ethernet.ethernet)[0]
src_mac = eth.src
dst_mac = eth.dst

# Block E
self.mac_to_port.setdefault(dpid, {})
self.mac_to_port[dpid][src_mac] = in_port

# Block F (DISTRACTOR - wrong: installs flow for every packet including floods)
match = parser.OFPMatch(eth_dst=dst_mac)
self._add_flow(datapath, 1, match, actions)
```

### Correct Order

<details>
<summary>Click to reveal</summary>

```python
# Block B - Function signature and extract event data
def on_packet_in(self, ev):
    msg = ev.msg
    datapath = msg.datapath
    ofproto = datapath.ofproto
    parser = datapath.ofproto_parser
    dpid = datapath.id
    in_port = msg.match["in_port"]

# Block D - Parse packet to get MAC addresses
pkt = packet.Packet(msg.data)
eth = pkt.get_protocols(ethernet.ethernet)[0]
src_mac = eth.src
dst_mac = eth.dst

# Block E - Learn source MAC → port mapping
self.mac_to_port.setdefault(dpid, {})
self.mac_to_port[dpid][src_mac] = in_port

# Block A - Look up destination, flood if unknown
out_port = self.mac_to_port.get(dpid, {}).get(dst_mac, ofproto.OFPP_FLOOD)

# Block C - Send the packet
actions = [parser.OFPActionOutput(out_port)]
out = parser.OFPPacketOut(
    datapath=datapath,
    buffer_id=ofproto.OFP_NO_BUFFER,
    in_port=in_port,
    actions=actions,
    data=msg.data
)
datapath.send_msg(out)
```

**Why this order:**
1. Extract message data from event
2. Parse the packet to read headers
3. Learn where the source MAC is (update table)
4. Decide where to send (lookup destination)
5. Actually send the packet

**Distractor:**
- Block F: Installing a flow for every packet would create flows for flood actions, which is incorrect. Flows should only be installed when we know the specific output port.

</details>

---

## Bonus Challenge: Complete the Handler

Extend the handler from P3 to also install a flow when the destination is known (not flooding).

<details>
<summary>Hint</summary>

Add this between Block A and Block C:

```python
# Only install flow if we know the destination (not flooding)
if out_port != ofproto.OFPP_FLOOD:
    match = parser.OFPMatch(in_port=in_port, eth_dst=dst_mac)
    self._add_flow(datapath, priority=1, match=match, actions=actions)
```

</details>

---

## Self-Assessment

After completing these problems, you should be able to:

- [ ] Configure NAT on a Linux router in the correct order
- [ ] Design SDN flow rules with appropriate priorities
- [ ] Implement basic packet-in handling logic
- [ ] Distinguish between necessary steps and distractors

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
