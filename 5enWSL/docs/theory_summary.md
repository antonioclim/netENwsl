# Theoretical Background: Network Layer IP Addressing

> Week 5 - NETWORKING class - ASE, Informatics
>
> by Revolvix

## 1. The Network Layer in Context

The network layer (Layer 3 of the OSI model) provides logical addressing and routing capabilities that enable end-to-end communication across heterogeneous physical networks. Unlike data link layer (Layer 2) addresses which have only local significance within a single network segment, network layer addresses provide global reachability across the entire internetwork.

### Key Functions

The network layer performs several critical functions in the protocol stack. Logical addressing assigns unique identifiers to network interfaces that remain consistent regardless of the underlying physical network technology. Routing determines the optimal path for packets to traverse from source to destination across multiple intermediate networks. Fragmentation and reassembly handle the division of packets when they must traverse networks with smaller maximum transmission units (MTUs).

## 2. IPv4 Addressing Architecture

IPv4 addresses consist of 32 bits, conventionally expressed in dotted-decimal notation where each octet (8 bits) is represented as a decimal value from 0 to 255. The address space is divided into two logical portions: the network portion identifying the specific network, and the host portion identifying a specific interface within that network.

### Address Classes (Historical)

The original classful addressing scheme divided the address space into five classes. Class A networks use the first 8 bits for the network portion, permitting 126 networks with approximately 16 million hosts each. Class B networks use 16 bits for the network portion, allowing approximately 16,000 networks with 65,534 hosts each. Class C networks use 24 bits for the network portion, providing over 2 million networks with 254 hosts each. This rigid structure proved inefficient, leading to the development of CIDR.

### CIDR Notation

Classless Inter-Domain Routing (CIDR) replaces the fixed class boundaries with a variable-length prefix notation. The prefix length, expressed as a suffix (e.g., /24), indicates how many bits constitute the network portion. This flexibility enables more efficient address allocation by permitting network sizes to match actual requirements rather than conforming to predetermined class boundaries.

### Special Addresses

Certain address ranges serve specific purposes and cannot be assigned to regular hosts. The network address (all host bits set to 0) identifies the network itself. The broadcast address (all host bits set to 1) enables communication to all hosts within the network. Loopback addresses (127.0.0.0/8) are reserved for local host testing. Private address ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) are reserved for internal use and are not routable on the public Internet.

## 3. Subnetting Fundamentals

Subnetting involves borrowing bits from the host portion to create additional network identifiers, effectively dividing a single network into multiple smaller subnetworks. This technique provides several benefits: improved security through network isolation, reduced broadcast domain size, and more efficient utilisation of address space.

### Fixed Length Subnet Mask (FLSM)

FLSM applies identical subnet masks to all subnets, creating equal-sized network segments. The number of subnets created must be a power of two, calculated as 2^n where n represents the number of borrowed bits. Each resulting subnet contains 2^h-2 usable host addresses, where h represents the remaining host bits (subtracting 2 accounts for network and broadcast addresses).

**Calculation Process:**
1. Determine the number of subnets required
2. Calculate bits to borrow: ceil(log₂(subnets))
3. Add borrowed bits to original prefix length
4. Calculate new subnet boundaries

### Variable Length Subnet Mask (VLSM)

VLSM permits different subnet masks within the same address space, enabling optimal address allocation for networks with heterogeneous size requirements. This technique reduces address waste by matching subnet sizes to actual host requirements.

**Allocation Algorithm:**
1. Sort requirements in descending order by host count
2. For each requirement, calculate minimum prefix: 32 - ceil(log₂(hosts + 2))
3. Align starting address to block boundary
4. Allocate subnet and advance to next available address

### Efficiency Considerations

Address utilisation efficiency measures the percentage of allocated addresses actually required. VLSM typically achieves higher efficiency than FLSM because it avoids allocating excess addresses to small networks. Optimal VLSM allocation considers both current requirements and potential future growth.

## 4. IPv6 Addressing

IPv6 addresses comprise 128 bits, expressed as eight groups of four hexadecimal digits separated by colons. This vastly expanded address space (approximately 3.4×10^38 addresses) eliminates the address exhaustion concerns that necessitated NAT in IPv4 networks.

### Address Representation

**Full notation** displays all 32 hexadecimal digits: `2001:0db8:0000:0000:0000:0000:0000:0001`

**Compressed notation** applies two simplification rules:
1. Leading zeros within each group may be omitted: `2001:db8:0:0:0:0:0:1`
2. One sequence of consecutive all-zero groups may be replaced with `::`: `2001:db8::1`

### Address Types

**Global Unicast (2000::/3):** Routable addresses equivalent to public IPv4 addresses. The first 48 bits typically represent the global routing prefix assigned by the ISP, the next 16 bits identify the subnet, and the final 64 bits constitute the interface identifier.

**Link-Local (fe80::/10):** Automatically configured addresses used for communication within a single network segment. Every IPv6-enabled interface has a link-local address.

**Unique Local (fc00::/7):** Addresses for private network use, analogous to RFC 1918 private addresses in IPv4. These addresses are not routable on the global Internet.

**Multicast (ff00::/8):** Addresses for one-to-many communication. Common examples include ff02::1 (all nodes) and ff02::2 (all routers).

### Subnetting IPv6

Standard practice allocates a /48 prefix to organisations, permitting 65,536 /64 subnets. The /64 subnet size is recommended for all end-user networks because it enables Stateless Address Autoconfiguration (SLAAC) and maintains compatibility with various IPv6 features.

## 5. Practical Applications

### Network Design Considerations

Effective IP addressing requires balancing several competing concerns. Address conservation minimises waste while providing sufficient capacity for growth. Administrative clarity ensures addresses follow logical patterns that simplify management and troubleshooting. Security segmentation places hosts with different security requirements in separate subnets.

### Documentation Requirements

Professional network documentation includes complete addressing tables showing all subnets, their masks, and assigned address ranges. Gateway assignments identify the router interface for each subnet. Host assignments track which addresses are allocated to specific devices. Reserved ranges identify addresses set aside for future expansion or special purposes.

## 6. References

Kurose, J. F., & Ross, K. W. (2021). *Computer Networking: A Top-Down Approach* (8th ed.). Pearson.

Postel, J. (1981). Internet Protocol. RFC 791.

Deering, S., & Hinden, R. (2017). Internet Protocol, Version 6 (IPv6) Specification. RFC 8200.

Rekhter, Y., Moskowitz, B., Karrenberg, D., de Groot, G. J., & Lear, E. (1996). Address Allocation for Private Internets. RFC 1918.

Hinden, R., & Deering, S. (2006). IP Version 6 Addressing Architecture. RFC 4291.
