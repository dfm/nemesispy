#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""Calculate the opacity of a mixture of gases using ktables."""
import numpy as np
from numba import jit

# @jit(nopython=True)
def interp_k(P_grid, T_grid, P_layer, T_layer, k_gas_w_g_p_t):
    """
    Adapted from chimera https://github.com/mrline/CHIMERA.
    Interpolates the k-tables to input atmospheric P & T for each wavenumber and
    g-ordinate for each gas with a standard bi-linear interpolation scheme.

    Parameters
    ----------
    P_grid(NPRESSKTA) : ndarray
        Pressure grid on which the k-coefficients are pre-computed.
        Unit: Pa
    T_grid(NTEMPKTA) : ndarray
        Temperature grid on which the k-coefficients are pre-computed.
        Unit: Kelvin
    P_layer(NLAYER) : ndarray
        Atmospheric pressure grid.
        Unit: Pa
    T_layer(NLAYER) : ndarray
        Atmospheric temperature grid.
        Unit: Kelvin
    k_gas_w_g_p_t(NGAS,NWAVEKTA,NG,NPRESSKTA,NTEMPKTA) : ndarray
        Array storing the k-coefficients.

    Returns
    -------
    k_gas_w_g_l(NGAS,NWAVE,NG,NLAYER) : ndarray
        The interpolated-to-atmosphere k-coefficients.
        Has dimension: NGAS x NWAVE x NG x NLAYER.
    Notes
    -----
    Units: bar for pressure and K for temperature.
    Code breaks if P_layer/T_layer is out of the range of P_grid/T_grid.
    Mainly need to worry about max(T_layer)>max(T_grid).
    No extrapolation outside of the TP grid of ktable.
    """
    NGAS, NWAVE, NG, Npress, Ntemp = k_gas_w_g_p_t.shape
    NLAYER = len(P_layer)
    k_gas_w_g_l = np.zeros((NGAS,NWAVE,NG,NLAYER))
    for ilayer in range(NLAYER): # loop through layers
        P = P_layer[ilayer]
        T = T_layer[ilayer]
        # Workaround when atmospheric layer pressure or temperature is out of
        # range of the ktable TP grid
        if T > T_grid[-1]:
            T = T_grid[-1]#-1
        if T <= T_grid[0]:
            T = T_grid[0]+1e-3
        if P > P_grid[-1]:
            P = P_grid[-1]#-1
        if P <= P_grid[0]:
            P = P_grid[0]+1e-3
        # find the points on the k table TP grid that sandwich the
        # atmospheric layer TP
        P_index_hi = np.where(P_grid >= P)[0][0]
        P_index_low = np.where(P_grid < P)[0][-1]
        T_index_hi = np.where(T_grid >= T)[0][0]
        T_index_low = np.where(T_grid < T)[0][-1]
        P_hi = P_grid[P_index_hi]
        P_low = P_grid[P_index_low]
        T_hi = T_grid[T_index_hi]
        T_low = T_grid[T_index_low]
        # interpolate
        for igas in range(NGAS): # looping through gases
            for iwave in range(NWAVE): # looping through wavenumber
                for ig in range(NG): # looping through g-ord
                    arr = k_gas_w_g_p_t[igas,iwave,ig,:,:]
                    Q11 = arr[P_index_low,T_index_low]
                    Q12 = arr[P_index_hi,T_index_low]
                    Q22 = arr[P_index_hi,T_index_hi]
                    Q21 = arr[P_index_low,T_index_hi]
                    fxy1 = (T_hi-T)/(T_hi-T_low)*Q11+(T-T_low)/(T_hi-T_low)*Q21
                    fxy2 = (T_hi-T)/(T_hi-T_low)*Q12+(T-T_low)/(T_hi-T_low)*Q22
                    fxy = (P_hi-P)/(P_hi-P_low)*fxy1+(P-P_low)/(P_hi-P_low)*fxy2
                    k_gas_w_g_l[igas, iwave, ig, ilayer] = fxy
    return k_gas_w_g_l

