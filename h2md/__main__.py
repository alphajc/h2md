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

import argparse
import fileinput

import h2md


def main(argv=None):

  parser = argparse.ArgumentParser()
  parser.add_argument('file', default='-', nargs='?', help='HTML 正文部分转 Markdown')
  args = parser.parse_args(argv)

  html = ''.join([line for line in fileinput.input(args.file)])
  print(h2md.convert(html))


if __name__ == '__main__':
  main()
