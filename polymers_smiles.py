import requests
import pandas as pd

polymer_names = [
    "Ethylene", "Propylene", "But-1-ene", "Isobutylene", "Styrene", 
    "Vinyl chloride", "Tetrafluoroethylene", "Chlorotrifluoroethylene", "Vinylidene fluoride", "Vinylidene chloride",
    "Methyl methacrylate", "Acrylonitrile", "Vinyl acetate", "Vinyl alcohol", "Vinylpyrrolidone",
    "Ethylene glycol", "Propylene glycol", "Diethylene glycol", "Triethylene glycol", "Bisphenol A", 
    "Terephthalic acid", "Dimethyl terephthalate", "Isophthalic acid", "Ethylene terephthalate", "Butylene terephthalate",
    "Lactic acid", "Glycolic acid", "Caprolactone", "Oxirane", "Propylene oxide",
    "Caprolactam", "Adipic acid", "Sebacic acid", "Hexamethylenediamine", "Ethylenediamine",
    "Diethylenetriamine", "Urea", "Melamine", "Acrylamide", "Methacrylamide",
    "Oxydianiline", "Pyromellitic dianhydride", "Isophorone diisocyanate", "Toluene diisocyanate", "Benzimidazole",
    "Buta-1,3-diene", "Isoprene", "Chloroprene", "ribose", "Maleimide",
    "Hexamethylcyclotrisiloxane", "Cyclopentadiene", "Maleic anhydride", "Fumaric acid", "Phthalic anhydride",
    "Glucose", "Fructose", "but-2-yne", "1,4-butanediol", "Hexamethylene diisocyanate", 
    "Glucuronic acid", "Ethyl beta-D-glucopyranoside", "Norbornene", "Glucosamine", "Galactose",
    "Xylose", "Mannose", "Glycerol", "Tartaric acid", "Succinic acid",
    "Acrylic acid", "Methacrylic acid", "Ethyl acrylate", "Butyl acrylate", "2-Ethylhexyl acrylate",
    "Methyl acrylate", "Crotonic acid", "Maleic acid", "Itaconic acid", "Sorbic acid",
    "Thiophene", "Pyrrole", "Aniline", "Acetylene", "3-Hexylthiophene", 
    "Fluorene", "Carbazole", "Stilbene", "Phenylene sulfide", "Pyridine",
    "Formaldehyde", "Phenol", "Resorcinol", "Benzene", "Toluene", 
    "Epichlorohydrin", "Bisphenol A diglycidyl ether", "Allyl alcohol", "Methanol", "Ethanol"
]

smiles_list = []

for name in polymer_names:
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{name}/property/ConnectivitySMILES/JSON"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        try:
            smiles = data['PropertyTable']['Properties'][0]['ConnectivitySMILES']
        except:
            smiles = None
    else:
        smiles = None
    
    smiles_list.append(smiles)

df = pd.DataFrame({"Polymer": polymer_names, "SMILES": smiles_list})

df.to_csv("api_smiles.csv", index=False)

df.to_excel("api_smiles.xlsx", index=False)
