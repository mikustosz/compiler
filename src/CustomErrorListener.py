from antlr4.error.ErrorListener import ErrorListener
import sys


def print_error(msg):
    print(f'ERROR\n{msg}', file=sys.stderr)


class CustomErrorListener(ErrorListener):

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        print_error("line " + str(line) + ":" + str(column) + " " + msg)
        raise Exception

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        print_error('reportAmbiguity')
        raise Exception

    # def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
    #     print_error('reportAttemptingFullContext')
    #     raise Exception

    # def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
    #     print_error('reportContextSensitivity')
    #     raise Exception
