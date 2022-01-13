# Name: Ben Nachmanson
from psElements import Value, StrConstant, ArrayConstant, FunctionBody


class Stacks:
    def __init__(self, scopeRule):
        self.scopeRule = scopeRule  # string static or dynamic
        # stack variables
        # assuming top of the stack is the end of the list
        self.opstack = []
        self.dictstack = []  # assuming top of the stack is the end of the list

        # The builtin operators supported by our interpreter
        self.builtin_operators = {
            # TO-DO in part1
            'add': self.add,
            'sub': self.sub,
            'mul': self.mul,
            'eq': self.eq,
            'lt': self.lt,
            'gt': self.gt,
            'length': self.length,
            'get': self.get,
            'put': self.put,
            'pop': self.pop,
            'stack': self.stack,
            'dup': self.dup,
            'copy': self.copy,
            'count': self.count,
            'clear': self.clear,
            'exch': self.exch,
            'def': self.psDef,
            'ifelse': self.psIfelse,
            'if': self.psIf,
            'for': self.psFor

        }

    # -------  Operand Stack Operators --------------
    """
        Helper function. Pops the top value from opstack and returns it.
    """

    def opPop(self):
        if len(self.opstack) < 1:
            print("Error. stack is empty")
        else:
            return self.opstack.pop()

    """
       Helper function. Pushes the given value to the opstack.
    """

    def opPush(self, value):
        self.opstack.append(value)

    # ------- Dict Stack Operators --------------

    """
       Helper function. Pops the top dictionary from dictstack and returns it.
    """

    def dictPop(self):
        return self.dictstack.pop()

    """
       Helper function. Pushes the given dictionary onto the dictstack.
    """

    def dictPush(self, d):
        self.dictstack.append(d)
    """
       Helper function. Adds name:value pair to the top dictionary in the dictstack.
       (Note: If the dictstack is empty, first adds an empty dictionary to the dictstack then adds the name:value to that.
    """

    def define(self, name, value):  # probably right
        if len(self.dictstack) < 1:
            self.dictPush((0, {}))
            myDict = self.dictPop()
            myDict[1][name] = value
            self.dictPush(myDict)
        else:
            myDict = self.dictPop()
            myDict[1][name] = value
            self.dictPush(myDict)

    """
       Helper function. Searches the dictstack for a variable or function and returns its value.
       (Starts searching at the top of the opstack; if name is not found returns None and prints an error message.
        Make sure to add '/' to the begining of the name.)
    """

    def lookup(self, name):  # gonna be different

        lookUpName = '/' + name

        if self.scopeRule == "static":
            myDict = self.dictPop()
            val = self.staticSearch(myDict, lookUpName)
            self.dictPush(myDict)
            return val
        else:
            myDict = self.dictstack[::-1]
            for f in myDict:
                if f[1].get(lookUpName) is not None:
                    return f[1].get(lookUpName)

    def staticSearch(self, myDict, lookUpName):
        if myDict[1].get(lookUpName) is not None:
            return myDict[1].get(lookUpName)
        else:
            ref = myDict[0]
            if ref == 0:
                d = self.dictstack[ref]
                if d[1].get(lookUpName) is not None:
                    return d[1].get(lookUpName)
            else:
                return self.staticSearch(self.dictstack[ref], lookUpName)
            pass

    # ------- Arithmetic Operators --------------

    def add(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if isinstance(op1, int) and isinstance(op2, int):
                self.opPush(op1 + op2)
            else:
                print("Error: add - one of the operands is not a number value")
                self.opPush(op2)
                self.opPush(op1)
        else:
            print("Error: add expects 2 operands")

    """
       Pop 2 values from opstack; checks if they are numerical (int); subtracts them; and pushes the result back to opstack.
    """

    def sub(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if isinstance(op1, int) and isinstance(op2, int):
                self.opPush(op2 - op1)
            else:
                print("Error: sub - one of the operands is not a number value")
                self.opPush(op2)
                self.opPush(op1)
        else:
            print("Error: sub expects 2 operands")

    """
        Pops 2 values from opstack; checks if they are numerical (int); multiplies them; and pushes the result back to opstack.
    """

    def mul(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if isinstance(op1, int) and isinstance(op2, int):
                self.opPush(op1 * op2)
            else:
                print("Error: mul - one of the operands is not a number value")
                self.opPush(op2)
                self.opPush(op1)
        else:
            print("Error: mul expects 2 operands")

    # ---------- Comparison Operators  -----------------
    """
       Pops the top two values from the opstack; pushes "True" is they are equal, otherwise pushes "False"
    """

    def eq(self):
        if len(self.opstack) >= 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if op1 == op2:
                self.opPush(True)
            else:
                self.opPush(False)
        else:
            print("error: less than two items in the stack.")

    """
       Pops the top two values from the opstack; pushes "True" if the bottom value is less than the top value, otherwise pushes "False"
    """

    def lt(self):
        if(len(self.opstack) > 1):
            op1 = self.opPop()
            op2 = self.opPop()
            if (op2 < op1):
                self.opPush(True)
            else:
                self.opPush(False)
        else:
            print("error: not enough items in the list.")

    """
       Pops the top two values from the opstack; pushes "False" if the bottom value is greater than the top value, otherwise pushes "False"
    """

    def gt(self):
        if(len(self.opstack) > 1):
            op1 = self.opPop()
            op2 = self.opPop()
            if(op2 > op1):
                self.opPush(True)
            else:
                self.opPush(False)
        else:
            print("error: not enough items in the list. ")

    # ------- String and Array Operators --------------
    """
       Pops a string or array value from the operand opstack and calculates the length of it. Pushes the length back onto the opstack.
       The `length` method should support both ArrayConstant and StrConstant values.
    """

    def length(self):
        if len(self.opstack) > 0:
            ob = self.opPop()
            if isinstance(ob, StrConstant):
                self.opPush(len(ob.value)-2)
            elif isinstance(ob, ArrayConstant):
                self.opPush(len(ob.value))
            else:
                self.opPush(ob.value)

    """
        Pops a StrConstant or an ArrayConstant and an index from the operand opstack.
        If the argument is a StrConstant, pushes the ascii value of the the character in the string at the index onto the opstack;
        If the argument is an ArrayConstant, pushes the value at the `index` of array onto the opstack;
    """

    def get(self):
        if len(self.opstack) > 1:
            index = self.opPop()
            ob = self.opPop()
            if(isinstance(ob, StrConstant)):
                self.opPush(ord(ob.value[index+1]))
            elif(isinstance(ob, ArrayConstant)):
                self.opPush(ob.value[index])
        else:
            print("error: stack does not have two values")

    """
    Pops a StrConstant or ArrayConstant value, an (zero-based) `index`, and an `item` from the opstack
    If the argument is a StrConstant, replaces the character at `index` of the StrConstant's string with the character having the ASCII value of `item`.
    If the argument is an ArrayConstant, replaces the element at `index` of the ArrayConstant's list with the value `item`.
    """

    def put(self):
        if len(self.opstack) > 2:
            item = self.opPop()
            index = self.opPop()
            ob = self.opPop()
            if(isinstance(ob, StrConstant)):
                ob.value = ob.value[: index+1] + \
                    chr(item) + ob.value[index + 2:]
            elif(isinstance(ob, ArrayConstant)):
                ob.value[index] = item
        else:
            print("error-put: not enough values")

    # ------- Stack Manipulation and Print Operators --------------

    """
       This function implements the Postscript "pop operator". Calls self.opPop() to pop the top value from the opstack and discards the value.
    """

    def pop(self):
        self.opPop()

    """
       Prints the opstack. The end of the list is the top of the stack.
    """

    def stack(self):
        print("===**opstack**===")
        reversedList = self.opstack[::-1]
        for x in reversedList:
            print(x)
        print("===**dictstack**===")
        count = len(self.dictstack)-1
        reversedDict = self.dictstack[::-1]

        for f in reversedDict:
            print("----", count, "----", f[0], "----")
            count -= 1
            for key, val in f[1].items():
                print(key, val, sep='   ')
        print("=================")
    """
       Copies the top element in opstack.
    """

    def dup(self):
        op1 = self.opPop()
        self.opPush(op1)
        self.opPush(op1)

    """
       Pops an integer count from opstack, copies count number of values in the opstack.
    """

    def copy(self):
        count = self.opPop()
        count += 1
        if len(self.opstack) >= count:
            for i in range(count):
                if(type(self.opstack[i]) is int):
                    self.opPush(self.opstack[i])

    """
        Counts the number of elements in the opstack and pushes the count onto the top of the opstack.
    """

    def count(self):
        count = len(self.opstack) - 1
        self.opPush(count)

    """
       Clears the opstack.
    """

    def clear(self):
        self.opstack[:] = []

    """
       swaps the top two elements in opstack
    """

    def exch(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            self.opPush(op1)
            self.opPush(op2)

    """
       Pops a name and a value from opstack, adds the name:value pair to the top dictionary by calling define.
    """

    def psDef(self):
        if len(self.opstack) > 1:
            value = self.opPop()
            name = self.opPop()
            self.define(name, value)
        else:
            print("error: op stack is too empty")

    # ------- if/ifelse Operators --------------
    """
       Inplements if operator.
       Pops the `ifbody` and the `condition` from opstack.
       If the condition is True, evaluates the `ifbody`.
    """

    def psIf(self):
        if len(self.opstack) > 1:
            ifBody = self.opPop()
            condition = self.opPop()
            if condition == True:
                self.dictPush((len(self.dictstack)-1, {}))
                ifBody.apply(self)
                self.dictPop()
            else:
                self.opPush(condition)
                self.opPush(ifBody)
        # TO-DO in part2

    """
       Inplements ifelse operator.
       Pops the `elsebody`, `ifbody`, and the condition from opstack.
       If the condition is True, evaluate `ifbody`, otherwise evaluate `elsebody`.
    """

    def psIfelse(self):
        if len(self.opstack) > 2:
            elseBody = self.opPop()
            ifBody = self.opPop()
            condition = self.opPop()
            if condition:
                self.dictPush((len(self.dictstack)-1, {}))
                ifBody.apply(self)
                self.dictPop()
            else:
                self.dictPush((len(self.dictstack)-1, {}))
                elseBody.apply(self)
                self.dictPop()
        else:
            self.opPush(condition)
            self.opPush(ifBody)
            self.opPush(elseBody)

        #TO-DO in part2

    # ------- Loop Operators --------------
    """
       implements for operator.
       Pops the `loopbody`, `end`index, `increment`, `start` index arguments from opstack;
       loop counter starts at `start` , incremented by `increment` value, and ends at `end`.
       for each value of loop counter, push the counter value on opstack, and  evaluate the `loopbody`.
    """

    def psFor(self):
        loopbody = self.opPop()
        end = self.opPop()
        increment = self.opPop()
        start = self.opPop()
        if increment < 0:
            for x in range(start, end-1, increment):
                self.opPush(x)
                self.dictPush((len(self.dictstack)-1, {}))
                loopbody.apply(self)
                self.dictPop()
        elif increment > 0:
            for x in range(start, end+1, increment):
                self.opPush(x)
                self.dictPush((len(self.dictstack)-1, {}))
                loopbody.apply(self)
                self.dictPop()

            # TO-DO in part2

    def clearBoth(self):
        self.opstack[:] = []
        self.dictstack[:] = []

    def cleanTop(self):
        if len(self.opstack) > 1:
            if self.opstack[-1] is None:
                self.opstack.pop()
