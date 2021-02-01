from tkinter import *
from math import sqrt

#logic of this calculator is to store two numbers and one math operation in Entry widget at the same time, like(2+4 or 12*25)
#if user wants to cuntinue calcululation we have to calculate currently stored expression, take a result and continue accept input.
#for example user types (2+5) and then user wants to multiply this by 5, when user clicks a multiply button, we calculate current expression, 
#and multiply the result by 5: (2+5) -> (7*) -> (7*5)

#i tried to decompose all the tasks and created many helpful functions
#also my aim was to avoid eval() function


root = Tk()

#set title and disable resizable option
root.title("calculator")
root.resizable(width=False, height=False)

#set a 0 at the begining so user will see that program is waiting for input
entryWindow = Entry(root, width=45, borderwidth=5, bg="#48c9b0", highlightbackground="green")
entryWindow.insert(0, '0')

def checkConversionToFloat(expression):
	""" function returns True if we can convert expression to float number, False is we cant """

	try:
		float(expression)
		return True
	except ValueError:
		return False


def checkConversionToInteger(expression):  
	""" function returns True if we can convert expression to integer number, False is we cant """

	try:
		return True if expression.is_integer() else False
	except AttributeError:
		return False


def getScreenString(window=entryWindow):
	""" function returns a string that is currently stored in Entry widget """

	if str(window.get())[-1] == ")":
		bracketIndex = str(window.get()).index("(")
		return str(window.get())[:bracketIndex] + str(window.get())[bracketIndex + 1:-1]

	return str(window.get())


def cleanWindow(stringToPlace='0', window=entryWindow):
	""" function deletes all the data from Entry widget string and place argument string instead of it ('0' by default) """

	window.delete(0, "end")
	window.insert(0, stringToPlace)


def checkIsWindowClean():
	""" function returns True if only '0' or empty string "" is in Entry widget string, False if not """

	screenString = getScreenString()
	return bool(((len(screenString) == 1) and (screenString[0] == '0')) or screenString == "")


def checkNegationOfNumber(number):
	""" function returns True if the first symbol of number is '-', False if is not """

	try:
		if number[0] == "-":
			return True
		return False
	except TypeError:
		return False


def deleteWarning():
	""" function checks is there a 'Zero Division!' massage currently in Entry widget, if it is - cleans widget and set '0' in it """

	if getScreenString() == "Zero Division!" or getScreenString() == "Invalid Syntax!":
		cleanWindow()


def getCountOfNumbers(expression=getScreenString()): 
	""" function returns number of numbers currently stored in Entry widget.Returns 0 if Entry widget has no numbers in it, 1 if one number,
	3 if there is one number and math operation near it, (like 123* or 92-), and 2 if there are two numbers and math operation between them"""

	if checkIsWindowClean(): 
		return 0
	else:
		if expression[-1] in "+-*/":
			return 3
		else:
			#here we avoid case of one negated number (-123 or -553.2)
			for i in "*/+":              
				if i in expression:
					return 2
			if "-" in expression[1:]:
				return 2

	#here there are no cases left except one number in Entry widget
	return 1


def getMathOperation(expression=getScreenString()): 
	""" function returns math operation of expression that is stored in Entry widget """

	#in case if we have a number and math operation in our expression, we will return the last character of expression, so it will be math operation (like 3+ or 213*)
	#but if there are two numbers, we will come from behind and add digits one by one until we meet math operation 
	#we should check, is there actually operation between two numbers or this is negation of the second number (like (3-2) not (3*-2))

	if getCountOfNumbers(expression) == 3:
		return expression[-1]
	elif getCountOfNumbers(expression) == 2:
		for digit in range(1, len(expression) + 1):
			if not checkConversionToFloat(expression[-digit]) and expression[-digit] != ".":
				if checkConversionToFloat(expression[-digit - 1]):
					return expression[-digit]
				else:
					return expression[-digit - 1]


def getSecondNumberString(expression=getScreenString()):
	""" function returns second number of expression, that is stored in Entry widget as a string """

	#we will go from behind and add a digits to our result, which will be the second number
	#when we will mete a math operation, we will check that it is not negation of the second number but actually math operation between two numbers

	if getCountOfNumbers(expression) == 2:
		result = ""
		for i in range(1, len(expression) + 1):
			if expression[-i] not in "*/+-":
				result = expression[-i] + result
			else:
				if expression[-i - 1] in "+-/*":
					return "-" + result
				else:
					return result


