"""
Created on 25 Apr 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

source repo: scs_analysis
"""

import optparse

from scs_core.data.path_dict import PathDict


# --------------------------------------------------------------------------------------------------------------------

class CmdNode(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [{ [-x] [-a] | -s }] [-v] [SUB_PATH_1 .. SUB_PATH_N]",
                                              version="%prog 1.0")

        # optional...
        self.__parser.add_option("--exclude", "-x", action="store_true", dest="exclude", default=False,
                                 help="include all sub-paths except the named one(s)")

        self.__parser.add_option("--array", "-a", action="store_true", dest="array", default=False,
                                 help="output the sequence of input JSON documents as array")

        self.__parser.add_option("--sequence", "-s", action="store_true", dest="sequence", default=False,
                                 help="output the contents of the input array node(s) as a sequence")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.exclude and self.sequence:
            return False

        if self.array and self.sequence:
            return False

        return True


    def includes(self, path):
        for sub_path in self.sub_paths:
            if PathDict.sub_path_includes_path(sub_path, path):
                return not self.exclude

        return self.exclude


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def exclude(self):
        return self.__opts.exclude


    @property
    def array(self):
        return self.__opts.array


    @property
    def sequence(self):
        return self.__opts.sequence


    @property
    def verbose(self):
        return self.__opts.verbose


    @property
    def sub_paths(self):
        return set(self.__args)


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdNode:{exclude:%s, array:%s, sequence:%s, verbose:%s, sub_paths:%s}" %  \
               (self.exclude, self.array, self.sequence, self.verbose, self.sub_paths)
