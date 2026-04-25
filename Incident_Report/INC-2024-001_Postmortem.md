# 📋 Post-Incident Review (Postmortem): INC-2024-001
**Meeting Date:** 2024-10-28
**Attendees:** SOC L1 Analyst, SOC L2 Analyst, Security Engineering Lead
**Facilitator:** Shriraksha Kulkarni

---

## 1. What Happened? (5-minute summary)

On 2024-10-25 at 08:15 UTC, our CSPM tool detected a critical cloud misconfiguration: a production server had its RDP port (3389) exposed to the entire internet. This allowed a known threat actor to perform a brute-force attack against the server. The SOC team detected the attack via SIEM, enriched the attacker's IP using an automated SOAR playbook (VirusTotal API), contained the threat by blocking the IP, and remediated the root cause by enforcing Just-In-Time access — all within 45 minutes.

---

## 2. What Went Well? ✅

- **Fast Detection:** SIEM alert fired within 7 minutes of the CSPM alert being generated.
- **Effective Automation:** The automated SOAR enrichment script immediately identified the attacker IP as HIGH-priority, cutting manual investigation time significantly.
- **Clear Escalation:** L1 → L2 handoff was clean and well-documented.
- **Full Visibility:** Sysmon logs on the endpoint provided full process-level telemetry for forensic analysis.

---

## 3. What Went Wrong / Could Be Better? ❌

| Issue | Impact | Owner |
|---|---|---|
| CSPM alert was not auto-ingested into the SIEM | Delayed alert correlation by ~7 minutes | Security Engineering |
| No automated blocking playbook existed | Required manual firewall rule creation from L2 | SOC / Automation Team |
| No alerting on brute-force RDP prior to this incident | Attack went undetected in the scanning phase | Detection Engineering |

---

## 4. Action Items (with owners & due dates)

| # | Action | Owner | Due Date |
|---|---|---|---|
| 1 | Build a SIEM connector to auto-ingest all CSPM CRITICAL alerts | Security Engineering | 2024-11-08 |
| 2 | Create an automated firewall block playbook for HIGH-priority IPs identified by SOAR | SOC Automation | 2024-11-15 |
| 3 | Deploy a brute-force RDP detection rule (>10 failed logins/10 min) across all VMs | Detection Engineering | 2024-11-01 |
| 4 | Enforce Azure Policy to deny internet-facing management ports on all production subscriptions | Cloud Engineering | 2024-11-22 |

---

## 5. Benchmark Metrics (Before vs. After)

| Metric | Before This Incident | Target (Post-Remediation) |
|---|---|---|
| Manual IP Triage Time | ~8 minutes/alert | <1 minute (automated) |
| CSPM → SIEM Alert Lag | ~7 minutes | <1 minute (auto-ingestion) |
| RDP Exposure Detection | Not monitored | Real-time (new alert rule) |

---

## 6. Conclusion

This incident demonstrated both the effectiveness of our detection pipeline and the gaps in our automation coverage. By implementing the four action items above, we will significantly reduce our Mean Time to Detect (MTTD) and Mean Time to Respond (MTTR) for similar cloud misconfiguration-based attacks in the future.
