# ================ UTIL FUNCTIONS ================ #

def multiply_by_scalar(scalar: float, matrix: [[]]):
    for vector in matrix:
        for i in range(len(vector)):
            vector[i] *= scalar


def one_dimension_determinant(matrix: (())) -> int:
    return matrix[0][0]


def two_dimension_determinant(matrix: (())) -> int:
    result = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    return result


def three_dimension_determinant(matrix: (())) -> int:
    result = 0
    for i in range(3):
        partial_result = 1
        for j in range(3):
            partial_result *= matrix[(i + j) % 3][j]
        result += partial_result

    for i in range(3):
        partial_result = 1
        for j in range(3):
            partial_result *= matrix[(-1 - i - j) % 3][j]
        result -= partial_result
    return result


def multiply_matrix_by_vector(matrix: [[]], vector: []) -> []:
    output_vector = []
    for matrix_vector in matrix:
        partial_result = 0
        for i in range(len(vector)):
            partial_result += matrix_vector[i] * vector[i]
        output_vector.append(partial_result)
    return output_vector


def boolean_to_pl(bool: bool) -> str:
    if bool:
        return "TAK"
    return "NIE"


# ================ GLOBAL VARIABLES ================ #


MAXIMUM_ITERATIONS = 20
MATRIX_MULTIPLAYER = 1.0 / 3.0
MATRIX_CASE_1 = [
    [0.0, -2.0, 2.0],
    [-2.0, 0.0, -2.0],
    [2.0, -2.0, 0.0]
]
MATRIX_CASE_2 = [
    [0.0, 1.1],
    [-1.0, 0.0]
]
multiply_by_scalar(MATRIX_MULTIPLAYER, MATRIX_CASE_1)

determinant_functions = {
    1: one_dimension_determinant,
    2: two_dimension_determinant,
    3: three_dimension_determinant
}

STABLE_POINTS = set()


# ================ INITIAL WEIGHT MATRIX VALIDATION ================ #

def is_symmetric(matrix: (())) -> bool:
    for i in range(len(matrix)):
        for j in range(i, len(matrix)):
            if i != j and matrix[i][j] != matrix[j][i]:
                return False
    return True


def has_non_negative_diagonal(matrix: (())) -> bool:
    for i in range(len(matrix)):
        if matrix[i][i] < 0:
            return False
    return True


def is_positively_determined(matrix: (())) -> bool:
    for i in range(len(matrix)):
        if determinant_functions[i + 1](matrix) <= 0:
            return False
    return True


# ================ ACTIVATION FUNCTION ================ #


def get_activation_value(value: int) -> int:
    if value > 0:
        return 1
    return -1


def apply_activation_function(vector: []) -> []:
    return [get_activation_value(element) for element in vector]


# ================ VECTORS PROCESSING ================ #


def get_cycle(vector_history: [[]]) -> [[]]:
    for i in range(len(vector_history)):
        for j in range(i + 1, len(vector_history)):
            if vector_history[i] == vector_history[j]:
                return [vector_history[k] for k in range(i, j + 1)]
    return []


def get_cyclic_configuration_str(vectors: [[]]) -> str:
    result_string = ""
    for i in range(len(vectors)):
        result_string += str(vectors[i])
        if i != len(vectors) - 1:
            result_string += " -> "
    return result_string


def process_vector(original_vector: (), processing_vector: (), iteration_count: int, result_vector_history: (()),
                   weight_matrix: (())):
    if iteration_count == MAXIMUM_ITERATIONS:
        print(f"Dla wektora {original_vector} sko??czono od??wie??anie, gdy?? zosta??a osi??gni??ta maksymalna liczba iteracji.")
        return

    multiplied_vector = multiply_matrix_by_vector(weight_matrix, processing_vector)
    result_vector = apply_activation_function(multiplied_vector)
    print(f"Rezultat iteracji {iteration_count}: {result_vector}")
    if processing_vector != result_vector:
        result_vector_history.append(result_vector)
        cycle = get_cycle(result_vector_history)
        if len(cycle) != 0:
            print(f"Dla wektora {original_vector} {len(cycle) - 1}-stopniowa konfiguracja zosta??a znaleziona:")
            print(get_cyclic_configuration_str(cycle))
        else:
            process_vector(original_vector, result_vector, iteration_count + 1, result_vector_history, weight_matrix)
    else:
        print(f"Dla wektora {original_vector} zosta?? znaleziony punkt stabilny {result_vector} w {iteration_count} iteracjach.")
        STABLE_POINTS.add(tuple(result_vector))


# ================ STARTUP ================ #


def validate_weight_matrix(matrix: (())):
    print(f"Czy macierz wej??ciowa ma nieujemn?? diagonale? -  {boolean_to_pl(has_non_negative_diagonal(matrix))}")
    print(f"Czy macierz wej??ciowa jest symetryczna? -        {boolean_to_pl(is_symmetric(matrix))}")
    print(f"Czy macierz wej??ciowa jest dodatnio okre??lona? - {boolean_to_pl(is_positively_determined(matrix))}")


def generate_vectors(dimension: int):
    nums = (1, -1)
    if dimension == 3:
        return ((i, j, k) for i in nums for j in nums for k in nums)
    else:
        return ((i, j) for i in nums for j in nums)


def process_vectors(vectors: (), weight_matrix: (())):
    for vector in vectors:
        print(f"\nRozpocz??to synchroniczne od??wie??anie dla wektora : {vector}")
        process_vector(vector, vector, 1, [], weight_matrix)


def process_for_case_1():
    print("\n================= ROZPOCZ??TO OD??WIE??ANIE DLA ZADANIA 1 =================\n")

    validate_weight_matrix(MATRIX_CASE_1)
    tested_vectors = generate_vectors(len(MATRIX_CASE_1))
    process_vectors(tested_vectors, MATRIX_CASE_1)

    print(f"Wszystkie punkty stabilne sieci : {STABLE_POINTS}")
    print("\n================= ZAKO??CZONO OD??WIE??ANIE DLA ZADANIA 1 =================\n")


def process_for_case_2():
    print("\n================= ROZPOCZ??TO OD??WIE??ANIE DLA ZADANIA 2 =================\n")

    validate_weight_matrix(MATRIX_CASE_2)
    tested_vectors = generate_vectors(len(MATRIX_CASE_2))
    process_vectors(tested_vectors, MATRIX_CASE_2)

    print(f"Wszystkie punkty stabilne sieci : {STABLE_POINTS}")
    print("\n================= ZAKO??CZONO OD??WIE??ANIE DLA ZADANIA 2 =================\n")


def main():
    global STABLE_POINTS
    process_for_case_1()
    print("\n================= ROZPOCZ??TO =================\n")

    process_for_case_1()
    STABLE_POINTS = set()
    process_for_case_2()

    print("\n================= ZAKO??CZONO =================\n")

main()
