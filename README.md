# Credit Risk Mortgage Stress Test
Use python creating synthetic loan records with metrics related to Expected Loss modelling and analysing stress scenario.
Mortgage Portfolio Stress Test

This project shows how a 15% shock to the housing market translates into an increase in credit risk for a bank’s mortgage portfolio. I used a Python framework to simulate 10,000 loans and model the downturn’s impact on key metrics: **PD**, **LGD**, and **IFRS-9** loan staging. The core mechanism is the **Loan-to-Value (LTV)** ratio, where the drop in housing prices pushes loans into zero or negative equity.

_IFRS-9 is the accounting standard that classifies loans into three stages (performing, underperforming, and credit-impaired) and requires banks to recognise Expected Credit Losses on each stage – International Accounting Standards Board (IASB)_

The final dashboard (using Looker Studio) and charts are explained alongside with how banks may enhance their models, whereas these results only mimic portfolio behaviour.

# Results & Visualisations from Looker Studio

After exporting the dataframe from Python as a csv file, I visualised some core metrics in Looker. The charts below illustrate the baseline KPIs alongside the stress KPIs.

The dashboard highlights how the **15% decline in property value** impacted the Expected Loss. It increased around +230% in this model, and it was due to higher LTV ratios but mainly due to the Stage migrations, Stage 1 to Stage 2.

<img width="235" height="183" alt="image" src="https://github.com/user-attachments/assets/23e3039c-f8c8-403b-8ab7-2a8554920031" />
<img width="251" height="148" alt="image" src="https://github.com/user-attachments/assets/fa06b9ab-67f7-4d50-a840-6a82ceb9bbe1" />

As LTV rises, PD reacts disproportionately, and the IFRS-9 rules amplify that effect by forcing loans to migrate into a stage with increased chance of defaulting. Once a loan enters the **underperforming stage**, the bank must recognise a **lifetime Expected Loss** instead of a 12-month one, by taking the PD over the remaining contractual lifetime – this is also why a small housing shock produces such a drastic change in total EL; hence the bank has to provision for the full, long-term risk of the asset. Whereas for Stage 1, the bank is required to hold the least capital out of the three stages, encouraging lending.

In real banks, they may use early-warning signals to monitor **Significant Increase in Credit Risk (SICR) indicators**, this can be rising utilisation of credit lines, repeated payment deferral, negative changes in employment, these trigger loan migrations.

<img width="237" height="184" alt="image" src="https://github.com/user-attachments/assets/b7188d93-904c-479b-bd80-2d458bc1dc01" />


In the 2008–2009 housing crisis: property prices fell sharply while unemployment rose, many mortgages did not immediately fall behind on payments, but the risk profile clearly increased. Under the IFRS-9 rules today, this would trigger Stage-2 migration reflecting forward-looking deterioration in credit quality.

<img width="237" height="178" alt="image" src="https://github.com/user-attachments/assets/8132d941-67ec-4bb9-a3a9-b4257336118a" />


Because property values were shocked by –15%, the Loan-to-Value ratios in the portfolio increase by roughly the same magnitude.

Loans that were originally in the 90%–100% can easily exceed 100%, becoming underwater.

In addition, banks typically track **LTV at three levels**: origination, current based on updated valuations, and stressed under forward-looking scenarios. Firstly, capturing the initial equity buffer that borrower has, and the latter applies an appropiate Housing Price Index (HPI) for a **Point In Tiime (PIT) assessment** to reflect the collateral security **today**. And lastly, the forward looking simulates an adverse economic scenario.

The LGD chart shows a much smaller change compared with PD or Expected Loss. This is mainly because the LGD structure in this simplified model is defined using broad LTV buckets, since the shift in the average LTV was from 0.79 🡪 0.92 it meant that most remained in the same LGD band.

<img width="241" height="173" alt="image" src="https://github.com/user-attachments/assets/a6ab9b99-ffd0-4f1c-80b7-199eaa3b75b9" />

LGD is calculated as 1 – Recovery rate

