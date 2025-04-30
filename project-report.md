# AWS Threat Detection & Auto-Response Project – Report

## 📌 1. Problem Statement

Cloud environments are increasingly targeted by attackers due to misconfigurations, unpatched systems, and exposed services. Many teams struggle with delayed responses to known threats due to the lack of centralized detection and automation.

**Goal**: 
Build an automated detection and response system using AWS-native tools to immediately alert and remediate EC2-related security threats.

---

## 🧱 2. System Design

The architecture uses several AWS security services working together to detect, aggregate, and respond to high-severity issues.

### Key Components:

| Component         | Purpose                                                                 |
|------------------|-------------------------------------------------------------------------|
| Amazon EC2        | Target instance to simulate vulnerabilities                             |
| GuardDuty         | Detects suspicious activities (e.g., port scanning, root usage)         |
| Inspector         | Scans for software vulnerabilities and missing patches                  |
| Macie             | Detects sensitive data (e.g., emails, SSNs) in S3 buckets               |
| AWS Config        | Tracks resource compliance (e.g., public S3 buckets, public IPs)        |
| Security Hub      | Centralizes findings from all services                                  |
| EventBridge       | Monitors Security Hub for HIGH/CRITICAL alerts                          |
| Lambda            | Stops EC2 instance in response to threats                               |
| SNS (Optional)    | Sends email notifications                                               |

---

## ⚙️ 3. Implementation

### Phase 1: Setup
- Launched EC2 (Amazon Linux 2, `t2.micro`)
- Created and attached Security Group with public SSH access (for testing GuardDuty)
- Enabled GuardDuty, Inspector, Macie, Config, and Security Hub
- Linked all services to Security Hub for central monitoring

### Phase 2: Alerting & Remediation
- Created SNS topic and email subscription
- Built a Lambda function in Python to:
  - Parse Security Hub findings
  - Identify EC2 instance IDs
  - Stop the associated instance
- Created EventBridge rule to trigger Lambda when Security Hub receives HIGH/CRITICAL findings

---

## 🔬 4. Simulated Scenarios

| Simulation                          | Expected Detection                    | Outcome                     |
|------------------------------------|----------------------------------------|-----------------------------|
| Opened SSH to `0.0.0.0/0`          | GuardDuty flagged as risky            | Security Hub triggered      |
| Uploaded fake SSNs to S3 bucket    | Macie detected sensitive data         | Finding showed in dashboard |
| Left EC2 unpatched                 | Inspector reported vulnerabilities     | Lambda triggered and stopped instance |
| Used AWS Root API actions          | GuardDuty flagged misuse              | Reflected in Security Hub   |

---

## ✅ 5. Results

- 🔒 Security Hub successfully collected findings from all sources
- ⚙️ Lambda executed automatically upon critical findings
- 🛑 EC2 instance was stopped automatically as part of remediation
- 📧 Email notifications received via SNS

---

## 📸 6. Evidence

Screenshots and sample data are stored in the [`/screenshots`](./screenshots) and [`/architecture`](./architecture) folders.

---

## 📈 7. Lessons Learned

- AWS-native tools are powerful but require correct IAM roles and region-aware configuration.
- Not all findings are actionable without customization (e.g., need to parse EC2 instance IDs from findings).
- Sample findings from GuardDuty are helpful for testing but need mapping for automation logic.
- Real-time automation is achievable with little to no cost using AWS Free Tier.

---

## 💡 8. Possible Enhancements

- Isolate EC2 instance instead of stopping it (e.g., apply a "quarantine" security group)
- Store all findings in DynamoDB for later analysis
- Add dashboard visualization using QuickSight or Grafana
