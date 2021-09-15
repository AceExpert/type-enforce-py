import setuptools

with open("./README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="type-enforce",
    version="3.8.6",
    author="Cybertron",
    packages=['type_enforce'],
    description="Supports enforcing type annotations on functions and coroutines. Complete support for types from typing module.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.0.0,<3.9.5',
    include_package_data=True,
    url="https://github.com/AceExpert/type-enforce-py",
    project_urls={
        "Issue Tracker": "https://github.com/AceExpert/type-enforce-py/issues",
        "Contribute": "https://github.com/AceExpert/type-enforce-py/pulls"
    },
     classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Typing :: Typed',
    ],
    license='Apache 2.0',
)