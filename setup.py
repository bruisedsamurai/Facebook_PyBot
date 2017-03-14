from setuptools import setup


def requirements():
	req_list=[]
	#List of requirements for this project
	with open("requirements.txt") as req:
		for each in req:
			req_list.append(each.strip())

	return req_list


setup(
    name='Facebook_PyBot',
    version='0.6a',
    author='hundredeir',
    author_email='hundredeir@protonmail.com',
    packages=['Facebook'],
    scripts=['examples/echo'],
    url='https://github.com/hundredeir/Facebook_PyBot',
    license='GPL3',
    description='This is an Unofficial Facebook bot API in python. Facebook Bots can be build using this library.',
    long_description=open('README.txt').read(),
    install_requires=requirements(),
    keywords="Facebook Bot API Wrapper Python",
    classifiers=[
              'Development Status :: 3 - Alpha',
              'Intended Audience :: Developers',
              'License :: GNU General Public License v3 (GPLv3)',
              'Operating System :: OS Independent',
              'Topic :: Software Development :: Libraries :: Python Modules',
              'Topic :: Communication :: Chat',
              'Topic :: Internet',
              'Programming Language :: Python',
          ],
)
