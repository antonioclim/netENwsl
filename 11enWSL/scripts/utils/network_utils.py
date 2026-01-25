#!/usr/bin/env python3
"""
Network testing utilities for Week 11 Laboratory.
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

Provides HTTP testing, health checking, and network diagnostics.
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import socket
import time
import urllib.request
import urllib.error
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed

from .logger import setup_logger

logger = setup_logger("network_utils")


@dataclass


# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class HTTPResponse:
    """HTTP response container."""
    status_code: int
    headers: Dict[str, str]
    body: str
    latency_ms: float
    error: Optional[str] = None



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def http_get(url: str, timeout: float = 5.0) -> HTTPResponse:
    """
    Perform an HTTP GET request.
    
    Args:
        url: Target URL
        timeout: Request timeout in seconds
    
    Returns:
        HTTPResponse with status, headers, body, and latency
    """
    start_time = time.time()
    
    try:
        req = urllib.request.Request(url, method='GET')
        req.add_header('User-Agent', 'Week11-LabClient/1.0')
        
        with urllib.request.urlopen(req, timeout=timeout) as response:
            latency_ms = (time.time() - start_time) * 1000
            headers = dict(response.headers.items())
            body = response.read().decode('utf-8', errors='replace')
            
            return HTTPResponse(
                status_code=response.status,
                headers=headers,
                body=body,
                latency_ms=latency_ms
            )
    
    except urllib.error.HTTPError as e:
        latency_ms = (time.time() - start_time) * 1000
        return HTTPResponse(
            status_code=e.code,
            headers=dict(e.headers.items()),
            body=e.read().decode('utf-8', errors='replace'),
            latency_ms=latency_ms
        )
    
    except Exception as e:
        latency_ms = (time.time() - start_time) * 1000
        return HTTPResponse(
            status_code=0,
            headers={},
            body='',
            latency_ms=latency_ms,
            error=str(e)
        )



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_port(host: str, port: int, timeout: float = 2.0) -> bool:
    """
    Check if a TCP port is open.
    
    Args:
        host: Target hostname or IP
        port: Port number
        timeout: Connection timeout
    
    Returns:
        True if port is accepting connections
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            return result == 0
    except Exception:
        return False



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def wait_for_port(host: str, 
                  port: int, 
                  timeout: float = 30.0,
                  interval: float = 1.0) -> bool:
    """
    Wait until a port becomes available.
    
    Args:
        host: Target hostname
        port: Port number
        timeout: Maximum wait time
        interval: Check interval
    
    Returns:
        True if port became available within timeout
    """
    start_time = time.time()
    
    while (time.time() - start_time) < timeout:
        if check_port(host, port, timeout=2.0):
            return True
        time.sleep(interval)
    
    return False



# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
def test_load_balancer(url: str, 
                       num_requests: int = 10,
                       concurrency: int = 1) -> Dict[str, Any]:
    """
    Test load balancer distribution.
    
    Args:
        url: Load balancer URL
        num_requests: Number of requests to send
        concurrency: Number of concurrent workers
    
    Returns:
        Dictionary with distribution statistics
    """
    results: List[HTTPResponse] = []
    backend_counts: Dict[str, int] = {}
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def make_request():
        return http_get(url)
    
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [executor.submit(make_request) for _ in range(num_requests)]
        
        for future in as_completed(futures):
            try:
                response = future.result()
                results.append(response)
                
                # Extract backend identifier from response
                backend = extract_backend_id(response)
                if backend:
                    backend_counts[backend] = backend_counts.get(backend, 0) + 1
            
            except Exception as e:
                logger.warning(f"Request failed: {e}")
    
    # Calculate statistics
    successful = [r for r in results if r.status_code == 200]
    latencies = [r.latency_ms for r in successful]
    
    stats = {
        'total_requests': num_requests,
        'successful': len(successful),
        'failed': num_requests - len(successful),
        'distribution': backend_counts,
        'latency': {
            'min_ms': min(latencies) if latencies else 0,
            'max_ms': max(latencies) if latencies else 0,
            'avg_ms': sum(latencies) / len(latencies) if latencies else 0,
        }
    }
    
    return stats



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def extract_backend_id(response: HTTPResponse) -> Optional[str]:
    """
    Extract backend identifier from HTTP response.
    
    Looks for:
    - X-Backend-ID header
    - X-Served-By header
    - Backend ID in response body
    
    Args:
        response: HTTP response
    
    Returns:
        Backend identifier or None
    """
    # Check headers
    for header_name in ['X-Backend-ID', 'X-Served-By', 'x-backend-id', 'x-served-by']:
        if header_name in response.headers:
            return response.headers[header_name]
    
    # Check body for pattern "Backend N"
    import re
    match = re.search(r'Backend\s*(\d+)', response.body)
    if match:
        return f"backend_{match.group(1)}"
    
    # Check body for web1/web2/web3
    for pattern in ['web1', 'web2', 'web3']:
        if pattern in response.body.lower():
            return pattern
    
    return None



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def benchmark_endpoint(url: str,
                       num_requests: int = 100,
                       concurrency: int = 10) -> Dict[str, Any]:
    """
    Benchmark an HTTP endpoint.
    
    Args:
        url: Target URL
        num_requests: Total number of requests
        concurrency: Number of concurrent workers
    
    Returns:
        Benchmark results with RPS and latency percentiles
    """
    latencies: List[float] = []
    errors = 0
    start_time = time.time()
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def make_request():
        return http_get(url, timeout=10.0)
    
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [executor.submit(make_request) for _ in range(num_requests)]
        
        for future in as_completed(futures):
            try:
                response = future.result()
                if response.status_code == 200:
                    latencies.append(response.latency_ms)
                else:
                    errors += 1
            except Exception:
                errors += 1
    
    total_time = time.time() - start_time
    
    # Calculate percentiles
    sorted_latencies = sorted(latencies)
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def percentile(p: float) -> float:
        if not sorted_latencies:
            return 0.0
        idx = int((p / 100.0) * (len(sorted_latencies) - 1))
        return sorted_latencies[idx]
    
    return {
        'total_requests': num_requests,
        'successful': len(latencies),
        'failed': errors,
        'total_time_s': total_time,
        'requests_per_second': len(latencies) / total_time if total_time > 0 else 0,
        'latency_ms': {
            'min': min(latencies) if latencies else 0,
            'max': max(latencies) if latencies else 0,
            'avg': sum(latencies) / len(latencies) if latencies else 0,
            'p50': percentile(50),
            'p90': percentile(90),
            'p95': percentile(95),
            'p99': percentile(99),
        }
    }



# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def print_benchmark_results(results: Dict[str, Any]) -> None:
    """Pretty print benchmark results."""
    print("\n" + "=" * 50)
    print("BENCHMARK RESULTS")
    print("=" * 50)
    print(f"Total Requests:      {results['total_requests']}")
    print(f"Successful:          {results['successful']}")
    print(f"Failed:              {results['failed']}")
    print(f"Total Time:          {results['total_time_s']:.2f}s")
    print(f"Requests/Second:     {results['requests_per_second']:.2f}")
    print("")
    print("Latency (ms):")
    lat = results['latency_ms']
    print(f"  Min:    {lat['min']:.2f}")
    print(f"  Max:    {lat['max']:.2f}")
    print(f"  Avg:    {lat['avg']:.2f}")
    print(f"  P50:    {lat['p50']:.2f}")
    print(f"  P90:    {lat['p90']:.2f}")
    print(f"  P95:    {lat['p95']:.2f}")
    print(f"  P99:    {lat['p99']:.2f}")
    print("=" * 50)



# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def print_distribution(distribution: Dict[str, int], total: int) -> None:
    """Pretty print backend distribution."""
    print("\nBackend Distribution:")
    print("-" * 40)
    for backend, count in sorted(distribution.items()):
        pct = (count / total * 100) if total > 0 else 0
        bar = "█" * int(pct / 5)
        print(f"  {backend:15} {count:4} ({pct:5.1f}%) {bar}")
    print("-" * 40)


# ing. dr. Antonio Clim

if __name__ == "__main__":
    # Module loaded directly - display module info
    print(f"Module {__name__} loaded successfully.")
    print(f"This module provides utility functions for the networking laboratory.")
