import matplotlib.pyplot as plt
import numpy as np
import time
from nemesispy.radtran.forward_model import ForwardModel

################################################################################
# Read GCM data
from nemesispy.data.gcm.process_gcm import (nlon,nlat,xlon,xlat,npv,pv,\
    tmap,h2omap,comap,co2map,ch4map,hemap,h2map,vmrmap,hvmap,\
    tmap_mod,h2omap_mod,comap_mod,co2map_mod,ch4map_mod,\
    hemap_mod,h2map_mod,vmrmap_mod,hvmap_mod,phase_grid,\
    kevin_phase_by_wave,kevin_wave_by_phase,\
    pat_phase_by_wave,pat_wave_by_phase,\
    vmrmap_mod_new,tmap_hot)

### Opacity data
lowres_files = ['/Users/jingxuanyang/ktables/h2owasp43.kta',
'/Users/jingxuanyang/ktables/cowasp43.kta',
'/Users/jingxuanyang/ktables/co2wasp43.kta',
'/Users/jingxuanyang/ktables/ch4wasp43.kta']
cia_file_path = '/Users/jingxuanyang/Desktop/Workspace/' \
    + 'nemesispy2022/nemesispy/data/cia/exocia_hitran12_200-3800K.tab'

################################################################################
### Wavelengths grid and orbital phase grid
wave_grid = np.array([1.1425, 1.1775, 1.2125, 1.2475, 1.2825, 1.3175, 1.3525, 1.3875,
       1.4225, 1.4575, 1.4925, 1.5275, 1.5625, 1.5975, 1.6325, 3.6   ,
       4.5   ])
phase_grid = np.array([ 22.5,  45. ,  67.5,  90. , 112.5, 135. , 157.5, 180. , 202.5,
       225. , 247.5, 270. , 292.5, 315. , 337.5])
nwave = len(wave_grid)
nphase = len(phase_grid)
wasp43_spec = np.array([3.341320e+25, 3.215455e+25, 3.101460e+25, 2.987110e+25,
       2.843440e+25, 2.738320e+25, 2.679875e+25, 2.598525e+25,
       2.505735e+25, 2.452230e+25, 2.391140e+25, 2.345905e+25,
       2.283720e+25, 2.203690e+25, 2.136015e+25, 1.234010e+24,
       4.422200e+23])

### Reference Planet Input
M_plt = 3.8951064000000004e+27 # kg
R_plt = 74065.70 * 1e3 # m
gas_id = np.array([  1, 2,  5,  6, 40, 39])
iso_id = np.array([0, 0, 0, 0, 0, 0])
NLAYER = 20
phasenumber = 3
nmu = 3
phase = phase_grid[phasenumber]
P_model = np.geomspace(20e5,100,NLAYER)
NITER = 1
### Set up forward model
FM = ForwardModel()
FM.set_planet_model(M_plt=M_plt,R_plt=R_plt,gas_id_list=gas_id,iso_id_list=iso_id,
    NLAYER=NLAYER)
FM.set_opacity_data(kta_file_paths=lowres_files, cia_file_path=cia_file_path)

### Testing one particular orbital phase (inhomogeneouus disc averaging)
one_phase =  FM.calc_disc_spectrum(phase=phase, nmu=nmu, P_model = P_model,
    global_model_P_grid=pv,
    global_T_model=tmap_mod, global_VMR_model=vmrmap_mod,
    mod_lon=xlon,
    mod_lat=xlat,
    solspec=wasp43_spec)
start_time = time.time()
for i in range(NITER):
    one_phase =  FM.calc_disc_spectrum(phase=phase, nmu=nmu, P_model = P_model,
        global_model_P_grid=pv,
        global_T_model=tmap_mod, global_VMR_model=vmrmap_mod,
        mod_lon=xlon,
        mod_lat=xlat,
        solspec=wasp43_spec)
end_time = time.time()
print('RUNTIME = ',(end_time-start_time)/NITER)


fig, axs = plt.subplots(nrows=2,ncols=1,sharex=True,
    dpi=100)
axs[0].set_title('phase = {}'.format(phase))
axs[0].plot(wave_grid,one_phase,color='b',label='Python')
axs[0].scatter(wave_grid,kevin_phase_by_wave[phasenumber,:,0],color='r',marker='+',label='Data')
axs[0].plot(wave_grid,pat_phase_by_wave[phasenumber,:],color ='k',label='Fortran')
axs[0].legend()
axs[0].grid()

diff = (one_phase - pat_phase_by_wave[phasenumber,:])/one_phase
axs[1].scatter(wave_grid,diff,marker='.',color='b')
axs[1].grid()
print(diff)
# plt.show(block=False)
# input()
# plt.close()
"""
### This is for plotting specta at all phases
for iphase in range(nphase):
    phasenumber = iphase
    nmu = 5
    phase = phase_grid[phasenumber]
    P_model = np.geomspace(20e5,1,NLAYER)
    P_model = pv
    one_phase =  FM.test_disc_spectrum(phase=phase, nmu=nmu, P_model = pv,
        global_model_P_grid=pv,
        global_T_model=tmap, global_VMR_model=vmrmap_mod_new,
        model_longitudes=xlon,
        model_lattitudes=xlat,
        solspec=wasp43_spec)

    fig, axs = plt.subplots(nrows=2,ncols=1,sharex=True,
        dpi=800)
    axs[0].set_title('phase = {}'.format(phase))
    axs[0].plot(wave_grid,one_phase,color='b',label='Python')
    axs[0].scatter(wave_grid,kevin_phase_by_wave[phasenumber,:,0],color='r',marker='+',label='Data')
    axs[0].plot(wave_grid,pat_phase_by_wave[phasenumber,:],color ='k',label='Fortran')
    axs[0].legend(loc='upper left')
    axs[0].grid()
    axs[0].set_ylabel('Flux ratio')

    diff = (one_phase - pat_phase_by_wave[phasenumber,:])/one_phase
    axs[1].scatter(wave_grid,diff,marker='.',color='b')
    axs[1].grid()
    axs[1].set_ylabel('Relative diff')
    axs[1].set_xlabel('Wavelength (Micron)')
    print(iphase,diff)
    plt.tight_layout()

    plt.show()
    # plt.savefig('good_discav_planet{}.pdf'.format(iphase),dpi=800)

"""