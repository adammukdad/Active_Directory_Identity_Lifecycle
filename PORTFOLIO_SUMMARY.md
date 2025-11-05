## 🧭 **Portfolio Summary – Project 1: Active Directory & Identity Lifecycle**

**Author:** Adam Mukdad  
**Focus:** Identity Lifecycle Management (Core + Azure Add-on)

---

### 🧩 **Project Overview**
This project simulates a **complete identity lifecycle** — from *hire* → *change* → *terminate* — using a **vendor-neutral Active Directory mock dataset**.  
It was designed for reproducibility and audit clarity, with a dry-run simulation and a parallel **Azure Entra ID PowerShell/Graph** implementation.

---

### ⚙️ **Key Features**
- 🧱 Structured folder layout (`/data`, `/scripts`, `/azure`, `/docs`)  
- 🧩 Mock lifecycle data via `users.csv`, `groups.csv`, `mapping.json`  
- 🔁 Python script (`simulate_lifecycle.py`) simulating account transitions  
- ☁️ Azure Entra ID variant using **Microsoft Graph PowerShell**  
- 📄 Documentation-first approach: diagram + README built automatically

---

### 🧠 **Core Skills Demonstrated**
- Identity lifecycle orchestration  
- AD → Entra ID mapping and automation  
- Microsoft Graph authentication + module setup  
- PowerShell 7.x environment configuration  
- Secure provisioning and de-provisioning logic

---

### 💡 **Next Steps**
In the next phase, extend this simulation with **role-based access control (RBAC)** and **Just-In-Time (Privileged Access Management)** modeling.
