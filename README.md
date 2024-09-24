<div align="left">

[![Build status](https://github.com/Case-Based/casebased/workflows/build/badge.svg?branch=master&event=push)](https://github.com/Case-Based/casebased/actions?query=workflow%3Abuild)
[![Python Version](https://img.shields.io/pypi/pyversions/casebased.svg)](https://pypi.org/project/casebased/)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/Case-Based/casebased/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/Case-Based/casebased/blob/master/.pre-commit-config.yaml)
[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/Case-Based/casebased/releases)
[![License](https://img.shields.io/github/license/casebased/casebased)](https://github.com/Case-Based/casebased/blob/master/LICENSE)
![Coverage Report](assets/images/coverage.svg)

---

### [📃 Our Paper on CBR](https://github.com/user-attachments/files/16977337/SA-I_IT22_KlockenhoffLukas-KloettschenJannekLiendlJonas.pdf)

---

# Casebased - A Python Library for Case-Based Reasoning

[![PyPI Version](https://img.shields.io/pypi/v/casebased.svg)](https://pypi.org/project/casebased/)
[![Python Versions](https://img.shields.io/pypi/pyversions/casebased.svg)](https://pypi.org/project/casebased/)
[![License](https://img.shields.io/pypi/l/casebased.svg)](https://github.com/your-username/casebased/blob/main/LICENSE)

**Casebased** is a Python library that provides a flexible and extensible framework for implementing case-based reasoning (CBR) systems. CBR is a problem-solving paradigm that focuses on solving new problems by adapting solutions that were used to solve similar past problems.

## Features

| Feature                | Description                                                                |
| ---------------------- | -------------------------------------------------------------------------- |
| Case Representation    | Represent cases using a variety of data structures, including dictionaries, JSON, and custom classes. |
| Case Retrieval         | Implement different case retrieval algorithms, such as nearest neighbor, fuzzy matching, and knowledge-guided search. |
| Case Adaptation        | Provide functions to adapt retrieved cases to fit the current problem. |
| Case Evaluation        | Assess the quality of the adapted solution and provide feedback to the system. |
| Case Learning          | Automatically learn from successful and unsuccessful problem-solving experiences to improve future performance. |
| Extensibility          | Easily integrate the library with your own domain-specific data and algorithms. |

## Installation

You can install the `casebased` library using pip:

```
pip install casebased
```

## Usage

Here's a simple example of how to use the `casebased` library:

<antArtifact identifier="casebased-example" type="application/vnd.ant.code" language="python" title="Casebased Library Example">
from casebased.case_base import CaseBase
from casebased.retrieval import NearestNeighborRetriever

# Create a case base
case_base = CaseBase()

# Add cases to the case base
```python
case_base.add_case({
"problem": {
"symptoms": ["fever", "headache", "sore throat"],
"duration": 3
},
"solution": {
"medication": "paracetamol",
"dosage": "500mg every 6 hours"
}
})
```

```python
case_base.add_case({
"problem": {
"symptoms": ["cough", "runny nose", "fatigue"],
"duration": 5
},
"solution": {
"medication": "ibuprofen",
"dosage": "400mg every 8 hours"
}
})
```
# Retrieve the most similar case
```python
new_problem = {
"symptoms": ["fever", "headache", "sore throat"],
"duration": 2
}

retriever = NearestNeighborRetriever()
similar_case = retriever.retrieve(case_base, new_problem)

print(f"Similar case: {similar_case}")
print(f"Suggested solution: {similar_case['solution']}")
```

## 📈 Releases

You can see the list of available releases on the [GitHub Releases](https://github.com/casebased/casebased/releases) page.

We follow [Semantic Versions](https://semver.org/) specification.

We use [`Release Drafter`](https://github.com/marketplace/actions/release-drafter). As pull requests are merged, a draft release is kept up-to-date listing the changes, ready to publish when you’re ready. With the categories option, you can categorize pull requests in release notes using labels.

### List of labels and corresponding titles

|               **Label**               |  **Title in Releases**  |
| :-----------------------------------: | :---------------------: |
|       `enhancement`, `feature`        |       🚀 Features       |
| `bug`, `refactoring`, `bugfix`, `fix` | 🔧 Fixes & Refactoring  |
|       `build`, `ci`, `testing`        | 📦 Build System & CI/CD |
|              `breaking`               |   💥 Breaking Changes   |
|            `documentation`            |    📝 Documentation     |
|            `dependencies`             | ⬆️ Dependencies updates |

You can update it in [`release-drafter.yml`](https://github.com/casebased/casebased/blob/master/.github/release-drafter.yml).

GitHub creates the `bug`, `enhancement`, and `documentation` labels for you. Dependabot creates the `dependencies` label. Create the remaining labels on the Issues tab of your GitHub repository, when you need them.

## 🛡 License

[![License](https://img.shields.io/github/license/casebased/casebased)](https://github.com/casebased/casebased/blob/master/LICENSE)

This project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/casebased/casebased/blob/master/LICENSE) for more details.

## 📃 Citation

```bibtex
@misc{casebased,
  author = {casebased},
  title = {CaseBased is a python library that implements the priciples of case-based reasoning.},
  year = {2024},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/casebased/casebased}}
}
```

## Credits [![🚀 Your next Python package needs a bleeding-edge project structure.](https://img.shields.io/badge/python--package--template-%F0%9F%9A%80-brightgreen)](https://github.com/TezRomacH/python-package-template)

This project was generated with [`python-package-template`](https://github.com/TezRomacH/python-package-template)
