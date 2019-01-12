from antlr4.error.ErrorListener import ErrorListener
import sys


def print_error(msg):
    print(f'ERROR\n{msg}', file=sys.stderr)


class CustomErrorListener(ErrorListener):

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        print_error("line " + str(line) + ":" + str(column) + " " + msg)
        sys.exit(1)

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        print_error('reportAmbiguity')
        sys.exit(1)

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        print_error('reportAttemptingFullContext')
        sys.exit(1)

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        print_error('reportContextSensitivity')
        sys.exit(1)
