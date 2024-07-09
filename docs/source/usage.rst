Usage
=====

Installation
------------

To use NEMESISPY, first clone the `GitHub repository <https://github.com/Jingxuan97/nemesispy>`_
to your computer. Then, navigate to the directory where you have saved the
repository and run the command

.. code-block:: console

    $ pip install .

This will install the package and make it available to use in your Python environment.
In order to install the package but still make it editable, run instead the command

.. code-block:: console

    $ pip install . --editable

NEMESISPY can also by direcly installed from `PyPI <https://pypi.org/project/nemesispy/>`_
by running

.. code-block:: console

    $ pip install nemesispy

We recommend installing the package from the GitHub repository
to make sure that you have the latest version of the package.

Data
----
**Opacity data**

The most important data files required by NEMESISPY are the opacity data files.
To perform correlated-k radiative transfer calculations, NEMESISPY requires opacity
data (k-tables) to be provided in the NEMESIS .kta format.
k-tables in the .kta format can be directly downloaded from
the `ExoMol database <https://www.exomol.com/data/data-types/opacity/>`_.
The NEMESISPY package comes with some example k-table files in the ``nemesispy/data/ktables`` folder.
If you want to modify exsisting k-tables,
the `Exo_k <https://perso.astrophy.u-bordeaux.fr/~jleconte/exo_k-doc/index.html>`_
package provides many helpful routines for working with opacity data.
In addition, the NEMESISPY package also comes with a collision-induced absorption (CIA) data file
in the ``nemesispy/data/cia`` folder, compiled using the data from the `HITRAN database <https://hitran.org/>`_.

**Stellar spectra**

In exoplanetary observations, the planetary spectra are often normalised to the stellar spectrum.
The NEMESISPY package comes with some example stellar spectra in the ``nemesispy/data/stellar`` folder.
Synthetic stellar spectra can be obtained from various open-access databases, such as the
`PHOENIX database <https://www.astro.uni-jena.de/Users/theory/for2285-phoenix/grid.php>`_.

**General Circulation Model (GCM) data**

The NEMESISPY package can compute emission spectra from GCMs.
The NEMESISPY package comes with some example GCM data for a hot Jupiter in the ``nemesispy/data/gcm`` folder.
These GCM data were calculated using the setup of
`Vivien Parmentier et al. (2016) <https://iopscience.iop.org/article/10.3847/0004-637X/828/1/22>`_.
It is not necessary to have GCM data to use the functionalities of the NEMESISPY package.

Issues and contributions
------------------------
To report issues or problems with NEMESISPY, please use the `GitHub issue tracker <https://github.com/Jingxuan97/nemesispy>`_.
If you would like to contribute to the development of NEMESISPY, or seek scientific
collaboration, please directly `contact us  <https://www.physics.ox.ac.uk/our-people/yangj>`_.
