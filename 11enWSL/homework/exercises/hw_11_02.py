#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
  Homework 11.02 – DNS Caching Resolver
═══════════════════════════════════════════════════════════════════════════════

NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim
Week 11: Application Protocols - FTP, DNS, SSH and Load Balancing

LEVEL: Advanced
ESTIMATED TIME: 60-90 minutes

PAIR PROGRAMMING NOTES:
  - Driver: Implement cache logic, handle UDP sockets
  - Navigator: Verify TTL handling, check thread safety
  - Swap after: Each major feature (cache, forwarding, statistics)

This assignment implements a local DNS caching resolver that:
1. Listens on UDP port 5353 for DNS queries
2. Caches responses with TTL-based expiration
3. Forwards cache misses to upstream DNS servers
4. Reports cache hit/miss statistics

PREDICTION PROMPTS:
  💭 Before testing: Will the second query for the same domain be faster?
  💭 Before TTL expiry: What happens when cached TTL reaches zero?
  💭 Before upstream failure: What RCODE will be returned if upstream is unreachable?

Usage:
    python hw_11_02.py --listen host:port --upstream server
    
Example:
    python hw_11_02.py --listen 127.0.0.1:5353 --upstream 8.8.8.8
    
Test with:
    nslookup google.com 127.0.0.1 -port=5353
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import argparse
import socket
import struct
import time
import threading
import signal
from dataclasses import dataclass
from typing import Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# DNS_PROTOCOL_CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

# Query/Response types
QTYPE_A = 1         # IPv4 address
QTYPE_NS = 2        # Nameserver
QTYPE_CNAME = 5     # Canonical name
QTYPE_SOA = 6       # Start of authority
QTYPE_PTR = 12      # Pointer (reverse DNS)
QTYPE_MX = 15       # Mail exchange
QTYPE_TXT = 16      # Text record
QTYPE_AAAA = 28     # IPv6 address
QTYPE_ANY = 255     # Any type

QTYPE_NAMES = {
    1: 'A', 2: 'NS', 5: 'CNAME', 6: 'SOA', 12: 'PTR',
    15: 'MX', 16: 'TXT', 28: 'AAAA', 255: 'ANY'
}

# Query classes
QCLASS_IN = 1       # Internet

# Response codes
RCODE_OK = 0
RCODE_FORMAT_ERROR = 1
RCODE_SERVER_FAILURE = 2
RCODE_NAME_ERROR = 3
RCODE_NOT_IMPLEMENTED = 4
RCODE_REFUSED = 5

# DNS header structure (12 bytes)
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
# |                      ID                       |
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
# |QR|   Opcode  |AA|TC|RD|RA|   Z    |   RCODE   |
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
# |                    QDCOUNT                    |
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
# |                    ANCOUNT                    |
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
# |                    NSCOUNT                    |
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
# |                    ARCOUNT                    |
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+


# ═══════════════════════════════════════════════════════════════════════════════
# DATA_STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class DNSHeader:
    """
    DNS packet header.
    
    Attributes:
        id: Transaction ID (16-bit)
        qr: Query (0) or Response (1)
        opcode: Operation code (4-bit)
        aa: Authoritative answer flag
        tc: Truncation flag
        rd: Recursion desired flag
        ra: Recursion available flag
        rcode: Response code (4-bit)
        qdcount: Question count
        ancount: Answer count
        nscount: Authority count
        arcount: Additional count
    """
    id: int = 0
    qr: int = 0
    opcode: int = 0
    aa: int = 0
    tc: int = 0
    rd: int = 1
    ra: int = 0
    rcode: int = 0
    qdcount: int = 1
    ancount: int = 0
    nscount: int = 0
    arcount: int = 0
    
    def pack(self) -> bytes:
        """
        Pack header into bytes.
        
        TODO: Implement this method
        
        Hints:
        - Use struct.pack with format '>HHHHHH' for 6 unsigned shorts
        - Second field combines: (qr<<15) | (opcode<<11) | (aa<<10) | (tc<<9) | (rd<<8) | (ra<<7) | rcode
        """
        pass
    
    @classmethod
    def unpack(cls, data: bytes) -> 'DNSHeader':
        """
        Unpack header from bytes.
        
        TODO: Implement this method
        
        Hints:
        - Use struct.unpack with format '>HHHHHH'
        - Extract individual flags using bit operations
        """
        pass


