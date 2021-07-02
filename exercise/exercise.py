import logging
import webbrowser

from random import randrange, sample
from enum import Enum, auto

from yattag import Doc

logger = logging.getLogger(__name__)


class AnswersID(Enum):
    A = 'answer_ID_1'
    B = 'answer_ID_2'
    C = 'answer_ID_3'
    D = 'answer_ID_4'
    E = 'answer_ID_5'
    F = 'answer_ID_6'


class UnknownVariable(Enum):
    x = auto()
    y = auto()
    z = auto()
    a = auto()
    b = auto()
    c = auto()


class PolynomialOrder(Enum):
    unordered = auto()
    increasing = auto()
    decreasing = auto()


class PolynomialCreator:

    def __init__(self, n_terms_min, n_terms_max, coefficients_range, exponent_range, unknown=UnknownVariable.x):
        if n_terms_min > n_terms_max:
            raise ArithmeticError("Minimum terms number must be lower than maximum terms number.")
        if n_terms_min < 2 or type(n_terms_min) != int or type(n_terms_max) != int:
            raise IOError("Number of terms must be at least 2.")
        self.n_terms_min = n_terms_min
        self.n_terms_max = n_terms_max

        if coefficients_range[1] < coefficients_range[0] or exponent_range[1] < exponent_range[0]:
            raise ArithmeticError("Upper range must be greater then lower range.")
        self.coefficients_range = coefficients_range

        if abs(exponent_range[1] - exponent_range[0]) < 1:
            raise IOError("Exponent range too small (at least 1).")
        self.exponent_range = exponent_range
        self._n_possible_terms = abs(self.exponent_range[1] - self.exponent_range[0]) + 1

        if type(unknown) != UnknownVariable:
            raise TypeError('Expecting %s, got %s' % (UnknownVariable.__name__, type(unknown).__name__))
        self.unknown = unknown.name

        # Log
        logger.debug("%s created for %i possible terms!", type(self).__name__, self._n_possible_terms)

    def new(self, n_terms=None, order=PolynomialOrder.unordered):
        # Calcolo il numero effettivo di termini
        n_actual_terms = self._evaluate_request(n_terms, order)

        # Ricavo i coefficienti del polinomio (inclusi i termini nulli)
        poly_coeffs = self._polynomial_coefficients(n_actual_terms)

        # Creo lista dei termini
        terms = self._term_list(poly_coeffs)

        # Ordino/disordino
        final_terms = self._order(terms, order)

        # Creo il polinomio
        polynomial = self._terms_to_str(final_terms)

        # Log
        logger.info("Final %s polynomial --> %s", order.name, polynomial)

        return polynomial

    def _evaluate_request(self, n_terms, order):
        # Controllo input
        if n_terms is not None:
            if type(n_terms) != int:
                raise TypeError("Expected int, got %s" % type(n_terms).__name__)
            if n_terms < self.n_terms_min or n_terms > self.n_terms_max:
                raise IOError("Number of terms requested out of range!")
            if type(order) != PolynomialOrder:
                raise TypeError("Expected %s, got %s" % (PolynomialOrder.__name__, type(order).__name__))
            # Tutto ok
            n_actual_terms = n_terms

        # Valuto n_terms anche in base a ordered
        else:
            # n_terms is None
            if order == PolynomialOrder.unordered:
                if self._n_possible_terms >= 3:
                    n_actual_terms = randrange(3, self._n_possible_terms)
                else:
                    raise RuntimeError("Too few terms for an unordered polynomial.")
            else:
                n_actual_terms = randrange(2, self._n_possible_terms)

        return n_actual_terms

    def _polynomial_coefficients(self, n_terms):
        # Verifico che non siano richiesti troppi termini rispetto al grado del polinomio
        if n_terms > self._n_possible_terms:
            raise ArithmeticError("Could not create a polynomial from grade %i to grade %i with %i terms."
                                  % (self.exponent_range[0], self.exponent_range[1], n_terms))

        coefficients = []
        zero_terms = 0
        allowed_zero_terms = self._n_possible_terms - n_terms
        while True:
            # Controllo se ho raggiunto il numero di termini desiderato
            if (len(coefficients) - zero_terms) == n_terms:
                break
            # Creo coefficiente random nel range
            coeff = randrange(self.coefficients_range[0], self.coefficients_range[1])
            if coeff == 0:
                # Se ho raggiunto il numero massimo di coefficienti nulli, non posso accettare 0
                if zero_terms >= allowed_zero_terms:
                    continue
                else:
                    zero_terms += 1

            coefficients.append(coeff)

        # Log
        logger.debug("New coefficient list: %s", str(coefficients))

        return coefficients

    def _term_list(self, poly_coefficients):
        # Inizializzo
        grade = self.exponent_range[0] - 1
        terms = []
        for coeff in poly_coefficients:
            # Setto il grado
            grade += 1
            # Se il termine è nullo salto
            if coeff == 0:
                continue
            # Creo il termine
            coeff_str = str(coeff) if coeff < 0 else '+' + str(coeff)
            if grade == 0:
                term = coeff_str
            elif grade == 1:
                term = coeff_str + self.unknown
            else:
                term = coeff_str + self.unknown + '<sup>' + str(grade) + '</sup>'
            # Lo aggiungo alla lista
            terms.append(term)

        # Log
        logger.debug("Polynomial terms: %s", str(terms))

        return terms

    @staticmethod
    def _order(terms, order):
        if len(terms) == 1:
            # Non c'è nulla da ordinare
            resulting_list = terms
            logger.warning("Trying to order a single term.")

        elif order == PolynomialOrder.increasing:
            # La lista dei termini è già stata scritta in ordine crescente
            resulting_list = terms

        elif order == PolynomialOrder.decreasing:
            # Scrivo la lista in ordine inverso
            resulting_list = terms[::-1]

        else:
            # Devo mettere in disordine la lista
            is_ordered = True
            resulting_list = []
            reverse_list = terms[::-1]
            while is_ordered:
                resulting_list = sample(terms, len(terms))

                # Controllo che effettivamente sia in disordine
                is_changed = False
                for original_term, res_term in zip(terms, resulting_list):
                    if original_term != res_term:
                        is_changed = True
                        break

                # Verifico che non sia diventata uguale alla reverse_list (che è ordinata)
                if is_changed:
                    for reverse_term, res_term in zip(reverse_list, resulting_list):
                        if reverse_term != res_term:
                            is_ordered = False
                            break

        return resulting_list

    @staticmethod
    def _terms_to_str(terms):
        # Creo la stringa
        s = ''
        polynomial = s.join(terms)

        # Rimuovo segno + iniziale se presente
        if polynomial[0] == '+':
            polynomial = polynomial[1:]

        return polynomial


