class Node:
    def __init__(self,UserID, Value):
        self.Profile = UserID
        self.score = Value

def matching(DesiredAttributes, AllAttributes):
    List = []
    DesiredAcademicStatus = DesiredAttributes[1]
    DesiredGPA  = DesiredAttributes[2]
    DesiredSH = DesiredAttributes[3]
    DesiredAU = DesiredAttributes[4]
    DesiredCU = DesiredAttributes[5]
    DesiredVU = DesiredAttributes[6]
    DesiredHC = DesiredAttributes[7]
    DesiredEth = DesiredAttributes[8]
    DesiredGender = DesiredAttributes[9]
    DesiredHE = DesiredAttributes[10]
    DesiredWeekendSt = DesiredAttributes[11]
    DesiredWeekendE = DesiredAttributes[12]
    DesiredWeekSt = DesiredAttributes[13]
    DesiredWeekE = DesiredAttributes[14]
    DesiredMajorID = DesiredAttributes[15]
    DesiredMajorName = DesiredAttributes[16]

    for k in range(len(AllAttributes)):
        Attributes = AllAttributes[k]
        Score = 0
        OtherAcademicStatus = Attributes[1]
        OtherGPA = Attributes[2]
        OtherSH = Attributes[3]
        OtherAU = Attributes[4]
        OtherCU = Attributes[5]
        OtherVU = Attributes[6]
        OtherHC = Attributes[7]
        OtherEth = Attributes[8]
        OtherGender = Attributes[9]
        OtherHE = Attributes[10]
        OtherWeekendSt = Attributes[11]
        OtherWeekendE = Attributes[12]
        OtherWeekSt = Attributes[13]
        OtherWeekE = Attributes[14]
        OtherMajorID = Attributes[15]
        OtherMajorName = Attributes[16]
        #GPA
        if(OtherGPA >DesiredGPA):
            Score+=2
        #StudyHabits
        if(DesiredSH==OtherSH):
            Score+=1
        #Academic
        if DesiredAcademicStatus == OtherAcademicStatus:
            Score+=2
        #Alcohol
        if(DesiredAU == OtherAU):
            Score+=1
        #Cigs
        if (DesiredCU == OtherCU):
            Score += 1
        #Vape
        if (DesiredVU == OtherVU):
            Score += 1
        #Hair Color
        if (DesiredHC == OtherHC):
            Score += 1
        #Ethnicity
        if (DesiredEth == OtherEth):
            Score += 1
        #Height
        if (DesiredHE < OtherHE):
            Score += 1
        #Weekend Intersection
        if((OtherWeekendSt <= DesiredWeekendSt <= OtherWeekendE ) or (DesiredWeekendSt <= OtherWeekendSt <= DesiredWeekendE)):
            Score+=4
        #WeekDay Intersection
        if ((OtherWeekSt <= DesiredWeekSt <= OtherWeekE) or (DesiredWeekSt <= OtherWeekSt <= DesiredWeekE)):
            Score+=6
        if (DesiredGender == OtherGender):
            Score += 2
        if (DesiredAS == OtherAcademicStatus):
            Score += 2

        newNode = Node(userID,Score)
        List.append(newNode)

    return list







if __name__ == '__main__':
    main()