# @jit(nopython=True)
def mix_two_gas_k(k_g1, k_g2, VMR1, VMR2, del_g):
    """
    Adapted from chimera https://github.com/mrline/CHIMERA.

    Mix the k-coefficients for two individual gases using the randomly
    overlapping absorption line approximation. The "resort-rebin" procedure
    is described in e.g. Goody et al. 1989, Lacis & Oinas 1991, Molliere et al.
    2015 and Amundsen et al. 2017. Each pair of gases can be treated as a
    new "hybrid" gas that can then be mixed again with another
    gas.  This is all for a *single* wavenumber bin for a single pair of gases
    at a particular pressure and temperature.

    Parameters
    ----------
    k_g1 : ndarray
        k-coeffs for gas 1 at a particular wave bin and temperature/pressure.
        Has dimension Ng.
    k_g2 : ndarray
        k-coeffs for gas 2
    VMR1 : ndarray
        Volume mixing ratio of gas 1
    VMR2 : ndarray
        Volume mixing ratio for gas 2
    g_ord : ndarray
        g-ordinates, assumed same for both gases.
    del_g : ndarray
        Gauss quadrature weights for the g-ordinates, assumed same for both gases.

    Returns
    -------
    k_g_combined
        Mixed k-coefficients for the given pair of gases
    VMR_combined
        Volume mixing ratio of "mixed gas".
    """
    """
    g_ord = np.array([0.0034357 , 0.01801404, 0.04388279, 0.08044151, 0.126834  ,
    0.1819732 , 0.2445665 , 0.3131469 , 0.3861071 , 0.4617367 ,
    0.5382633 , 0.6138929 , 0.6868531 , 0.7554335 , 0.8180268 ,
    0.873166  , 0.9195585 , 0.9561172 , 0.981986  , 0.9965643 ])
    """
    VMR_combined = VMR1+VMR2
    Ng = len(del_g)
    k_g_combined = np.zeros(Ng)
    cut_off = 1e-30
    if k_g1[-1] * VMR1 < cut_off and k_g2[-1] * VMR2 < cut_off:
        pass
    elif k_g1[-1] * VMR1 < cut_off:
        k_g_combined = k_g2*VMR2/VMR_combined
    elif k_g2[-1] * VMR2 < cut_off:
        k_g_combined = k_g1*VMR1/VMR_combined
    else:
        # Overlap Ng k-coeffs with Ng k-coeffs: Ng x Ng possible pairs
        k_g_mix = np.zeros(Ng**2)
        weight_mix = np.zeros(Ng**2)
        # Mix k-coeffs of gases weighted by their relative VMR.
        for i in range(Ng):
            for j in range(Ng):
                #equation 9 Amundsen 2017 (equation 20 Mollier 2015)
                k_g_mix[i*Ng+j] = (k_g1[i]*VMR1+k_g2[j]*VMR2)/VMR_combined
                 #equation 10 Amundsen 2017
                weight_mix[i*Ng+j] = del_g[i]*del_g[j]

        # Resort-rebin procedure: Sort new "mixed" k-coeff's from low to high
        # see Amundsen et al. 2016 or section B.2.1 in Molliere et al. 2015
        ascending_index = np.argsort(k_g_mix)
        k_g_mix_sorted = k_g_mix[ascending_index]
        weight_mix_sorted = weight_mix[ascending_index]
        #combining w/weights--see description on Molliere et al. 2015
        sum_weight = np.cumsum(weight_mix_sorted)
        x = sum_weight/np.max(sum_weight)*2.-1

        # Get the cumulative g ordinate upper bound
        # g_ord[ig+1] = g_ord[ig] + del_g[ig]
        # IndexError: index 20 is out of bounds for axis 0 with size 20
        g_ord = np.zeros(Ng+1)
        # g_ord = np.zeros(Ng)
        for ig in range(Ng):
            g_ord[ig+1] = g_ord[ig] + del_g[ig]
        # g_ord[0] = 0.0
        # g_ord[Ng] = 1.0
        """can improve the code here"""

        # g_ord = g_ord[:-1]
        # print('g_ord',g_ord)
        for i in range(Ng):
            loc = np.where(x >=  g_ord[i])[0][0]
            k_g_combined[i] = k_g_mix_sorted[loc]

    return k_g_combined, VMR_combined

# @jit(nopython=True)
def mix_multi_gas_k(k_gas_g, VMR, del_g):
    """
      Adapted from chimera https://github.com/mrline/CHIMERA.

      Key function that properly mixes the k-coefficients
      for multiple gases by treating a pair of gases at a time.
      Each pair becomes a "hybrid" gas that can be mixed in a pair
      with another gas, succesively. This is performed at a given
      wavenumber and atmospheric layer.

      Parameters
      ----------
      k_gas_g : ndarray
          array of k-coeffs for each gas at a given wavenumber and pressure level.
          Has dimension: Ngas x Ng.
      VMR : ndarray
          array of volume mixing ratios for Ngas.
      g_ord : ndarray
          g-ordinates, assumed same for all gases.
      del_g : ndarray
          Gauss quadrature weights for the g-ordinates, assumed same for all gases.

      Returns
      -------
      k_g_combined : ndarray
          mixed k_gas_g coefficients for the given gases.
      VMR_combined : ndarray
          Volume mixing ratio of "mixed gas".
    """
    """
    g_ord = np.array([0.0034357 , 0.01801404, 0.04388279, 0.08044151, 0.126834  ,
    0.1819732 , 0.2445665 , 0.3131469 , 0.3861071 , 0.4617367 ,
    0.5382633 , 0.6138929 , 0.6868531 , 0.7554335 , 0.8180268 ,
    0.873166  , 0.9195585 , 0.9561172 , 0.981986  , 0.9965643 ])
    """
    ngas = k_gas_g.shape[0]
    k_g_combined,VMR_combined = k_gas_g[0,:],VMR[0]
    #mixing in rest of gases inside a loop
    for j in range(1,ngas):
        k_g_combined,VMR_combined\
            = mix_two_gas_k(k_g_combined,k_gas_g[j,:],VMR_combined,VMR[j],del_g)
    return k_g_combined, VMR_combined