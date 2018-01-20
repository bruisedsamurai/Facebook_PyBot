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
    version='0.8b9',
    author='hundredeir',
    author_email='hundredeir@protonmail.com',
    packages=['Facebook'],
    scripts=['examples/echo.py','examples/userInfo.py'],
    url='https://github.com/hundredeir/Facebook_PyBot',
    license='LGPL3',
    description='This is an Unofficial Facebook bot API in python. Facebook Bots can be build using this library.',
    long_description=open('readme.md').read(),
    install_requires=requirements(),
    extras_require={'UltraJSON':["ujson"]},
    keywords="Facebook Bot API Wrapper Python",
    classifiers=[
              'Development Status :: 4 - Beta',
              'Intended Audience :: Developers',
              'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
              'Operating System :: OS Independent',
              'Topic :: Software Development :: Libraries :: Python Modules',
              'Topic :: Communications :: Chat',
              'Topic :: Internet',
              'Programming Language :: Python',
          ],
)
