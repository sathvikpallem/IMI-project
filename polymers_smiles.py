import requests
import pandas as pd
import time

polymer_names = [

#  Fluoropolymers
"Tetrafluoroethylene","Vinylidene fluoride","Chlorotrifluoroethylene","Hexafluoropropene",
"Perfluoropropyl vinyl ether","Perfluoroalkyl acrylate","Trifluoromethacrylic acid","2,2,2-Trifluoroethanol",

#  Polyamide / RO membranes
"Caprolactam","Adipic acid","Hexamethylenediamine","Ethylenediamine",
"Sebacic acid","Dodecanedioic acid","m-Phenylenediamine","p-Phenylenediamine",
"Trimesoyl chloride","Isophthaloyl chloride","Piperazine","1,3,5-Benzenetricarbonyl chloride",

#  Polyester / Polycarbonate
"Bisphenol A","Bisphenol F","Terephthalic acid","Dimethyl terephthalate",
"Isophthalic acid","Ethylene glycol","1,4-butanediol","Neopentyl glycol",
"Carbonyl dichloride","Diphenyl carbonate",

#  Acrylates / Hydrophilic
"Acrylic acid","Methacrylic acid","Methyl methacrylate","Acrylamide",
"Methacrylamide","Ethyl acrylate","Butyl acrylate","2-Ethylhexyl acrylate",
"Hydroxyethyl methacrylate","Hydroxypropyl acrylate",

#  PAN
"Acrylonitrile","Methacrylonitrile",

#  Epoxy / Crosslinking
"Epichlorohydrin","Bisphenol A diglycidyl ether","Glycidyl methacrylate",

#  Polyimide (gas separation)
"Pyromellitic dianhydride","Oxydianiline",
"4,4'-Diaminodiphenyl ether","3,3'-Diaminobenzidine",
"Trimellitic anhydride","Benzophenone tetracarboxylic dianhydride",

#  Polyurethane
"Toluene diisocyanate","Isophorone diisocyanate","Hexamethylene diisocyanate",
"Methylene diphenyl diisocyanate","4,4'-Diaminodiphenyl methane",

# Polysulfone / PES
"Diphenyl sulfone","4,4'-Dichlorodiphenyl sulfone",
"Bisphenol S","Sulfanilic acid",

#  Ether-based
"Oxirane","Propylene oxide","Ethylene oxide","Tetrahydrofuran",

#  Hydrophilic modifiers
"Glycerol","Sorbitol","Polyethylene glycol diacrylate","N,N-Dimethylacrylamide",

#  Vinyl-based
"Vinyl acetate","Vinyl chloride","Vinyl alcohol","Vinylpyrrolidone","Vinylidene chloride",
"Styrene","Divinylbenzene",

#  Functional additives / crosslinkers
"Maleic anhydride","Fumaric acid","Maleimide","Itaconic acid","Crotonic acid",
"Divinyl sulfone","Glutaraldehyde",

#  Elastomer monomers
"Buta-1,3-diene","Chloroprene","Isoprene",

#  Silicon-based
"Hexamethylcyclotrisiloxane","Octamethylcyclotetrasiloxane",
"Dimethylsiloxane",

#  Norbornene
"Norbornene","Dicyclopentadiene",

#  Biopolymer-related
"Alginate","Chitosan","Cellulose acetate",

#  Biodegradable polymers
"Caprolactone","Lactic acid","Glycolic acid","Succinic acid","Tartaric acid",

#  Diols / chain extenders
"1,6-hexanediol","1,3-propanediol","Diethylene glycol","Triethylene glycol",

#  Advanced membrane monomers
"Triazine","Melamine","Urea","Formaldehyde",

#  Functional monomers
"Sulfonated styrene","Aminostyrene","Fluoroacrylate","Ionic liquid monomer","Allylamine"
]

smiles_list = []

for name in polymer_names:
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{name}/property/ConnectivitySMILES/JSON"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            try:
                smiles = data['PropertyTable']['Properties'][0]['ConnectivitySMILES']
            except:
                smiles = None
        else:
            smiles = None

    except Exception as e:
        print(f"Error for {name}: {e}")
        smiles = None

    print(f"{name} → {smiles}")   
    smiles_list.append(smiles)
    time.sleep(0.3)


df = pd.DataFrame({
    "Polymer": polymer_names,
    "SMILES": smiles_list
})

df.dropna(inplace=True)
df.drop_duplicates(subset="SMILES", inplace=True)

# Save
df.to_csv("api_smiles.csv", index=False)
df.to_excel("api_smiles.xlsx", index=False)

print("Dataset saved!")
print("Total valid entries:", len(df))
