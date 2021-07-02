import exercise

from random import sample


if __name__ == '__main__':
    # Logger config
    # logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')

    # General settings
    n_terms_min = 2  # Numero minimo di termini del polinomio
    n_terms_max = 4  # Numero massimo di termini del polinomio
    coefficients_range = [-12, 12]  # Intervallo da cui ricavare i coefficienti (interi) dei termini
    exponent_range = [1, 5]  # Intervallo da cui ricavare gli esponenti (interi) dei termini
    unknown = exercise.UnknownVariable.x  # Incognita da utilizzare

    # Tool for creating polynomials
    poly_creator = exercise.PolynomialCreator(n_terms_min, n_terms_max, coefficients_range, exponent_range, unknown)

    # Define delivery
    delivery = f'Seleziona i polinomi ordinati rispetto a {unknown.name}'

    # Define answers
    [nA, nB, nC] = sample([2, 3, 4], 3)
    answers = {
        exercise.AnswersID.A: poly_creator.new(n_terms=nA, order=exercise.PolynomialOrder.increasing),
        exercise.AnswersID.B: poly_creator.new(n_terms=nB, order=exercise.PolynomialOrder.increasing),
        exercise.AnswersID.C: poly_creator.new(n_terms=nC, order=exercise.PolynomialOrder.decreasing),
        exercise.AnswersID.D: poly_creator.new(),
        exercise.AnswersID.E: poly_creator.new(),
        exercise.AnswersID.F: poly_creator.new(),
    }

    # Define solution
    sol_step_1 = ('Un polinomio è ordinato rispetto a una lettera se i suoi termini sono ordinati secondo le ' \
                  'potenze crescenti (o decrescenti) di quella lettera: devi escludere i polinomi in cui gli ' \
                  f'esponenti di {unknown.name} non sono in ordine crescente o decrescente.',
                  'Escludi quindi:')
    sol_step_2 = ('I polinomi',
                  f'sono ordinati secondo le potenze crescenti di {unknown.name}.',
                  'Infine il polinomio',
                  f'è ordinato secondo le potenze decrescenti di {unknown.name}')
    solution = (sol_step_1, sol_step_2)

    # Create exercise
    ex = exercise.Exercise(delivery, answers, solution)

    # Output
    ex.output_to_console()
    ex.output_to_html()
