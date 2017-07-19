import xlrd

class EXCEL:
    """EXCEL class contains definitions for many useful and custom utilities required to address the capabilities
       of the Dev/Test framework.It contains methods for reading and writing from/to an Excel workbook
    """

    def __init__(self, workbook, worksheet):
        """
        workbook    : the excel file itself
        worksheet   : specific sheet name in the workbook """
        self.workbook = workbook
        self.worksheet = worksheet
        try:
            self.wb = xlrd.open_workbook(self.workbook)
            self.ws = self.wb.sheet_by_name(self.worksheet)
        except Exception as e:
            raise Exception("Error opening excel %s :%s" % (self.workbook, e))

    def _openworkbooknsheet(self):
        """Custom function for opening a workbook and reading the content of the sheet specified
        USAGE:
        _openworkbooknsheet()
        """

        try:
            self.wb = xlrd.open_workbook(self.workbook)
            self.ws = self.wb.sheet_by_name(self.worksheet)
        except Exception as e:
            raise Exception("Error opening excel %s :%s" % (self.workbook, e))

    def _celladress4matchingvalue(self, matchstring):
        """
        Custom function for getting the address of the cell for a matched value
        USAGE:
        _celladress4matchingvalue(matchstring)

        matchstring : Specific string to be matched in the sheet ex: 'column headers'

        NOTE:
        This method/function can be used for any test involving Excel read
        """

        global row_addr, column_addr, cell_addr
        self.matchstring = matchstring

        self._openworkbooknsheet()
        rows = []
        columns = []

        try:

            for erowtup in range(self.ws.nrows):
                row = self.ws.row_values(erowtup)
                for ecol in range(len(row)):
                    if row[ecol] == matchstring:
                        rows.append(erowtup)
                        columns.append(ecol)
                        row_addr = rows[0]
                        column_addr = columns[0]
                        cell_addr = [rows[0], columns[0]]
                        return cell_addr

        except TypeError:
            raise Exception('TypeError')

        except Exception as e:
            raise Exception("Error Occurred : %s" % e)

