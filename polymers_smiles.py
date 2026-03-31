import requests
import pandas as pd
import time

polymer_names = [

#  Fluoropolymers (gas separation, hydrophobic membranes)
"Tetrafluoroethylene","Vinylidene fluoride","Chlorotrifluoroethylene","Hexafluoropropene",
"Perfluoropropyl vinyl ether","Perfluoroalkyl acrylate","Trifluoromethacrylic acid","2,2-Bis(4-hydroxyphenyl)hexafluoropropane",

#  Polyamide / Nylon membranes (RO membranes)
"Caprolactam","Adipic acid","Hexamethylenediamine","Ethylenediamine",
"Sebacic acid","Dodecanedioic acid","m-Phenylenediamine","p-Phenylenediamine",
"Trimesoyl chloride","Isophthaloyl chloride","Piperazine", 

#  Polyester / Polycarbonate membranes
"Bisphenol A","Bisphenol F","Terephthalic acid","Dimethyl terephthalate",
"Isophthalic acid","Ethylene glycol","1,4-butanediol","Neopentyl glycol",
"Carbonyl dichloride","Diphenyl carbonate",

#  Polyacrylate / Hydrophilic membranes
"Acrylic acid","Methacrylic acid","Methyl methacrylate","Acrylamide",
"Methacrylamide","Ethyl acrylate","Butyl acrylate","2-Ethylhexyl acrylate",
"Hydroxyethyl methacrylate","Hydroxypropyl acrylate",

#  PAN-based membranes
"Acrylonitrile","Methacrylonitrile",

#  Epoxy / Crosslinked membranes
"Epichlorohydrin","Bisphenol A diglycidyl ether","Glycidyl methacrylate",
"Diglycidyl ether","Epoxy resin monomer",

#  Polyimide (gas separation membranes)
"Pyromellitic dianhydride","Oxydianiline",
"4,4'-Diaminodiphenyl ether","3,3'-Diaminobenzidine",
"Trimellitic anhydride","Benzophenone tetracarboxylic dianhydride",

#  Polyurethane membranes
"Toluene diisocyanate","Isophorone diisocyanate","Hexamethylene diisocyanate",
"Methylene diphenyl diisocyanate","Polyether polyol","Polyester polyol","4,4'-Diaminodiphenyl methane",

#  Polysulfone / PES membranes
"Diphenyl sulfone","4,4'-Dichlorodiphenyl sulfone",
"Bisphenol S","Bisphenol sulfone","Sulfanilic acid",

#  Ether-based membranes
"Oxirane","Propylene oxide","Ethylene oxide","Tetrahydrofuran",
"Polyethylene glycol","Polypropylene glycol",

#  Hydrophilic modifiers
"Glycerol","Sorbitol","Polyvinyl alcohol","Polyethylene glycol diacrylate",

#  Vinyl polymers (membrane materials)
"Vinyl acetate","Vinyl chloride","Vinyl alcohol","Vinylpyrrolidone","Vinylidene chloride",
"Styrene","Divinylbenzene","1,3,5-Benzenetricarbonyl chloride",

#  Crosslinkers / functional additives
"Maleic anhydride","Fumaric acid","Maleimide","Itaconic acid","Crotonic acid",
"Divinyl sulfone","Glutaraldehyde",

#  Elastomer membranes
"Buta-1,3-diene","Chloroprene","Isoprene","Styrene-butadiene",

#  Silicon-based membranes
"Hexamethylcyclotrisiloxane","Octamethylcyclotetrasiloxane",
"Dimethylsiloxane","Methylsiloxane",

#  Norbornene-based membranes
"Norbornene","Dicyclopentadiene",

#  Biopolymer-based membranes
"Alginate","Chitosan","Cellulose","Cellulose acetate",

#  Misc membrane-relevant biodegradable polymers
"Caprolactone","Lactic acid","Glycolic acid","Succinic acid","Tartaric acid",
"Polylactic acid","Polycaprolactone","Perfluorooctanoic acid",

#  Diols / chain extenders
"1,6-hexanediol","1,3-propanediol","Diethylene glycol","Triethylene glycol",

# Advanced membrane monomers
"Triazine","Melamine","Urea","Formaldehyde",

# Additional functional monomers
"Sulfonated styrene","Aminostyrene","Fluoroacrylate","Ionic liquid monomer"
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
