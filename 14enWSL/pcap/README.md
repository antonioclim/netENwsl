# Packet Captures

This directory stores packet capture files (PCAP) generated during laboratory exercises.

## Generating Captures

```powershell
python scripts/capture_traffic.py --duration 30 --output pcap/demo.pcap
```

## Analysing Captures

```powershell
# Open in Wireshark
wireshark pcap/demo.pcap

# Command-line analysis
tshark -r pcap/demo.pcap -q -z conv,tcp
tshark -r pcap/demo.pcap -Y http.request
```

---
*NETWORKING class - ASE, Informatics | by Revolvix*
