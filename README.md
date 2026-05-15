# Financial Leverage & Risk Simulator

This version is based on the uploaded preferred `app.py` file and only changes EBIT from lakhs to crores.

## Main update

- EBIT slider unit changed from `₹ lakh` to `₹ crore`
- EBIT range changed to `₹0 crore` to `₹20 crore`
- EBIT step changed to `₹1 crore`
- Backend calculation still uses lakh internally, so the selected EBIT in crore is converted as: `EBIT lakh = EBIT crore × 100`
- Scenario card and comparison table display EBIT, PBT, and PAT in crores for consistency

## Fixed assumptions

- Capital Employed: ₹100 crore
- Interest Rate: 10%
- Tax Rate: 30%
- Maximum Debt: 90%

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```
