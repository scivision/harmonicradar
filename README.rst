==============
Harmonic Radar
==============
Code for modeling, simulating, processing [harmonic radar](https://www.scivision.co/harmonic-radar) data.

Let me know if you'd like to see more.

.. contents::

Prereqs
=======
Pygame (optional) for playing the baseband radar signals audibly, to help user gain intuition::

    pip install pygame

Install
=======
Install ``pygame`` first so that it uses the easy ``.whl`` install::

    python setup.py develop


Harmonic Radar Simulations
===========================
These are geared towards maximum simplicity for someone wanting to understand a bit about radar.
I certainly have fancier things to show if you'd like to discuss offline....

* ``Sim917.py`` a simple look at the harmonic output of an ideal diode
* ``SimHarmonicRadar.py`` forward model of CW and FMCW (chirp) harmonic radar


Notes
=====
To manually compile Pygame: Linux: ``apt install libsdl2-dev``

