# Physician Causal Analysis

This repository demonstrates how to estimate the causal effect of **physician popularity** on **patient satisfaction** using the [DoWhy](https://github.com/microsoft/dowhy) and [EconML](https://github.com/microsoft/EconML) libraries. We walk through the four steps of causal inference—model, identify, estimate, and refute—on a hypothetical healthcare dataset.



## 📂 Repository Structure

```
.
├── physician_causal_analysis.py   # Main analysis script
├── physician_data.csv             # Input data (must be provided)
└── README.md                      # This file
```


## 📝 Data

Your `physician_data.csv` should include at least the following columns:

| Column                       | Type        | Description                                         |
| ---------------------------- | ----------- | --------------------------------------------------- |
| `physician_popularity`       | binary      | 1 = highly popular, 0 = less popular                |
| `patient_satisfaction_score` | continuous  | Measured satisfaction outcome                       |
| `years_experience`           | numeric     | Physician’s years of experience                     |
| `hospital_rating`            | numeric     | Rating of the hospital where they practice          |
| `specialty`                  | categorical | Medical specialty (e.g. “Cardiology”, “Pediatrics”) |
| `region`                     | categorical | Geographic region of practice                       |

> **Note**: If you have a continuous popularity score, binarize it around its median.


## ⚙️ Installation

1. Clone this repo:

   ```bash
   git clone https://github.com/yourusername/physician-causal-analysis.git
   cd physician-causal-analysis
   ```
2. Create a virtual environment and install dependencies:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip install dowhy econml pandas scikit-learn numpy graphviz
   ```



## 🚀 Usage

1. Place your cleaned `physician_data.csv` in the repo root.
2. Run the analysis:

   ```bash
   python physician_causal_analysis.py
   ```
3. The script will:

   * Preprocess and one‑hot‑encode categorical confounders
   * Build & visualize a causal graph
   * Identify the backdoor estimand
   * Estimate causal effects via:

     * Propensity‑score stratification
     * Double Machine Learning (EconML)
   * Run refutation tests (random common cause, placebo treatment)
   * Print a summary of estimated treatment effects



## 🔍 Key Dependencies

* **DoWhy** — a Python library for causal inference
* **EconML** — Microsoft’s library for machine‑learning‐based causal effect estimation
* **scikit‑learn**, **pandas**, **numpy**, **graphviz**



## 📈 Outputs

* **Console logs** of:

  * Identified estimand
  * Estimated causal effects (propensity stratification & DML)
  * Refutation test results
* **Causal graph** image (requires Graphviz; saved as `causal_model.png` if you uncomment the display code)



## 🤝 Acknowledgments

This example builds upon the ideas and APIs of:

* [DoWhy (Microsoft)](https://github.com/microsoft/dowhy)
* [EconML (Microsoft)](https://github.com/microsoft/EconML)



## 📚 References

1. Künzel, S. R., Sekhon, J. S., Bickel, P. J., & Yu, B. (2019). **Metalearners for estimating heterogeneous treatment effects**.
2. Sharma, A., Sharma, A., Saha, S., et al. (2020). **DoWhy: An end‑to‑end library for causal inference**.
3. https://www.microsoft.com/en-us/research/group/causal-inference/
4. https://github.com/py-why/dowhy
5. https://github.com/py-why/dowhy?tab=readme-ov-file