def getFirstNumberString(expression=getScreenString()):
	""" function returns first number of expression, that is stored in Entry widget as a string """

	if getCountOfNumbers(expression) == 1:
		return expression
	elif getCountOfNumbers(expression) == 3:
		return expression[:-1]
	elif getCountOfNumbers(expression) == 2:
		index = expression.find(getMathOperation(expression) + getSecondNumberString(expression))
		return expression[:index]


def getStringWithSecondNumberInBrackets(expression=getScreenString()): 
	""" function returns an Entry widget expression with added brackets for second number, we will use it to negate second number """

	return getFirstNumberString(expression) + getMathOperation(expression) + "(" + getSecondNumberString(expression) + ")"

	
def squareRootButton():
	""" function calculates square root of expression, that if currently stored in Entry widget 
	and stores an error massage in Entry widget if this operation is impossible """

	#checks if there one number or two numbers with math operation between them in Entry widget, prints in Entry widget square root of a number or square root of a result of 
	#math operation between two numbers (if it is positive number or 0), does nothing if not
	#also we should chek if there are any error warnings in Entry widget, and if there are we have to delete them

	screenString = getScreenString()
	deleteWarning()

	if checkIsWindowClean():
		pass
	else:
		if getCountOfNumbers(screenString) == 1 and float(screenString) >= 0:
			result = float(screenString) ** (1/2)
			if checkConversionToInteger(result): 
				result = int(result)
			cleanWindow(result)

		elif getCountOfNumbers(screenString) == 2 and float(getEqualString(screenString)) >= 0:
			result  = getEqualString(screenString)
			result = float(result) ** (1/2)
			if checkConversionToInteger(result): 
				result = int(result)
			cleanWindow(result)

		else:
			cleanWindow("Invalid Syntax!")


def squareNumberButton():
	""" function calculates square number of expression, that if currently stored in Entry widget 
	and stores an error massage in Entry widget if this operation is impossible  """

	#completely the same logic as in squareRootButton() function

	screenString = getScreenString()
	deleteWarning()
	if checkIsWindowClean():
		pass
	else:
		if getCountOfNumbers(screenString) == 1:
			result = float(screenString) ** 2
			if checkConversionToInteger(result): 
				result = int(result)
			cleanWindow(result)
		elif getCountOfNumbers(screenString) == 2:
			result  = getEqualString(screenString)
			result = float(result) ** 2
			if checkConversionToInteger(result): 
				result = int(result)
			cleanWindow(result)
		else:
			cleanWindow("Invalid Syntax!")


def onePerXDivisionButton():
	""" function tries to divide one by currently stored number or expression in Entry widget 
	and stores an error massage in Entry widget if this operation is impossible"""

	#I used try/exept block for division because we can get a lot of errors here
	#in case if there is single 0 in Entry widget we will raise an ZeroDivisionError
	#in other cases (for example if only single number with math operation is in Entry widget) we will raise ValueError
	#for every error we will show an suitable error massage  

	screenString = getScreenString()

	try:
		if getCountOfNumbers(screenString) == 0:
			raise ZeroDivisionError
		elif getCountOfNumbers(screenString) == 1:
			result = 1 / float(screenString)
			if checkConversionToInteger(result): 
				result = int(result)
			cleanWindow(result)
		elif getCountOfNumbers(screenString) == 2:
			result = 1 / float(getEqualString(screenString))
			if checkConversionToInteger(result): 
				result = int(result)
			cleanWindow(result)
		else:
			raise ValueError

	except ZeroDivisionError:
		cleanWindow("Zero Division!")
	except ValueError:
		cleanWindow("Invalid Syntax!")


def negateNumberButton():
	""" function negates a number and stores resual in Entry widgetif there is one number in Entry widget, 
	if there are two numbers in Entry widget - negates the second one, does nothing in other cases """

	screenString = getScreenString()
	deleteWarning()

	if getCountOfNumbers(screenString) == 0:
		pass
	elif getCountOfNumbers(screenString) == 1:
		if checkNegationOfNumber(getFirstNumberString(screenString)):
			screenString = screenString[1:]
		else:
			screenString = "-" + screenString
	elif getCountOfNumbers(screenString) == 2:
		if checkNegationOfNumber(getSecondNumberString(screenString)):
			screenString = getFirstNumberString(screenString) + getMathOperation(screenString) + getSecondNumberString(screenString)[1:]
		else:
			screenString = getFirstNumberString(screenString) + getMathOperation(screenString) + "-" + getSecondNumberString(screenString)
			screenString = getStringWithSecondNumberInBrackets(screenString)
	
	cleanWindow(screenString)


