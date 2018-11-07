#!/usr/bin/env python

# Copyright (c) 2018, G. vd. Hoorn
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rosnode
import rosgraph
import sys
import argparse

# lots of things 'borrowed' from rosnode

try:
    from xmlrpc.client import ServerProxy
except ImportError:
    from xmlrpclib import ServerProxy

parser = argparse.ArgumentParser()
parser.add_argument('ROS_MASTER_URI', type=str, nargs='?', metavar='URI', help='ROS master URI to use.')
args = parser.parse_args()

ID = '/rosnode'
master = rosgraph.Master(ID, master_uri=args.ROS_MASTER_URI)
print ("Using master at {}".format(master.getUri()))

nodes = rosnode.get_node_names()
print ("Known nodes: " + ', '.join(nodes))

for node in nodes:
    print ("  " + node)

    node_api = rosnode.get_api_uri(master, node)
    if not node_api:
        print("    API URI: error (unknown node: {}?)".format(node))
        continue
    print ("    API URI: " + node_api)

    node = ServerProxy(node_api)
    pid = rosnode._succeed(node.getPid(ID))
    print ("    PID    : {}".format(pid))
