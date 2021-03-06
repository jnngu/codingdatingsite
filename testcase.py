import sys
import traceback
import signal
import os
#print ('Number of arguments:', len(sys.argv), 'arguments.')
#print ('Argument List:', str(sys.argv))



timeout_ex = """def foo(x):
    print(x)
    """

test_ex = """def foo(x): return x"""

test_c = """#include<stdio.h>
void foo(int x) {printf(\"%d\\n\", x);}"""

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
            signal.signal(signal.SIGALRM, signal_handler)                
            if language == "python":
                signal.alarm(timeoutTime) 
                eval('{}({})'.format(functionName, testInputs[i]))
            elif language == "c":
                generateC(codeStr, functionName, testInputs[i])
                compileOut = os.popen('gcc -o temp temp.c -w').read()

                if "error" in compileOut:
                    outString += compileOut
                    sys.stdout.close()
                    sys.stdout = oldOut
                    return -1
                    
                signal.alarm(timeoutTime) 
                out = os.popen("./temp").read()
                print(out.strip())
            signal.alarm(0)
        sys.stdout.close()
        sys.stdout = oldOut

        return 0
    except TimeOutError as te:
        outString += "Timed out!\n"
        sys.stdout.close()
        sys.stdout = oldOut
        return -1

    except Exception as e:
        tb = traceback.format_exc()
        outString += tb
        sys.stdout.close()
        sys.stdout = oldOut
        return -1

def compareFiles (userFile, goldenFile):
    user = open(userFile, "r")
    golden = open(goldenFile, "r")
    numWrong = 0
    userLine = user.readlines()
    goldenLine = golden.readlines()
    for idx in range(len(goldenLine)):
        if idx >= len(userLine):
            print("Test Case {} Failed".format(idx))
            numWrong += 1            
        elif userLine[idx].strip() == goldenLine[idx].strip():
            print("Test Case {} Passed".format(idx))
        else:
            print("Test Case {} Failed".format(idx))
            numWrong += 1

    user.close()
    golden.close()
    return numWrong





output = runCode("python", timeout_ex, "foo", [1,2,3])
x = compareFiles("out.txt", "golden.txt")
print(x)

output = runCode("c", "test_c", "foo", [1,2,3])
x = compareFiles("out.txt", "golden.txt")
print(x)

