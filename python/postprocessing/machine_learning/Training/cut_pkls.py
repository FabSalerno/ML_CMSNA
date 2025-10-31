infile = "/eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1_jets_60_boosted_0_pt/pkls/trainingSet_QCD_HT1000to1200_2022.pkl"
with open(inFile, "rb") as fpkl:
    dataset = pkl.load(fpkl)
components  = dataset.keys()
categories  = ["3j1fj", "3j0fj", "2j1fj"]

### DATASET cut (remove some events) ###
for c in components:
    for cat in categories:
        idx_todrop = [i for i, x in enumerate(dataset[c][cat][4]) if x==True]
        print("stiamo selezionando i top per:",c,"",cat)
        ids_todrop   = random.sample(idx_todrop, int(len(dataset[c][cat][4])*(0.6)))
        dataset[c][cat][0] = np.delete(dataset[c][cat][0], ids_todrop, axis=0)
        dataset[c][cat][1] = np.delete(dataset[c][cat][1], ids_todrop, axis=0)
        dataset[c][cat][2] = np.delete(dataset[c][cat][2], ids_todrop, axis=0)
        dataset[c][cat][3] = np.delete(dataset[c][cat][3], ids_todrop, axis=0)
        dataset[c][cat][4] = np.delete(dataset[c][cat][4], ids_todrop, axis=0)

