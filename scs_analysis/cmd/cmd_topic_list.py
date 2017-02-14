"""
Created on 14 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdTopicList(object):
    """unix command line handler"""

    def __init__(self):
        """stuff"""
        self.__parser = optparse.OptionParser(usage="%prog ORG_ID [-p PATH] [-v]", version="%prog 1.0")

        # optional...
        self.__parser.add_option("--path", "-p", type="string", nargs=1, action="store", default="/", dest="path",
                                 help="partial path")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.org_id is None:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def org_id(self):
        return self.__args[0] if len(self.__args) > 0 else None


    @property
    def path(self):
        return self.__opts.path


    @property
    def verbose(self):
        return self.__opts.verbose


    @property
    def args(self):
        return self.__args


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdTopicList:{org_id:%s, path:%s, verbose:%s, args:%s}" % \
                    (self.org_id, self.path, self.verbose, self.args)