def pointButton():
	""" function adds a point '.' symbol to a number if number is integer """

	#in case if we have one number and math operation near it, adds '0.' to current expression, like (3*->3*0. or 12/->12/0.), 
	#if we have two numbers in Entry widget, adds point to the second one, stores '0.' in Entry widget in other cases "

	screenString = getScreenString()

	if getCountOfNumbers(screenString) == 1:
		if '.' not in screenString:
			buttonPressed('.')
	elif getCountOfNumbers(screenString) == 2:
		if '.' not in getSecondNumberString(screenString):
			buttonPressed('.')
	elif getCountOfNumbers(screenString) == 3:
		cleanWindow(screenString + '0.')
	else:
		cleanWindow('0.')

	


def equalButton():
	""" function tries to calculate expression that is currently in Entry winget using getEqualString() function """

	#we only want to calculate expression if there are two numbers and a math operation in it

	screenString = getScreenString()

	if getCountOfNumbers(screenString) == 2:
		result = getEqualString(screenString)
		cleanWindow(result)




def getEqualString(expression):
	""" function returns a string of result of math operation between two numbers if expression is correct, returns error masssage in other cases """


	operationsList = ["+", "-", "*", "/"]
	expressionOperationString = ""
	result = getScreenString()
	
	for operation in operationsList:
		if getMathOperation(expression) == operation:
			expressionOperationString = operation
			break

	if expressionOperationString == "+":
		result = float(getFirstNumberString(expression)) + float(getSecondNumberString(expression)) 
	elif expressionOperationString == "-":
		result = float(getFirstNumberString(expression)) - float(getSecondNumberString(expression)) 
	elif expressionOperationString == "*":
		result = float(getFirstNumberString(expression)) * float(getSecondNumberString(expression)) 
	elif expressionOperationString == "/":
		try:
			result = float(getFirstNumberString(expression)) / float(getSecondNumberString(expression)) 
		except ZeroDivisionError:
			result = "Zero Division!"

	if checkConversionToInteger(result): 
		result = int(result)

	return str(result)


def buttonPressed(enteredChar):
	""" function takes a char and checks if this char is a number or math operation than depends on what an entered char is, stores it in Entry widget in an appropriate way"""

	#if we have empty string we have two oportunities: start entering number (0->3->34->345) or start calculations with 0 (0->0+2 or 0->0*3)
	#if we have one number in Entry widget strind and user wants to enter math operation and this number has point as a last symbol (3. or 21.) we will add a 0 to it (3.0+ or 21.*)
	#if we have number with math operation in Entry widget we only can accept a number or another operation from user (in second case we will simply change operation (132+ -> 132*))
	#if we have two numbers stored in Entry widget we can add another numbers or point '.' in all the other cases we should calculate currently expression and let user a result he can work with

	#but we have a problem with zeroes row of second number (1+0002 or 23/02)
	#we dont want a number to start from several or even one zero, but we want let user possibility to make calculations with second number as 0, like (132+0 or 23*0 or even 123/0)
	#so we will check, is there already second number is 0 (if it is, it can only be one digit)
	#but if it already 0, and user continues typing, we will change this 0 to currently number (if 123+0 is on the screen and user click '3' it will be ->123+3 instead of 123+03)
	#but still we will have a case if second number is 0 and user tryes to type a point, to prevent this, we have to check if this char isnt a point to allow user make second number a float number


	deleteWarning()
	enteredChar = str(enteredChar)
	screenString = getScreenString()


	if getCountOfNumbers(screenString) == 0:
		if checkConversionToFloat(enteredChar):
			screenString = screenString[1:] + enteredChar
		else:
			screenString = screenString + enteredChar

	elif getCountOfNumbers(screenString) == 1:
		if screenString[-1] == "." and enteredChar in "+-/*":
			screenString = screenString + "0" + enteredChar
		else:
			screenString += enteredChar

	elif getCountOfNumbers(screenString) == 3:
		if checkConversionToFloat(enteredChar):
			screenString += enteredChar
		else:
			screenString = screenString[:-1] + enteredChar

	elif getCountOfNumbers(screenString) == 2:
		if checkConversionToFloat(enteredChar) or enteredChar == '.':
			if screenString[-1] == '0' and screenString[-2] in '+-*/' and enteredChar != '.':
				screenString = screenString[:-1] + enteredChar
			else:
				screenString += enteredChar
		else:
			screenString = getEqualString(screenString) + enteredChar

		#this line is to correct work in situation when second number is negated and in brackets and we want to add numbers after point to it (we want to see this numbers also in brackets like 2*(-1.32) )
		if checkNegationOfNumber(getSecondNumberString(screenString)):
			screenString = getStringWithSecondNumberInBrackets(screenString)

	cleanWindow(screenString)