class Exercise:

    def __init__(self, delivery, answers, solution):
        self.delivery = delivery
        self.answers = answers
        self.solution = solution

    def output_to_html(self):
        doc, tag, text = Doc().tagtext()

        with tag('html'):
            with tag('body'):
                with tag('header'):
                    with tag('title'):
                        text('Esercizio')

                # Consegna
                with tag('section'):
                    with tag('h3'):
                        text('Consegna:')
                    with tag('p'):
                        text(self.delivery)

                # Opzioni di risposta
                with tag('section'):
                    with tag('h3'):
                        text('Opzioni di risposta:')
                    with tag('p', style='margin-left:40px'):
                        text(AnswersID.A.value)
                    with tag('p', style='margin-left:40px'):
                        text(AnswersID.B.value)
                    with tag('p', style='margin-left:40px'):
                        text(AnswersID.C.value)
                    with tag('p', style='margin-left:40px'):
                        text(AnswersID.D.value)
                    with tag('p', style='margin-left:40px'):
                        text(AnswersID.E.value)
                    with tag('p', style='margin-left:40px'):
                        text(AnswersID.F.value)

                # Risoluzione guidata
                with tag('section'):
                    with tag('h3'):
                        text('Risoluzione guidata:')
                    with tag('ol'):
                        with tag('li', style='white-space: pre-line'):
                            text(f'{self.solution[0][0]}\n{self.solution[0][1]}')
                            with tag('ul'):
                                with tag('li'):
                                    text(AnswersID.D.value)
                                with tag('li'):
                                    text(AnswersID.E.value)
                                with tag('li'):
                                    text(AnswersID.F.value)
                        with tag('li', style='white-space: pre-line'):
                            text(self.solution[1][0])
                            with tag('ul'):
                                with tag('li'):
                                    text(AnswersID.A.value)
                                with tag('li'):
                                    text(AnswersID.B.value)
                            text(f'{self.solution[1][1]}\n{self.solution[1][2]}')
                            with tag('ul'):
                                with tag('li'):
                                    text(AnswersID.C.value)
                            text(self.solution[1][3])

        html = doc.getvalue()
        for ans_id in AnswersID:
            html = html.replace(ans_id.value, self.answers[ans_id])
        file_name = 'exercise.html'
        f = open(file_name, 'w')
        f.write(html)
        f.close()
        webbrowser.open_new_tab(file_name)

    def output_to_console(self):
        print("\nConsegna:")
        print(self.delivery)
        print("\nOpzioni di risposta:")
        for key in self.answers:
            print("\t\t", self._replace_sup_tag(self.answers[key]))
        print("\nRisoluzione guidata:")
        step = self.solution[0]
        print("1. ", step[0])
        print(step[1])
        print("\t* ", self._replace_sup_tag(self.answers[AnswersID.D]))
        print("\t* ", self._replace_sup_tag(self.answers[AnswersID.E]))
        print("\t* ", self._replace_sup_tag(self.answers[AnswersID.F]))
        step = self.solution[1]
        print("2. ", step[0])
        print("\t* ", self._replace_sup_tag(self.answers[AnswersID.A]))
        print("\t* ", self._replace_sup_tag(self.answers[AnswersID.B]))
        print(step[1])
        print(step[2])
        print("\t* ", self._replace_sup_tag(self.answers[AnswersID.C]))
        print(step[3])

    @staticmethod
    def _replace_sup_tag(poly_str):
        new_poly = poly_str.replace('<sup>', '^')
        return new_poly.replace('</sup>', '')
