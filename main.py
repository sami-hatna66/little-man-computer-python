class Computer:
    def __init__(self):
        self.PC = 0
        self.ACC = 0
        self.IR = 0
        self.MAR = 0
        self.RAM = [0 for x in range(0, 100)]
        self.Instructions = [["INP", 901], ["ADD", 1], ["SUB", 2], ["STA", 3], ["LDA", 5], ["BRA", 6], ["BRZ", 7],
                             ["BRP", 8], ["OUT", 902], ["HLT"], ["DAT"]]
        self.Code = []
        self.Key = []
        self.Functions = []
        self.DatPointer = None
        self.Variables = []
        self.Running = True

    def Compile(self, Code):
        self.Code = []
        self.Key = []
        self.Functions = []
        self.DatPointer = None
        self.Variables = []
        self.Instructions = [["INP", 901], ["ADD", 1], ["SUB", 2], ["STA", 3], ["LDA", 5], ["BRA", 6], ["BRZ", 7],
                             ["BRP", 8], ["OUT", 902], ["HLT"], ["DAT"]]
        Counter = 0
        FoundDat = False
        for line in Code.splitlines():
            ContainsInstruction = False
            Split = line.split()
            if len(Split) <= 3:
                for instruction in self.Instructions:
                    if instruction[0].lower() in line.lower():
                        ContainsInstruction = True
                        break
                if ContainsInstruction:
                    if len(Split) == 1:
                        self.Code.append([Counter, None, line.strip(), None])
                    elif len(Split) == 3:
                        self.Code.append([Counter, Split[0], Split[1], Split[2]])
                        if "dat" not in line.lower():
                            self.Functions.append([Split[0], Counter])
                        else:
                            if not FoundDat:
                                self.DatPointer = Counter
                                FoundDat = True
                            self.Variables.append([Split[0], Counter])
                    elif len(Split) == 2 and "dat" not in line.lower():
                        self.Code.append([Counter, None, Split[0], Split[1]])
                    elif len(Split) == 2 and "dat" in line.lower():
                        if not FoundDat:
                            self.DatPointer = Counter
                            FoundDat = True
                        self.Code.append([Counter, Split[0], Split[1], 0])
                        self.Variables.append([Split[0], Counter])
                Counter += 1
        print(self.Code)
        print(self.Functions)
        print(self.Variables)
        print(self.DatPointer)

    def AssembleIntoRam(self):
        self.RAM = [0 for x in range(0, 100)]
        if self.DatPointer is not None:
            for x in range(self.DatPointer, len(self.Code)):
                self.RAM[x] = self.Code[x][3]
        else:
            self.DatPointer = len(self.Code)
        RAMCounter = 0
        for x in range(0, self.DatPointer):
            for word in self.Code[x]:
                if word is not None and type(word) != int:
                    for instruction in self.Instructions:
                        address = 0
                        if instruction[0].lower() == word.lower():
                            if instruction[0].lower() == "inp" or instruction[0].lower() == "out":
                                address = instruction[1]
                                self.RAM[RAMCounter] = instruction[1]
                            elif instruction[0].lower() == "hlt":
                                address = 0
                            else:
                                try:
                                    int(self.Code[x][3])
                                    self.RAM[RAMCounter] = int(str(instruction[1]) + str(self.Code[x][3]).zfill(2))
                                    address = int(str(instruction[1]) + str(self.Code[x][3]).zfill(2))
                                except:
                                    Found = False
                                    for var in self.Variables:
                                        if var[0] == self.Code[x][3]:
                                            self.RAM[RAMCounter] = int(str(instruction[1]) + str(var[1]).zfill(2))
                                            address = int(str(instruction[1]) + str(var[1]).zfill(2))
                                            Found = True
                                            break
                                    if not Found:
                                        for func in self.Functions:
                                            if func[0] == self.Code[x][3]:
                                                self.RAM[RAMCounter] = int(str(instruction[1]) + str(func[1]).zfill(2))
                                                address = int(str(instruction[1]) + str(func[1]).zfill(2))
                            self.Code[x].append(address)
                            RAMCounter += 1
        print(self.Code)

    def run(self):
        self.Running = True
        while self.PC < self.DatPointer and self.Running:
            Current = self.Code[self.PC][2].lower()
            if Current != "hlt":
                self.IR = str(self.Code[self.PC][4])[0]
                self.MAR = str(self.Code[self.PC][4])[-2:]
            if Current == "inp":
                self.Input()
            elif Current == "add":
                self.Add(self.Code[self.PC])
            elif Current == "sub":
                self.Subtract(self.Code[self.PC])
            elif Current == "sta":
                self.Store(self.Code[self.PC])
            elif Current == "lda":
                self.Load(self.Code[self.PC])
            elif Current == "bra":
                self.Branch(self.Code[self.PC])
            elif Current == "brz":
                self.BranchZero(self.Code[self.PC])
            elif Current == "brp":
                self.BranchPositive(self.Code[self.PC])
            elif Current == "out":
                self.Output()
            elif Current == "hlt":
                self.Running = False
            print("Line: " + str(self.Code[self.PC]) + " PC: " + str(self.PC) + " ACC: " + str(self.ACC) + " IR: " + str(self.IR) + " MAR: " + str(self.MAR))
            self.OutputRam()
            print("-------------------------------\n")
            self.PC += 1

    def Branch(self, line):
        FunctionSearch = self.FindFunction(line)
        if not FunctionSearch and type(FunctionSearch) == bool:
            self.Error("Logic", line[0])
        else:
            self.PC = FunctionSearch - 1

    def BranchZero(self, line):
        if self.ACC == 0:
            FunctionSearch = self.FindFunction(line)
            if not FunctionSearch and type(FunctionSearch) == bool:
                self.Error("Logic", line[0])
            else:
                self.PC = FunctionSearch - 1

    def BranchPositive(self, line):
        if self.ACC >= 0:
            FunctionSearch = self.FindFunction(line)
            if not FunctionSearch and type(FunctionSearch) == bool:
                self.Error("Logic", line[0])
            else:
                self.PC = FunctionSearch - 1

    def Load(self, line):
        try:
            int(line[3])
            self.ACC = int(self.RAM[int(line[3])])
        except:
            VariableSearch = self.FindVariable(line)
            if not VariableSearch and type(VariableSearch) == bool:
                self.Error("Logic", line[0])
            else:
                self.ACC = int(self.RAM[VariableSearch])

    def Output(self):
        print("OUTPUT: " + str(self.ACC))

    def Store(self, line):
        try:
            int(line[3])
            self.RAM[int(line[3])] = self.ACC
        except:
            VariableSearch = self.FindVariable(line)
            if not VariableSearch and type(VariableSearch) == bool:
                self.Error("Logic", line[0])
            else:
                self.RAM[VariableSearch] = self.ACC

    def Input(self):
        userinput = input("Input: ")
        self.ACC = int(userinput)

    def Add(self, line):
        Adder = 0
        try:
            int(line[3])
            Adder = self.RAM[int(line[3])]
        except:
            VariableSearch = self.FindVariable(line)
            if not VariableSearch and type(VariableSearch) == bool:
                self.Error("Logic", line[0])
            else:
                Adder = self.RAM[VariableSearch]
        self.ACC += int(Adder)

    def Subtract(self, line):
        Sub = 0
        try:
            int(line[3])
            Sub = self.RAM[int(line[3])]
        except:
            VariableSearch = self.FindVariable(line)
            if not VariableSearch and type(VariableSearch) == bool:
                self.Error("Logic", line[0])
            else:
                Sub = self.RAM[VariableSearch]
        self.ACC -= int(Sub)

    def OutputRam(self):
        Counter = 0
        for x in range(0, 10):
            String = ""
            for z in range(0, 10):
                String += str(self.RAM[Counter]) + ", "
                Counter += 1
            print(String)

    def Error(self, errortype, linenum):
        # Logic or syntax
        print(errortype + " error, line " + str(linenum))
        self.Running = False

    def FindVariable(self, line):
        FoundVar = False
        for var in self.Variables:
            if var[0] == line[3]:
                return var[1]
        if not FoundVar:
           return False

    def FindFunction(self, line):
        FoundFunc = False
        for Func in self.Functions:
            if Func[0] == line[3]:
                return Func[1]
        if not FoundFunc:
            return False

# Example usage of LMC without UI
ComputerInstance = Computer()
ComputerInstance.Compile("loop lda A\nout A\nsub one\nsta A\nbrp loop\nhlt\nA dat 10\none dat 1")
ComputerInstance.AssembleIntoRam()
ComputerInstance.OutputRam()
print("\n")
ComputerInstance.run()