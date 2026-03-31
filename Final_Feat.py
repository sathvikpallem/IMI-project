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
            "FractionCSP3": Descriptors.FractionCSP3(mol),
            "HDonors": Descriptors.NumHDonors(mol),
            "HAcceptors": Descriptors.NumHAcceptors(mol),
            "Heteroatoms": Descriptors.NumHeteroatoms(mol),
            "NOCount": Descriptors.NOCount(mol),
            "NHOHCount": Descriptors.NHOHCount(mol),
            "AliphaticRings": Descriptors.NumAliphaticRings(mol),
            "AromaticHeterocycles": Descriptors.NumAromaticHeterocycles(mol),
            "SaturatedRings": Descriptors.NumSaturatedRings(mol),
            "ValenceElectrons": Descriptors.NumValenceElectrons(mol),
            "MaxPartialCharge": Descriptors.MaxPartialCharge(mol),
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

final = pd.DataFrame(features)
final = pd.concat([df, final], axis=1)
final.to_csv("Final_DataSet.csv", index=False)
final.to_excel("Final_DataSet.xlsx", index=False)
