# Phase 1 Form Submission Checklist & Rubric Mapping

Use this checklist to ensure all evaluation requirements for the Phase 1 submission form and demonstration video are completely met.

---

## General Project Metadata
 
- **Team Name:** Team X / Private Network Service Platform
- **Members & Enrollments:**
  | Name | Enrollment | Role |
  | --- | --- | --- |
  | **Antik Mondal** | `2401010084` | Project Lead & Backend Servers A & B |
  | **Vansh Panwar** | `2401010494` | Nginx Load Balancer & TLS Setup |
  | **Tanmay Singh** | `2401010476` | Private DNS Server (`dnsmasq`) |
- **Repository:** Ensure GitHub repository contains clean documentation, configs, and evidence.
- **Demo Video:** $\le$ 5 minutes, $\le$ 500 MB, Google Drive link set to *"Anyone with the link can view"*.
- **Naming Convention:** `CN_Phase1_[TeamName/RollNo].mp4`.

---

## Section A: Private DNS & Host Addressing

- [ ] **A1:** Provide network inventory table listing all nodes (DNS, Edge, Backend A, Backend B) with hostnames, IP addresses, listening ports, and interfaces (`en0`/`lo0`).
- [ ] **A2:** Paste real `dnsmasq.conf` contents showing domain mapping and explicit 30s TTL.
- [ ] **A3:** Paste full `dig @<DNS_IP> app.teamX.test` output showing resolver IP and matching answer (`10.7.10.162`).
- [ ] **A4:** Paste `dig @8.8.8.8 app.teamX.test` output showing `NXDOMAIN` or timeout (proving private namespace isolation).
- [ ] **A5:** Provide ping results verifying pairwise reachability across nodes on the network.

---

## Section B: Edge Proxy, TLS Termination & Load Balancing

- [ ] **B1:** Paste complete verbose `curl -v https://app.teamX.test` output verifying valid TLS certificate without `-k`.
- [ ] **B2:** Paste series of consecutive requests showing load balancing across Backend A and Backend B (`X-Backend` header).
- [ ] **B3:** Paste the nginx configuration showing the `upstream` backend pool, `listen 443 ssl`, and `proxy_pass`.

---

## Section C: Wireshark Packet Breakdown & Protocol Analysis

- [ ] **C1: DNS Analysis**
  - Document query packet (Source, Destination UDP 53, query name).
  - Document response packet (Answer IP, TTL = 30 seconds).
- [ ] **C2: TCP 3-Way Handshake Analysis**
  - Document SYN packet (Client ephemeral port $\to$ Server 443, initial Seq).
  - Document SYN-ACK packet (Server $\to$ Client, Ack = Seq + 1).
  - Document ACK packet (Client $\to$ Server, completing connection).
- [ ] **C3: TLS Handshake & Application Data**
  - Document ClientHello (SNI hostname, cipher suites).
  - Document ServerHello, Certificate, and Key Exchange.
  - Document ChangeCipherSpec and subsequent encrypted Application Data records.

---

## Section D: Caching & Fault Tolerance

- [ ] **D1:** Paste response headers from `/api/cache` showing `Cache-Control: public, max-age=60` and `ETag`.
- [ ] **D2:** Explain client-side caching mechanism and paste conditional request returning `HTTP 304 Not Modified`.
- [ ] **D3: Failure Demonstration:**
  - Show active load balancing across A and B.
  - Stop Backend A process.
  - Execute requests showing seamless failover to Backend B.
  - Explain why DNS and TLS remain unaffected (application layer failure isolation).
  - Restart Backend A and demonstrate recovery.
