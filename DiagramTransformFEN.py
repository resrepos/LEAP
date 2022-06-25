#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import re, pprint, unicodedata, string, os
def extract_pieces_positions(ranks):
    print(':::Extract Pieces Positions:::')
    files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    rank = ['8', '7', '6', '5', '4', '3', '2', '1']
    White_Pieces = ['^R', '^N', '^B', '^Q', '^K','^P']
    Black_Pieces = ['#R', '#N', '#B', '#Q', '#K','#P']
    Pieces_position = []
    White_Pieces_Positions = []
    Black_Pieces_Positions = []
    Empty_Positions = []
    for row in enumerate(ranks):
        #print(row[1], len(row[1]))
        #print(len(row), len(row[1].replace(' ','')))
        cleaned_row = row[1].replace(' ','')
        #rank.append(cleaned_row[0])

        #print('cleaned_row', cleaned_row.split('|'), len(cleaned_row.split('|')))
        #Pieces_position.append(cleaned_row.split('|'))
        #print('Pieces_position', Pieces_position)
        #RankDic[row[0]] = cleaned_row
        splitted_row = cleaned_row.split('|')
        del splitted_row[9:]
        #print('splitted_row',splitted_row, len(splitted_row))
        for l in enumerate(splitted_row):
            #if l[1] in rank:
                #print('Rank', l[1])
            #else:
            if l[1] not in rank:
                square = str(files[l[0]-1]) + str(splitted_row[0])
                if len(l[1]) == 0:
                    #print('empty square','at Rank', splitted_row[0], 'Square',square)
                    Empty_Positions.append(['', square])
                if l[1] in White_Pieces:
                    if l[1] == White_Pieces[len(White_Pieces) - 1]:
                        piece = str(l[1]) + str(l[0])
                        #print('White Piece', piece,'at Rank', splitted_row[0], 'Square',square)
                        White_Pieces_Positions.append([piece, square])

                    else:
                        piece = l[1]
                        #print('White Piece', piece,'at Rank', splitted_row[0], 'Square',square)
                        White_Pieces_Positions.append([piece, square])
                if l[1] in Black_Pieces:
                    if l[1] == Black_Pieces[len(Black_Pieces) - 1]:
                        piece = str(l[1]) + str(l[0])
                        #print('Black Piece', str(l[1])+str(l[0]),'at Rank', splitted_row[0], 'Square',square)
                        Black_Pieces_Positions.append([piece, square])
                    else:
                        piece = l[1]
                        #print('Black Piece', l[1],'at Rank', splitted_row[0], 'Square',square)
                        Black_Pieces_Positions.append([piece, square])

    print('Empty_Positions:',Empty_Positions,len(Empty_Positions),'\nWhite_Pieces_Positions:', White_Pieces_Positions, len(White_Pieces_Positions), '\nBlack_Pieces_Positions', Black_Pieces_Positions, len(Black_Pieces_Positions), '\n')
    #print(rank)
    return Empty_Positions, White_Pieces_Positions, Black_Pieces_Positions

