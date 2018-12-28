# Development dependencies
pip install numpy==1.15.4
pip install -r devrequirements.txt

# Compile CMBTR extension with cython. The .so file is not generated, as it
# will be compiled during package setup
#cythonize dscribe/libmbtr/cmbtrwrapper.pyx

python --version
pkgutil --pkg-info=com.apple.pkg.CLTools_Executables
pkgutil --pkg-info=com.apple.pkg.DeveloperToolsCLI

softwareupdate --list
pip install .
