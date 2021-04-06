from pepfeature import utils
import numpy as np
import pandas as pd

def calc_aa_descriptors(dataframe, aa_column = 'Info_window_seq'):
    # Dictionary mapping each Amino-Acid to its respective group-value

    AA_properties_df = []
    properties = ['crucianiProperties', 'kideraFactors', 'zScales', 'FASGAI', 'VHSE', 'ProtFP', 'stScales', 'tScales', 'MSWHIM', 'BLOSUM']
    for sheet in properties:
        AA_properties_df.append(pd.read_excel('AAdescriptors.xls', sheet, index_col=0, header=0))

    for row in dataframe.itertuples():

        peptide = list(getattr(row, aa_column))

        every_unique_aa, counts_of_every_unique_aa = np.unique(peptide, return_counts=True)

        for df in AA_properties_df:

            for row_df in df.itertuples():
                # to keep count of weighted sum for each aa in the peptide
                weight = 0
                for aa, counts in zip(every_unique_aa, counts_of_every_unique_aa):

                    weight += counts * getattr(row_df, aa)

                    # Creating the features and setting them
                    dataframe.loc[row.Index, 'feat_{}'.format(row_df.Index)] = weight/len(peptide)

    return (dataframe)

def calculate_csv(dataframe, Ncores=4, chunksize = 50000, csv_path_filename = ['', 'result'], aa_column = 'Info_window_seq'): #function that the client should call.
    utils.calculate_export_csv(dataframe = dataframe, function = calc_aa_descriptors, Ncores= Ncores, chunksize= chunksize, aa_column = aa_column, csv_path_filename = csv_path_filename)

def calculate_df(dataframe, Ncores=4, chunksize = 50000, aa_column = 'Info_window_seq'): #function that the client should call.
    return utils.calculate_return_df(dataframe = dataframe, function = calc_aa_descriptors, Ncores= Ncores, aa_column = aa_column, chunksize= chunksize)