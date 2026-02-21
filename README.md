# Activity 6.2 – Hotel Reservation System

Simple hotel reservation system implemented in Python following PEP-8.

---

## Setup

### 1. Create the virtual environment
```bash
python3 -m venv venv
```

### 2. Activate it
```bash
source venv/bin/activate   # macOS / Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt --index-url https://pypi.org/simple/
```

---

## Running the Tests

```bash
pytest
```

![Pytest](images/pytest.png)

## Code Coverage

```bash
coverage run --source=. -m pytest
coverage report -m
```

![Pytest](images/coverage.png)


## Linting

Both linters are configured via their respective config files and require no extra flags.

### pylint — `.pylintrc`

```bash
pylint .
```
![Pytest](images/pylint.png)

### flake8 — `.flake8`

```bash
flake8 src/ tests/
```
![Pytest](images/flake8.png)
