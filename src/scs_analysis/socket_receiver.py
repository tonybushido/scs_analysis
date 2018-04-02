#!/usr/bin/env python3

"""
Created on 18 Aug 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The socket_receiver utility is used to accept data via a Unix socket, with data sourced from the same host, or
another host on the same local area network. A socket_sender utility is provided for the purpose of sourcing data,
as part of the scs_dev package.

The socket_receiver utility should be started before socket_sender. When socket_sender terminates, socket_receiver
will also terminate.

EXAMPLES
./socket_receiver.py -p 2002

SEE ALSO
scs_analysis/uds_receiver
scs_dev/socket_sender
"""

import sys

from scs_analysis.cmd.cmd_socket_receiver import CmdSocketReceiver

from scs_host.comms.network_socket import NetworkSocket


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdSocketReceiver()

    if cmd.verbose:
        print(cmd, file=sys.stderr)

    receiver = None

    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        receiver = NetworkSocket('', cmd.port)

        if cmd.verbose:
            print(receiver, file=sys.stderr)
            sys.stderr.flush()


        # ------------------------------------------------------------------------------------------------------------
        # run...

        for message in receiver.read():
            print(message)
            sys.stdout.flush()

            receiver.ack()


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        if cmd.verbose:
            print("socket_receiver: KeyboardInterrupt", file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # close...

    finally:
        if receiver:
            receiver.close()
