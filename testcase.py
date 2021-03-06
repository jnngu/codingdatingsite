import sys
import traceback
import signal
#print ('Number of arguments:', len(sys.argv), 'arguments.')
#print ('Argument List:', str(sys.argv))



timeout_ex = """def foo(x):
    while 1==1:
        continue
    return x"""

test_ex = """def foo(x): return x"""
#exec(bar)

#print(foo(1))
class TimeOutError(Exception):
    pass

def signal_handler(signum, frame):
    raise TimeOutError("Timed out!")



def test (codeStr, functionName, testList):
    incorrectCases = 0
    outString = ""

    try:
        exec(codeStr)

        for i in range(len(testList)):
            print(testList[i])
            signal.signal(signal.SIGALRM, signal_handler)
            signal.alarm(2) 
            out = eval('{}({})'.format(functionName, testList[i][0]))
            signal.alarm(0)
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


output = test(test_ex, "foo", [(1,1), (2,3)])
print(output[0])
print(output[1])