def Print_Diagram(doc):
    print(':::Read Board Diagram File:::')
    count = 0#to count the number of lines of the diagrm
    topLine = "^(\s*?)\+?-+-\+?$"
    middleLine = '(\s*)?\|-+-\|$'
    files = '^(\s*?)A\s*B\s*C\s*D\s*E\s*F\s*G\s*H\W*?$|^((\s)*?[0-9])*$'
    rank = '(\W*?)\w*?(\W*?)\|(\W*?)|(\W*?)\#+[A-Za-z]?(\W*?)|(\W*?)\^+[A-Za-z]?(\W*?)\|+(\W*?)(\w*?)$'
    DIAG = '^\s+Diagram\.?\s+?[0-9]+?\.?$|^\s+Diagram\.?\s+?[0-9]+?\.?-+((\w)*(\.)*|(-)*|\W*?(\s)?)*$'
    ranks = []
    NEWdiag = 0#to count how many diagram in the text
    ReadNewFile = open(doc,'r')
    #Diagram_doc = doc.replace('_PreProcessed.txt','_DiagramFile.txt')
    DiagramFile = []
    lines = ReadNewFile.readlines()
    newCount = 0
    #print(len(lines))
    for i in range(0, len(lines)):
        i = i + newCount
        newCount = 0
        if i < len(lines):
            lne = lines[i]
            #print('i', i, 'line', lne)
            if lne !="\n":#to remove extra whitelines
                lne = ''.join(filter(lambda x: x in string.printable, lne))
                if (re.findall(files, lne) or re.findall(topLine, lne)):
                    check = lines[i+1]
                    if (re.findall(rank, check) or re.findall(topLine, check)):
                        while count != -1:
                            count = count + 1
                            if re.findall(files, lne):
                                DiagramFile.append(lne)
                            elif re.findall(topLine, lne):
                                DiagramFile.append(lne)
                            elif re.findall(middleLine, lne):
                                DiagramFile.append(lne)
                            elif re.findall(files, lne):
                                DiagramFile.append(lne)
                            elif re.findall(rank, lne):
                                DiagramFile.append(lne)
                                ranks.append(lne.replace('\n','').replace('     ', ''))
                            elif re.findall(DIAG, lne):
                                NEWdiag = NEWdiag+1
                                DiagramFile.append(lne)
                                newCount = count
                                break
                            i = i + 1
                            lne = lines[i]
            count=0
    #print("Total number of diagram", NEWdiag)
    
    #DiagramFile.close()
    print('ranks', ranks, '\n')
    return ranks

def prepareBoard(Empty_Positions, White_Pieces_Positions, Black_Pieces_Positions):
    print(':::Parse Board Diagram:::')
    ranks = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    tempF = []

    for black in Black_Pieces_Positions:

        tempF.append([int(black[1][1]), [black[1][0], black[0]]])

    for white in White_Pieces_Positions:

        tempF.append([int(white[1][1]), [white[1][0], white[0]]])

    for empty in Empty_Positions:

        tempF.append([int(empty[1][1]), [empty[1][0], empty[0]]])


    tempF = sorted(tempF,key=lambda l:l[0], reverse=True)
    #print('row', tempF)   

    row8 = []
    row7 = []
    row6 = []
    row5 = []
    row4 = []
    row3 = []
    row2 = []
    row1 = []

    for e, r in enumerate(tempF):
        p = ''
        #print(r)
        i = ranks.index(r[1][0])
        #print(i)

        if '#' in r[1][1]:
            p = str(r[1][1][1]).lower()
        if '^' in r[1][1]:
            p = str(r[1][1][1])

        #print(p)
        tempF[e] = [r[0], [i+1, p]]

        if r[0] == 1:
            row1.append([i+1, p])
        if r[0] == 2:
            row2.append([i+1, p])
        if r[0] == 3:
            row3.append([i+1, p])
        if r[0] == 4:
            row4.append([i+1, p])
        if r[0] == 5:
            row5.append([i+1, p])
        if r[0] == 6:
            row6.append([i+1, p])
        if r[0] == 7:
            row7.append([i+1, p])
        if r[0] == 8:
            row8.append([i+1, p])

    row1 = sorted(row1,key=lambda l:l[0])
    row2 = sorted(row2,key=lambda l:l[0])
    row3 = sorted(row3,key=lambda l:l[0])
    row4 = sorted(row4,key=lambda l:l[0])
    row5 = sorted(row5,key=lambda l:l[0])
    row6 = sorted(row6,key=lambda l:l[0])
    row7 = sorted(row7,key=lambda l:l[0])
    row8 = sorted(row8,key=lambda l:l[0])
    board = []
    board.append(row8)
    board.append(row7)
    board.append(row6)
    board.append(row5)
    board.append(row4)
    board.append(row3)
    board.append(row2)
    board.append(row1)
    print('board', board, '\n')
    return board


