# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install kratos
#
# You can edit this file again by typing:
#
#     spack edit kratos
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *
import os


class Kratos(CMakePackage):
    """Package for installing Kratos Multiphysics."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.cimne.com/kratos/"
    url      = "https://github.com/KratosMultiphysics/Kratos/archive/refs/tags/v9.1.4.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('9.1', sha256='2a2415089ffefb288b61e7d9f8dab55564c7b84498c8edfa5677560c90c97b64')
    version('9.1.4', sha256='efe255921b279bc866af2311a6da96c3d11c4f5c3d11ddbe3f2d2751178bd81f')

    # FIXME: Add dependencies if required.
    depends_on('boost')
    depends_on('python@3.6:')
    depends_on('blas')

    #variant
    variant('mpi', default=False, description='Builds a MPI version of the library')
    depends_on('mpi', when='+mpi')
    variant('mmg', default=False, description='Builds a MMG version of the library')
    depends_on('mmg', when='+mmg')
    variant('apps', default='none', multi=True, description='Builds apps version of the library')
    variant('eigen_mkl', default=False, description='Builds a Eigen_mkl version of the library')
    depends_on('intel-mkl', when='+eigen_mkl')
   
    def url_for_version(self, version):
        url = "https://github.com/KratosMultiphysics/Kratos/archive/refs/tags/v{0}.tar.gz"
        return url.format(version)

    def setup_build_environment(self, env):
        apps = self.spec.variants['apps'].value
        if apps != 'none':
            kratos_apps=""
            applications_path=os.path.join(self.stage.source_path,  "applications")
            for app in apps:
                kratos_apps = kratos_apps + os.path.join(applications_path,  app) + ";"
            env.set('KRATOS_APPLICATIONS', kratos_apps)
        print("PYTHON_EXECUTABLE:" + str(self.spec['python'].prefix.bin + "/python3"))
        env.set('PYTHON_EXECUTABLE',self.spec['python'].prefix.bin + "/python3")

    def setup_run_environment(self, env):
        env.prepend_path('LD_LIBRARY_PATH', self.prefix.lib)
        env.prepend_path('PYTHONPATH', self.prefix)


    def cmake_args(self):
        # Add arguments other than
        # CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE
        args = []
        if self.spec.variants['mpi'].value == True:
            args.append('-DUSE_MPI=ON')
        else:
            args.append('-DUSE_MPI=OFF')
        if self.spec.variants['mmg'].value == True:
            args.append('-DUSE_MMG=ON')
        if self.spec.variants['eigen_mkl'].value == True:
            args.append('-DUSE_EIGEN_MKL=ON')
        return args

