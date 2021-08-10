# Little Man Computer

A compiler/editor for the Little Man Computer instruction set. 

main.py can be used as a standalone compiler or the Qt frontend can be used for a more interactive experience.

# Installation
main.py doesn't require any dependencies. However, to use the UI application you need to install PyQt5 using pip
```bash
pip install pyqt5
```

# Example usage without frontend

```bash
ComputerInstance = Computer()
ComputerInstance.Compile("loop lda A\nout A\nsub one\nsta A\nbrp loop\nhlt\nA dat 10\none dat 1")
ComputerInstance.AssembleIntoRam()
ComputerInstance.OutputRam()
ComputerInstance.run()
```

# Screenshots

![screenshot1](/screenshots/screenshot1.png)
![screenshot2](/screenshots/screenshot2.png)