if __name__ == "__main__":

	#define buttons
	button7 = Button(root,text="7", padx=50, pady=25, borderwidth=1, bg="#d7bde2", command=lambda: buttonPressed(7))
	button8 = Button(root, text="8", padx=50, pady=25, borderwidth=1, bg="#d7bde2", command=lambda: buttonPressed(8))
	button9 = Button(root, text="9", padx=51, pady=25, borderwidth=1, bg="#d7bde2", command=lambda: buttonPressed(9))
	
	button4 = Button(root,text="4", padx=50, pady=25, borderwidth=1, bg="#d7bde2", command=lambda: buttonPressed(4))
	button5 = Button(root, text="5", padx=50, pady=25, borderwidth=1, bg="#d7bde2", command=lambda: buttonPressed(5))
	button6 = Button(root, text="6", padx=51, pady=25, borderwidth=1, bg="#d7bde2", command=lambda: buttonPressed(6))
	
	button1 = Button(root,text="1", padx=50, pady=25, borderwidth=1, bg="#d7bde2", command=lambda: buttonPressed(1))
	button2 = Button(root, text="2", padx=50, pady=25, borderwidth=1, bg="#d7bde2", command=lambda: buttonPressed(2))
	button3 = Button(root, text="3", padx=51, pady=25, borderwidth=1, bg="#d7bde2", command=lambda: buttonPressed(3))

	button0 = Button(root, text="0 ", padx=105, pady=25, borderwidth=1, bg="#d7bde2", command=lambda: buttonPressed(0))


	buttonPoint = Button(root, text=". ", padx=51, pady=25, borderwidth=1, bg="#d7bde2", command=pointButton)
	buttonEqual = Button(root, text="= ", padx=47, pady=61, borderwidth=1, bg="#ffb3fe", command=equalButton)
	buttonAddition = Button(root, text="+ ", padx=47, pady=61, borderwidth=1, bg="#f1948a", command=lambda: buttonPressed('+'))

	buttonSubtraction = Button(root, text="- ", padx=49, pady=25, borderwidth=1, bg="#f1948a", command=lambda: buttonPressed('-'))
	buttonMultiplication = Button(root, text="x", padx=51, pady=25, borderwidth=1, bg="#f1948a", command=lambda: buttonPressed('*'))
	buttonDivision = Button(root, text="/", padx=50, pady=25, borderwidth=1, bg="#f1948a", command=lambda: buttonPressed('/'))

	buttonClear = Button(root, text="clear ", padx=39, pady=25, borderwidth=1, bg="#f7dc6f", command=cleanWindow)

	buttonOnePerX = Button(root, text="1/x ", padx=43, pady=25, borderwidth=1, bg="#f1948a", command=onePerXDivisionButton)
	buttonPowerOfTwo = Button(root, text="×²", padx=48, pady=25, borderwidth=1, bg="#f1948a", command=squareNumberButton)
	buttonSquareRoot = Button(root, text="√ ", padx=47, pady=25, borderwidth=1, bg="#f1948a", command=squareRootButton)

	buttonHash = Button(root, text="+/-", padx=44, pady=25, borderwidth=1, bg="#f7dc6f", command=negateNumberButton)





	entryWindow.grid(row=0, column=0, columnspan=4, padx=10, pady=10)


	#store buttons
	button7.grid(row=3, column=0)
	button8.grid(row=3, column=1)
	button9.grid(row=3, column=2)

	button4.grid(row=4, column=0)
	button5.grid(row=4, column=1)
	button6.grid(row=4, column=2)

	button1.grid(row=5, column=0)
	button2.grid(row=5, column=1)
	button3.grid(row=5, column=2)

	button0.grid(row=6, column=0, columnspan=2)

	buttonPoint.grid(row=6, column=2)
	buttonEqual.grid(row=5, column=3, rowspan=2)
	buttonAddition.grid(row=3, column=3, rowspan=2)

	buttonSubtraction.grid(row=2, column=1)
	buttonMultiplication.grid(row=2, column=2)
	buttonDivision.grid(row=2, column=3)

	buttonClear.grid(row=2, column=0)

	buttonOnePerX.grid(row=1, column=1)
	buttonPowerOfTwo.grid(row=1, column=2, columnspan=1)
	buttonSquareRoot.grid(row=1, column=3)

	buttonHash.grid(row=1, column=0)



	root.mainloop()