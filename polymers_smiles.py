import requests
import pandas as pd
import time

polymer_names = [

#Gas Separation
"Tetrafluoroethylene","Vinylidene fluoride","Chlorotrifluoroethylene","Hexafluoropropene",
"Perfluoropropyl vinyl ether","Perfluoroalkyl acrylate","Trifluoromethacrylic acid","2,2,2-Trifluoroethanol",
"Pyromellitic dianhydride","Oxydianiline","4,4'-Diaminodiphenyl ether","3,3'-Diaminobenzidine",
"Trimellitic anhydride","Benzophenone tetracarboxylic dianhydride",
"Hexamethylcyclotrisiloxane","Octamethylcyclotetrasiloxane","Dimethylsiloxane",

#Water Purification (RO/NF/UF)
"Caprolactam","Adipic acid","Hexamethylenediamine","Ethylenediamine",
"Sebacic acid","Dodecanedioic acid","m-Phenylenediamine","p-Phenylenediamine",
"Trimesoyl chloride","Isophthaloyl chloride","Piperazine","1,3,5-Benzenetricarbonyl chloride",
"Acrylic acid","Methacrylic acid","Acrylamide","Methacrylamide",
"Hydroxyethyl methacrylate","Hydroxypropyl acrylate",
"Glycerol","Sorbitol","Polyethylene glycol diacrylate","N,N-Dimethylacrylamide",
"Alginate","Chitosan","Cellulose acetate",

#Filtration / Structural (UF support)
"Bisphenol A","Bisphenol F","Terephthalic acid","Dimethyl terephthalate",
"Isophthalic acid","Ethylene glycol","1,4-butanediol","Neopentyl glycol",
"Carbonyl dichloride","Diphenyl carbonate",
"Diphenyl sulfone","4,4'-Dichlorodiphenyl sulfone","Bisphenol S","Sulfanilic acid",
"Oxirane","Propylene oxide","Ethylene oxide","Tetrahydrofuran",

#Functional / Advanced
"Methyl methacrylate","Ethyl acrylate","Butyl acrylate","2-Ethylhexyl acrylate",
"Acrylonitrile","Methacrylonitrile",
"Epichlorohydrin","Bisphenol A diglycidyl ether","Glycidyl methacrylate",
"Toluene diisocyanate","Isophorone diisocyanate","Hexamethylene diisocyanate",
"Methylene diphenyl diisocyanate","4,4'-Diaminodiphenyl methane",
"Vinyl acetate","Vinyl chloride","Vinyl alcohol","Vinylpyrrolidone","Vinylidene chloride",
"Styrene","Divinylbenzene",
"Maleic anhydride","Fumaric acid","Maleimide","Itaconic acid","Crotonic acid",
"Divinyl sulfone","Glutaraldehyde",
"Buta-1,3-diene","Chloroprene","Isoprene",
"Norbornene","Dicyclopentadiene",
"Caprolactone","Lactic acid","Glycolic acid","Succinic acid","Tartaric acid",
"1,6-hexanediol","1,3-propanediol","Diethylene glycol","Triethylene glycol",
"Triazine","Melamine","Urea","Formaldehyde",
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
