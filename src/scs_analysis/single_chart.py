#!/usr/bin/env python3

"""
Created on 21 Jul 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The single_chart utility is used to display a Matplotlib categorical chart for one or more data sources. Data is
provided by a sequence of JSON documents on stdin. The charting source is specified by a path to a leaf node in the
JSON document.

A "relative" ("-r") option ploys the first data point at y position zero, and all subsequent points relative to the
first point. This is useful when examining noise on a signal whose absolute values may be far from zero.

Note that the chart is a simple approximation to a timeline chart - values are plotted successively, with no account
taken of the interval between samples.

EXAMPLES
./socket_receiver.py | ./single_chart.py -r val.afe.sns.CO.cnc

SEE ALSO
scs_analysis/histo_chart
scs_analysis/multi_chart
"""

import sys
import warnings

from scs_analysis.chart.single_chart import SingleChart
from scs_analysis.cmd.cmd_single_chart import CmdSingleChart

from scs_core.data.json import JSONify
from scs_core.data.path_dict import PathDict

from scs_core.sync.line_reader import LineReader


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    warnings.filterwarnings("ignore", module="matplotlib")

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdSingleChart()

    if cmd.verbose:
        print(cmd, file=sys.stderr)

    chart = None
    proc = None

    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        # reader...
        reader = LineReader(sys.stdin.fileno())

        if cmd.verbose:
            print(reader, file=sys.stderr)

        # chart...
        chart = SingleChart(cmd.batch_mode, cmd.x, cmd.y[0], cmd.y[1], cmd.relative, cmd.path)

        if cmd.verbose:
            print(chart, file=sys.stderr)
            sys.stderr.flush()


        # ------------------------------------------------------------------------------------------------------------
        # run...

        proc = reader.start()

        for line in reader.lines:
            if chart.closed:
                break

            if line is None:
                chart.pause()
                continue

            datum = PathDict.construct_from_jstr(line)

            if datum is None:
                break

            if cmd.echo:
                print(JSONify.dumps(datum.node()))
                sys.stdout.flush()

            chart.plot(datum)


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        if cmd.verbose:
            print("single_chart: KeyboardInterrupt", file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # close...

    finally:
        if proc:
            proc.terminate()

        if chart is not None and not chart.closed:
            if cmd.verbose:
                print("single_chart: holding", file=sys.stderr)

            # noinspection PyBroadException

            try:
                chart.hold()
            except Exception:
                pass