@dataclass
class DNSQuestion:
    """
    DNS question section.
    
    Attributes:
        name: Domain name being queried
        qtype: Query type (A, AAAA, MX, etc.)
        qclass: Query class (usually IN = 1)
    """
    name: str
    qtype: int = QTYPE_A
    qclass: int = QCLASS_IN
    
    def pack(self) -> bytes:
        """
        Pack question into bytes.
        
        TODO: Implement this method
        
        Domain name format:
        - Each label prefixed with length byte
        - Terminated with null byte
        - Example: "www.google.com" -> b'\x03www\x06google\x03com\x00'
        """
        pass
    
    @classmethod
    def unpack(cls, data: bytes, offset: int) -> tuple['DNSQuestion', int]:
        """
        Unpack question from bytes starting at offset.
        
        TODO: Implement this method
        
        Returns:
            Tuple of (DNSQuestion, new_offset)
            
        Hints:
        - Handle label length bytes
        - Watch for compression pointers (first 2 bits = 11)
        """
        pass


@dataclass
class CacheEntry:
    """
    DNS cache entry with TTL tracking.
    
    Attributes:
        response: Raw DNS response packet
        expiry_time: Unix timestamp when entry expires
        original_ttl: Original TTL from response
    """
    response: bytes
    expiry_time: float
    original_ttl: int
    
    def is_expired(self) -> bool:
        """Check if cache entry has expired."""
        return time.time() >= self.expiry_time
    
    def remaining_ttl(self) -> int:
        """Calculate remaining TTL in seconds."""
        remaining = int(self.expiry_time - time.time())
        return max(0, remaining)


@dataclass
class Statistics:
    """Resolver statistics."""
    queries_received: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    upstream_queries: int = 0
    upstream_failures: int = 0
    
    @property
    def hit_ratio(self) -> float:
        """Calculate cache hit ratio."""
        total = self.cache_hits + self.cache_misses
        return (self.cache_hits / total * 100) if total > 0 else 0.0
    
    def __str__(self) -> str:
        return (
            f"Queries: {self.queries_received} | "
            f"Hits: {self.cache_hits} | "
            f"Misses: {self.cache_misses} | "
            f"Hit ratio: {self.hit_ratio:.1f}%"
        )


# ═══════════════════════════════════════════════════════════════════════════════
# DNS_PACKET_HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def encode_domain_name(name: str) -> bytes:
    """
    Encode domain name to DNS wire format.
    
    Example: "www.google.com" -> b'\x03www\x06google\x03com\x00'
    
    TODO: Implement this function
    """
    pass


def decode_domain_name(data: bytes, offset: int) -> tuple[str, int]:
    """
    Decode domain name from DNS wire format.
    
    Handles:
    - Regular labels (length-prefixed)
    - Compression pointers (2 bytes starting with 0xC0)
    
    TODO: Implement this function
    
    Returns:
        Tuple of (domain_name, new_offset)
    """
    pass


def extract_ttl_from_response(response: bytes) -> int:
    """
    Extract minimum TTL from DNS response.
    
    TODO: Implement this function
    
    Hints:
    - Parse header to get ANCOUNT
    - Skip questions section
    - Parse answer records to find TTL field
    - TTL is at offset 6 in each resource record (4 bytes)
    - Return minimum TTL across all answers
    """
    pass


def build_cache_key(name: str, qtype: int) -> tuple[str, int]:
    """Build normalised cache key."""
    return (name.lower().rstrip('.'), qtype)


# ═══════════════════════════════════════════════════════════════════════════════
# DNS_CACHE_CLASS
# ═══════════════════════════════════════════════════════════════════════════════

class DNSCache:
    """
    Thread-safe DNS response cache with TTL expiration.
    
    TODO: Complete the implementation.
    """
    
    def __init__(self):
        self._cache: dict[tuple[str, int], CacheEntry] = {}
        self._lock = threading.Lock()
    
    def get(self, name: str, qtype: int) -> Optional[bytes]:
        """
        Get cached response if present and not expired.
        
        TODO: Implement this method
        
        Returns:
            Cached DNS response or None if not found/expired
        """
        pass
    
    def put(self, name: str, qtype: int, response: bytes, ttl: int) -> None:
        """
        Store response in cache with TTL.
        
        TODO: Implement this method
        """
        pass
    
    def flush(self) -> int:
        """
        Remove all cache entries.
        
        Returns:
            Number of entries removed
        """
        with self._lock:
            count = len(self._cache)
            self._cache.clear()
            return count
    
    def cleanup_expired(self) -> int:
        """
        Remove expired entries from cache.
        
        Returns:
            Number of entries removed
        """
        # TODO: Implement this method
        pass
    
    def __len__(self) -> int:
        return len(self._cache)


# ═══════════════════════════════════════════════════════════════════════════════
# DNS_RESOLVER_CLASS
# ═══════════════════════════════════════════════════════════════════════════════

