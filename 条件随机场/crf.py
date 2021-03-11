
#全局变量
#读取语料库
wordFile=open("msr_training.utf8.ic",'r',encoding='utf-8')
wordFeed=wordFile.readlines() #[0]=字 [2]=标注
wordFile.close
wordFeedLen=len(wordFeed)
#print(wordFeed)
 
#创建字的列表
def setList(a):  #a为要分词的句子
    testWord = [ ]
    for i in a:
        testWord.append(i)
    return testWord
 
 
#创建及初始化矩阵（字典）
def setDict(testWord): #testWord为句子每个字的列表
    testDict = { }
    for i in testWord:
        testDict[i]=[0,0,0,0]  #[B,M,E,S]
    return testDict
 
####### 特征二 #######
#特征二 计算状态频率矩阵值
def  charaB(testWord): #testDict为每个字的字典
    testDict=setDict(testWord)
    for i in testWord:
        B=0
        M=0
        E=0
        S=0
        BMESsum=0
        for j in range(wordFeedLen):
            #print(wordFeed[j][0])
            if i == wordFeed[j][0]:
                if wordFeed[j][2] == 'B':
                    B=B+1
                elif  wordFeed[j][2] == 'M':
                    M=M+1
                elif  wordFeed[j][2] == 'E':
                    E=E+1
                elif  wordFeed[j][2] == 'S':
                    S=S+1
        BMESsum=B+M+E+S
        testDict[i]=[B/BMESsum,M/BMESsum,E/BMESsum,S/BMESsum]
    return testDict
 
 
####### 特征三 #######
#创建及初始化字的4x4的矩阵（字典）
def setDict2(testWord): #testWord为句子每个字的列表
    testDict = { }
    for i in testWord:
        testDict[i]=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]  #[B,M,E,S]的四阶矩阵
    return testDict
 
#特征三内的判断判断函数
def charCJudge(i,mark1): #i为要判断的字符 mark1为i的状态
        B=0
        M=0
        E=0
        S=0
        BMESsum=0
        for j in range(wordFeedLen):
            #print(wordFeed[j][0])
            if i == wordFeed[j][0] and wordFeed[j][2]==mark1 and j+1<len(wordFeed):
                if wordFeed[j+1][2] == 'B':
                    B=B+1
                elif  wordFeed[j+1][2] == 'M':
                    M=M+1
                elif  wordFeed[j+1][2] == 'E' :
                    E=E+1
                elif  wordFeed[j+1][2] == 'S' :
                    S=S+1
                else:
                    pass
        BMESsum=B+M+E+S
        if BMESsum>0 :
            return [B/BMESsum,M/BMESsum,E/BMESsum,S/BMESsum]
        elif BMESsum==0 :
            return [0,0,0,0]
 
#特征三 计算转移频率矩阵值
def  charaC(testWord):
    testDict=setDict2(testWord)
    for i in testWord:
        j=0
        for mark1 in ['B','M','E','S']:
            testDict[i][j]=charCJudge(i,mark1)
            j=j+1
            #print(i,j)
            #print(testDict)
    return testDict
 
 
 
####### 特征四 #######
#创建及初始化上下文字典
def setDict3(testWord): #testWord为句子每个字的列表
    testDict = { }
    for i in testWord:
        testDict[i]={'B':{},'M':{},'E':{},'S':{}}  #[B,M,E,S]的四阶矩阵
    return testDict
 
#特征四内的上下文关系概率函数
def charDJudge(i,mark1): #i为要判断的字符 mark1为i的状态
    testDict = { }
    lastSum=0
    nextSum=0
    for j in range(wordFeedLen):
    #print(wordFeed[j][0])
        if i == wordFeed[j][0] and wordFeed[j][2]==mark1 and j+1<len(wordFeed):
            #特征四内的上文关系概率函数 
            if wordFeed[j-1][0] not in testDict:
                testDict[wordFeed[j-1][0]]=[1,0]
                lastSum=lastSum+1
            elif wordFeed[j-1][0] in testDict:
                testDict[wordFeed[j-1][0]][0]=testDict[wordFeed[j-1][0]][0]+1
                lastSum=lastSum+1
            #特征四内的下文关系概率函数        
            if wordFeed[j+1][0] not in testDict:
                testDict[wordFeed[j+1][0]]=[0,1]
                nextSum=nextSum+1
            elif wordFeed[j+1][0] in testDict:
                testDict[wordFeed[j+1][0]][1]=testDict[wordFeed[j+1][0]][1]+1
                nextSum=nextSum+1
    for key, value in testDict.items():
        testDict[key][0]=testDict[key][0]/lastSum
        testDict[key][1]=testDict[key][1]/nextSum
    return testDict
 
 
#特征四计算特定的字与上下文关系
def  charaD(testWord):
    testDict=setDict3(testWord)
    for i in testWord:
        for mark1 in ['B','M','E','S']:
            testDict[i][mark1]=charDJudge(i,mark1)
    return testDict
 
 
####### 实现分词  #######
 