In reality, banks incorporate factors such as **Forced-Sale Discounts**, which explain why banks rarely recover 100% of the property’s market value. Repossessed properties must be sold fast to **minimise carrying costs** and to comply with **regulatory recovery timelines**. Other factors like **Time in Default (TID)** that depict the foregone interest, and selling costs may also be applied.

The PD chart highlights a close to doubling as consequence of the stress, This is expected, since PD is more sensitive to collateral deterioration than LGD.

<img width="241" height="177" alt="image" src="https://github.com/user-attachments/assets/1d1af560-9204-4765-8209-83ac2035765a" />


In real banking, PD is not driven by a simple multiplier but by full statistical models that incorporate borrower data such as income, employment status, interest rates.

Institutions model the Expected Loss using **three different PD’s**, these are each representative of their scenario, such as baseline, adverse and severe. Each so, as an input receives macroeconomic drivers to have a reasonable weighted forward-looking model.

For example, the **baseline** EL can have the highest weight of the three such as 60%. Then the **adverse**, modelling a mild downturn may receive 30%. Lastly the **severe** case can depict a financial crisis or deep housing downturn, receiving 10%. With these, a final EL can be calculated capturing the non-linearity of credit risk.

# Improvements and Real-World Extensions

In a real bank environment, many enhancements are applied making analysis robust and in line with professional risk practices.

Banks typically rely on Statistical or Machine-Learning models trained on extense historical default and recovery data rather than simple multipliers or buckets. **PD models** may include, as previously mentioned, income, employment history, interest rate sensitivity. It can be modelled with **logistic regression**, linking a binary outcome to a linear combination of variables: Debt-to-Income, current LTV, interest rate changes.

**LGD models** incorporate factors which influence the recovery rate, directly tied to LGD, Forrced-Sale Discounts, Time in Default. LGD is constrained between 0 and 1 so **beta regression** could be used, having LTV as a primary driver, and others like Time in Default and selling costs.

For the model to behave like a real Point-in-Time IFRS-9 model we could integrate several scenarios like previously mentioned, baseline, adverse, severe.

## Using Looker

Current dashboard makes use of a variety of bar charts showing before-after effects. A more advanced, realistic setup can contain Heatmaps, Flow charts to show Stage migrations, Geographical maps if regional HPI data is integrated.

To operationalise model, LookML can be implemented into a centralised semantic layer, ensuring that all metrics are consistent throughout the reports.

# Simple Model Methodology

## Initial Portfolio Setup

- **Days Past Due**:

75% of loans are assigned DPD = 0.

2% of loans are DPD >= 90.

- **Probability of Default**: drawn randomly from Uniform Distribution (0.01% – 5%)
- Loss Given Default: drawn randomly from Uniform Distribution (5% – 40%)
- Exposure At Default: original property value increased by (–5%,+30%)

## Determining Initial IFRS-9 Stages

- Stage 1: if the loan is less than 30 days past due (DPD < 30)
- Stage 2: if the loan is between 30 and 89 days past due (30 ≤ DPD < 90)
- Stage 3: if the loan is 90 days past due or more (DPD ≥ 90)

## Loan-to-Value Ratio

- B = current balance
- V = current property value

(initialised as a randomised value between 100k and 700k).

## House–Price Shock and LGD classification

(recalculate LTV after shock with new property values).

Increases LTV across the entire book, especially pushing loans close to 90% or 100% LTV into high-risk territory.

- LGD = 0.05 if the stressed LTV is below 0.60
- LGD = 0.15 if the stressed LTV is between 0.60 and 0.80
- LGD = 0.30 if the stressed LTV is between 0.80 and 1.00
- LGD = 0.50 if the stressed LTV is 1.00 or higher (loan is underwater)

## PD Stress Rules (based on stressed LTV)

- PD is tripled if the stressed LTV is greater than 1.00 (the loan is underwater).
- PD is doubled if the stressed LTV is between 0.90 and 1.00.
- PD remains unchanged if the stressed LTV is 0.90 or below.

## Stage Migration Under Stress

- If DPD ≥ 90, remain Stage 3
- If DPD ≥ 30, or stressed PD > 2× baseline PD, move to Stage 2
- Otherwise remain Stage 1

## Computing Expected Loss
