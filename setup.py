from setuptools import setup

with open('README.md', 'r') as fh:
      long_description = fh.read()

setup(name='cab',
      version='0.0.1',
      description='Unpack cab archives',
      long_description=long_description,
      long_description_content_type='text/markdown',
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