#返回分词结果
def getResult(signList):
    resultString=''
    for iList in signList:
        if iList[1]=='B':
            resultString=resultString+' '+iList[0]
        elif iList[1]=='M':
            resultString=resultString+iList[0]
        elif iList[1]=='E':
            resultString=resultString+iList[0]+' '
        elif iList[1]=='S':
            resultString=resultString+' '+iList[0]+' '
    return resultString
 
#返回分词标记转换
def trans(num):
    if num==0:
        return 'B'
    elif num==1:
        return 'M'
    elif num==2:
        return 'E'
    elif num==3:
        return 'S'
 
#字与状态对应关系计算
def separateWords(testString):
    testString=str1     #要测试的句子
    testList=setList(testString) #字符串列表
    #计算 特征二 特征三 特征四
    print('字符串列表:',testList,'\n')
    testCharaB=charaB(testList) #特征二 字符BMES矩阵
    #print('特征二:',testCharaB,'\n')
    testCharaC=charaC(testList) #特征三 转移频率
    #print('特征三',testCharaC,'\n')
    testCharaD=charaD(testList) #特征四 上下关联关系
    print('特征四',testCharaD,'\n')
    
    #生成字与状态对应关系矩阵值（字典）
    column=['B','M','E','S']
    relaDict=setDict(testList)
    wayList=[]
    a=0
    b=0
    c=0
    d=0
    for i in range(len(testList)):
        oneWaylist=[]
        for j in range(len(column)):
            #print(testList[i],column[j])
            if i==0 :
                if testList[i+1] not in testCharaD[testList[i]][column[j]] :
                    e=0
                else:
                    e=testCharaD[testList[i]][column[j]][testList[i+1]][0]
                relaDict[testList[i]][j]= e + testCharaB[testList[i]][j]
            elif i>0 and i<len(testList)-1:
                a=testCharaC[testList[i-1]][0][j] * relaDict[testList[i-1]][0]
                b=testCharaC[testList[i-1]][1][j] * relaDict[testList[i-1]][1]
                c=testCharaC[testList[i-1]][2][j] * relaDict[testList[i-1]][2]
                d=testCharaC[testList[i-1]][3][j] * relaDict[testList[i-1]][3]
                if testList[i-1] not in testCharaD[testList[i]][column[j]] : #特征四上文
                    e=0
                else:
                    e=testCharaD[testList[i]][column[j]][testList[i-1]][0]
                if testList[i+1] not in testCharaD[testList[i]][column[j]] : #特征四下文
                    f=0
                else:
                    f=testCharaD[testList[i]][column[j]][testList[i+1]][1]
                relaDict[testList[i]][j]=max(a,b,c,d) + testCharaB[testList[i]][j]  + e + f
            elif i==len(testList)-1:
                a=testCharaC[testList[i-1]][0][j] * relaDict[testList[i-1]][0]
                b=testCharaC[testList[i-1]][1][j] * relaDict[testList[i-1]][1]
                c=testCharaC[testList[i-1]][2][j] * relaDict[testList[i-1]][2]
                d=testCharaC[testList[i-1]][3][j] * relaDict[testList[i-1]][3]
                if testList[i-1] not in testCharaD[testList[i]][column[j]] : #特征四上文
                     e=0
                else:
                    e=testCharaD[testList[i]][column[j]][testList[i-1]][0]
                relaDict[testList[i]][j]= max(a,b,c,d) + testCharaB[testList[i]][j] +e
            #wayDict={'a':a,'b':b,'c':c,'d':d}
            findMax=[a,b,c,d]
            oneWaylist.append(findMax.index(max(findMax)))
        #print(oneWaylist)
        wayList.append(oneWaylist)
    print('\n关系矩阵:',relaDict,'\n\n回溯路径:',wayList)
    
    
    
    signList=[]
    lenList=[]
    #lenList=list(range(len(testList))).reverse()
    for i in range(len(testList)):
        lenList.append(i)
    
    lenList.reverse()
    
    for i in lenList:
        testWord=testList[i]
        if i == len(testList)-1:
            indexNum=relaDict[testWord].index(max(relaDict[testWord]))
            sign=trans(indexNum)
            signList.append([testWord,sign])
            nextIndexNum=wayList[i][indexNum]
        else:
            sign=trans(nextIndexNum)
            signList.append([testWord,sign])
            indexNum=relaDict[testWord].index(max(relaDict[testWord]))
            nextIndexNum=wayList[i][indexNum]
            
    
    signList.reverse()
    print("\n分词标记：",signList,'\n')
    print("分词原句:",testString,'\n')
    print("分词结果:",getResult(signList))
 
 
 
################主函数################
import time
 
#from multiprocessing.dummy import Pool as ThreadPool
#pool = ThreadPool(processes=8)
 
str1=input("请输入要分词的字符串:")
print('\n')
start = time.clock()
separateWords(str1)
 
            
#results2 = pool.map(separateWords, str1)
#pool.close()
#pool.join()
 
print('\n')
 
elapsed = (time.clock() - start)
print("分词用时:",elapsed,'秒')
 
 
