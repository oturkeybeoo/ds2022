file = open("worddocument.txt", "r").read()
wordList = []
elementToRemove = []

def map():
    splitList = file.split()
    for word in splitList:
        wordList.append([word, 1])
    print("Mapping: ", wordList)
    
def reduce():
    for index, keyAndValue in enumerate(wordList):
        #print(index, keyAndValue)
        for incrementComparator in range(index+1, len(wordList)):
            #print(incrementComparator)
            if index != len(wordList)-1:
                if keyAndValue[0] == wordList[incrementComparator][0]:
                    wordList[index][1]+=1
                    if incrementComparator not in elementToRemove:
                        elementToRemove.append(incrementComparator)
    print(elementToRemove)
    elementToRemove.sort()
    for i in range(len(elementToRemove)-1, -1, -1):
        wordList.pop(elementToRemove[i])
    print("Reducing: ", wordList)
    
def main():
    map()
    reduce()
main()
