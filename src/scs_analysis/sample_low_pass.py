#!/usr/bin/env python3

"""
Created on 24 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The XX utility is used to .

EXAMPLES
xx

FILES
~/SCS/aws/

DOCUMENT EXAMPLE
xx

SEE ALSO
scs_analysis/




command line example:
./socket_receiver.py | ./sample_low_pass.py -d 10 -c 0.01 val.NO2.cnc
"""

import sys

from scs_analysis.cmd.cmd_sample_low_pass_filter import CmdLowPassFilter

from scs_core.data.json import JSONify
from scs_core.data.low_pass_filter import LowPassFilter
from scs_core.data.path_dict import PathDict

from scs_core.sys.exception_report import ExceptionReport


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdLowPassFilter()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print(cmd, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    lpf = LowPassFilter.construct(cmd.delta, cmd.cut_off)

    if cmd.verbose:
        print(lpf, file=sys.stderr)
        sys.stderr.flush()

    try:
        # ------------------------------------------------------------------------------------------------------------
        # run...

        for line in sys.stdin:
            datum = PathDict.construct_from_jstr(line)

            if datum is None:
                break

            value = datum.node(cmd.path)

            if value is None:
                break

            target = PathDict()

            target.copy(datum, 'rec')

            target.append(cmd.path + '.src', value)
            target.append(cmd.path + '.lpf', round(lpf.compute(value), cmd.precision))

            print(JSONify.dumps(target.node()))
            sys.stdout.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        if cmd.verbose:
            print("sample_low_pass: KeyboardInterrupt", file=sys.stderr)

    except Exception as ex:
        print(JSONify.dumps(ExceptionReport.construct(ex)), file=sys.stderr)