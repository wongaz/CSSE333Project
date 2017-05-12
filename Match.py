class Node:
    def __init__(self, UserID, Value):
        self.Profile = UserID
        self.score = Value


def matching(DesiredAttributes, AllAttributes):
    List = []
    DesiredAcademicStatus = DesiredAttributes[]
    DesiredGPA = DesiredAttributes[]
    DesiredSH = DesiredAttributes[]
    Desired__ = DesiredAttributes[]
    Desired__ = DesiredAttributes[]
    Desired__ = DesiredAttributes[]
    Desired__ = DesiredAttributes[]
    Desired__ = DesiredAttributes[]
    Desired__ = DesiredAttributes[]
    Desired__ = DesiredAttributes[]
    Desired__ = DesiredAttributes[]
    Desired__ = DesiredAttributes[]
    Desired__ = DesiredAttributes[]
    Desired__ = DesiredAttributes[]
    Desired__ = DesiredAttributes[]
    Desired__ = DesiredAttributes[]
    Desired__ = DesiredAttributes[]

    for k in range(len(AllAttributes)):
        currentProfile = AllAttributes[k]
        Score = 0
        oGPA = currentProfile[]
        oProfileID = currentProfile[]
        oGPA = currentProfile[]
        oProfile = currentProfile[]
        oGPA = currentProfile[]
        oProfile = currentProfile[]
        oGPA = currentProfile[]
        oProfile = currentProfile[]
        oGPA = currentProfile[]
        oProfile = currentProfile[]
        if (oGPA > DesiredGPA):
            Score += 1
        if (DesiredSH == oSH):
            Score += 1
        if (DesiredAS == oAS):
            Score += 1
        if (DesiredAU == oAU):
            Score += 1
        if (DesiredCU == oCU):
            Score += 1
        if (DesiredVU == oVU):
            Score += 1
        if (DesiredHC == oHC):
            Score += 1
        if (DesiredEth == oEth):
            Score += 1
        if (DesiredH < oHeight):
            Score += 1

        newNode = Node(userID, Score)
        List.append(newNode)


if __name__ == '__main__':
    main()