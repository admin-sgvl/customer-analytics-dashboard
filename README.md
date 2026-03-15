# 🎯 Predictive Customer Insights & RFM Engine - Version: 1.0.0

A professional-grade Data Science application that transforms raw transaction logs into a strategic marketing roadmap. This tool categorizes customers by value and uses probabilistic modeling to predict future churn.

## 🚀 Key Features
- **Automated Data Sanitization:** An intelligent "gatekeeper" that cleans date formats, removes duplicates, and handles invalid transaction entries.
- **RFM Segmentation:** Automatically segments customers into behavioral groups:
    - **Champions:** High-value, frequent, recent buyers.
    - **At Risk:** Previously loyal customers who haven't returned recently.
    - **Hibernating:** Low-value, infrequent customers.
- **Predictive Analytics (BG/NBD):** Calculates the **P(Alive)** score—the statistical probability that a customer is still active—and predicts expected purchases over the next 30 days.
- **Interactive Visualization:** Executive-level treemaps and KPI metrics for at-a-glance business health checks.
- **Actionable Exports:** Filter by segment and download targeted CSV lists for direct integration with email marketing tools (Mailchimp, HubSpot, etc.).

---

## 📂 Data Requirements
The application is "plug-and-play." To use it, upload a CSV file with these exact column headers:

| Column | Description | Format Example |
| :--- | :--- | :--- |
| `CustomerID` | Unique identifier for the client | `C-1001` or `email@domain.com` |
| `TransactionDate` | Date the purchase occurred | `YYYY-MM-DD` |
| `TransactionAmount` | The total value of the sale | `150.50` |

---

## 🛠️ Quick Start

### 1. Local Setup
1. **Clone the repository** to your local machine.
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt


## By using this tool, companies can move from "Mass Marketing" to "Precision Marketing":

- Reduce Churn: Identify "At Risk" customers before they leave.

- Optimize Spend: Focus ad budget on "Promising" segments rather than "Hibernating" ones.

- Increase LTV: Use predictions to time "We Miss You" offers perfectly.


### Final Project Checklist
This project consists of the following:
1.  **`app.py`**: The "Brain" (The logic and UI).
2.  **`requirements.txt`**: The "Environment" (The libraries).
3.  **`generate_data.py`**: The "Demo" (The fake data).
4.  **`README.md`**: The "Manual" (The explanation).

**Since we've completed the full RFM and Predictive suite, would you like me to help you draft the email or presentation text to send to a potential client or your manager to introduce them to this tool?**

### Developed by: SG Venture Consulting's Data Science Team

### Principal Consultant: Patrick Oh