def FENboard(board):
    print(':::Get FEN Board Position:::')
    fenBoard = ''

    for ind, rank in enumerate(board):
        #print(ind+1)
        ll = []
        empty = 0
        for i, r in enumerate(rank):
            
            if r[1] != '':
                ll.append(r[1])
                #print(ll)
            if r[1] =='':
                empty =1
                ll.append(empty)
                
        count = 0 
        for l in ll:
            if type(l) is int:
                count +=1
            else:
                if count >0:
                    fenBoard = fenBoard+str(count)+str(l)
                    count =0
                    
                else:
                    fenBoard = fenBoard+str(l)
            
        if count>0:
            fenBoard = fenBoard+str(count)

        if ind != len(board)-1:
            fenBoard = fenBoard+'/'
    #print(len(fenBoard))

    fenBoard = fenBoard + ' w '
    #print(len(fenBoard), fenBoard)
    
    last = fenBoard.rfind('/')
    castleIndex = fenBoard[last:fenBoard.index(' w ')]
    #print(castleIndex)

    if 'K' in castleIndex:
        K = castleIndex.index('K')
        #print(fenBoard[56])
        firtR= castleIndex.find('R')
        lastR = castleIndex.rfind('R')
        if firtR< K:
            if lastR >K:
                if lastR == len(castleIndex)-1:
                    fenBoard = fenBoard + 'K'
                if firtR == 1:
                    fenBoard = fenBoard + 'Q'


    first = fenBoard.find('/')
    castleIndex = fenBoard[:first]

    if 'k' in castleIndex:
        k = castleIndex.index('k')
        firtR= castleIndex.find('r')
        lastR = castleIndex.rfind('r')
        if firtR< k:
            if lastR >k:
                if lastR == len(castleIndex)-1:
                    fenBoard = fenBoard + 'k'
                if firtR == 0:
                    fenBoard = fenBoard + 'q'
                
        
    if (fenBoard[-1] != 'K') and (fenBoard[-1] != 'Q') and (fenBoard[-1] != 'k') and (fenBoard[-1] != 'q'):
        fenBoard = fenBoard + '-'

    fenBoard = fenBoard + ' - 0 1'
    print('fenBoard', fenBoard)
    return fenBoard


def createFENfile(fenBoard, filepath):
    filepath = filepath.replace('_PreProcessed.txt', 'FENboard.txt')
    FENfile = open(filepath, 'w')
    FENfile.write(fenBoard)
    FENfile.close()
    return filepath
    
#   
Game_Types = ['INTRODUCTORY_Edited','Openings_Edited','Endings_Edited','Middle_Edited']
for gt, p_dir in enumerate(Game_Types):
    print(p_dir, 'folder')
    # Parent Directory path
    parent_dir = "./" + p_dir + "/"
    #createFolders(parent_dir) commented for now because I already done it
    for subdir, dirs, files in os.walk(parent_dir):
        #print('sub_Directors: \'{}\'\nDirectors: \'{}\'\nFiles: \'{}\' '.format(subdir, dirs, files))
        if subdir != parent_dir:

            for subfiles in files:
                if subfiles.endswith('PreProcessed.txt'):
                    #print('sub_files: \'{}\' \nfile path: \'{}\' '.format(subfiles, filepath))
                    #print('File: \'{}\''.format(subfiles))
                    print(':::Prepare File: \'{}\':::'.format(subfiles))
                    filepath = subdir + os.sep + subfiles
                    PreProcessedFile = filepath
                    ranks = Print_Diagram(PreProcessedFile)
                    Empty_Positions, White_Pieces_Positions, Black_Pieces_Positions = extract_pieces_positions(ranks)
                    board = prepareBoard(Empty_Positions, White_Pieces_Positions, Black_Pieces_Positions)
                    fenBoard = FENboard(board)
                    FENfile = createFENfile(fenBoard, filepath)
                    file = open(FENfile, 'r')
                    print(file.read())

