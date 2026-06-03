<div align="center">

# 🛡️ CHAKRAVYUHA 1.0: Real-Time Digital Evidence Vault
### *Agent SAKSHI — The Phantom*

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=24&pause=1000&color=00FF99&center=true&vCenter=true&width=600&lines=Silent+Stenographer;Always-On+Forensic+Monitor;Real-Time+Threat+Detection;Tamper-Proof+Evidence+Vault" alt="Typing SVG" />

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)](#)
[![FastAPI](https://img.shields.io/badge/Routing-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](#)
[![React](https://img.shields.io/badge/Frontend-React-61DAFB?style=for-the-badge&logo=react&logoColor=black)](#)
[![MongoDB](https://img.shields.io/badge/Database-MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](#)

*Empowering Law Enforcement with Instant, Tamper-Proof Digital Evidence.*

</div>

<br/>

## 🚨 The Problem: Ephemeral Evidence in Cybercrime
When a cybercrime occurs, there is a critical delay between the attack and the formal investigation. During this window, attackers erase logs, clear histories, and destroy valuable digital evidence. By the time the Cybercrime Investigation Unit steps in, the trail is cold. 
**Key Pain Points:**
- **Zero Real-Time Capture:** No mechanism to freeze evidence at the moment of compromise.
- **Fragmented Reporting:** Bureaucratic delays before technical investigation begins.
- **Data Tampering:** Device logs are easily deleted by malicious actors.

---

## 💡 Our Ideology & Solution
**Agent SAKSHI** is a lightweight, strictly permissioned, ethical background agent designed to act as a **"Silent Stenographer"**. 

It passively monitors the system using a 30-minute rolling buffer. The moment anomalous behavior is detected (e.g., suspicious process spikes, multiple login failures, unauthorized network tunneling), SAKSHI instantly crystallizes the last 30 minutes of telemetry, captures screenshots, and packages them into a **Tamper-Proof, SHA-256 Hashed Evidence Vault**. It immediately alerts the user via an OS-level SOS Toast and dispatches encrypted evidence strictly to verified investigators.

---

## 🏛️ System Architecture

Our agent follows a highly optimized, cross-platform pipeline designed for instant triggering with zero persistence of sensitive unencrypted user data.

```mermaid
graph TD
    classDef core fill:#5A67D8,stroke:#4C51BF,stroke-width:2px,color:#fff;
    classDef monitor fill:#2C7A7B,stroke:#285E61,stroke-width:2px,color:#fff;
    classDef buffer fill:#4A5568,stroke:#2D3748,stroke-width:2px,color:#fff;
    classDef detector fill:#B7791F,stroke:#975A16,stroke-width:2px,color:#fff;
    classDef vault fill:#822727,stroke:#63171B,stroke-width:2px,color:#fff;
    classDef alert fill:#2B6CB0,stroke:#2C5282,stroke-width:2px,color:#fff;

    A[ Phantom Capture Agent <br/> Silent stenographer · always on ]:::core

    A --> B[ Device Monitor <br/> OS, apps, clipboard ]:::monitor
    A --> C[ Network Monitor <br/> DNS, IP, transfers ]:::monitor
    A --> D[ Baseline AI <br/> Learns normal behaviour ]:::monitor
    A --> E[ Screenshot <br/> Evidence capture ]:::monitor

    B --> F[ 30-min Rolling Buffer <br/> CSV · overwritten · SHA-256 ]:::buffer
    C --> F
    D --> G[ Anomaly Detector <br/> Flags suspicious events ]:::detector

    F --> H[ Permanent Evidence Vault <br/> SHA-256 hashed · tamper-proof CSV · root path logged ]:::vault
    G --> H
    E ---> H

    H --> I[ Shamir 5-Shard Split <br/> 3-of-5 reconstruction ]:::core
    H --> J[ Auto Email Alert <br/> SHA encoded payload ]:::vault
    H --> K[ OS Notification <br/> Link ➔ portal + SOS button ]:::alert
```

---

## 🗄️ Database Connection Schema 
The backend connects to MongoDB mimicking the structure of a high-security vault. Collections include:
- `Users`: Encrypted demographics and law-enforcement ID mappings.
- `Incidents`: Stores trigger conditions, metadata, temporal bounds, and IP logs.
- `EvidenceHashes`: An append-only ledger storing the SHA-256 signatures of evidence ZIPs to prevent mid-flight tampering (serving as a blockchain-lite mechanism).

---

## 🛠️ Setup & Local Deployment

Get the Phantom up and running on your local machine instantly:

```bash
# 1. Clone the repository
git clone https://github.com/poojamurugan23/CyberShield-project.git
cd CyberShield-project

# 2. Navigate to the agent branch
git checkout Agent-Sakshi-The-PHANTOM

# 3. Create a virtual environment & activate it
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 4. Install Core Engine dependencies
pip install -r requirements.txt

# 5. Build Environment Variables
cp .env.example .env
# Edit .env and supply your SMTP configurations 

# 6. Execute the Agent (Demo Attack Simulation Mode)
python -m agent.main run --demo
# (Watch as the phantom detects, crystallizes, and notifies you instantly!)
```

### 📂 Folder Structure
```bash
Backend Agent V1/
├── agent/
│   ├── main.py         # 🚀 Core Execution Loop & Process Shield
│   ├── config.py       # ⚙️ Constants & Configuration Loader  
│   ├── monitor.py      # 👁️ Telemetry, Port & Process Watcher
│   ├── detector.py     # 🧠 Anomaly Detection & Logic Engine
│   ├── evidence.py     # 📦 Crystallization & Vault Packaging
│   ├── hasher.py       # 🔐 SHA-256 Anti-Tamper Verification
│   ├── emailer.py      # 📧 Encrypted Transmission Pipeline
│   └── notifier.py     # 🔔 High-Priority OS SOS Notifications
├── logs/               # 🔄 Ephemeral 30-min Rolling Buffers
├── evidence/           # 🛑 Permanent Tamper-Proof Archives
├── config.json         # 🎛️ Tunable Thresholds & Preferences
└── requirements.txt    # 📦 Dependency Manifest
```

---

<div align="center">

## 👥 Hackathon Squad: Hawkins Hacker
**University College of Engineering, Kanchipuram**

<br/>

<table>
  <tr>
    <td align="center">
      <img src="https://media.giphy.com/media/LmNwrBhejkK9EFP504/giphy.gif" width="60" alt="Security"/>
    </td>
    <td>
      <b>Kiruthigaa Rajkumar</b><br/>
      <i>System Security Implementation and Core Logic Development</i>
    </td>
    <td align="center">
      <img src="https://media.giphy.com/media/WUlplcMpOCEmTGBtBW/giphy.gif" width="60" alt="UI/UX"/>
    </td>
    <td>
      <b>Pooja Murugan</b><br/>
      <i>UI/UX Design and User Interaction Experience</i>
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="https://media.giphy.com/media/qgQUggCGvnkNC/giphy.gif" width="60" alt="Research"/>
    </td>
    <td>
      <b>Pavithra Balamurugan</b><br/>
      <i>Research Analysis and Technical Documentation</i>
    </td>
    <td align="center">
      <img src="https://media.giphy.com/media/L1R1tvI9svkIWwpVYr/giphy.gif" width="60" alt="Architecture"/>
    </td>
    <td>
      <b>Archana Muruganantham</b><br/>
      <i>Overall System Architecture Design and Integration</i>
    </td>
  </tr>
</table>

<br/>

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=20&pause=2000&color=F7FAFC&center=true&vCenter=true&width=500&lines=Forged+during+CHAKRAVYUHA+1.0;24+Hours+of+Relentless+Coding;Protecting+the+Digital+Frontier" alt="Footer Typing SVG" />

</div>