class DNSResolver:
    """
    DNS caching resolver.
    
    TODO: Complete the implementation.
    """
    
    def __init__(self, listen_host: str, listen_port: int, upstream_server: str):
        """
        Initialise the resolver.
        
        Args:
            listen_host: Host to listen on
            listen_port: Port to listen on (usually 5353)
            upstream_server: Upstream DNS server IP (e.g., 8.8.8.8)
        """
        self.listen_host = listen_host
        self.listen_port = listen_port
        self.upstream_server = upstream_server
        self.upstream_port = 53
        
        self.cache = DNSCache()
        self.stats = Statistics()
        self.running = False
        
        self._socket: Optional[socket.socket] = None
    
    def query_upstream(self, query: bytes) -> Optional[bytes]:
        """
        Forward query to upstream DNS server.
        
        TODO: Implement this method
        
        Steps:
        1. Create UDP socket
        2. Set timeout (2 seconds recommended)
        3. Send query to upstream
        4. Receive response
        5. Return response or None on failure
        """
        pass
    
    def handle_query(self, query: bytes, client_addr: tuple) -> Optional[bytes]:
        """
        Handle incoming DNS query.
        
        TODO: Implement this method
        
        Steps:
        1. Parse query header and question
        2. Check cache for existing response
        3. If cache hit: return cached response (update ID)
        4. If cache miss: query upstream
        5. Extract TTL and cache response
        6. Return response
        """
        pass
    
    def update_response_id(self, response: bytes, new_id: int) -> bytes:
        """
        Update transaction ID in DNS response.
        
        The client expects the response ID to match the query ID.
        """
        return struct.pack('>H', new_id) + response[2:]
    
    def run(self) -> None:
        """Start the DNS resolver."""
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind((self.listen_host, self.listen_port))
        
        self.running = True
        
        logger.info(f"DNS Caching Resolver listening on {self.listen_host}:{self.listen_port}")
        logger.info(f"Upstream server: {self.upstream_server}:{self.upstream_port}")
        logger.info("Press Ctrl+C to stop")
        
        # Start statistics reporter thread
        stats_thread = threading.Thread(target=self._report_stats, daemon=True)
        stats_thread.start()
        
        try:
            while self.running:
                try:
                    self._socket.settimeout(1.0)
                    query, client_addr = self._socket.recvfrom(512)
                    
                    self.stats.queries_received += 1
                    
                    response = self.handle_query(query, client_addr)
                    
                    if response:
                        self._socket.sendto(response, client_addr)
                    
                except socket.timeout:
                    continue
                    
        except KeyboardInterrupt:
            logger.info("Shutting down...")
        finally:
            self.running = False
            self._socket.close()
            logger.info(f"Final statistics: {self.stats}")
    
    def _report_stats(self) -> None:
        """Periodically report statistics."""
        while self.running:
            time.sleep(30)
            logger.info(f"Stats: {self.stats} | Cache size: {len(self.cache)}")
    
    def flush_cache(self) -> None:
        """Flush the DNS cache (can be triggered by signal)."""
        count = self.cache.flush()
        logger.info(f"Cache flushed: {count} entries removed")


# ═══════════════════════════════════════════════════════════════════════════════
# SIGNAL_HANDLING
# ═══════════════════════════════════════════════════════════════════════════════

def setup_signal_handlers(resolver: DNSResolver) -> None:
    """Set up signal handlers for cache management."""
    def handle_flush(signum, frame):
        resolver.flush_cache()
    
    # On Unix systems, SIGUSR1 triggers cache flush
    if hasattr(signal, 'SIGUSR1'):
        signal.signal(signal.SIGUSR1, handle_flush)
        logger.info("Send SIGUSR1 to flush cache")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Week 11 Homework: DNS Caching Resolver",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python hw_11_02.py --listen 127.0.0.1:5353 --upstream 8.8.8.8
  python hw_11_02.py --listen 0.0.0.0:5353 --upstream 1.1.1.1

Test with:
  nslookup google.com 127.0.0.1 -port=5353
  dig @127.0.0.1 -p 5353 google.com A
        """
    )
    
    parser.add_argument(
        '--listen', '-l',
        default='127.0.0.1:5353',
        help='Listen address (default: 127.0.0.1:5353)'
    )
    parser.add_argument(
        '--upstream', '-u',
        default='8.8.8.8',
        help='Upstream DNS server (default: 8.8.8.8)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Parse listen address
    listen_parts = args.listen.split(':')
    listen_host = listen_parts[0]
    listen_port = int(listen_parts[1])
    
    # Create resolver
    resolver = DNSResolver(listen_host, listen_port, args.upstream)
    
    # Set up signal handlers
    setup_signal_handlers(resolver)
    
    # Run resolver
    resolver.run()
    
    return 0


if __name__ == '__main__':
    exit(main())
