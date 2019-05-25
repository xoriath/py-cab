from setuptools import setup

setup(name='cab',
      version='0.1',
      description='Unpack cab archives',
      url='https://github.com/xoriath/py-cab',
      author='Morten Engelhardt Olsen',
      author_email='moro.engelhardt@gmail.com',
      license='MIT',
      py_modules=['cabfile', 'cabinet', 'data', 'folder', 'header'],
      package_dir={'': 'src'},
      classifiers=[
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
      ]
)