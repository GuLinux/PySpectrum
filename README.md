PySpectrum
==========

PySpectrum is a Python-Qt5 application for amatorial spectrography. It aims at being simple to use, yet still powerful thanks to the scientific support available on python.

### Requirements ###
* python3
* PyQt5
* astropy
* matplotlib
* numpy
* scipy

On ubuntu you might install all required dependencies with the following command:

    sudo apt-get install -y python3-pyqt5 python3-astropy python3-matplotlib python3-scipy
    
### Download ###

You can get PySpectrum by simply cloning its main git repository:

    git clone https://gulinux@bitbucket.org/gulinux/pyspectrum.git
    
Alternatively, you can download a [snapshot of the repository](https://bitbucket.org/gulinux/pyspectrum/get/master.tar.gz):

    wget https://bitbucket.org/gulinux/pyspectrum/get/master.tar.gz
    tar xzf master.tar.gz

    
### Launching ###

Just launch the pyspectrum.py script in a shell from the main sources directory:

    ./pyspectrum.py

Or use your python3 binary:

    /usr/bin/python3.5 pyspectrum.py

    
### Author ###
    
[Marco Gulino](http://gulinux.net) <marco@gulinux.net> 

Licensed under GPLv3 (see COPYING file)


### Acknowledgments ###

* Sample spectra:
    + [Spectrophotometric Atlas of Standard Stellar Spectra (Pickles 1985)](http://vizier.u-strasbg.fr/viz-bin/VizieR-4)
    + [The MILES Library](http://miles.iac.es/pages/stellar-libraries/the-catalogue.php)