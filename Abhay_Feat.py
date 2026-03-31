from rdkit import Chem
from rdkit.Chem import Descriptors
import pandas as pd

df = pd.read_csv("api_smiles.csv")

features = []

for smi in df["SMILES"]:
    mol = Chem.MolFromSmiles(smi)
    if mol:
        features.append({
            "LogP": Descriptors.MolLogP(mol),
            "MinPartialCharge": Descriptors.MinPartialCharge(mol),
            "MaxAbsPartialCharge": Descriptors.MaxAbsPartialCharge(mol),
            "MinAbsPartialCharge": Descriptors.MinAbsPartialCharge(mol),
            "BalabanJ": Descriptors.BalabanJ(mol),
            "BertzCT": Descriptors.BertzCT(mol),
            "Chi0": Descriptors.Chi0(mol),
            "Chi1": Descriptors.Chi1(mol),
            "Kappa1": Descriptors.Kappa1(mol),
            "Kappa2": Descriptors.Kappa2(mol)
        })
    else:
        features.append({})

df3 = pd.DataFrame(features)
df3 = pd.concat([df, df3], axis=1)
df3.to_csv("Abhay_gokul.csv", index=False)
df3.to_excel("Abhay_gokul.xlsx", index=False)
