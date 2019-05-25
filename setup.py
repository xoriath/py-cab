from setuptools import setup, find_packages

setup(name='cab',
      version='0.1',
      description='Unpack cab archives',
      url='https://github.com/xoriath/py-cab',
      author='Morten Engelhardt Olsen',
      author_email='moro.engelhardt@gmail.com',
      license='MIT',
      packages=find_packages('cab'),  
      zip_safe=False)