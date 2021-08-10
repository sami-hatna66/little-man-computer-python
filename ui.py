from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import time

class ExecuteThread(QThread):
    UpdatePos = pyqtSignal(list, list)
    DoneSignal = pyqtSignal(bool, object)
    DoneSignal2 = pyqtSignal()
    def __init__(self, Instruction, Destination = None, IsBranch = None):
        super(ExecuteThread, self).__init__()
        self.Position1 = [15, 150, 15, 15]
        self.Position2 = [0, 0, 0, 0]
        self.Instruction = Instruction
        self.Destination = Destination
        self.IsBranch = IsBranch
        self.Running = True
        self.OutputFlag = False
    def run(self):
        Path = [[-15, -15]]
        Path2 = [[0, 0]]
        Coords1 = {0:40, 1:89, 2:137, 3:186, 4:233, 5:281, 6:330, 7:377, 8:425, 9:473}
        Coords2 = {0:45, 1:86, 2:127, 3:170, 4:213, 5:255, 6:296, 7:339, 8:381, 9:423}
        if self.Instruction.lower() == "inp":
            Path = [[x, 530] for x in range(70, 93, 2)]
            Path += [[93, x] for x in range(530, 350, -2)]
            Path += [[x, 350] for x in range(93, 70, -2)]
        elif self.Instruction.lower() == "sta":
            Path = [[x, 350] for x in range(70, 113, 3)]
            Path += [[113, x] for x in range(350, 473, 3)]
            Path += [[x, 473] for x in range(113, 144, 3)]
            Path += [[143, x] for x in range(473, Coords1[self.Destination // 10], -3)]
            Path += [[x, Coords1[self.Destination // 10]] for x in range(143, 143 + Coords2[(self.Destination - (10 * (self.Destination // 10)))], 3)]
        elif self.Instruction.lower() == "lda" or self.Instruction.lower() == "add" or self.Instruction.lower() == "sub":
            LineA = [[x, 283] for x in range(20, 113, 3)]
            LineB = [[113, x] for x in range(283, 473, 3)]
            LineC = [[x, 473] for x in range(113, 144, 3)]
            LineD = [[143, x] for x in range(473, Coords1[self.Destination // 10], -3)]
            LineE = [[x, Coords1[self.Destination // 10]] for x in range(143, 143 + Coords2[(self.Destination - (10 * (self.Destination // 10)))], 3)]
            LineF = [[113, x] for x in range(473, 347, -3)]
            LineG = [[x, 347] for x in range(113, 60, -3)]
            Path = LineA + LineB + LineC + LineD + LineE + LineE[::-1] + LineD[::-1] + LineC[::-1] + LineF + LineG
        elif self.Instruction.lower() == "out":
            Path = [[x, 347] for x in range(70, 115, 2)]
            Path += [[115, x] for x in range(347, 158, -2)]
            Path += [[x, 158] for x in range(115, 45, -2)]
            Path += [[45, x] for x in range(158, 100, -2)]
            self.OutputFlag = True
        if self.Instruction.lower() == "add" or self.Instruction.lower() == "sub":
            Path += [[x, 347, None] for x in range(60, 17, -3)]
            Path += [[17, x, None] for x in range(347, 435, 3)]
            Path += [[x, 435, None] for x in range(17, 37, 3)]
            Path += [[37, x, None] for x in range(435, 347, -3)]
            Path += [[x, 347, None] for x in range(37, 60, 3)]
            Path2 = [[x, 347] for x in range(60, 40, -3)]
            Path2 += [[40, x] for x in range(347, 435, 3)]
            Path2 += [[x, 435] for x in range(40, 26, -3)]
            Path2.append([26, 435])
        if (self.Instruction.lower() == "bra" or self.Instruction.lower() == "brp" or self.Instruction.lower() == "brz") \
                and self.Destination is not None:
            Path = [[x, 283] for x in range(20, 113, 3)]
            Path += [[113, x] for x in range(283, 195, -3)]
            Path += [[x, 195] for x in range(113, 20, -3)]
        Counter = 0
        Counter2 = 0
        while self.Running:
            if Counter < len(Path):
                self.Position1[0] = Path[Counter][0]
                self.Position1[1] = Path[Counter][1]
                if len(Path[Counter]) == 3 and Counter2 < len(Path2):
                    self.Position2[2] = 15
                    self.Position2[3] = 15
                    self.Position2[0] = Path2[Counter2][0]
                    self.Position2[1] = Path2[Counter2][1]
                    Counter2 += 1
                else:
                    self.Position2 = [0, 0, 0, 0]
                self.UpdatePos.emit(self.Position1, self.Position2)
                Counter += 1
            else:
                self.Running = False
            time.sleep(0.01)
        self.Position2 = [0, 0, 0, 0]
        self.Position1 = [0,0,0,0]
        self.UpdatePos.emit(self.Position1, self.Position2)
        self.DoneSignal.emit(self.OutputFlag, self.IsBranch)
        time.sleep(0.5)
        self.DoneSignal2.emit()
        self.quit()

class FetchThread(QThread):
    UpdatePos = pyqtSignal(list, list, list)
    DoneSignal = pyqtSignal()
    ChangePCSignal = pyqtSignal()
    def __init__(self, Destination):
        super(FetchThread, self).__init__()
        self.Position1 = [15,195,15,15]
        self.Position2 = [15,195,15,15]
        self.Position3 = [15,195,15,15]
        self.Destination = Destination
        Coords1 = {0:40, 1:89, 2:137, 3:186, 4:233, 5:281, 6:330, 7:377, 8:425, 9:473}
        Coords2 = {0:45, 1:86, 2:127, 3:170, 4:213, 5:255, 6:296, 7:339, 8:381, 9:423}
        ListA = [[x, 195] for x in range(15, 112, 4)]
        ListB = [[112, x] for x in range(195, 475, 4)]
        ListC = [[x, 473] for x in range(112, 145, 4)]
        ListD = [[143, x] for x in range(473, Coords1[self.Destination//10], -4)]
        ListD.append([143, Coords1[self.Destination//10]])
        ListE = [[x, Coords1[self.Destination//10]] for x in range(143, 143 + Coords2[(self.Destination - (10 * (self.Destination//10)))], 4)]
        ListF = [[112, x] for x in range(475, 283, -4)]
        self.Path = ListA + ListB + ListC + ListD + ListE + ListE[::-1] + ListD[::-1] + ListC[::-1] + ListF

        self.MARPath = [[x, 283] for x in range(112, 17, -4)]

        ListG = [[112, x] for x in range(280, 235, -4)]
        ListH = [[x, 235] for x in range(112, 15, -4)]
        self.IRPath = ListG + ListH

        ListI = [[15, x] for x in range(195, 430, 2)]
        ListJ = [[x, 430] for x in range(15, 38, 2)]
        ListK = [[38, x] for x in range(430, 195, -2)]
        ListL = [[x, 195] for x in range(38, 15, -2)]
        self.PCPath = ListI + ListJ + ListK + ListL

        self.Running = True

    def run(self):
        Done1 = False
        IntermediaryDone1 = False
        IntermediaryDone2 = False
        Done2 = False
        DoneChangePC = False
        Counter1 = 0
        Counter2 = 0
        Counter3 = 0
        Counter4 = 0
        while self.Running:
            if Counter4 < len(self.PCPath):
                self.Position1[0] = self.PCPath[Counter4][0]
                self.Position1[1] = self.PCPath[Counter4][1]
                Counter4 += 1
            else:
                self.Position1 = [0, 0, 0, 0]
                Done1 = True
                if not DoneChangePC:
                    self.ChangePCSignal.emit()
                    DoneChangePC = True
            if Counter1 < len(self.Path):
                self.Position2[0] = self.Path[Counter1][0]
                self.Position2[1] = self.Path[Counter1][1]
                self.Position3[0] = self.Path[Counter1][0]
                self.Position3[1] = self.Path[Counter1][1]
                Counter1 += 1
            else:
                if IntermediaryDone1 and IntermediaryDone2:
                    Done2 = True
                else:
                    if Counter2 < len(self.MARPath):
                        self.Position2[0] = self.MARPath[Counter2][0]
                        self.Position2[1] = self.MARPath[Counter2][1]
                        Counter2 += 1
                    else:
                        self.Position2 = [0,0,0,0]
                        IntermediaryDone1 = True
                    if Counter3 < len(self.IRPath):
                        self.Position3[0] = self.IRPath[Counter3][0]
                        self.Position3[1] = self.IRPath[Counter3][1]
                        Counter3 += 1
                    else:
                        self.Position3 = [0,0,0,0]
                        IntermediaryDone2 = True

            self.UpdatePos.emit(self.Position1, self.Position2, self.Position3)
            time.sleep(0.01)
            if Done1 and Done2:
                self.DoneSignal.emit()
                self.Running = False
        self.Position1 = [0, 0, 0, 0]
        self.Position2 = [0, 0, 0, 0]
        self.Position3 = [0, 0, 0, 0]
        self.quit()

class Computer(QObject):
    OutputSignal = pyqtSignal(int)
    InputSignal = pyqtSignal()
    FinishedStepSignal = pyqtSignal()
    UpdatePos = pyqtSignal(list, list, list)
    UpdatePosExecute = pyqtSignal(list, list)
    UpdateCPU = pyqtSignal()
    def __init__(self):
        super(Computer, self).__init__()
        self.PC = 0
        self.DisplayPC = 0
        self.ACC = 0
        self.DisplayACC = 0
        self.IR = 0
        self.MAR = 0
        self.RAM = [0 for x in range(0, 100)]
        self.DisplayRAM = [0 for x in range(0, 100)]
        self.Instructions = [["INP", 901], ["ADD", 1], ["SUB", 2], ["STA", 3], ["LDA", 5], ["BRA", 6], ["BRZ", 7],
                             ["BRP", 8], ["OUT", 902], ["HLT"], ["DAT"]]
        self.Code = []
        self.Key = []
        self.Functions = []
        self.DatPointer = None
        self.Variables = []
        self.Running = True

    def Reset(self):
        try:
            self.FetchWorkerInstance.Running = False
        except:
            pass
        try:
            self.ExecuteThreadInstance.Running = False
        except:
             pass
        self.PC = 0
        self.DisplayPC = 0
        self.ACC = 0
        self.DisplayACC = 0
        self.IR = 0
        self.MAR = 0
        self.RAM = [0 for x in range(0, 100)]
        self.DisplayRAM = [0 for x in range(0, 100)]
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
        self.DisplayRAM = self.RAM

    def CreateDisplayString(self):
        DisplayString = ""
        for y in range(0, self.DatPointer):
            DisplayString += str(y).zfill(2) + "   "
            DisplayString += str(self.Code[y][2]) + "   "
            Found = False
            if self.Code[y][3] is not None:
                for var in self.Variables:
                    if var[0] == self.Code[y][3]:
                        DisplayString += str(var[1]).zfill(2)
                        Found = True
                        break
                if not Found:
                    for func in self.Functions:
                        if func[0] == self.Code[y][3]:
                            DisplayString += str(func[1]).zfill(2)
                            break
            DisplayString += "\n"
        for x in range(0, len(self.Code) - self.DatPointer):
            DisplayString += str(self.DatPointer + x).zfill(2) + "   "
            DisplayString += "DAT   " + str(self.RAM[self.Variables[x][1]]).zfill(2) + "\n"
        return DisplayString

    def run(self):
        if self.PC < self.DatPointer and self.Running:
            self.FetchWorkerInstance = FetchThread(self.PC)
            self.FetchWorkerInstance.UpdatePos.connect(self.UpdatePos.emit)
            self.FetchWorkerInstance.DoneSignal.connect(self.run2)
            self.FetchWorkerInstance.ChangePCSignal.connect(self.UpdateDisplayPC)
            self.FetchWorkerInstance.start()

    def UpdateDisplayPC(self):
        self.DisplayPC = self.PC
        self.DisplayPC += 1
        self.UpdateCPU.emit()

    def run2(self):
        Current = self.Code[self.PC][2].lower()
        if Current != "hlt":
            self.IR = str(self.Code[self.PC][4])[0]
            self.MAR = str(self.Code[self.PC][4])[-2:]
        self.UpdateCPU.emit()
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
            self.PC = 0

    def run3(self, Flag, BranchFlag):
        self.DisplayACC = self.ACC
        self.DisplayRAM = [x for x in self.RAM]
        if Flag:
            self.OutputSignal.emit(self.ACC)
        if BranchFlag is not None:
            self.DisplayPC = BranchFlag

    def run4(self):
        if self.Running:
            self.PC += 1
            self.FinishedStepSignal.emit()

    def StartExecution(self, Instruction, Destination = None, IsBranch = None):
        self.ExecuteThreadInstance = ExecuteThread(Instruction, Destination, IsBranch)
        self.ExecuteThreadInstance.UpdatePos.connect(self.UpdatePosExecute.emit)
        self.ExecuteThreadInstance.DoneSignal.connect(self.run3)
        self.ExecuteThreadInstance.DoneSignal2.connect(self.run4)
        self.ExecuteThreadInstance.start()

    def Branch(self, line):
        FunctionSearch = self.FindFunction(line)
        if not FunctionSearch and type(FunctionSearch) == bool:
            self.Error("Logic", line[0])
        else:
            self.PC = FunctionSearch - 1
            self.StartExecution("BRA", FunctionSearch, FunctionSearch)

    def BranchZero(self, line):
        if self.ACC == 0:
            FunctionSearch = self.FindFunction(line)
            if not FunctionSearch and type(FunctionSearch) == bool:
                self.Error("Logic", line[0])
            else:
                self.PC = FunctionSearch - 1
                self.StartExecution("BRZ", FunctionSearch, FunctionSearch)
        else:
            self.StartExecution("BRZ", None)

    def BranchPositive(self, line):
        if self.ACC >= 0:
            FunctionSearch = self.FindFunction(line)
            if not FunctionSearch and type(FunctionSearch) == bool:
                self.Error("Logic", line[0])
            else:
                self.PC = FunctionSearch - 1
                self.StartExecution("BRP", FunctionSearch, FunctionSearch)
        else:
            self.StartExecution("BRP", None)

    def Load(self, line):
        try:
            int(line[3])
            self.ACC = int(self.RAM[int(line[3])])
            Execute = True
            Destination = int(line[3])
        except:
            VariableSearch = self.FindVariable(line)
            if not VariableSearch and type(VariableSearch) == bool:
                self.Error("Logic", line[0])
                Execute = False
            else:
                self.ACC = int(self.RAM[VariableSearch])
                Execute = True
                Destination = VariableSearch
        if Execute:
            self.StartExecution("LDA", Destination)

    def Output(self):
        self.StartExecution("OUT")

    def Store(self, line):
        try:
            int(line[3])
            self.RAM[int(line[3])] = self.ACC
            Execute = True
            Destination = int(line[3])
        except:
            VariableSearch = self.FindVariable(line)
            if not VariableSearch and type(VariableSearch) == bool:
                self.Error("Logic", line[0])
                Execute = False
            else:
                self.RAM[VariableSearch] = self.ACC
                Execute = True
                Destination = VariableSearch
        if Execute:
            self.StartExecution("STA", Destination)

    def Input(self):
        self.InputSignal.emit()

    def ReceivedInput(self, value):
        self.ACC = int(value)
        self.StartExecution("INP")

    def Add(self, line):
        Adder = 0
        try:
            int(line[3])
            Adder = self.RAM[int(line[3])]
            Execute = True
            Destination = int(line[3])
        except:
            VariableSearch = self.FindVariable(line)
            if not VariableSearch and type(VariableSearch) == bool:
                self.Error("Logic", line[0])
                Execute = False
            else:
                Adder = self.RAM[VariableSearch]
                Execute = True
                Destination = VariableSearch
        self.ACC += int(Adder)
        if Execute:
            self.StartExecution("ADD", Destination)

    def Subtract(self, line):
        Sub = 0
        try:
            int(line[3])
            Sub = self.RAM[int(line[3])]
            Execute = True
            Destination = int(line[3])
        except:
            VariableSearch = self.FindVariable(line)
            if not VariableSearch and type(VariableSearch) == bool:
                self.Error("Logic", line[0])
                Execute = False
            else:
                Sub = self.RAM[VariableSearch]
                Execute = True
                Destination = VariableSearch
        self.ACC -= int(Sub)
        if Execute:
            self.StartExecution("SUB", Destination)

    def OutputRam(self):
        Counter = 0
        for x in range(0, 10):
            String = ""
            for z in range(0, 10):
                String += str(self.RAM[Counter]) + ", "
                Counter += 1

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

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.CentralWidget = QWidget()
        self.setCentralWidget(self.CentralWidget)
        self.MainLayout = QHBoxLayout()
        self.CentralWidget.setLayout(self.MainLayout)

        self.setFixedSize(1050, 600)

        self.Computer = Computer()
        self.Computer.OutputSignal.connect(self.Output)
        self.Computer.InputSignal.connect(self.Input)
        self.Computer.FinishedStepSignal.connect(self.RunProgram)

        self.CPU = CPUWidget(Computer = self.Computer)
        self.Computer.UpdatePos.connect(self.CPU.PosChange)
        self.Computer.UpdatePosExecute.connect(self.CPU.ExecutePosChange)
        self.Computer.UpdateCPU.connect(self.CPU.update)

        self.DetectingInput = False

        self.Timer = QTimer()

        self.InitUI()

        self.show()

    def InitUI(self):
        self.VBL1 = QVBoxLayout()
        self.MainLayout.addLayout(self.VBL1)
        self.HBL1 = QHBoxLayout()
        self.VBL1.addLayout(self.HBL1)

        self.CodeTextBox = QTextEdit()
        self.HBL1.addWidget(self.CodeTextBox)

        self.CompiledCode = CompiledCodeWidget()
        self.HBL1.addWidget(self.CompiledCode)

        self.MainLayout.addWidget(self.CPU)

        self.ControlsGL = QGridLayout()
        self.VBL1.addLayout(self.ControlsGL)

        self.CompileBTN = QPushButton("Assemble into RAM")
        self.CompileBTN.clicked.connect(self.CompileCode)
        self.ControlsGL.addWidget(self.CompileBTN, 0, 0)
        self.ResetBTN = QPushButton("Reset")
        self.ResetBTN.clicked.connect(self.Reset)
        self.ControlsGL.addWidget(self.ResetBTN, 0, 1)
        self.RunBTN = QPushButton("Run")
        self.RunBTN.clicked.connect(self.FirstRun)
        self.ControlsGL.addWidget(self.RunBTN, 1, 0, 1, 2)

    def keyPressEvent(self, QKeyEvent):
        if (QKeyEvent.key() == Qt.Key_Return or QKeyEvent == Qt.Key_Enter) and self.DetectingInput and self.CPU.InputBox.hasFocus():
            self.Computer.ReceivedInput(self.CPU.InputBox.text())
            self.CPU.InputBox.setText("")
            self.CPU.InputBox.setEnabled(False)
            self.CPU.InputBox.setStyleSheet("border: 1px solid black")
            self.Computer.Running = True
            self.DetectingInput = False

    def Input(self):
        self.Computer.Running = False
        self.CPU.InputBox.setEnabled(True)
        self.CPU.InputBox.setStyleSheet("border: 2px solid red")
        self.DetectingInput = True

    def Output(self, Value):
        self.CPU.OutputBox.append(str(Value))

    def FirstRun(self):
        self.CPU.OutputBox.setText("")
        self.Computer.Running = True
        self.RunProgram()

    def RunProgram(self):
        self.Computer.run()
        self.CPU.update()

    def CompileCode(self):
        self.Computer.Compile(self.CodeTextBox.toPlainText())
        self.Computer.AssembleIntoRam()
        self.CPU.update()
        DisplayString = self.Computer.CreateDisplayString()
        self.CompiledCode.setText(DisplayString)

    def Reset(self):
        self.Computer.Reset()
        self.CompiledCode.setText("")
        self.CPU.OutputBox.setText("")
        self.CPU.InputBox.setText("")
        self.CPU.update()

class CompiledCodeWidget(QTextEdit):
    def __init__(self):
        super(CompiledCodeWidget, self).__init__()

        self.setReadOnly(True)
        Font = QFont("Courier", 11)
        self.setFont(Font)

        self.setFixedWidth(150)

class CPUWidget(QWidget):
    def __init__(self, Computer):
        super(CPUWidget, self).__init__()
        self.Computer = Computer
        self.setFixedSize(600, 600)

        self.ActiveAddress = None

        self.Pos1 = [0, 0, 0, 0]
        self.Pos2 = [0, 0, 0, 0]
        self.Pos3 = [0, 0, 0, 0]
        self.Pos4 = [0,0,0,0]
        self.Pos5 = [0,0,0,0]

        self.InputBox = QLineEdit(self)
        self.InputBox.setStyleSheet("border: 1px solid black")
        self.InputBox.setEnabled(False)
        self.InputBox.textChanged.connect(self.ValidateText)
        self.InputBox.setAlignment(Qt.AlignCenter)
        InputFont = QFont("Arial", 18)
        self.InputBox.setFont(InputFont)
        OnlyInt = QIntValidator()
        self.InputBox.setValidator(OnlyInt)
        self.InputBox.setAttribute(Qt.WA_MacShowFocusRect, False)
        self.InputBox.setFixedSize(70, 40)
        self.InputBox.move(10, 520)

        self.OutputBox = QTextEdit(self)
        self.OutputBox.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.OutputBox.setStyleSheet("border: 1px solid black")
        self.OutputBox.setReadOnly(True)
        self.OutputBox.setAttribute(Qt.WA_MacShowFocusRect, False)
        self.OutputBox.setFixedSize(90, 105)
        self.OutputBox.move(10, 25)

        self.show()

    def ValidateText(self):
        if len(self.InputBox.text()) > 3:
            self.InputBox.setText(self.InputBox.text()[:-1])

    def PosChange(self, Position1, Position2, Position3):
        self.Pos1 = Position1
        self.Pos2 = Position2
        self.Pos3 = Position3
        self.update()

    def ExecutePosChange(self, Position1, Position2):
        self.Pos4 = Position1
        self.Pos5 = Position2
        self.update()

    def paintEvent(self, QPaintEvent):
        Painter = QPainter()
        Painter.begin(self)
        Painter.setBrush(QBrush(QColor("#5cad2d")))
        Painter.setPen(QPen(QColor("#5cad2d")))
        Painter.drawRect(0, 0, 600, 575)

        Painter.setPen(QPen(QColor("#222222")))
        Painter.setBrush(QBrush(QColor("#222222")))
        Painter.drawRect(170, 20, 425, 485)

        Counter = 0
        Level = 0
        Font = QFont("Arial", 14)
        BoldFont = QFont("Arial", 14, QFont.Bold)
        FontMetric = QFontMetrics(Font)
        Painter.setFont(Font)
        for x in range(0, 10):
            for z in range(0, 10):
                if z + (x*10) == self.Computer.PC:
                    Painter.setPen(QPen(Qt.red, 2))
                else:
                    Painter.setPen(QPen(QColor("#767676")))
                Painter.setBrush(QBrush(QColor("#767676")))
                xpos = 175 + (37 * z) + (z * 5)
                ypos = ((z // 10) * 43 + 25) + (Level * 43) + (x * 5)
                Painter.drawRect(xpos, ypos, 37, 43)
                Painter.setPen(QPen(Qt.black))
                Painter.setBrush(QBrush(Qt.white))
                Painter.drawRect(xpos + 3, ypos + 20, 31, 20)
                Painter.drawText(xpos + (37 - FontMetric.width((str(self.Computer.RAM[Counter]).zfill(3)))) / 2,
                                         ypos + 35, str(self.Computer.DisplayRAM[Counter]).zfill(3))
                Painter.setPen(QPen(QColor("#daa520")))
                Painter.drawText(xpos + (37 - FontMetric.width(str(Counter)))/2, ypos + 15, str(Counter))
                Counter += 1
            Level += 1

        Painter.setBrush(QBrush(QColor("#b19cd9")))
        Painter.setPen(QPen(QColor("#b19cd9")))
        Painter.drawRect(5, 5, 100, 130)
        Painter.setPen(QPen(Qt.black))
        Painter.setFont(BoldFont)
        Painter.drawText(25, 18, "OUTPUT")

        Painter.setPen(QPen(QColor("#f4b860")))
        Painter.setBrush(QBrush(QColor("#f4b860")))
        Painter.drawRect(5, 150, 130, 230)
        Painter.drawRect(5, 410, 60, 60)
        Painter.setPen(QPen(Qt.black))
        Painter.drawText(55, 170, "CPU")
        Painter.drawText(20, 445, "ALU")

        Painter.setBrush(QBrush(Qt.white))
        Painter.drawRect(10, 185, FontMetric.width(str(self.Computer.PC)) + 20, 30)
        Painter.drawRect(10, 230, FontMetric.width(str(self.Computer.IR)) + 20, 30)
        Painter.drawRect(10, 275, FontMetric.width(str(self.Computer.IR).zfill(2)) + 20, 30)
        Painter.drawRect(60 - (FontMetric.width(str(self.Computer.ACC).zfill(3)) / 2), 340,
                         FontMetric.width(str(self.Computer.ACC).zfill(3)) + 20, 30)

        Painter.setFont(Font)
        Painter.drawText(20, 205, str(self.Computer.DisplayPC))
        Painter.drawText(FontMetric.width(str(self.Computer.PC)) + 35, 198, "Program")
        Painter.drawText(FontMetric.width(str(self.Computer.PC)) + 35, 213, "Counter")
        Painter.drawText(20, 250, str(self.Computer.IR))
        Painter.drawText(FontMetric.width(str(self.Computer.PC)) + 35, 243, "Instruction")
        Painter.drawText(FontMetric.width(str(self.Computer.PC)) + 35, 258, "Register")
        Painter.drawText(20, 295, str(self.Computer.MAR).zfill(2))
        Painter.drawText(FontMetric.width(str(self.Computer.PC).zfill(2)) + 35, 288, "Address")
        Painter.drawText(FontMetric.width(str(self.Computer.PC).zfill(2)) + 35, 303, "Register")
        Painter.drawText(60 - (FontMetric.width(str(self.Computer.ACC).zfill(3)) / 2) + 10, 360, str(self.Computer.DisplayACC).zfill(3))
        Painter.drawText(30, 333, "Accumulator")

        Painter.setPen(QPen(QColor("#7b7bf7")))
        Painter.setBrush(QBrush(QColor("#7b7bf7")))
        Painter.drawRect(5, 500, 80, 65)
        Painter.setPen(QPen(Qt.black))
        Painter.setFont(BoldFont)
        Painter.drawText(25, 515, "INPUT")

        Painter.setPen(QPen(QColor("#add8e6")))
        Painter.setBrush(QBrush(QColor("#add8e6")))
        Painter.drawRect(145, 515, 450, 50)

        Painter.setPen(QPen(QColor("#C1C1C1")))
        Painter.setBrush(QBrush(QColor("#C1C1C1")))
        Painter.drawRect(48, 136, 10, 13)
        Painter.drawRect(20, 381, 10, 28)
        Painter.drawRect(40, 381, 10, 28)
        Painter.drawRect(95, 381, 10, 150)
        Painter.drawRect(86, 531, 19, 10)

        WirePolygon = QPolygon([QPoint(115, 381), QPoint(115, 485),
                                QPoint(169, 485), QPoint(169, 475), QPoint(155, 475), QPoint(155, 437),
                                QPoint(169, 437), QPoint(169, 427), QPoint(155, 427), QPoint(155, 389),
                                QPoint(169, 389), QPoint(169, 379), QPoint(155, 379), QPoint(155, 341),
                                QPoint(169, 341), QPoint(169, 331), QPoint(155, 331), QPoint(155, 293),
                                QPoint(169, 293), QPoint(169, 283), QPoint(155, 283), QPoint(155, 245),
                                QPoint(169, 245), QPoint(169, 235), QPoint(155, 235), QPoint(155, 197),
                                QPoint(169, 197), QPoint(169, 187), QPoint(155, 187), QPoint(155, 149),
                                QPoint(169, 149), QPoint(169, 139), QPoint(155, 139), QPoint(155, 101),
                                QPoint(169, 101), QPoint(169, 91), QPoint(155, 91), QPoint(155, 53),
                                QPoint(169, 53), QPoint(169, 43), QPoint(145, 43), QPoint(145, 475),
                                QPoint(125, 475), QPoint(125, 381)])
        Painter.drawPolygon(WirePolygon)

        Painter.setPen(QPen(QColor("#d5d5d5")))
        Painter.setBrush(Qt.NoBrush)
        Path = QPainterPath()
        Path.moveTo(118, 381)
        Path.lineTo(118, 482)
        Path.lineTo(169, 482)
        Path.moveTo(122, 381)
        Path.lineTo(122, 478)
        Path.lineTo(148, 478)
        Path.moveTo(152, 478)
        Path.lineTo(169, 478)
        Path.moveTo(148, 478)
        Path.lineTo(148, 46)
        Path.lineTo(169, 46)
        Path.moveTo(169, 50)
        Path.lineTo(152, 50)
        Path.lineTo(152, 94)
        Path.lineTo(169, 94)
        Path.moveTo(169, 98)
        Path.lineTo(152, 98)
        Path.lineTo(152, 142)
        Path.lineTo(169, 142)
        Path.moveTo(169, 146)
        Path.lineTo(152, 146)
        Path.lineTo(152, 190)
        Path.lineTo(169, 190)
        Path.moveTo(169, 194)
        Path.lineTo(152, 194)
        Path.lineTo(152, 238)
        Path.lineTo(169, 238)
        Path.moveTo(169, 242)
        Path.lineTo(152, 242)
        Path.lineTo(152, 286)
        Path.lineTo(169, 286)
        Path.moveTo(169, 290)
        Path.lineTo(152, 290)
        Path.lineTo(152, 334)
        Path.lineTo(169, 334)
        Path.moveTo(169, 338)
        Path.lineTo(152, 338)
        Path.lineTo(152, 382)
        Path.lineTo(169, 382)
        Path.moveTo(169, 386)
        Path.lineTo(152, 386)
        Path.lineTo(152, 430)
        Path.lineTo(169, 430)
        Path.moveTo(169, 434)
        Path.lineTo(152, 434)
        Path.lineTo(152, 478)

        Path.moveTo(98, 381)
        Path.lineTo(98, 534)
        Path.lineTo(86, 534)
        Path.moveTo(86, 538)
        Path.lineTo(102, 538)
        Path.lineTo(102, 381)

        Path.moveTo(51, 136)
        Path.lineTo(51, 149)
        Path.moveTo(55, 149)
        Path.lineTo(55, 136)

        Path.moveTo(23, 381)
        Path.lineTo(23, 409)
        Path.moveTo(27, 409)
        Path.lineTo(27, 381)
        Path.moveTo(43, 381)
        Path.lineTo(43, 409)
        Path.moveTo(47, 409)
        Path.lineTo(47, 381)

        Painter.drawPath(Path)

        Painter.setBrush(QBrush(Qt.red))
        Painter.setPen(QPen(Qt.red))
        Painter.drawEllipse(self.Pos1[0], self.Pos1[1], self.Pos1[2], self.Pos1[3])
        Painter.setBrush(QBrush(Qt.blue))
        Painter.setPen(QPen(Qt.blue))
        Painter.drawEllipse(self.Pos2[0], self.Pos2[1], self.Pos2[2], self.Pos2[3])
        Painter.drawEllipse(self.Pos3[0], self.Pos3[1], self.Pos3[2], self.Pos3[3])

        Painter.setBrush(QBrush(Qt.darkGreen))
        Painter.setPen(QPen(Qt.darkGreen))
        Painter.drawEllipse(self.Pos4[0], self.Pos4[1], self.Pos4[2], self.Pos4[3])
        Painter.setPen(QPen(Qt.red))
        Painter.setBrush(QBrush(Qt.red))
        Painter.drawEllipse(self.Pos5[0], self.Pos5[1], self.Pos5[2], self.Pos5[3])

        Painter.setPen(QPen(Qt.blue))
        Painter.setBrush(QBrush(Qt.blue))
        Painter.drawEllipse(152, 490, 10, 10)
        RobotPolygon = QPolygon([QPoint(145, 575), QPoint(130, 510), QPoint(200, 500), QPoint(190, 575)])
        Painter.drawPolygon(RobotPolygon)
        Painter.setPen(QPen(Qt.black))
        Painter.setBrush(QBrush(Qt.white))
        Painter.drawEllipse(150, 512, 35, 35)
        Painter.setBrush(QBrush(Qt.black))
        Painter.drawEllipse(160, 522, 15, 15)
        MouthPath = QPainterPath()
        MouthPath.moveTo(157, 553)
        MouthPath.arcTo(157, 538, 20, 30, 0, -180)
        Painter.drawPath(MouthPath)
        Painter.drawLine(162, 505, 159, 500)
        Painter.drawLine(161, 505, 158, 500)
        Painter.setPen(QPen(Qt.white))
        Painter.setBrush(QBrush(Qt.white))
        Painter.drawRect(162, 553, 4, 5)


        Painter.setBrush(QBrush(Qt.black))
        Painter.setPen(QPen(Qt.black))
        InstructionFont = QFont("Arial", 18, QFont.Bold)
        Painter.setFont(InstructionFont)
        Instruction = ""
        if len(self.Computer.Code) != 0:
            Code = self.Computer.Code[self.Computer.PC]
            Instruction += str(Code[0]).zfill(2) + "    "
            for x in range(1, 4):
                if Code[x] is not None:
                    Instruction += str(Code[x]) + "  "
            Painter.drawText(210, 545, Instruction)

        Painter.end()



if __name__ == "__main__":
    App = QApplication(sys.argv)
    Root = MainWindow()
    sys.exit(App.exec())