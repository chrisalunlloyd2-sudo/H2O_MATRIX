import numpy as np
from matrix_operations import add_matrices, subtract_matrices, multiply_matrices

def main():
    # Get user input
    matrix1 = np.array([[1, 2], [3, 4]])
    matrix2 = np.array([[5, 6], [7, 8]])

    # Perform matrix operations
    result_add = add_matrices(matrix1, matrix2)
    result_subtract = subtract_matrices(matrix1, matrix2)
    result_multiply = multiply_matrices(matrix1, matrix2)

    # Print results
    print("Matrix 1:")
    print(matrix1)
    print("Matrix 2:")
    print(matrix2)
    print("Result (Addition):")
    print(result_add)
    print("Result (Subtraction):")
    print(result_subtract)
    print("Result (Multiplication):")
    print(result_multiply)

if __name__ == "__main__":
    main()
