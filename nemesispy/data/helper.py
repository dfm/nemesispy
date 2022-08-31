# -*- coding: utf-8 -*-
import os
import numpy as np

### Reliably find the path to this folder
__location__ = os.path.realpath(
    os.path.dirname(__file__)
    )

### k-tables
# All k-tables are assummed to share the same g ordinates and gordinate
# quadrature weights below, unless stated otherwise

# g ordinates
g_ordinates = np.array(
    [0.0034357 , 0.01801404, 0.04388279, 0.08044151, 0.12683405,
       0.18197316, 0.2445665 , 0.31314695, 0.3861071 , 0.46173674,
       0.53826326, 0.6138929 , 0.68685305, 0.7554335 , 0.81802684,
       0.87316597, 0.91955847, 0.9561172 , 0.981986  , 0.9965643 ],
      dtype=np.float32)
# g ordinates quadrature weights
del_g = np.array(
    [0.008807  , 0.02030071, 0.03133602, 0.04163837, 0.05096506,
       0.05909727, 0.06584432, 0.07104805, 0.0745865 , 0.07637669,
       0.07637669, 0.0745865 , 0.07104805, 0.06584432, 0.05909727,
       0.05096506, 0.04163837, 0.03133602, 0.02030071, 0.008807  ],
      dtype=np.float32)

### Low resolution k-table, HST/WFC3 + Spizter wavelengths
lowres_pressure_grid = np.array(
    [3.0995553e-02, 8.6981423e-02, 2.4409227e-01, 6.8498516e-01,
       1.9222448e+00, 5.3943086e+00, 1.5137805e+01, 4.2480560e+01,
       1.1921134e+02, 3.3453738e+02, 9.3879810e+02, 2.6345066e+03,
       7.3930977e+03, 2.0746936e+04, 5.8221188e+04, 1.6338364e+05,
       4.5849616e+05, 1.2866571e+06, 3.6106880e+06, 1.0132529e+07],
      dtype=np.float32)
lowres_temperature_grid = np.array(
    [ 100.,  250.,  400.,  550.,  700.,  850., 1000., 1150., 1300.,
       1450., 1600., 1750., 1900., 2050., 2200., 2350., 2500., 2650.,
       2800., 2950.], dtype=np.float32)
lowres_wavelengths = np.array(
    [1.14250004, 1.17750001, 1.21249998, 1.24749994, 1.28250003,
       1.3175    , 1.35249996, 1.38750005, 1.42250001, 1.45749998,
       1.49249995, 1.52750003, 1.5625    , 1.59749997, 1.63250005,
       3.5999999 , 4.5       ])

ktable_path = os.path.join(__location__, "ktables")
lowres_file_paths = [
    'h2owasp43.kta',
    'co2wasp43.kta',
    'cowasp43.kta',
    'ch4wasp43.kta']
for ipath,path in enumerate(lowres_file_paths):
    lowres_file_paths[ipath] = os.path.join(ktable_path,path)


### ARIEL k-tables
ariel_file_paths = [
    'H2O_Katy_ARIEL_test.kta',
    'CO2_Katy_ARIEL_test.kta',
    'CO_Katy_ARIEL_test.kta',
    'CH4_Katy_ARIEL_test.kta']
for ipath,path in enumerate(ariel_file_paths):
    ariel_file_paths[ipath] = os.path.join(ktable_path,path)

### High resolution k-tables
hires_file_paths = [
    'H2O_Katy_R1000.kta',
    'CO2_Katy_R1000.kta',
    'CO_Katy_R1000.kta',
    'CH4_Katy_R1000.kta']
for ipath,path in enumerate(hires_file_paths):
    hires_file_paths[ipath] = os.path.join(ktable_path,path)

cia_folder_path = os.path.join(__location__ , "cia")
cia_file_path = os.path.join(cia_folder_path,'exocia_hitran12_200-3800K.tab')
