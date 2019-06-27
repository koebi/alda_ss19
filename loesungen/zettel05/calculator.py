# Wir definieren zuerst die beiden Knotenklassen fuer den Baum:

# Die Blattknoten des Parse-Baums repraesentieren Zahlenwerte.
class Number:
    def __init__(self, n):
        self.number = n

        # evaluate() wertet den Ausdruck aus, den der Knoten repraesentiert.
        # Bei Blattknoten wird einfach der String in die entsprechende Zahl
        # umgewandelt.
    def evaluate(self):
        return float(self.number)

        # zum Ausdrucken als String
    def __repr__(self):
        return self.number

        # zum Ausdrucken als Baum
    def printTree(self, indent=''):
        return '(' + self.number + ')\n'

# Die inneren Knoten des Parse-Baumes repaesentieren Operatoren
# mit ihren linken und rechten Operanden.
class Operator:
    def __init__(self, left, operator, right):
        if not operator in '+-*/':
            raise SyntaxError('unknown operator')
        self.left = left
        self.operator = operator
        self.right = right

    # Bei inneren Knoten wertet evaluate() zuerst den linken und rechten
    # Operanden rekursiv aus, dann werden die Ergebnisse mit dem
    # gespeicherten Operator verknuepft.
    def evaluate(self):
        left, right = self.left.evaluate(), self.right.evaluate()
        if self.operator == '+':
            return left + right
        if self.operator == '-':
            return left - right
        if self.operator == '*':
            return left * right
        if self.operator == '/':
            return left / right

    # zum Ausdrucken als String
    def __repr__(self):
        return '(' + repr(self.left) + self.operator + repr(self.right) + ')'

    # zum Ausdrucken als Baum
    def printTree(self, indent=''):
       return '(' + self.operator + ') -- ' + self.right.printTree(indent + ' |     ') + \
              indent + ' |\n' + \
              indent + self.left.printTree(indent)

# An Position i ist eine oeffnende Klammer, suche die zugehoerige
# schliessende Klammer durch Zaehlen von oeffnenden und
# schliessenden Paaren.
def findClosingBracket(t, i):
    count = 1
    for k in range(i+1, len(t)):
        if t[k] == '(':
            count += 1
        elif t[k] == ')':
            count -= 1
        if count == 0:
            return k
    # Wenn wir hier landen, gab es keine passende schliessende Klammer.
    raise SyntaxError('invalid expression')

# Teste ob rechts von Position i ein hoeherwertiger Operator steht
# als links.
def rightPriorityIsHigher(t, i):
    if i == len(t)-1:
        # rechts ist nichts => die Bedingung ist nie erfuellt
        return False

    if i == 0:
        # links ist nichts => die Bedingung ist immer erfuellt
        return True

    # Die Bedingung ist erfuellt, wenn links Strichrechnung und rechts
    # Punktrechnung verwendet wird.
    return t[i-1] in '+-' and t[i+1] in '*/'

