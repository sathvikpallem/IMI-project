import pandas as pd
from rdkit import Chem
from rdkit.Chem import AllChem, DataStructs

# Load CSV
df = pd.read_csv("api_smiles.csv")

# Extract columns
names = df["Polymer"].tolist()
smiles_list = df["SMILES"].tolist()

# Convert to molecules
molecules = []
valid_data = []

for name, s in zip(names, smiles_list):
    mol = Chem.MolFromSmiles(s)
    if mol is not None:
        molecules.append(mol)
        valid_data.append((name, s))

# Generate fingerprints
fingerprints = [
    AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=1024)
    for mol in molecules
]

# Tanimoto similarity
threshold = 0.9
remove_indices = set()

for i in range(len(fingerprints)):
    for j in range(i+1, len(fingerprints)):
        sim = DataStructs.TanimotoSimilarity(fingerprints[i], fingerprints[j])
        if sim > threshold:
            remove_indices.add(j)

# Keep non-redundant data
clean_data = [
    valid_data[i] for i in range(len(valid_data)) if i not in remove_indices
]

# Save clean dataset with names
clean_df = pd.DataFrame(clean_data, columns=["Name", "SMILES"])
clean_df.to_csv("Cleaned_Dataset.csv", index=False)
clean_df.to_excel("Cleaned_Dataset.xlsx", index=False)

print("Saved with names!")
