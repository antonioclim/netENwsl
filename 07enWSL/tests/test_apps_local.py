"""Local, dependency-free tests for Week 7 applications.

These tests start the Python applications as subprocesses on ephemeral ports.
They do not require Docker and they provide fast regression coverage in CI.
"""

from __future__ import annotations

import socket
import subprocess
import sys
import time
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _free_port() -> int:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    port = int(s.getsockname()[1])
    s.close()
    return port


def _wait_tcp(host: str, port: int, timeout: float = 3.0) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.2)
        try:
            if s.connect_ex((host, port)) == 0:
                s.close()
                return True
        except Exception:
            pass
        finally:
            try:
                s.close()
            except Exception:
                pass
        time.sleep(0.05)
    return False


def _run(cmd: list[str], *, timeout: float = 10.0) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(PROJECT_ROOT),
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )


def test_tcp_server_client_echo_local() -> None:
    port = _free_port()
    server = subprocess.Popen(
        [
            sys.executable,
            "src/apps/tcp_server.py",
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
        ],
        cwd=str(PROJECT_ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        assert _wait_tcp("127.0.0.1", port), "TCP server did not start"

        msg = "hello-week7"
        client = _run(
            [
                sys.executable,
                "src/apps/tcp_client.py",
                "--host",
                "127.0.0.1",
                "--port",
                str(port),
                "--message",
                msg,
            ],
            timeout=10.0,
        )
        assert client.returncode == 0, client.stderr or client.stdout
        assert msg in (client.stdout or ""), "Echo not observed in client output"
    finally:
        try:
            server.terminate()
        except Exception:
            pass
        try:
            server.wait(timeout=3)
        except Exception:
            try:
                server.kill()
            except Exception:
                pass


def test_udp_sender_receiver_local() -> None:
    port = _free_port()
    receiver = subprocess.Popen(
        [
            sys.executable,
            "src/apps/udp_receiver.py",
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
            "--count",
            "1",
            "--timeout",
            "3",
        ],
        cwd=str(PROJECT_ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        # UDP receiver does not have a readiness signal, give it a moment
        time.sleep(0.2)

        msg = "udp-week7"
        sender = _run(
            [
                sys.executable,
                "src/apps/udp_sender.py",
                "--host",
                "127.0.0.1",
                "--port",
                str(port),
                "--message",
                msg,
            ],
            timeout=5.0,
        )
        assert sender.returncode == 0, sender.stderr or sender.stdout

        out, err = receiver.communicate(timeout=5.0)
        assert receiver.returncode == 0, err or out
        assert msg in (out or ""), "UDP payload not observed in receiver output"
    finally:
        try:
            receiver.terminate()
        except Exception:
            pass
        try:
            receiver.wait(timeout=2)
        except Exception:
            try:
                receiver.kill()
            except Exception:
                pass


def test_packet_filter_proxy_local() -> None:
    upstream_port = _free_port()
    proxy_port = _free_port()

    tcp_server = subprocess.Popen(
        [
            sys.executable,
            "src/apps/tcp_server.py",
            "--host",
            "127.0.0.1",
            "--port",
            str(upstream_port),
        ],
        cwd=str(PROJECT_ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    proxy = subprocess.Popen(
        [
            sys.executable,
            "src/apps/packet_filter.py",
            "--listen-host",
            "127.0.0.1",
            "--listen-port",
            str(proxy_port),
            "--upstream-host",
            "127.0.0.1",
            "--upstream-port",
            str(upstream_port),
        ],
        cwd=str(PROJECT_ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    try:
        assert _wait_tcp("127.0.0.1", upstream_port), "Upstream TCP server did not start"
        assert _wait_tcp("127.0.0.1", proxy_port), "Packet filter did not start"

        msg = "proxy-week7"
        client = _run(
            [
                sys.executable,
                "src/apps/tcp_client.py",
                "--host",
                "127.0.0.1",
                "--port",
                str(proxy_port),
                "--message",
                msg,
            ],
            timeout=10.0,
        )
        assert client.returncode == 0, client.stderr or client.stdout
        assert msg in (client.stdout or ""), "Echo not observed through proxy"
    finally:
        for p in (proxy, tcp_server):
            try:
                p.terminate()
            except Exception:
                pass
        for p in (proxy, tcp_server):
            try:
                p.wait(timeout=3)
            except Exception:
                try:
                    p.kill()
                except Exception:
                    pass


def test_port_probe_local_open_and_closed() -> None:
    # Create a simple listening socket as an "open" port target
    host = "127.0.0.1"
    open_port = _free_port()
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind((host, open_port))
    listener.listen(1)

    closed_port = _free_port()

    try:
        proc = _run(
            [
                sys.executable,
                "src/apps/port_probe.py",
                "--host",
                host,
                "--ports",
                f"{open_port},{closed_port}",
                "--timeout",
                "0.3",
            ],
            timeout=10.0,
        )
        assert proc.returncode == 0, proc.stderr or proc.stdout
        out = proc.stdout or ""
        assert f"{host}:{open_port} -> open" in out
        assert f"{host}:{closed_port} -> closed" in out
    finally:
        try:
            listener.close()
        except Exception:
            pass


def test_firewallctl_dry_run_allow_all() -> None:
    proc = _run(
        [
            sys.executable,
            "src/apps/firewallctl.py",
            "--config",
            "docker/configs/firewall_profiles.json",
            "--profile",
            "allow_all",
            "--dry-run",
        ],
        timeout=10.0,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout
    out = proc.stdout or ""
    assert "[dry-run] iptables -F FORWARD" in out
    assert "[dry-run] iptables -P FORWARD ACCEPT" in out
