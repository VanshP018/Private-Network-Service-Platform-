# Phase 1 Video Presentation Script

This script is designed for a concise **< 5 minute** screen recording demonstration meeting all evaluation criteria.

---

## Preparation Checklist
1. All services active (DNS on port 53, Nginx on port 443, Backend A on 3001, Backend B on 3002).
2. Terminal windows and Wireshark ready.
3. Architecture diagram opened in browser/preview.

---

## 0:00 - 0:30 | Introduction & Architecture Overview

**Visual:** Display Architecture Diagram in [`docs/architecture.md`](architecture.md).

**Speaker Dialogue:**
> "Hello everyone. Today we are demonstrating Phase 1 of our Computer Networks project: a Private, Secure, and Load-Balanced Network Service Platform.
> 
> In this setup, we have segregated our network into distinct service roles:
> 1. A private DNS server running dnsmasq.
> 2. An edge reverse proxy and TLS terminator running Nginx.
> 3. Two independent Python REST backends: Backend A on port 3001 and Backend B on port 3002.
> 
> The client resolves the domain name privately, initiates an encrypted HTTPS connection to Nginx, and Nginx balances traffic across the backend pool."

---

## 0:30 - 1:15 | Configuration Inspection

### 1. DNS Configuration
**Visual:** Show `dnsmasq.conf`.
```bash
tail -n 12 /opt/homebrew/etc/dnsmasq.conf
```
**Speaker Dialogue:**
> "Here is our dnsmasq configuration. It binds to port 53 and maps our private domain `app.teamX.test` to our Nginx edge IP with an explicit 30-second TTL."

### 2. Backend Implementation
**Visual:** Show `backend/app.py`.
```bash
cat backend/app.py
```
**Speaker Dialogue:**
> "Both backends execute this lightweight Python application. Environment variables distinguish Backend A on port 3001 from Backend B on port 3002. It provides health status, ETag support, and caching headers."

### 3. Nginx Edge Configuration
**Visual:** Show Nginx config.
```bash
cat /opt/homebrew/etc/nginx/servers/cn-project.conf
```
**Speaker Dialogue:**
> "Nginx defines an upstream block containing both Backend A and Backend B. It listens on port 443 with SSL and HTTP/2 enabled, terminating TLS securely and reverse proxying requests."

---

## 1:15 - 2:30 | Live System Verification

### 1. Private DNS Resolution
**Command:**
```bash
dig @10.7.7.19 app.teamX.test
dig @8.8.8.8 app.teamX.test
```
**Speaker Dialogue:**
> "First, we query our private DNS server. It successfully resolves `app.teamX.test` to our Nginx IP `10.7.10.162` with a 30-second TTL. When queried against a public DNS resolver like 8.8.8.8, it returns NXDOMAIN, confirming complete namespace isolation."

### 2. HTTPS & TLS Trust
**Command:**
```bash
curl -v https://app.teamX.test/api/status
```
**Speaker Dialogue:**
> "Next, we perform an HTTPS request. Notice that certificate verification succeeds without using `-k`, and HTTP/2 is negotiated over TLS."

### 3. Load Balancing Demonstration
**Command (Run repeatedly 4-6 times):**
```bash
curl -i https://app.teamX.test/api/status
```
**Speaker Dialogue:**
> "As we make consecutive requests to the status endpoint, observe the `X-Backend` header alternating between Backend A and Backend B, proving round-robin load distribution."

### 4. HTTP Caching & 304 Validation
**Command:**
```bash
curl -I https://app.teamX.test/api/cache
curl -i -H 'If-None-Match: "cn-cache-v1"' https://app.teamX.test/api/cache
```
**Speaker Dialogue:**
> "Our `/api/cache` endpoint returns `Cache-Control: max-age=60` along with an ETag. When the client presents `If-None-Match`, the server returns `HTTP 304 Not Modified` with no payload, saving bandwidth."

---

## 2:30 - 3:45 | Wireshark Packet Analysis

**Visual:** Switch to Wireshark.

### 1. DNS Exchange
**Filter:** `dns && ip.addr == 10.7.7.19`
**Speaker Dialogue:**
> "In Wireshark, we see the standard DNS query over UDP 53 for `app.teamX.test` and the DNS response returning the edge IP with a 30-second TTL."

### 2. TCP 3-Way Handshake
**Filter:** `tcp.flags.syn == 1 && tcp.port == 443` $\to$ Stream `0`
**Speaker Dialogue:**
> "Here is the TCP three-way handshake: the client sends SYN to port 443, the server replies with SYN-ACK, and the client finishes with ACK, establishing the transport connection."

### 3. TLS Handshake & Application Data
**Filter:** `tcp.stream eq 0 && tls`
**Speaker Dialogue:**
> "Following TCP establishment, we see the TLS handshake: ClientHello containing SNI, ServerHello with our public certificate, key exchange, and ChangeCipherSpec. All subsequent HTTP/2 data is encrypted inside Application Data records."

---

## 3:45 - 4:45 | Fault Tolerance & Failover (Rubric D3)

**Visual:** Terminal.

**Actions:**
1. Stop Backend A (`kill <PID_A>`).
2. Run requests:
   ```bash
   curl -i https://app.teamX.test/api/status
   ```
**Speaker Dialogue:**
> "Now we demonstrate system resilience. We terminate Backend A. As we make requests to Nginx, every request is automatically routed to Backend B without any 502 error or failure. Notice that DNS resolution and TLS connections remain completely unaffected because the failure is strictly isolated to the application layer."

**Actions:**
3. Restart Backend A (`./scripts/run-backend.sh A`).
4. Re-run requests to show recovery.
**Speaker Dialogue:**
> "Once Backend A is restored, Nginx automatically resumes round-robin load balancing across both backends.
> 
> Thank you! That concludes our Phase 1 demonstration."
