# books-apis
APIs project made in Ironhack August '20 cohort.

![](https://openmindapp.wpengine.com/wp-content/uploads/2017/11/library-cropped.jpg)

## Objective
The objective of this project is to practice querying APIs via the `requests` module. The secondary objective is to learn how to use python's built-in `argparse` module, which allows the user to pass arguments via the CLI.

In order to do so, a books dataset obtained from *kaggle.com* is used as a starting point. Then, this dataset is extended via the *O'Reilly Platform Search API* to include books on data science topics. Finally, the *Goodreads API* is used to obtain the review statistics of the added books.

## Project Structure
The structure and contents of the project are as follows:
- `notebooks/`: Two jupyter notebooks.
  1. `cleaning.ipynb`: Dataset cleaning process.
  2. `enreach.ipynb`: Dataset enreaching process.
- `src/`: Three source code files.
  1. `cleanfuncs.py`: Functions used in the cleaning process.
  2. `enreachfuncs.py`: Functions used in the enreaching process.
  3. `mainhelpers.py`: Functions used in the main program.
- `main.py`: Executable script to filter, sort and aggregate the books dataset via the CLI.

## References
1. [*O'Reilly Platform Search API*](https://www.oreilly.com/online-learning/integration-docs/search.html)
2. [*Goodreads API*](https://www.goodreads.com/api)
3. [`requests`](https://requests.readthedocs.io/en/master/)
4. [`argparse`](https://docs.python.org/3/library/argparse.html)
