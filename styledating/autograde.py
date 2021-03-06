import sys
import traceback
#import signal
import os


python_ex = """def foo(x):
    print(x)
    """

test_ex = """def foo(x): return x"""

test_c = """#include<stdio.h>
void foo(char* x) {printf(\"%s\\n\", x);}"""

class TimeOutError(Exception):
    pass

def signal_handler(signum, frame):
    raise TimeOutError("Timed out!")


def generateC (codeStr, functionName, testInput):
    functionName = "foo"

    inputVal = testInput
    if os.path.exists("temp.c"):
        os.remove("temp.c")

    f = open("temp.c","x")
    f.write(test_c)

    f.write("\nint main(){")
    f.write("{}({});".format(functionName, inputVal))
    f.write(" return 0;}")

    f.close()



#language: python, c
#codeStr: string representation of code
#functionName: name of function to be called
#testInputs: list of input vals
def runCode (language, codeStr, functionName, testInputs):
    incorrectCases = 0
    outString = ""
    timeoutTime = 5
    oldOut = sys.stdout

    if os.path.exists("out.txt"):
        os.remove("out.txt")
    sys.stdout = open('out.txt', 'w')
    try:
        if language == "python":
            exec(codeStr)

        for i in range(len(testInputs)):
            
            ######"""signal.signal(signal.SIGALRM, signal_handler) """               
            if language == "python":
                #signal.alarm(timeoutTime) 
                if isinstance(testInputs[i], str):
                    eval('{}(\"{}\")'.format(functionName, testInputs[i]))
                else:
                    eval('{}({})'.format(functionName, testInputs[i]))
            elif language == "c":
                if isinstance(testInputs[i], str):
                    testInputs[i] = "\"{}\"".format(testInputs[i])
                generateC(codeStr, functionName, testInputs[i])
                compileOut = os.popen('gcc -o temp temp.c -w').read()

                if "error" in compileOut:
                    sys.stdout.close()
                    sys.stdout = oldOut
                    return (-1, compileOut)
                    
                #signal.alarm(timeoutTime) 
                out = os.popen("./temp").read() #does not detect segmentation faults
                print(out.strip())
            #signal.alarm(0)
        sys.stdout.close()
        sys.stdout = oldOut

        return (0,"")
    except TimeOutError as te:
        sys.stdout.close()
        sys.stdout = oldOut
        return (-1, "Timed Out!\n")

    except Exception as e:
        tb = traceback.format_exc()
        sys.stdout.close()
        sys.stdout = oldOut
        return (-1,tb)

def compareFiles (userFile, goldenFile):
    user = open(userFile, "r")
    golden = open(goldenFile, "r")
    numWrong = 0
    userLine = user.readlines()
    goldenLine = golden.readlines()
    outStr = ""
    for idx in range(len(goldenLine)):
        if idx >= len(userLine):
            outStr += "Test Case {} Failed\n".format(idx)
            numWrong += 1            
        elif userLine[idx].strip() == goldenLine[idx].strip():
            outStr += "Test Case {} Passed\n".format(idx)
        else:
            outStr += "Test Case {} Failed\n".format(idx)
            numWrong += 1

    user.close()
    golden.close()
    return (numWrong, outStr)



def runAutograder(language, codeStr, functionName, inputFile, goldenFile):
    inputList = [eval(i.strip().split()[0]) for i in open(inputFile).readlines()]

    print(inputList)
    output = runCode(language, codeStr, functionName, inputList)
    if output[0] == -1:
        print(output[1])
        return (-1, output[1])
    else:
        if not os.path.exists("out.txt"):
            print("output file not generated")
            return (-1, "output file not generated")
        elif not os.path.exists(goldenFile):
            print("golden not found")
            return (-1, "golden not found")
        else:
            numWrong, outStr = compareFiles("out.txt", goldenFile)
            return (numWrong, outStr)


#inputList = ["hi", "bye", "seeya"]
#a = runAutograder("python", python_ex, "foo", "input.txt", "golden.txt")
#print(a)
#b= runAutograder("c", test_c, "foo", "input.txt", "golden.txt")
#print(b)