import xlrd
book = xlrd.open_workbook("skroty_klubow.xls")
print("The number of worksheets is {0}".format(book.nsheets))
print("Worksheet name(s): {0}".format(book.sheet_names()))
sh = book.sheet_by_index(0)
print("{0} {1} {2}".format(sh.name, sh.nrows, sh.ncols))
print("Cell D30 is {0}".format(sh.cell_value(rowx=29, colx=3)))
for rx in range(3,sh.nrows):
    skrot = sh.cell_value(rx,1)
    nazwa = sh.cell_value(rx, 2)
    woj = sh.cell_value(rx, 3)
    siedz = sh.cell_value(rx, 4)
