
# Logistics Exploratory Data Analysis (EDA)

## 📌 Project Overview
This project focuses on analyzing logistics data using Exploratory Data Analysis (EDA) and data visualization. The objective is to understand delivery performance, shipping patterns, sales trends, and relationships between important variables using Python.

The analysis converts raw logistics data into meaningful insights through statistical summaries and visualizations.

## 🎯 Objectives
- Analyze delivery status and delivery performance.
- Compare actual and scheduled shipping times.
- Evaluate different shipping modes.
- Explore monthly order trends and regional distribution.
- Analyze sales and product quantities.
- Identify relationships between numerical variables.
- Create visualizations and a detailed project report.

## 🛠️ Technologies Used
- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn

## 📂 Project Structure
```text
Week3_Logistics_EDA/
├── data/
│   └── DataCo_Logistics_Cleaned.csv
├── src/
│   └── eda_analysis.py
├── outputs/
│   └── figures/
├── reports/
│   ├── eda_summary.json
│   ├── dataset_profile.csv
│   ├── central_tendency_and_spread.csv
│   ├── numeric_descriptive_statistics.csv
│   ├── numeric_correlation_matrix.csv
│   ├── monthly_order_counts.csv
│   ├── top_regions_by_records.csv
│   ├── category_record_counts.csv
│   └── delay_flag_rate_by_shipping_mode.csv
├── Week3_Logistics_EDA_Report.docx
├── requirements.txt
└── README.md
```

## 📊 Dataset Information
- **Dataset:** DataCo Logistics
- **Total Records:** 180,519
- **Total Columns:** 45
- **Missing Cells:** 0
- **Exact Duplicate Rows:** 0

The dataset contains information about orders, products, sales, shipping methods, delivery status, and shipping durations.

## 📈 Key Findings
- Late delivery records: 98,977
- Advance shipping records: 41,592
- Shipping on time records: 32,196
- Shipping canceled records: 7,754
- Average actual shipping time: 3.50 days
- Average scheduled shipping time: 2.93 days
- Average difference between actual and scheduled shipping time: 0.57 days

These findings highlight delivery performance as an important area for further investigation.

## 📉 Visualizations
The project generates the following visualizations:

1. Delivery Status Distribution
2. Actual and Scheduled Shipping-Time Distributions
3. Average Shipping-Time Comparison
4. Shipping-Mode Performance
5. Monthly Order Trends
6. Numerical Correlation Heatmap
7. Quantity vs. Sales
8. Top Regions by Record Count
9. Category-Wise Record Counts
10. Delay Indicators by Shipping Mode

All generated charts are saved in the `outputs/figures/` directory.

## ⚙️ Installation and Setup

### 1. Clone the Repository
```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Week3_Logistics_EDA
```

Replace the placeholder with your actual GitHub repository URL.

### 2. Create a Virtual Environment
```bash
python -m venv venv
```

Activate it on Windows:
```bash
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Analysis
Ensure the dataset is available at `data/DataCo_Logistics_Cleaned.csv`, then run:

```bash
python src/eda_analysis.py
```

The script generates charts and analysis outputs in the project directories.

## 🔍 Methodology
1. Load the dataset using Pandas.
2. Inspect the dataset structure and data quality.
3. Calculate descriptive statistics.
4. Analyze delivery status and shipping durations.
5. Compare shipping modes and monthly order trends.
6. Examine numerical relationships using correlation analysis.
7. Generate and save visualizations.
8. Export analysis summaries and interpret findings.

## 💡 Key Insights
The analysis helps identify delivery patterns, compare shipping performance, examine regional activity, and explore relationships between sales and product quantities. These insights can support further investigation into delivery delays and logistics efficiency.

## 📄 Project Report
The detailed Word report, `Week3_Logistics_EDA_Report.docx`, contains the methodology, visualizations, observations, and recommendations.

## ⚠️ Limitations
- The analysis identifies patterns and associations, not necessarily causes.
- Record counts may represent order items rather than unique orders.
- Results depend on the quality and definitions of the dataset.
- Further validation is required before making operational decisions.

## 👨‍💻 Author
**Sparsh Kulshrestha**

MCA | Python | Data Analysis | Data Visualization

---

*Completed as part of a logistics data analysis internship task to develop practical skills in exploratory data analysis and visualization.*
