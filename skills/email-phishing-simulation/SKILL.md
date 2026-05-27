---
name: email-phishing-simulation
description: - Measuring employee susceptibility to phishing attacks as part of a security awareness program - Testing the effectiveness of email security controls (secure email gateway, DMARC, SPF, DKIM) - Conducting the social engineering component of a red team exercise to gain initial access - Establishing a baseline for phishing susceptibility before deplo
domain: cybersecurity
---
---|------------|
| **Pretext** | The fabricated scenario and social context used to persuade the target to take a desired action such as clicking a link or entering credentials |
| **Credential Harvesting** | Collecting usernames and passwords through fake login pages that mimic legitimate services |
| **GoPhish** | Open-source phishing simulation platform that manages email templates, landing pages, target groups, and campaign tracking |
| **Spear Phishing** | Targeted phishing directed at specific individuals using personalized information gathered through reconnaissance |
| **Typosquatting** | Registering domains that are visually similar to legitimate domains through character substitution, addition, or omission |
| **Security Awareness** | Training programs designed to educate employees about social engineering threats and proper reporting procedures |
| **DMARC** | Domain-based Message Authentication, Reporting, and Conformance; email authentication protocol that prevents unauthorized use of a domain for sending email |

## Tools & Systems

- **GoPhish**: Open-source phishing simulation framework providing campaign management, email templates, landing pages, and detailed analytics
- **Evilginx2**: Advanced phishing framework capable of capturing session tokens and bypassing multi-factor authentication through reverse proxy technique
- **King Phisher**: Phishing campaign toolkit with advanced features including two-factor authentication testing and geolocation tracking
- **SET (Social Engineering Toolkit)**: Framework for social engineering attacks including phishing, credential harvesting, and payload delivery

## Common Scenarios

### Scenario: Enterprise Phishing Simulation for Security Awareness Baseline

**Context**: A 2,000-employee company has never conducted a phishing simulation. The CISO wants to establish a baseline susceptibility rate before deploying a new security awareness training program. The campaign should test all employees using a realistic but not overly sophisticated pretext.

**Approach**:
1. Develop a Microsoft 365 password expiration pretext: "Your password expires in 24 hours. Click here to update."
2. Register `m365-targetcorp.com`, set up GoPhish, and build a landing page cloning the Microsoft 365 login portal
3. Import all 2,000 employee emails and schedule sends in batches of 100 over 20 hours
4. Campaign results after 72 hours: 1,847 delivered (92.4%), 1,243 opened (67.3%), 487 clicked (26.4%), 312 submitted credentials (16.9%), 23 reported to IT (1.2%)
5. Analysis reveals Finance (28% submission) and Marketing (24% submission) have the highest susceptibility; IT department has the lowest (4%)
6. Recommend targeted training for high-susceptibility departments, phishing report button deployment, and quarterly simulation cadence

**Pitfalls**:
- Using overly aggressive or threatening pretexts that cause employee anxiety or legal issues
- Not coordinating with HR and legal before launching the campaign, risking employee relations problems
- Sending all emails simultaneously, overwhelming the email server or triggering bulk-send detection
- Focusing only on click and submission rates while ignoring the critically low report rate (1.2%)

## Output Format

```
## Phishing Simulation Campaign Report

**Campaign Name**: Q4 2025 Baseline Phishing Assessment
**Pretext**: Microsoft 365 Password Expiration Notice
**Campaign Duration**: November 15-18, 2025
**Target Population**: 2,000 employees (all departments)

### Campaign Metrics
| Metric | Count | Rate |
|--------|-------|------|
| Emails Sent | 2,000 | 100% |
| Emails Delivered | 1,847 | 92.4% |
| Emails Opened | 1,243 | 67.3% |
| Links Clicked | 487 | 26.4% |
| Credentials Submitted | 312 | 16.9% |
| Reported to IT | 23 | 1.2% |

### Department Breakdown
| Department | Employees | Clicked | Submitted | Reported |
|------------|-----------|---------|-----------|----------|
| Finance    | 120       | 38.3%   | 28.3%     | 0.8%     |
| Marketing  | 85        | 35.3%   | 24.7%     | 1.2%     |
| Engineering| 300       | 15.0%   | 8.3%      | 3.7%     |
| IT         | 45        | 8.9%    | 4.4%      | 11.1%    |

### Key Findings
1. Baseline credential submission rate of 16.9% exceeds industry average (12%)
2. Report rate of 1.2% indicates employees are not trained to report suspicious emails
3. Finance department is the highest-risk group with 28.3% credential submission rate
4. Email security gateway did not flag the phishing domain despite being registered 48 hours prior

### Recommendations
1. Deploy mandatory security awareness training with emphasis on phishing identification
2. Install a phishing report button in email clients and train all employees on its use
3. Implement DMARC enforcement (p=reject) and enhanced email filtering rules
4. Conduct targeted training for Finance and Marketing departments
5. Schedule quarterly phishing simulations to track improvement
```