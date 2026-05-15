# Financial Leverage & Risk Simulator

**Developed by Dr. Nitin Dhir**

A professional, scenario-based financial leverage simulator built with **Python, Streamlit, Plotly, and Pandas**.

This project is designed for **classroom teaching, interview demonstration, and LinkedIn portfolio showcase**. It helps users understand how different debt levels and EBIT assumptions affect profitability, return on equity, interest coverage, financial leverage, and risk level.

---

## Project Purpose

The main objective of this simulator is to demonstrate the practical impact of **financial leverage** on business performance and risk.

In finance, the use of debt can increase returns for shareholders when profits are strong, but it can also increase financial risk when earnings are weak. This simulator allows users to compare three capital structure scenarios side by side and observe how leverage affects key financial indicators.

This project is useful for:

- Commerce and management classroom teaching
- Finance subject demonstrations
- Interview presentations
- LinkedIn portfolio projects
- Business analytics and financial modelling demonstrations
- Explaining capital structure decisions in a simple visual way

---

## Live App

After deployment on Streamlit Community Cloud, add your app link here:

```text
https://your-app-name.streamlit.app
```

---

## Key Features

### 1. Three Scenario Comparison

The simulator compares three scenarios simultaneously:

- Scenario 1
- Scenario 2
- Scenario 3

Each scenario has independent inputs for:

- Debt Percentage
- EBIT

This makes it easy to compare conservative, moderate, and aggressive financing structures.

---

### 2. Fixed Business Assumptions

The simulator uses the following fixed assumptions:

| Assumption | Value |
|---|---:|
| Capital Employed | ₹100 crore |
| Interest Rate | 10% |
| Tax Rate | 30% |
| Maximum Debt Percentage | 90% |

These assumptions keep the simulator simple and focused on the effect of debt and EBIT.

---

### 3. EBIT Input in Crores

EBIT is entered using a slider:

| Input | Range |
|---|---:|
| EBIT | ₹0 crore to ₹20 crore |
| Step | ₹1 crore |

Internally, the app converts EBIT from crore to lakh for consistency with backend calculations.

---

### 4. Debt Percentage Input

Debt percentage is entered using a number input:

| Input | Range |
|---|---:|
| Debt Percentage | 0% to 90% |
| Step | 10% |

Debt is capped at 90% to avoid unrealistic 100% debt financing and divide-by-zero issues in ROE calculation.

---

### 5. Scenario Summary Cards

Each scenario displays a professional summary card containing:

- Debt
- Equity
- Interest
- PBT
- PAT
- ROE
- Interest Coverage Ratio
- Degree of Financial Leverage
- Risk Level

---

### 6. Detailed Scenario Comparison Table

The dashboard includes a full comparison table showing all important values across the three scenarios.

The table includes:

| Column | Meaning |
|---|---|
| Scenario | Scenario name |
| Capital Employed | Fixed capital base |
| Debt % | Debt percentage selected |
| Debt | Debt amount |
| Equity | Equity amount |
| EBIT | Earnings before interest and tax |
| Interest | Interest cost |
| PBT | Profit before tax |
| PAT | Profit after tax |
| ROE | Return on equity |
| ICR | Interest coverage ratio |
| DFL | Degree of financial leverage |
| Risk Level | Safe, Moderate, or High Risk |

---

### 7. Risk Gauges

Each scenario has a risk gauge with a score from 0 to 100.

| Risk Score Range | Interpretation |
|---:|---|
| 0–35 | Safe |
| 36–70 | Moderate |
| 71–100 | High Risk |

Risk score is based on the Interest Coverage Ratio.

---

### 8. Debt vs Equity Donut Charts

Each scenario includes a donut chart showing the debt-equity composition.

This helps users visually understand how capital structure changes across scenarios.

---

## Financial Logic Used

### 1. Capital Employed

```text
Capital Employed = ₹100 crore
```

The app internally converts capital employed into lakhs:

```text
₹100 crore = ₹10,000 lakh
```

---

### 2. Debt

```text
Debt = Capital Employed × Debt Percentage
```

---

### 3. Equity

```text
Equity = Capital Employed − Debt
```

---

### 4. Interest

```text
Interest = Debt × Interest Rate
```

Interest rate is fixed at:

```text
10%
```

---

### 5. Profit Before Tax

```text
PBT = EBIT − Interest
```

---

### 6. Tax

Tax rate is fixed at:

```text
30%
```

Tax is applied only when PBT is positive:

```text
If PBT > 0:
    Tax = PBT × 30%

If PBT <= 0:
    Tax = 0
```

---

### 7. Profit After Tax

```text
PAT = PBT − Tax
```

---

### 8. Return on Equity

```text
ROE = PAT ÷ Equity × 100
```

---

### 9. Interest Coverage Ratio

```text
ICR = EBIT ÷ Interest
```

ICR shows how many times EBIT can cover interest obligations.

