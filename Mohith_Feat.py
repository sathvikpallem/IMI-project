from rdkit import Chem
from rdkit.Chem import Descriptors
import pandas as pd

df = pd.read_csv("api_smiles.csv")

features = []

for smi in df["SMILES"]:
    mol = Chem.MolFromSmiles(smi)
    if mol:
        features.append({
            "HDonors": Descriptors.NumHDonors(mol),
            "HAcceptors": Descriptors.NumHAcceptors(mol),
            "Heteroatoms": Descriptors.NumHeteroatoms(mol),
            "NOCount": Descriptors.NOCount(mol),
            "NHOHCount": Descriptors.NHOHCount(mol),
            "AliphaticRings": Descriptors.NumAliphaticRings(mol),
            "AromaticHeterocycles": Descriptors.NumAromaticHeterocycles(mol),
            "SaturatedRings": Descriptors.NumSaturatedRings(mol),
            "ValenceElectrons": Descriptors.NumValenceElectrons(mol),
            "MaxPartialCharge": Descriptors.MaxPartialCharge(mol)
        })
    else:
        features.append({})

df2 = pd.DataFrame(features)
df2 = pd.concat([df, df2], axis=1)
df2.to_csv("Mohith.csv", index=False)
df2.to_excel("Mohith.xlsx", index=False)