# Wandle den Ausdruck t in einen Parse-Baum um, gegebenenfalls rekursiv.
# Die Funktion gibt die Wurzel des resultierenden Baumes zurueck.
def parse(t):
    # Vorverarbeitung: Erzeugen einer Token-Liste
    if type(t) is str:
        # Entferne eventuelle Leerzeichen
        t = t.replace(' ', '')

        # Wandle den String in ein Array von 'Tokens' um.
        # Die Uebungsaufgabe ist so gestellt, dass die Tokens gerade den
        # einzelnen Zeichen des Strings entsprechen.
        # (Bei realen Programmiersprachen muss man zusammengesetzte
        # Zahlen (z.B. 324), Operatoren aus mehreren Zeichen (z.B. **) etc.
        # jeweils zu einem Token zusammenfassen. Dies die Aufgabe des 'Lexers',
        # der stets dem eigentlichen Parser vorgeschaltet ist.)
        t = [k for k in t]

    k = 0
    while True:
        # Wenn k ueber das Ende von t hinauslaeuft, kann t kein gueltiger
        # Ausdruck sein.
        if k >= len(t):
            raise SyntaxError('invalid expression')

        # Wenn t[k] noch nicht verarbeitet wurde…
        if type(t[k]) is str:
            # …generiere einen Blattknoten, wenn t[k] eine Zahl ist,…
            if t[k] in '0123456789':
                t[k] = Number(t[k])
            # …oder parse den Klammerausdruck, wenn t[k] eine oeffnende Klammer ist…
            elif t[k] == '(':
                # Finde das Ende des Klammerausdrucks.
                end = findClosingBracket(t, k)
                # Parse den Unterausdruck zwischen den Klammern rekursiv.
                # sub ist die Wurzel des resultierenden Teilbaums.
                sub = parse(t[k+1:end])
                # Ersetze den Klammerausdruck in t durch das Ergebnis des Parsings.
                t[k:end+1] = [ sub ]
            # …oder signalisiere einen Syntaxfehler. (Da k immer gerade
            # ist, enthaelt t[k] entweder eine Zahl oder die Wurzel eines
            # bereits fertigen Teilbaumes oder es ist der Beginn eines
            # Klammerausdrucks. Alles andere ist deshalb ein Fehler.)
            else:
                raise SyntaxError('invalid expression')

        # Wenn die Prioritaet des rechten Operators hoeher ist, kuemmern wir uns
        # zuerst um den rechten Teilausdruck…
        if rightPriorityIsHigher(t, k):
            k += 2
        # …andernfalls, wenn es einen linken Teilausdruck gibt, erzeugen wir einen
        # Operatorknoten im Baum und ersetzen den linken Teilausdruck durch diesen
        # Knoten. Die Verarbeitungsreihenfolge garantiert, dass t[k-2] und t[k]
        # bereits geparsed wurden, also fertige Teilbaeume enthalten.
        elif k >= 2:
            t[k-2:k+1] = [ Operator(t[k-2], t[k-1], t[k]) ]
            k -= 2

        # Wenn t keine Operatoren und Klammern mehr enthaelt, sind wir fertig.
        # => t[0] ist jetzt die Wurzel des Parse-Baumes.
        if len(t) == 1:
            return t[0]

import unittest

def evaluateTree(root):
        return root.evaluate()

class testCalc(unittest.TestCase):
    def setUp(self):
        # Wir nutzen python selber, um die korrekten Ergebnisse ausrechnen zu lassen
        self.mathStrings = [
            ("1+1", 1+1),
            ("1-1", 1-1),
            ("1+1+1", 1+1+1),
            ("1+1*1", 1+1*1),
            ("2+2*2/2", 2+2*2/2),
            ("(2*3)+(4*5)", (2*3)+(4*5)),
            ("2*9/4*(1+(4*5)/3-(2+0))-1+5", 2*9/4*(1+(4*5)/3-(2+0))-1+5),
            ("1/5", 1/5),
            ("0", 0),
            ("2*4*(3+(4-7)*8)-(1-6)", 2*4*(3+(4-7)*8)-(1-6)),
            ("2*3+4*5", 2*3+4*5),
            ("(2-5)", (2-5)),
            ("(((1+5*3+5)+7*8)*(1+3*2)+9+(1*2))+5", (((1+5*3+5)+7*8)*(1+3*2)+9+(1*2))+5)]

    def test_calc(self):
        for test in self.mathStrings:
            tree = parse(test[0])
            res = evaluateTree(tree)
            self.assertEqual(res, test[1], f"Fehler in {test[0], {test[1]} erwartet aber {res} erhalten")

if __name__ == '__main__':
    unittest.main(exit=False)
    print (parse('2+5*3').printTree())
    print (parse('2*4*(3+(4-7)*8)-(1-6)').printTree())
