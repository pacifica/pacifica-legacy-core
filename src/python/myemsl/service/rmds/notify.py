#!/usr/bin/python

import os
import sys
import struct
from pacifica.notification import *
from myemsl.getconfig import getconfig
config = getconfig()

from myemsl.logging import getLogger

logger = getLogger(__name__)

wsw = writer_socket_writer(writer_socket_get('rmds'))

def notify(user, item_id, version):
	logger.debug("rmds notify:", item_id, version)
	packed = struct.pack("<2q", int(item_id), int(version))
	wsw.write(packed)
	return 200

