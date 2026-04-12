# ================================
# POLYMER MEMBRANE FORWARD MODEL
# Predict Membrane Category from Molecular Descriptors
# ================================

# Import required libraries
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

import matplotlib.pyplot as plt
import seaborn as sns


# ================================
# LOAD DATASET
# ================================
# Replace with your CSV filename/path
df = pd.read_csv("Final_Labeled_Dataset.csv")

# ==========================================
# REASSIGN FUNCTIONAL CATEGORY
# ==========================================

def reassign_category(row):
    
    # Keep existing non-functional labels
    if row["Category"] != "Functional / Advanced":
        return row["Category"]
    
    # Water Purification (hydrophilic)
    if row["TPSA"] > 60 and row["LogP"] < 1:
        return "Water Purification"
    
    # Gas Separation (hydrophobic)
    elif row["LogP"] > 2:
        return "Gas Separation"
    
    # Otherwise Structural
    else:
        return "Filtration / Structural"


# Apply reassignment
df["Category"] = df.apply(reassign_category, axis=1)

print("\nUpdated Category Counts:\n", df["Category"].value_counts())


# ================================
# DEFINE INPUT FEATURES (DESCRIPTORS)
# ================================
descriptor_cols = [
    'MolWt','NumAtoms','NumBonds','HeavyAtoms',
    'RotatableBonds','RingCount','AromaticRings',
    'TPSA','MolMR','FractionCSP3','HDonors',
    'HAcceptors','Heteroatoms','NOCount',
    'NHOHCount','AliphaticRings',
    'AromaticHeterocycles','SaturatedRings',
    'ValenceElectrons','MaxPartialCharge',
    'LogP','MinPartialCharge',
    'MaxAbsPartialCharge','MinAbsPartialCharge',
    'BalabanJ','BertzCT','Chi0','Chi1',
    'Kappa1','Kappa2'
]


# ================================
# DEFINE X (INPUTS) AND y (TARGET)
# ================================
# X = Molecular descriptors
# y = Membrane category labels
X = df[descriptor_cols]
y = df['Category']


# ================================
# FEATURE SCALING / NORMALIZATION
# Standardizes features to mean=0, variance=1
# ================================
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


# ================================
# TRAIN TEST SPLIT
# 80% Training, 20% Testing
# stratify=y keeps class balance same
# ================================
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# ================================
# TRAIN RANDOM FOREST MODEL
# ================================
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)


# ================================
# MAKE PREDICTIONS
# ================================
y_pred = model.predict(X_test)


# ================================
# EVALUATE MODEL PERFORMANCE
# ================================
print("========== MODEL PERFORMANCE ==========")

print("\nAccuracy Score:")
print(accuracy_score(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
cm = confusion_matrix(y_test, y_pred)
print(cm)


# ================================
# VISUALIZE CONFUSION MATRIX
# ================================
plt.figure(figsize=(6,5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()
plt.savefig("confusion_matrix.png")


# ================================
# CROSS VALIDATION FOR ROBUSTNESS
# 5-Fold CV gives more scientific reliability
# ================================
cv_scores = cross_val_score(model, X_scaled, y, cv=5)

print("\n========== CROSS VALIDATION ==========")
print("CV Scores:", cv_scores)
print("Mean CV Accuracy:", cv_scores.mean())


# ================================
# FEATURE IMPORTANCE ANALYSIS
# Shows most influential descriptors
# ================================
importance_df = pd.DataFrame({
    'Feature': descriptor_cols,
    'Importance': model.feature_importances_
})

importance_df = importance_df.sort_values(
    by='Importance',
    ascending=False
)

print("\n========== TOP IMPORTANT FEATURES ==========")
print(importance_df.head(10))


# ================================
# VISUALIZE FEATURE IMPORTANCE
# ================================
plt.figure(figsize=(10,6))
plt.barh(
    importance_df['Feature'][:10],
    importance_df['Importance'][:10]
)
plt.gca().invert_yaxis()

plt.title("Top 10 Important Molecular Descriptors")
plt.xlabel("Importance Score")
plt.show()

# ==========================================
# ADVANCED INVERSE DESIGN (USER-DRIVEN)
# ==========================================

def inverse_design_advanced(model, X_scaled, df, target_category):
    
    print("\n--- Additional Preferences ---")
    
    # User preferences
    mw_pref = input("Molecular Weight (low / high / any): ")
    tpsa_pref = input("TPSA (low / high / any): ")
    logp_pref = input("Hydrophilicity (hydrophilic / hydrophobic / any): ")
    
    probs = model.predict_proba(X_scaled)
    class_index = list(model.classes_).index(target_category)
    scores = probs[:, class_index]
    
    df_copy = df.copy()
    df_copy["Score"] = scores
    
    # Apply preference scoring
    for i, row in df_copy.iterrows():
        
        bonus = 0
        
        # Molecular Weight
        if mw_pref == "low" and row["MolWt"] < 200:
            bonus += 0.05
        elif mw_pref == "high" and row["MolWt"] > 300:
            bonus += 0.05
        
        # TPSA
        if tpsa_pref == "high" and row["TPSA"] > 60:
            bonus += 0.05
        elif tpsa_pref == "low" and row["TPSA"] < 40:
            bonus += 0.05
        
        # LogP (hydrophilicity)
        if logp_pref == "hydrophilic" and row["LogP"] < 1:
            bonus += 0.05
        elif logp_pref == "hydrophobic" and row["LogP"] > 2:
            bonus += 0.05
        
        df_copy.at[i, "Score"] += bonus
    
    # Sort
    df_copy = df_copy.sort_values(by="Score", ascending=False)
    
    return df_copy.head(5)
# ==========================================
# INTERPRETATION FUNCTION (VERY IMPORTANT)
# ==========================================

def explain_recommendation(category):
    
    if category == "Water Purification":
        return "Use as membrane for removing salts and contaminants"
    
    elif category == "Gas Separation":
        return "Use for selective gas transport and separation"
    
    elif category == "Filtration / Structural":
        return "Use as support layer for membrane stability"
# ==========================================
# USER INPUT + OUTPUT
# ==========================================

def run_inverse_design():
    
    print("\nAvailable Categories:")
    for c in model.classes_:
        print("-", c)
    
    target = input("\nEnter desired membrane type: ")
    
    results = inverse_design_advanced(model, X_scaled, df, target)
    
    print("\n===== RECOMMENDED POLYMERS =====\n")
    
    for _, row in results.iterrows():
        print(f"Polymer: {row['Name']}")
        print(f"Score: {row['Score']:.3f}")
        print("Role:", explain_recommendation(row['Category']))
        print("-"*50)

# ==========================================
# RUN
# ==========================================

run_inverse_design()
