import pandas as pd
import dowhy
from dowhy import CausalModel
import logging
from econml.dml import DMLCateEstimator
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import OneHotEncoder
import numpy as np

# -----------------------------------------------------------------------------
# Load and preprocess
# -----------------------------------------------------------------------------
df = pd.read_csv("physician_data.csv")

# Binarize popularity if needed
# df["physician_popularity"] = (df["popularity_score"] > df["popularity_score"].median()).astype(int)

# One‑hot encode categorical confounders
cat_cols = ["specialty", "region"]
encoder = OneHotEncoder(drop="first", sparse=False)
encoded = encoder.fit_transform(df[cat_cols])
encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out(cat_cols))
df = pd.concat([df.drop(columns=cat_cols), encoded_df], axis=1)

treatment = "physician_popularity"
outcome   = "patient_satisfaction_score"
common_causes = ["years_experience", "hospital_rating"] + list(encoded_df.columns)

# -----------------------------------------------------------------------------
# Build and view the causal model
# -----------------------------------------------------------------------------
logging.getLogger("dowhy").setLevel(logging.WARNING)
model = CausalModel(
    data=df,
    treatment=treatment,
    outcome=outcome,
    common_causes=common_causes
)
model.view_model(layout="dot")  # requires graphviz
# from IPython.display import Image, display
# display(Image(filename="causal_model.png"))

# -----------------------------------------------------------------------------
# Identification
# -----------------------------------------------------------------------------
identified_estimand = model.identify_effect(proceed_when_unidentifiable=True)
print("Estimand:")
print(identified_estimand)

# -----------------------------------------------------------------------------
# Estimation
# -----------------------------------------------------------------------------
# Propensity‑score stratification
ps_estimate = model.estimate_effect(
    identified_estimand,
    method_name="backdoor.propensity_score_stratification"
)
print("\nPropensity Score Stratification Estimate:")
print(ps_estimate)

# Double Machine Learning with EconML
dml_estimate = model.estimate_effect(
    identified_estimand,
    method_name="backdoor.econml.dml.DML",
    method_params={
        "init_params": {
            "model_y": GradientBoostingRegressor(n_estimators=100),
            "model_t": GradientBoostingRegressor(n_estimators=100),
            "model_final": LassoCV(cv=5)
        },
        "fit_params": {}
    }
)
print("\nDouble ML (EconML) Estimate:")
print(dml_estimate)

# -----------------------------------------------------------------------------
# Refutation
# -----------------------------------------------------------------------------
print("\nRefutation: Add a Random Common Cause")
res_random = model.refute_estimate(
    identified_estimand, 
    dml_estimate,
    method_name="random_common_cause"
)
print(res_random)

print("\nRefutation: Placebo Treatment")
res_placebo = model.refute_estimate(
    identified_estimand, 
    dml_estimate,
    method_name="placebo_treatment_refuter",
    placebo_type="permute",
    num_simulations=20
)
print(res_placebo)

# -----------------------------------------------------------------------------
# Summary
# -----------------------------------------------------------------------------
print(f"\nCausal effect of physician popularity → patient satisfaction:\n"
      f" - Propensity strat: {ps_estimate.value:.3f}\n"
      f" - Double ML estimate: {dml_estimate.value:.3f}")
