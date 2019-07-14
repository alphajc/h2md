#!/usr/bin/python
# -*- coding: utf8 -*-
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.

from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="h2md",
    version="0.0.1",
    author="Jerry Chan（陈家俊）",
    author_email="jerry@mydream.ink",
    description="这能html中正文部分转化为markdown文件",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/canovie/h2md",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'h2md = src.__main__:main'
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
