import numpy as np

def add_matrices(matrix1, matrix2):
    return np.add(matrix1, matrix2)

def subtract_matrices(matrix1, matrix2):
    return np.subtract(matrix1, matrix2)

def multiply_matrices(matrix1, matrix2):
    return np.matmul(matrix1, matrix2)
```

[CMD]
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/chrisalunlloyd2-sudo/H2O_MATRIX.git
git push -u origin master
