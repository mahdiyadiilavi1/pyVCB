"""
Types:
1: Ink        2: Write  3: Read  4: Cross  --> Inks

5: OR/Buffer  6: AND    7: XOR
8: NOR/NOT    9: NAND  10: XNOR            --> Components

0: Nothing    11, 12 --> inf: Filter       --> Non logical Cells
"""


def neighborhood(x, y):
    return [[x, y + 1], [x, y - 1], [x - 1, y], [x + 1, y]]


def ctgr(ctp):
    if (ctp > 4) and (ctp < 12):
        ctg = 'c'
    elif ctp < 5:
        ctg = 'i'
    elif ctp > 11:
        ctg = 'n'
    return ctg


def check(cell, in_list, nx=0, ny=0):
    result = [[[item for item in x] for x in y] for y in in_list]
    ns = neighborhood(nx, ny)
    ncts = []
    ncps = []
    for n in ns:
        try:
            nc = in_list[n[0]][n[1]]
            ncts.append(nc[0])
            ncps.append(nc[1])
        except:
            print("reached to an end")
    if cell[0] == 1:  # ink
        if [1, 2, 3] in ncts:
            counter = 0
            for t in ncts:
                if [1, 2, 3] in t:
                    cell[1] = check(ns[counter], result)[cell[2]][cell[3]][1]
                    counter += 1
        if True:
            if ncts[0] == 4:
                cell[1] = in_list[ns[0][0]][ns[0][1]][5] or cell[1]
            if ncts[1] == 4:
                cell[1] = in_list[ns[1][0]][ns[1][1]][4] or cell[1]
            if ncts[2] == 4:
                cell[1] = in_list[ns[2][0]][ns[2][1]][7] or cell[1]
            if ncts[3] == 4:
                cell[1] = in_list[ns[3][0]][ns[3][1]][6] or cell[1]
        result[cell[2]][cell[3]][1] = cell[1]
    elif cell[0] == 2:  # write
        if [1, 2, 3] in ncts:
            counter = 0
            for t in ncts:
                if [1, 2, 3] in t:
                    cell[1] = check(ns[counter], result)[cell[2]][cell[3]][1]
                    counter += 1
        counter = 0
        for c in ncts:
            if c == 4:
                if counter == 0:
                    cell[1] = in_list[ns[0][0]][ns[0][1]][5] or cell[1]
                if counter == 1:
                    cell[1] = in_list[ns[1][0]][ns[1][1]][4] or cell[1]
                if counter == 2:
                    cell[1] = in_list[ns[2][0]][ns[2][1]][7] or cell[1]
                if counter == 3:
                    cell[1] = in_list[ns[3][0]][ns[3][1]][6] or cell[1]
            else:
                cell[1] = in_list[ns[counter][0]][ns[counter][1]][1]
            counter += 1
        result[cell[2]][cell[3]][1] = cell[1]
    elif cell[0] == 3:  # read
        # ink code start
        if [1, 2, 3] in ncts:
            counter = 0
            for t in ncts:
                if [1, 2, 3] in t:
                    cell[1] = check(ns[counter], result)[cell[2]][cell[3]][1]
                    counter += 1
        if True:
            if ncts[0] == 4:
                cell[1] = in_list[ns[0][0]][ns[0][1]][5] or cell[1]
            if ncts[1] == 4:
                cell[1] = in_list[ns[1][0]][ns[1][1]][4] or cell[1]
            if ncts[2] == 4:
                cell[1] = in_list[ns[2][0]][ns[2][1]][7] or cell[1]
            if ncts[3] == 4:
                cell[1] = in_list[ns[3][0]][ns[3][1]][6] or cell[1]
        # ink code end
        result[cell[2]][cell[3]][1] = cell[1]
    elif cell[0] == 4:  # cross
        cell.upower = in_list[ns[1][0]][ns[1][1]][1] if (ctgr(ncts[0]) == ctgr(ncts[1]) and ctgr(ncts[0]) == 'i') or (
                ncts[0] == ncts[1]) else None  # any ink or same cmp
        cell.dpower = in_list[ns[0][0]][ns[0][1]][1] if (ctgr(ncts[0]) == ctgr(ncts[1]) and ctgr(ncts[0]) == 'i') or (
                ncts[0] == ncts[1]) else None
        cell.lpower = in_list[ns[3][0]][ns[3][1]][1] if (ctgr(ncts[2]) == ctgr(ncts[3]) and ctgr(ncts[0]) == 'i') or (
                ncts[0] == ncts[1]) else None
        cell.rpower = in_list[ns[2][0]][ns[2][1]][1] if (ctgr(ncts[2]) == ctgr(ncts[3]) and ctgr(ncts[0]) == 'i') or (
                ncts[0] == ncts[1]) else None
    elif cell[0] == 5:  # or / buffer
        counter = 0
        objs = 0
        pows = 0
        for n in ns:
            ty = in_list[n[0]][n[1]][0]
            pw = in_list[n[0]][n[1]][1]
            if ty in [3, 5]:  # 3 = read
                objs += 1
                pows += pw
            counter += 1
        if pows > 0:
            cell[1] = 1
        result[cell[2]][cell[3]][1] = cell[1]
    elif cell[0] == 6:  # and
        counter = 0
        objs = 0
        pows = 0
        for n in ns:
            ty = in_list[n[0]][n[1]][0]
            pw = in_list[n[0]][n[1]][1]
            if ty in [3, 6]:  # 3 = read
                objs += 1
                pows += pw
            counter += 1
        if pows == objs:
            cell[1] = 1
        result[cell[2]][cell[3]][1] = cell[1]
    elif cell[0] == 7:  # xor
        counter = 0
        pows = 0
        for n in ns:
            ty = in_list[n[0]][n[1]][0]
            pw = in_list[n[0]][n[1]][1]
            if (ty == 3) or ((ty == 7) and pw):  # 3 = read
                pows += pw
            counter += 1
        if (pows % 2) == 1:
            cell[1] = 1
        result[cell[2]][cell[3]][1] = cell[1]
    elif cell[0] == 8:  # nand
        counter = 0
        objs = 0
        pows = 0
        for n in ns:
            ty = in_list[n[0]][n[1]][0]
            pw = in_list[n[0]][n[1]][1]
            if ty in [3, 6]:  # 3 = read
                objs += 1
                pows += pw
            counter += 1
        if pows != objs:
            cell[1] = 1
        result[cell[2]][cell[3]][1] = cell[1]
    elif cell[0] == 9:  # nor
        counter = 0
        objs = 0
        pows = 0
        for n in ns:
            ty = in_list[n[0]][n[1]][0]
            pw = in_list[n[0]][n[1]][1]
            if ty in [3, 5]:  # 3 = read
                objs += 1
                pows += pw
            counter += 1
        if pows <= 0:
            cell[1] = 1
        result[cell[2]][cell[3]][1] = cell[1]
    elif cell[0] == 10:  # xnor
        counter = 0
        pows = 0
        for n in ns:
            ty = in_list[n[0]][n[1]][0]
            pw = in_list[n[0]][n[1]][1]
            if (ty == 3) or ((ty == 7) and pw):  # 3 = read
                pows += pw
            counter += 1
        if (pows % 2) == 0:
            cell[1] = 1
        result[cell[2]][cell[3]][1] = cell[1]
    return result


if __name__ == '__main__':
    y = 0
    x = 3
    Celllist = [
        [[3, 1, 0, 0], [7, 0, 0, 1], [3, 0, 0, 2]],
        [[6, 0, 1, 0], [4, 0, 1, 1, 0, 0, 0, 0], [6, 0, 1, 2]],
        [[6, 0, 2, 0], [7, 0, 2, 1], [7, 0, 2, 2]],
        [[2, 0, 3, 0], [0, 0, 3, 1], [2, 0, 3, 2]]
    ]
    for i in check(Celllist[x][y], Celllist, x, y):
        print(i)
