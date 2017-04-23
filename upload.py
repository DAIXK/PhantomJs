#coding:utf-8

import sqlite3
import xlrd
import xlwt
import parser
import time

# cookies = parser.get_cookies()
table = xlrd.open_workbook('04-1.xlsx')
table = table.sheet_by_index(0)
nrows = table.nrows
print(nrows)
read_word = []
w = xlwt.Workbook()
ws = w.add_sheet('sheet1',cell_overwrite_ok=True)



aso100 = parser.aso100('20170411.xlsx')

for row in range(3,nrows):
    if table.row_values(row)[1]:
        print(table.row_values(row)[1])
        ws.write(row, 1, table.row_values(row)[1])
        if table.row_values(row)[1] in aso100:
            ws.write(row,2,aso100[table.row_values(row)[1]]['排名'])
            ws.write(row,3, aso100[table.row_values(row)[1]]['指数'])
            ws.write(row,4, aso100[table.row_values(row)[1]]['结果数'])
            print('匹配\n')
            continue

        else:
            result = parser.cqaso(table.row_values(row)[1])
            print('爬取')
            # print(result)
            if len(result) == 0:
                ws.write(row, 3, 'none')
                print('没有获取\n')

            else:
                # print(result)
                for item in result:
                    if item['id'] == table.row_values(row)[1]:
                         ws.write(row, 3, item['priority'])
                         print('获取'+'指数:'+str(item['priority'])+'\n')
                         break
                    else:
                        ws.write(row, 3, 'none')
                        print('没有获取\n')




    else:
        continue

w.save('update.xlsx')
