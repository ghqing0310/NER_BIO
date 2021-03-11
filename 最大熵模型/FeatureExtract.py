
file = open('sentences.txt', 'r', encoding="utf-8")

sentenceList = []
tag = []
IOBList = []
tempList = []
numSentences = 0
counter=0
dic = {'S','B','I','E'}
for line in inFileGenia:
    # split the current token and entity and load into initial list
    inputTokenEntity = line.split()
    # if numSentences >= 50:
    #     break
    # statement determines whether end of sentence or not.  If not end of sentence, then keep getting tokens to build sentence
    # once sentence is built, then do processing to create feature set for each token
    if len(inputTokenEntity) == 0:
        for item in IOBList:
            if item in dic:
                counter=counter+1
                break
        i = 0
        for token in sentenceList:
            # append IOBs
            tempList.append(IOBList[i])
            # append token and POSTags
            tempList.append(token)

            if i == 0 and len(IOBList) > 2:
                tempList.append('0')
                tempList.append('0')
                tempList.append(sentenceList[i + 1])
                tempList.append(sentenceList[i + 2])

            if i == len(IOBList) - 1 and len(IOBList) > 2:
                tempList.append(sentenceList[i - 2])
                tempList.append(sentenceList[i - 1])
                tempList.append('0')
                tempList.append('0')

            if i == 1 and len(IOBList) > 3:
                tempList.append('0')
                # tempList.append('0')
                tempList.append(sentenceList[i - 1])
                # tempList.append(tag[i - 1])
                tempList.append(sentenceList[i + 1])
                # tempList.append(tag[i + 1])
                tempList.append(sentenceList[i + 2])
                # tempList.append(tag[i + 2])

            if i == len(IOBList) - 2:
                tempList.append(sentenceList[i - 2])
                tempList.append(sentenceList[i - 1])
                tempList.append(sentenceList[i + 1])
                tempList.append('0')

            if i >= 2 and i < len(IOBList) - 2:
                tempList.append(sentenceList[i - 2])
                # tempList.append(tag[i - 2])
                tempList.append(sentenceList[i - 1])
                # tempList.append(tag[i - 1])
                tempList.append(sentenceList[i + 1])
                # tempList.append(tag[i + 1])
                tempList.append(sentenceList[i + 2])
                # tempList.append(tag[i + 2])

            # 前一个词与当前词
            if i > 0:
                tempList.append(sentenceList[i - 1] + '/' + token)
            else:
                tempList.append('0')
            # 当前词与后一个词
            if i < len(IOBList) - 1:
                tempList.append(token + '/' + sentenceList[i + 1])
            else:
                tempList.append('0')
            # 当前词与前两个词
            if i > 1:
                tempList.append(sentenceList[i - 2] + '/' + sentenceList[i - 1] + '/' + token)
            else:
                tempList.append('0')

            # 当前词与后两个词
            if i < len(IOBList) - 2:
                tempList.append(token + '/' + sentenceList[i + 1] + '/' + sentenceList[i + 2])
            else:
                tempList.append('0')

            # 当前词与前后两个词
            if i > 1 and i < len(IOBList) - 2:
                tempList.append(
                    sentenceList[i - 2] + '/' + sentenceList[i - 1] + '/' + token + '/' + sentenceList[i + 1] + '/' +
                    sentenceList[i + 2])
            else:
                tempList.append('0')

            # write out token and features to file
            for item in tempList[:-1]:
                oFileTrain.write("%s\t" % item)
            oFileTrain.write("%s" % tempList[-1])
            oFileTrain.write("\n")

            # clear out tempList and increment current token
            tempList = []
            i = i + 1

        oFileTrain.write("\n")
        sentenceList = []
        tag = []
        IOBList = []

        # increment number of sentences processed and print to screen
        numSentences = numSentences + 1
        print(numSentences)

    else:
        # not end of sentence, so continue to build arrays
        sentenceList.append(inputTokenEntity[0])
        # tag.append(inputTokenEntity[1])
        IOBList.append(inputTokenEntity[1])

print("Feature Extraction Complete")
print(counter)