---

### 10. Degree of Financial Leverage

```text
DFL = EBIT ÷ PBT
```

DFL shows the sensitivity of profits to changes in operating earnings.

---

## Risk Classification Rule

Risk level is based on the Interest Coverage Ratio.

| Interest Coverage Ratio | Risk Level |
|---:|---|
| Above 3.00x | Safe |
| 1.50x to 3.00x | Moderate |
| Below 1.50x | High Risk |

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web app framework |
| Plotly | Interactive charts and gauges |
| Pandas | Data handling and scenario table |
| HTML/CSS | Professional dashboard styling |
| GitHub | Code hosting |
| Streamlit Community Cloud | Free app deployment |

---

## Project Structure

```text
financial-leverage-simulator/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Installation and Local Setup

### Step 1: Install Python

Install Python 3.10 or above.

During installation, select:

```text
Add Python to PATH
```

---

### Step 2: Download or Clone the Repository

Using Git:

```bash
git clone https://github.com/your-username/financial-leverage-simulator.git
cd financial-leverage-simulator
```

Or download the ZIP file and extract it.

---

### Step 3: Install Required Libraries

Run this command inside the project folder:

```bash
pip install -r requirements.txt
```

---

### Step 4: Run the Streamlit App

```bash
streamlit run app.py
```

The app will open in your browser at:

```text
http://localhost:8501
```

---

## Requirements File

The `requirements.txt` file should contain:

```text
streamlit
pandas
plotly
```

---

## Deployment on Streamlit Community Cloud

### Step 1: Create a GitHub Repository

Create a new public GitHub repository.

Suggested repository name:

```text
financial-leverage-simulator
```

---

### Step 2: Upload Project Files

Upload the following files:

```text
app.py
requirements.txt
README.md
.gitignore
```

---

### Step 3: Open Streamlit Community Cloud

Go to Streamlit Community Cloud and sign in using your GitHub account.

---

### Step 4: Create a New App

Click:

```text
New app
```

---

### Step 5: Select Repository

Choose your GitHub repository.

Example:

```text
financial-leverage-simulator
```

---

### Step 6: Select Main File

Set the main file path as:

```text
app.py
```

---

### Step 7: Deploy

Click:

```text
Deploy
```

After deployment, Streamlit will generate a public app link.

---

## Suggested Screenshot Section

After deploying or running the app locally, add screenshots here.

### Dashboard Preview

```text
Add screenshot of the main dashboard here.
```

### Scenario Summary Cards

```text
Add screenshot of scenario cards here.
```

### Risk Gauges

```text
Add screenshot of risk gauges here.
```

### Debt vs Equity Donut Charts

```text
Add screenshot of donut charts here.
```

---

## Suggested LinkedIn Caption

```text
I developed a Financial Leverage & Risk Simulator using Python, Streamlit, Plotly, and Pandas.

The simulator compares three capital structure scenarios and shows how debt percentage and EBIT affect interest cost, profit before tax, profit after tax, return on equity, interest coverage ratio, degree of financial leverage, and risk level.

This project was designed for classroom teaching, interview demonstration, and financial decision analysis.

It combines finance concepts with interactive analytics and demonstrates how business decisions can be explained through data-driven simulation.
```

---

## Use Cases

This simulator can be used for:

- Teaching financial leverage
- Explaining capital structure
- Demonstrating debt risk
- Showing the effect of interest burden
- Comparing financing scenarios
- Discussing ROE improvement and risk trade-off
- Interview portfolio demonstration
- LinkedIn project showcase

---

## Educational Value

This simulator helps students understand that debt is not always bad and equity is not always risk-free. The impact of leverage depends on the relationship between:

- EBIT
- Interest cost
- Debt level
- Equity base
- Tax impact
- Coverage capacity

A firm may show higher ROE under higher leverage, but the same leverage can also increase financial risk if EBIT is not sufficient to cover interest obligations.

---

## Important Notes

- This simulator is for academic and educational demonstration only.
- It is not intended to provide financial, investment, or credit advice.
- The assumptions are simplified for teaching purposes.
- Real company analysis should include additional factors such as cash flows, repayment schedules, industry risk, liquidity, working capital, debt maturity, and macroeconomic conditions.

---

## Future Improvements

Possible future upgrades:

- Add company data upload option
- Add Excel export
- Add PDF report generation
- Add real company comparison
- Add sensitivity analysis
- Add operating leverage module
- Add combined leverage module
- Add break-even analysis
- Add Monte Carlo simulation
- Add industry benchmark comparison
- Add login-based student access
- Add AI-generated interpretation

---

## License

This project is intended for academic and demonstration purposes.

You may add a license later, such as:

```text
MIT License
```

---

## Author

**Dr. Nitin Dhir**

Financial Leverage & Risk Simulator  
Academic Demonstration and Financial Decision Analysis Project
