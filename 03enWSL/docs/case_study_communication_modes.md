# Case Study: Choosing the Right Communication Mode

> NETWORKING class - ASE, CSIE | by ing. dr. Antonio Clim

**LO6** — Evaluate appropriateness of broadcast, multicast and unicast.

---

## Scenario 1: University Campus Video Streaming

**Context:** 10,000 students, 5 subnets, live lecture streaming

| Mode | Bandwidth | Feasibility |
|------|-----------|-------------|
| Unicast | 50 Gbps (5Mbps × 10,000) | ❌ Infeasible |
| Broadcast | Cannot cross routers | ❌ Not possible |
| **Multicast** | 5 Mbps total | ✅ Optimal |

**Decision:** IP Multicast with IGMP — single stream serves all subscribers.

---

## Scenario 2: Microservices Service Discovery

**Context:** 50 containers in single Docker network

| Approach | Complexity | Scalability |
|----------|------------|-------------|
| **Broadcast** | Low | Medium |
| Multicast | Medium | Medium |
| Service Registry | High | High |

**Decision:** Broadcast acceptable for <100 services; migrate to registry (Consul/etcd) for production scale.

---

## Scenario 3: Industrial IoT Sensor Network

**Context:** 1,000 sensors, 10 network segments, 99.9% reliability required

| Approach | Power Efficiency | Reliability |
|----------|-----------------|-------------|
| Unicast TCP | Low | High |
| Multicast UDP | Medium | Low |
| **MQTT QoS 1** | High | High |

**Decision:** MQTT with QoS 1 — persistent connections, at-least-once delivery, works across routed networks.

---

## Decision Framework

### Step 1: Network Topology
| Topology | Broadcast? | Multicast? |
|----------|------------|------------|
| Single subnet | ✅ Yes | ✅ Yes |
| Multiple subnets | ❌ No | ✅ With IGMP |
| Internet/WAN | ❌ No | ❌ No |

### Step 2: Scale
| Scale | Recommendation |
|-------|---------------|
| < 50 receivers | Unicast/broadcast OK |
| 50-1,000 | Multicast preferred |
| > 1,000 | Multicast + CDN |

### Step 3: Reliability
| Need | Protocol |
|------|----------|
| Best-effort | UDP broadcast/multicast |
| At-least-once | MQTT QoS 1 |
| Exactly-once | TCP unicast |

---

## Self-Assessment Questions

1. Gaming company: 100 players on internet — can they use IP multicast? (No — multicast not deployed on public internet)

2. Home automation: discover local smart devices — appropriate protocol? (mDNS/DNS-SD with broadcast)

3. Financial trading: 500 subscribers, guaranteed delivery — why is UDP multicast insufficient? (No delivery guarantee; use reliable multicast or message queue)

---

## Further Reading
- RFC 3376: IGMPv3
- RFC 7252: CoAP
- Tanenbaum: Computer Networks, Ch. 5

---
*Week 3: Network Programming — Broadcast, Multicast and TCP Tunnelling*
