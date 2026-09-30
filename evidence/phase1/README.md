# Phase 1 Wireshark Packet Evidence Guide

This document catalogs and explains the packet capture artifacts and visual evidence gathered for Phase 1 verification.

---

## 1. Packet Capture Files

- **Raw Capture:** [`phase1-original-live-capture.pcapng`](phase1-original-live-capture.pcapng) — Complete unedited live capture across the network interface.
- **Filtered Project Capture:** [`phase1-dns-tcp-tls.pcapng`](phase1-dns-tcp-tls.pcapng) — Isolated capture containing only relevant DNS, TCP 3-way handshake, and TLS/HTTPS streams.

---

## 2. DNS Evidence

**Wireshark Display Filter:**
```text
dns && ip.addr == 10.7.7.19
```

| Event | Protocol / Port | Source | Destination | Details |
| --- | --- | --- | --- | --- |
| **DNS Query** | UDP 53 | Client | `10.7.7.19` | Standard query `app.teamX.test` Type A |
| **DNS Response** | UDP 53 | `10.7.7.19` | Client | Response `10.7.10.162` with **TTL = 30s** |

---

## 3. TCP 3-Way Handshake Evidence

**Wireshark Display Filter:**
```text
tcp.flags.syn == 1 && tcp.port == 443
```
*(Follow Stream: `tcp.stream eq 0`)*

| Step | Flag | Source | Destination | Details |
| --- | --- | --- | --- | --- |
| 1 | **SYN** | Client | `10.7.10.162:443` | Connection initiation, initial Seq number |
| 2 | **SYN-ACK** | `10.7.10.162:443` | Client | Server acknowledgement & synchronization |
| 3 | **ACK** | Client | `10.7.10.162:443` | Handshake completion, TCP established |

---

## 4. TLS Handshake & Encrypted Application Data

**Wireshark Display Filter:**
```text
tcp.stream eq 0 && tls
```

| Packet Event | TLS Record Type | Protocol Version | Details |
| --- | --- | --- | --- |
| **ClientHello** | Handshake (1) | TLS 1.2 / 1.3 | SNI: `app.teamX.test`, Cipher suites list |
| **ServerHello** | Handshake (2) | TLS 1.2 / 1.3 | Selected cipher, session ID |
| **Certificate** | Handshake (11) | TLS 1.2 | X.509 Certificate presentation |
| **Key Exchange** | Handshake | TLS 1.2 / 1.3 | Key parameters exchange |
| **Encrypted Data** | Application Data (23) | TLS 1.2 / 1.3 | HTTP/2 encrypted request/response payloads |

---

## 5. Visual Screenshots

Place your captured screenshot files in [`screenshots/`](screenshots/):

### 1. DNS Query & Response
![DNS query and response](screenshots/dns-query-response.png)

### 2. DNS Answer Details with TTL
![DNS answer details](screenshots/dns-answer-details.png)

### 3. TCP 3-Way Handshake
![TCP three-way handshake](screenshots/tcp-three-way-handshake.png)

### 4. TLS Stream & Encrypted Application Data
![TLS stream overview](screenshots/tls-stream-overview.png)
