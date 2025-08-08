from setuptools import setup, find_packages
from torch.utils.cpp_extension import BuildExtension, CUDAExtension

import os
# os.environ["TORCH_CUDA_ARCH_LIST"] = "8.6"  # Or "native" if supported
os.environ["TORCH_CUDA_ARCH_LIST"] = "7.5;8.0;8.6;8.9;9.0+PTX"
readme = open('README.md').read()

VERSION = '0.0.7'

requirements = []

setup(
    # Metadata
    name='balinski-and-gomory',
    version=VERSION,
    author='cestwc',
    author_email='80936226+cestwc@users.noreply.github.com',
    url='https://github.com/cestwc/primal-linear-assignment',
    long_description=readme,
    long_description_content_type='text/markdown',
    license='MIT',

    # Package info
    packages=find_packages(exclude=('*test*',)),

    # CUDA extension
    ext_modules=[
        CUDAExtension(
            'balinski_and_gomory.cuda_solver',  # module name (import solve)
            sources=[
                'balinski_and_gomory/solve.cpp',
                'balinski_and_gomory/balinski-and-gomory-cuda/src/solver.cu',
                # 'balinski_and_gomory/balinski-and-gomory-cuda/src/solver.h'
            ],
            # include_dirs=[
            #     "balinski_and_gomory/balinski-and-gomory-cuda/src",  # ✅ where solver.h lives
            # ],
            extra_compile_args={
                'cxx': ['-O3'],
                'nvcc': ['-O3'],# '-arch=sm_86'],  # adjust as needed
            }
        )
    ],
    cmdclass={'build_ext': BuildExtension},

    zip_safe=False,
    install_requires=requirements,
    include_package_data=True,
    package_data={
        "balinski_and_gomory.hylac_shortcut": ["libhylac.so"],
    },

    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
