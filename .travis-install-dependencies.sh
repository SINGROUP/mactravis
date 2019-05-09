# Query the CLT version for the default installation
pkgutil --pkg-info=com.apple.pkg.CLTools_Executables

# Development dependencies
pip install numpy==1.15.4
#pip install -r devrequirements.txt

# Compile CMBTR extension with cython. The .so file is not generated, as it
# will be compiled during package setup
#cythonize dscribe/libmbtr/cmbtrwrapper.pyx

#python --version


#pkgutil --pkg-info=com.apple.pkg.CLTools_Executables
#pkgutil --pkg-info=com.apple.pkg.DeveloperToolsCLI

#softwareupdate --list
#softwareupdate -i "Command Line Tools (macOS High Sierra version 10.13) for Xcode-10.1"

# Update to the latest CLT
#softwareupdate -i "Command Line Tools (macOS High Sierra version 10.13) for Xcode"
#softwareupdate -i --install -a

# Check the CLT version after update
#pkgutil --pkg-info=com.apple.pkg.CLTools_Executables

# Install package with newest CLT
pip install .
