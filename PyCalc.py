from PyQt6.QtWidgets import (
    QWidget,
    QApplication,
    QMainWindow,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QGridLayout,
    QFrame,
)
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt, QTimer
from functools import partial
import sys
import math
import qdarkstyle


WINDOW_WIDTH = 310
WINDOW_HEIGHT = 420
DISPLAY_HEIGHT = 70
BUTTON_SIZE = 60
ERROR_MSG = "ERROR"
BUTTON_FONTSIZE = 16


class Window(QMainWindow):
    """A window for the PyCalc 2 calculator.

    This class represents the main window of the calculator application. It provides the user interface
    for entering and displaying mathematical expressions and results.

    Attributes:
        shiftState (bool): The current state of the shift key.
        display (QLabel): The label widget for displaying the current expression or result.
        generalLayout (QVBoxLayout): The layout for the main window.
        buttonsLayout (QGridLayout): The layout for the calculator buttons.
        buttonMap (dict): A mapping of button texts to QPushButton objects.
        font (QFont): The font used for the calculator buttons.

    Methods:
        _createDisplay: Creates and configures the display label widget.
        _createButtons: Creates and configures the calculator buttons.
        _styleButton: Styles a calculator button with a specific button style.
        setDisplayText: Sets the text of the display label widget.

    """

    def __init__(self):
        """Initialize the Window instance.

        This method sets up the main window of the calculator application. It configures the window size,
        style, and icon, and creates the necessary widgets and layouts.

        Args:
            self: The Window instance.

        Returns:
            None.

        """
        super().__init__()
        self.setWindowTitle("PyCalc 2")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt6())
        self.setWindowIcon(
            QIcon("D:/Python Codes/PyQt6 Tutorials/Py Calculator/calculatorIcon.png")
        )
        self.font = QFont("Rockwell", BUTTON_FONTSIZE)  # type: ignore

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        self.generalLayout = QVBoxLayout()
        centralWidget.setLayout(self.generalLayout)

        self.shiftState = False
        self._createDisplay()
        self._createButtons()

    def _createDisplay(self):
        """Create and configure the display label widget.

        This method creates a QLabel widget for displaying the current expression or result. It sets the
        fixed height, word wrap, frame shape, style sheet, alignment, and font of the label. Finally, it
        adds the label to the general layout.

        Args:
            self: The Window instance.

        Returns:
            None.

        """
        self.display = QLabel()
        self.display.setFixedHeight(DISPLAY_HEIGHT)
        self.display.setWordWrap(True)
        self.display.setFrameShape(QFrame.Shape.Box)
        self.display.setStyleSheet(
            "border: 1px solid lightgrey; border-radius: 5px; padding: 8px; background-color: #81C8F3; color: #333; font-size: 20px;"
        )
        self.display.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.display.setFont(QFont("Courier New Bold"))  # type: ignore
        self.generalLayout.addWidget(self.display)

    def _createButtons(self):
        """Create and configure the calculator buttons.

        This method creates the calculator buttons based on the specified keyboard layout. It creates a
        QPushButton for each key, sets its fixed size, font, and style sheet, and adds it to the buttons
        layout. Finally, it adds the buttons layout to the general layout.

        Args:
            self: The Window instance.

        Returns:
            None.

        """
        self.buttonsLayout = QGridLayout()
        self.buttonMap = {}

        keyBoard = [
            ["shift", "x\u02b8", "\u221Ax", "log", "sin"],
            ["\u03C0", "e", "(", ")", "MOD"],
            ["7", "8", "9", "DEL", "AC"],
            ["4", "5", "6", "*", "/"],
            ["1", "2", "3", "+", "-"],
            ["0", ".", "*10\u02b8", "ANS", "="],
        ]

        for row, keys in enumerate(keyBoard):
            for col, key in enumerate(keys):
                self.buttonMap[key] = QPushButton(key)
                self.buttonMap[key].setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
                self.buttonMap[key].setFont(self.font)
                self._styleButton(self.buttonMap[key])
                self.buttonsLayout.addWidget(self.buttonMap[key], row, col)

        self.generalLayout.addLayout(self.buttonsLayout)

    def _styleButton(self, button):
        """Style a calculator button with a specific button style.

        This method sets the style sheet of a QPushButton to a specific button style, including background
        color, border, text color, and transition effects.

        Args:
            button (QPushButton): The button to style.

        Returns:
            None.

        """
        buttonStyle = """
            QPushButton {
                background-color: #094E78;
                border: none;
                color: #FFFADA;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                transition-duration: 0.4s;
                cursor: pointer;
                border-radius: 5px;
                box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            }
            QPushButton:hover {
                background-color: #28A1ED;
                color: #000407;
                border: 2px solid #86B6F6
            }
        """
        button.setStyleSheet(buttonStyle)

    def setDisplayText(self, text):
        """Set the text of the display label widget.

        This method sets the text of the display label widget to the specified text and gives it focus.

        Args:
            text (str): The text to set.

        Returns:
            None.

        """
        self.display.setText(text)
        self.display.setFocus()


