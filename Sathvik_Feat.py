from rdkit import Chem
from rdkit.Chem import Descriptors
import pandas as pd

df = pd.read_csv("api_smiles.csv")

features = []

for smi in df["SMILES"]:
    mol = Chem.MolFromSmiles(smi)
    if mol:
        features.append({
            "MolWt": Descriptors.MolWt(mol),
            "NumAtoms": mol.GetNumAtoms(),
            "NumBonds": mol.GetNumBonds(),
            "HeavyAtoms": Descriptors.HeavyAtomCount(mol),
            "RotatableBonds": Descriptors.NumRotatableBonds(mol),
            "RingCount": Descriptors.RingCount(mol),
            "AromaticRings": Descriptors.NumAromaticRings(mol),
            "TPSA": Descriptors.TPSA(mol),
            "MolMR": Descriptors.MolMR(mol),
            "FractionCSP3": Descriptors.FractionCSP3(mol)
        })
    else:
        features.append({})

df1 = pd.DataFrame(features)
df1 = pd.concat([df, df1], axis=1)
df1.to_csv("Sathvik.csv", index=False)
df1.to_excel("Sathvik.xlsx", index=False)
