import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='rawsocketpy',
      version='0.4.0',
      description='This library allows you to implement a custom layer 2 communication using raw sockets in Python 2 and Python 3, synchronous and asynchronous, with and without callbacks.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/AlexisTM/rawsocket_python',
      author='AlexisTM',
      author_email='alexis.paques@gmail.com',
      license='MIT',
      packages=setuptools.find_packages(),
      classifiers=(
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 3",
          "Development Status :: 4 - Beta",
          "License :: OSI Approved :: MIT License",
          "Operating System :: POSIX :: Linux",
          "Topic :: Internet",
          "Topic :: System :: Networking",
          "Topic :: System :: Networking :: Monitoring",
      ),
      zip_safe=False)