def evaluateExpression(expression):
    """Evaluate a mathematical expression.

    This function evaluates a mathematical expression and returns the result as a string. It uses the
    `eval` function to perform the evaluation, with a custom dictionary of math-related functions and
    constants.

    Args:
        expression (str): The mathematical expression to evaluate.

    Returns:
        str: The result of the evaluation as a string.

    Raises:
        None.

    """
    try:
        result = str(eval(expression, {"math": math, "e": math.e, "\u03C0": math.pi}))
    except Exception:
        result = ERROR_MSG
    return result


class Controller:
    """Controller for the PyCalc 2 calculator.

    This class handles the user interactions and logic of the calculator application. It connects the
    calculator buttons to their respective actions and manages the current expression, result, and display.

    Attributes:
        _view (Window): The Window instance representing the calculator's user interface.
        _model (function): The function used to evaluate mathematical expressions.
        _currentExpression (str): The current mathematical expression being built.
        _currentResult (str): The current result of the evaluation.
        _currentDisplay (str): The current text displayed in the calculator's display.
        _powerParenthesesCount (int): The count of power parentheses in the current expression.

    Methods:
        _handleButtonClick: Handles the button click event and performs the corresponding action.
        _buildExpression: Builds the mathematical expression based on the button clicked.
        _toggleShiftState: Toggles the shift state of the calculator.
        _updateButtonLabels: Updates the labels of the calculator buttons based on the shift state.
        _calculateResult: Calculates the result of the current expression and updates the display.
        _connectSignalAndSlots: Connects the button click signals to the corresponding slots.

    """

    def __init__(self, view, model):
        """Initialize the Controller instance.

        This method sets up the Controller instance by connecting it to the Window instance and the
        evaluateExpression function.

        Args:
            view (Window): The Window instance representing the calculator's user interface.
            model (function): The function used to evaluate mathematical expressions.

        Returns:
            None.

        """
        self._view = view
        self._model = model
        self._currentExpression = ""
        self._currentResult = ""
        self._currentDisplay = ""
        self._powerParenthesesCount = 0
        self._needsClosingParentheses = False
        self._connectSignalAndSlots()

    def _handleButtonClick(self, button):
        """Handle the button click event and perform the corresponding action.

        This method handles the button click event and performs the corresponding action based on the
        clicked button. It updates the button style, toggles the shift state, builds the mathematical
        expression, or calculates the result.

        Args:
            button (QPushButton): The clicked button.

        Returns:
            None.

        """
        originalStyle = button.styleSheet()
        animationStyle = (
            "background-color: #28A1ED; color: #000407; border: 2px solid #86B6F6"
        )

        button.setStyleSheet(animationStyle)
        QTimer.singleShot(100, lambda: button.setStyleSheet(originalStyle))

        if button.text() == "shift":
            self._toggleShiftState()
        elif button.text() == "=":
            self._calculateResult()
        else:
            self._buildExpression(button.text())

    def _buildExpression(self, subExpression):  # sourcery skip: low-code-quality
        """Build the mathematical expression based on the button clicked.

        This method builds the mathematical expression based on the button clicked. It handles different
        cases such as toggling the shift state, adding operators or functions, deleting characters, or
        adding parentheses.

        Args:
            subExpression (str): The button text representing the clicked button.

        Returns:
            None.

        """
        if self._currentDisplay == ERROR_MSG or self._currentExpression == "":
            self._currentDisplay = ""

        subExpression = self.applyShiftSubstitutions(subExpression)
        
        self._handlePowerParentheses(subExpression)

        if self._currentExpression == "" and subExpression in {"+", "-", "*", "/", "*10\u02b8", "MOD"}:
            self._handleEmptyExpression(subExpression)

        else:
            self._handleSpecialExpressions(subExpression)
        
        self._view.setDisplayText(self._currentDisplay)
        
    def _handlePowerParentheses(self, subExpression):
        """
        The function increments the count of power parentheses if the subExpression is one of the
        specified values.
        
        :param subExpression: The subExpression parameter is a string that represents a part of a
        mathematical expression
        """
        if self._powerParenthesesCount and subExpression in {"log", "sin", "(", "\u221Ax", "\u221Bx", "ln", "sin⁻¹"}:
            self._powerParenthesesCount += 1
            
    def applyShiftSubstitutions(self, subExpression):
        """Apply substitutions based on the shift state.

        Args:
            subExpression (str): The button text representing the clicked button.

        Returns:
            str: The modified subExpression based on the shift state.

        """
        if self._view.shiftState:
            substitutions = {
                "\u221Ax": "\u221Bx",
                "x\u02b8": "e\u02b8",
                "log": "ln",
                "sin": "sin⁻¹"
            }

            return substitutions.get(subExpression, subExpression)

        return subExpression       
        
    def _handleEmptyExpression(self, subExpression):
        """
        The function handles an empty expression by checking if the subExpression is an operator and
        updating the current display and expression accordingly.
        
        :param subExpression: The `subExpression` parameter represents a mathematical operator or
        function that is being entered by the user. It can be one of the following values: "+", "-",
        "*", "/", "*10ᵈ", "MOD"
        """
        if subExpression == "*10\u02b8":
            self._currentDisplay = "ANS*10<sup>("
            self._currentExpression = f"{self._currentResult}*10**("
            self._powerParenthesesCount += 1
        elif subExpression == "MOD":
            self._currentDisplay = "ANS MOD "
            self._currentExpression = f"{self._currentResult}%"
        else:
            self._currentDisplay = f"ANS{subExpression}"
            self._currentExpression = f"{self._currentResult}{subExpression}"
                
    def _handleSpecialExpressions(self, subExpression):
        if subExpression == "AC":
            self._clearAll()

        elif subExpression == "ANS":
            self._handleAnswer()

        elif subExpression == "DEL":
            self._handleDelete()

        elif subExpression == "MOD":
            self._handleMod()

        elif subExpression in {"*10\u02b8", "x\u02b8", "e\u02b8"}:
            self._handleExponential(subExpression)
            self._powerParenthesesCount += 1

        elif subExpression in {"\u221Ax", "\u221Bx"}:
            self._handleSquareRoot(subExpression)

        elif subExpression in {"log", "ln", "sin", "sin⁻¹"}:
            self._handleUnaryFunction(subExpression)

        elif subExpression == ")":
            self._handleClosingParentheses(subExpression)

        else:
            self._appendExpression(subExpression)

    def _clearAll(self):
        self._currentDisplay = ""
        self._currentExpression = ""

    def _appendExpression(self, value):
        self._currentDisplay += str(value)
        self._currentExpression += str(value)
        
    def _handleAnswer(self):
        self._currentDisplay += "ANS"
        self._currentExpression += self._currentResult

    def _handleDelete(self):
        if self._currentDisplay.endswith("ANS"):
            self._clearLastResult()
        elif self._currentDisplay.endswith(")</sup>"):
            self._currentDisplay = self._currentDisplay[:-7]
            self._currentExpression = self._currentExpression[:-1]
        elif self._currentDisplay.endswith("<sup>("):
            self._currentDisplay = self._currentDisplay[:-6]
            self._currentExpression = self._currentExpression[:-3]
        else:
            self._currentDisplay = self._currentDisplay[:-1]
            self._currentExpression = self._currentExpression[:-1]
            
    def _clearLastResult(self):
        self._currentDisplay = self._currentDisplay[:-3]
        length = len(self._currentResult)
        self._currentExpression = self._currentExpression[:-length]
        
    def _handleMod(self):
        self._currentDisplay += " MOD "
        self._currentExpression += "%"

    def _handleExponential(self, subExpression):
        if subExpression == "*10\u02b8":
            self._currentDisplay += "*10<sup>("
            self._currentExpression += "*10**("
        elif subExpression == "x\u02b8":
            self._currentDisplay += "<sup>("
            self._currentExpression += "**("
        else:
            self._currentDisplay += "e<sup>("
            self._currentExpression += "e**("

    def _handleSquareRoot(self, subExpression):
        self._currentDisplay += f"{subExpression[:-1]}("
        if subExpression == '√':
            self._currentExpression += 'math.sqrt('
        else:
            self._currentExpression += 'math.cbrt('

    def _handleUnaryFunction(self, subExpression):
        operationMapping = {
            'sin': 'math.sin(math.radians(',
            'sin⁻¹': 'math.asin(math.degrees(',
            'log': 'math.log10(',
            'ln': 'math.log('
        }
        self._currentDisplay += f"{subExpression}("
        self._currentExpression += f"{operationMapping[subExpression]}"
        if subExpression in {"sin", "sin⁻¹"}:
            self._needsClosingParentheses = True

    def _handleClosingParentheses(self, subExpression):
        if self._powerParenthesesCount:
            if self._powerParenthesesCount == 1:
                self._currentDisplay += f"{subExpression}</sup>"
            else:
                self._currentDisplay += f"{subExpression}"
            self._powerParenthesesCount -= 1
        else:
            self._currentDisplay += f"{subExpression}"
        self._currentExpression += f"{subExpression}"
        if self._needsClosingParentheses:
            self._currentExpression += ")"
            self._needsClosingParentheses = False


    def _toggleShiftState(self):
        """Toggle the shift state of the calculator.

        This method toggles the shift state of the calculator, which affects the labels of certain buttons.
        It updates the shift state attribute of the view and calls the _updateButtonLabels method to update
        the button labels accordingly.

        Args:
            None.

        Returns:
            None.

        """
        self._view.shiftState = not self._view.shiftState
        self._updateButtonLabels(self._view.shiftState)

    def _updateButtonLabels(self, checked):
        """Update the labels of the calculator buttons based on the shift state.

        This method updates the labels of the calculator buttons based on the shift state. It uses a mapping
        of button texts to their shifted labels and sets the corresponding labels based on the shift state.

        Args:
            checked (bool): The current state of the shift key.

        Returns:
            None.

        """
        shiftMapping = {
            "\u221Ax": "\u221Bx",
            "x\u02b8": "e\u02b8",
            "log": "ln",
            "sin": "sin⁻¹"
        }
        for key, newText in shiftMapping.items():
            self._view.buttonMap[key].setText(newText if checked else key)

    def _calculateResult(self):
        """Calculate the result of the current expression and update the display.

        This method calculates the result of the current expression by evaluating it using the evaluateExpression
        function. It updates the display label with the result, clears the current expression and display, and
        resets the power parentheses count.

        Args:
            None.

        Returns:
            None.

        """
        self._currentResult = self._model(self._currentExpression)
        self._view.setDisplayText(self._currentResult)
        self._currentExpression = ""
        self._currentDisplay = ""

    def _connectSignalAndSlots(self):
        """Connect the button click signals to the corresponding slots.

        This method connects the button click signals of the calculator buttons to the corresponding slots
        in the controller. It uses the functools.partial function to pass the clicked button as an argument
        to the _handleButtonClick method.

        Args:
            None.

        Returns:
            None.

        """
        for keySymbol, button in self._view.buttonMap.items():
            button.clicked.connect(partial(self._handleButtonClick, button))


def main():
    """Run the PyCalc 2 calculator application.

    This function initializes the QApplication, creates an instance of the Window class, shows the main
    window, creates an instance of the Controller class, and starts the application event loop.

    Args:
        None.

    Returns:
        None.

    """
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    Controller(view=window, model=evaluateExpression)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

