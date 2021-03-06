import sys
import traceback
import signal
import os
#print ('Number of arguments:', len(sys.argv), 'arguments.')
#print ('Argument List:', str(sys.argv))



timeout_ex = """def foo(x):
    while 1==1:
        continue
    return x"""

test_ex = """def foo(x): return x"""

test_c = "int foo(int x) {return x;}"
#exec(bar)

#print(foo(1))
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
    f.write("#include <stdio.h>\n")
    f.write(test_c)

    f.write("\nint main(){")
    f.write("int out = {}({});".format(functionName, inputVal))
    f.write(" return out;}")

    f.close()



#language: python, c
#codeStr: sstring representation of code
#functionName: name of function to be called
#testList: lists of (input val, expected output)
def test (language, codeStr, functionName, testList):
    incorrectCases = 0
    outString = ""
    timeoutTime = 5
    try:
        if language == "python":
            exec(codeStr)

        for i in range(len(testList)):
            print(testList[i])
            signal.signal(signal.SIGALRM, signal_handler)
            if language == "python":
                signal.alarm(timeoutTime) 
                out = eval('{}({})'.format(functionName, testList[i][0]))
            elif language == "c":
                generateC(codeStr, functionName, testList[i][0])
                compileOut = os.popen('gcc -o temp temp.c -w').read()
                if "error" in compileOut:
                    outString += compileOut
                    return (outString, -1)
                signal.alarm(timeoutTime) 
                out = int(os.popen("./temp; echo $?").read())

            signal.alarm(0)
            if os.path.exists("temp.c"):
                os.remove("temp.c")
            if os.path.exists("temp"):
                os.remove("temp")

            if out == testList[i][1]:
                outString += "Testcase {} Passed\n".format(i)
            else:
                outString += "Testcase {} Failed\n".format(i)
                incorrectCases += 1

        return (outString,incorrectCases)
    except TimeOutError as te:
        outString += "Timed out!\n"
        return (outString, -1)

    except Exception as e:
        tb = traceback.format_exc()
        outString += tb
        return (outString, -1)


output = test("c", test_ex, "foo", [(1,1), (2,3), (4,4)])
print(output[0])
print(output[1])

