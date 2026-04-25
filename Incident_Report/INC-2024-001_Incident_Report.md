# 🛡️ Incident Report: INC-2024-001
**Classification:** CONFIDENTIAL — Internal SOC Use Only

---

## 1. Incident Summary

| Field | Details |
|---|---|
| **Incident ID** | INC-2024-001 |
| **Title** | Cloud Misconfiguration Exploited — RDP Brute Force & Suspicious C2 Beacon |
| **Severity** | HIGH |
| **Status** | Closed — Remediated |
| **Date Detected** | 2024-10-25 |
| **Analyst (L1)** | Shriraksha Kulkarni |
| **Escalated To (L2)** | SOC Team Lead |

---

## 2. Incident Timeline

| Time (UTC) | Event |
|---|---|
| 08:15 | **CSPM Alert (Wiz/Mock):** `Prod-Web-Server-01` has Port 3389 (RDP) open to 0.0.0.0/0 — severity CRITICAL. |
| 08:22 | **SIEM Alert Fired (Splunk):** Detection Rule `CSPM - Critical Cloud Misconfiguration Detected` triggered. |
| 08:25 | **L1 Triage:** Analyst reviewed the Splunk alert. Confirmed resource is a production web server. |
| 08:30 | **Threat Hunting:** SPL query run to detect failed RDP logon attempts — 47 failures from IP `5.188.86.172` in 10 minutes. |
| 08:35 | **SOAR Enrichment:** Automated Python playbook queried VirusTotal API for `5.188.86.172`. |
| 08:36 | **Enrichment Result:** IP flagged as HIGH priority — 2 malicious flags, 1 suspicious flag. Escalated to L2. |
| 08:45 | **Containment:** Firewall rule applied — IP `5.188.86.172` blocked. RDP port restricted to VPN IP range only. |
| 09:00 | **Remediation:** Just-In-Time (JIT) access enabled on the VM. CSPM alert closed. |

---

## 3. Root Cause Analysis

The initial root cause was a **Cloud Misconfiguration**: the Network Security Group (NSG) associated with `Prod-Web-Server-01` had an inbound rule allowing **all traffic (0.0.0.0/0)** on port **3389 (RDP)**. This was detected by the Cloud Security Posture Management (CSPM) tool.

This exposed port allowed an external threat actor at IP `5.188.86.172` to launch a **credential brute-force attack** against the server. The attacker made 47 failed login attempts within a 10-minute window.

---

## 4. Attack Chain (MITRE ATT&CK)

| Stage | Technique ID | Technique Name |
|---|---|---|
| **Reconnaissance** | T1595 | Active Scanning |
| **Initial Access** | T1110.001 | Brute Force: Password Guessing |
| **Execution (Attempted)** | T1059.001 | Command and Scripting Interpreter: PowerShell |
| **C2 (Potential)** | T1071 | Application Layer Protocol |

---

## 5. Containment & Remediation Actions

- **Immediate:** Blocked attacker IP `5.188.86.172` at the network perimeter.
- **Short-term:** Restricted RDP access (port 3389) to the organization's VPN IP range only.
- **Long-term:** Enabled Azure Just-In-Time (JIT) VM access — port 3389 is now closed by default and only opens on-demand for approved user sessions.
- **Process:** Created a new Splunk alert rule for brute-force RDP detection (>10 failed logins in 10 minutes).

---

## 6. Key Metrics

| Metric | Value |
|---|---|
| **Time to Detect (TTD)** | 7 minutes |
| **Time to Triage (TTT)** | 10 minutes |
| **Time to Contain (TTC)** | 30 minutes |
| **Time to Remediate (TTR)** | 45 minutes |

---

## 7. Lessons Learned

1. CSPM alerts must be integrated into the SIEM alert pipeline with automatic ticket creation.
2. Automated IP enrichment via SOAR reduced L1 investigation time by an estimated **70%** compared to manual lookups.
3. Production VMs should never have management ports open to the internet — enforce via Cloud Policy.
