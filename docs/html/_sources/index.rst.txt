.. NEMESISPY documentation master file, created by
   sphinx-quickstart on Sun Mar 10 22:23:59 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to NEMESISPY's documentation!
=====================================

.. toctree::
   :maxdepth: 2
   :caption: Table of Contents:

Table of Contents
-----------------

.. toctree::

   usage
   tutorial
   api
   publications

Introduction
------------

**NEMESISPY** is a Python package developed for atmospheric retrievals,
which is the inference of atmospheric properties such as chemical abundances
from observed spectra of planetary atmospheres. The workflow of atmospheric
retrievals can be devided into two steps: **forward modelling** and **model fitting**:

* The **forward modelling** step requires an atmospheric model for the observed
  planet and a radiative transfer pipeline that can calculate model spectra given an atmospheric model.

* The **model fitting** step requires a parameter estimation code that can
  constrain the free parameters of the forward model by fitting the observed spectra.

**NEMESISPY** can perform both parametric atmospheric modelling
and radiative transfer calculation for the retrievals of planetary spectra.
It is a recent development of the well-established Fortran `NEMESIS library <https://github.com/nemesiscode>`_,
which has been applied to the atmospheric retrievals of both solar system planets
and exoplanets.
**NEMESISPY** can be easily interfaced with Bayesian inference algorithms
such as nested sampling to retrieve atmospheric properties from spectroscopic observations.
The radiative transfer calculations in **NEMESISPY** are done with the
fast correlated-k method, and are accelerated with the
``Numba`` just-in-time compiler to match the speed of
compiled languages such as Fortran. The radiative transfer
routines are based on the well-tested `NEMESIS library <https://github.com/nemesiscode>`_
developed by Patrick Irwin (University of Oxford) and collaborators.

**NEMESISPY** comes ready with some spectral data and General Circulation
Model (GCM) data so you can start simulating spectra immediately.
There are a few demonstration routines in the ``nemesispy/examples`` folder;
in particular, ``demo_fit_eclipse.py`` contains an interactive plot routine
which allows you to fit a hot Jupiter eclipse spectrum by hand by varying
its chemical abundance and temperature profile.
The current release of **NEMESISPY** is focused on the calculation of
thermal emission spectra of exoplanets. It is capale of calculating emission spectra
at multiple orbital phases from an arbitray atmospheric model.
Future releases will include more features such
as multiple scattering and transmission geometry.

**NEMESISPY** has the following nice features:

* Written fully in Python (not a wrapper!): highly portable and customisable
  compared to packages written in compiled languages and
  can be easily installed on computer clusters.
* Fast calculation speed: the most time consuming routines are accelerated with
  just-in-time (JIT) compilation, which compiles Python code to machine
  code at run time.
* Radiative transfer routines are benchmarked against
  the extensively used `NEMESIS library <https://github.com/nemesiscode>`_.
* Contains routines to simulate spectra from General
  Circulation Models (GCMs).
* Contains unit tests to check if
  the code is working correctly after modifications.

To install the package and keep it editable, clone the repository and type
the following in the terminal:

.. code-block:: console

    $ pip install --editable .

To run all unit tests, change directory to the software folder and type the
following in the terminal:

.. code-block:: console

    $ python -m unittest discover test/

.. note::

   This project is under active development.
