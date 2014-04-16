"""
 mbed CMSIS-DAP debugger
 Copyright (c) 2006-2013 ARM Limited

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

import logging
import traceback

from pyOCD.gdbserver import GDBServer
from pyOCD.board import MbedBoard
from optparse import OptionParser

logging.basicConfig(level=logging.INFO)

parser = OptionParser()
parser.add_option("-p", "--port", dest = "port_number", default = 3333, help = "Write the port number that GDB server will open")
parser.add_option("-b", "--board", dest = "board_name", default = None, help = "Write the board name you want to connect")
parser.add_option("-l", "--list", action = "store_true", dest = "list_all", default = False, help = "List all the connected board")
(option, args) = parser.parse_args()

gdb = None
if option.list_all == True:
    MbedBoard.listConnectedBoards()
else:
    try:
        board_selected = MbedBoard.chooseBoard(board_name = option.board_name)
        if board_selected != None:
            gdb = GDBServer(board_selected, int(option.port_number))
            while gdb.isAlive():
                gdb.join(timeout = 0.5)

    except KeyboardInterrupt:
        if gdb != None:
            gdb.stop()
    except Exception as e:
        print "uncaught exception: %s" % e
        traceback.print_exc()
        if gdb != None:
            gdb.stop()