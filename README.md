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

## Main Program Usage
```bash
main.py [-h] [--topic TOPIC] [--rating MIN_RATING] [--count MIN_COUNT] [--sort {rating,pages,ratings_count,title,reviews_count}] [--aggregate] [--list LIST]

Filter, sort, and potentially aggregate books dataset.

optional arguments:
  -h, --help            show this help message and exit
  --topic TOPIC, -t TOPIC
                        filter by topic.
  --rating MIN_RATING, -r MIN_RATING
                        filter by minimum average rating.
  --count MIN_COUNT, -c MIN_COUNT
                        filter by minimum ratings count.
  --sort {rating,pages,ratings_count,title,reviews_count}, -s {rating,pages,ratings_count,title,reviews_count}
                        sort by specified column (default: title).
  --aggregate, -a       perform aggregations.
  --list LIST, -l LIST  number of books to list (default: 10).
  ```
Example:
```bash
./main.py -t machine_learning -r 3.5 -c 5 -s rating
                                          Authors  Average Rating Language Code  Num Pages  Ratings Count  Text Reviews Count                                              Title
ISBN                                                                                                                                                                            
9781492032649                      Aurélien Géron            4.70           eng       1284             17                   0  Hands-On Machine Learning with Scikit-Learn, K...
9781491962299                      Aurélien Géron            4.54           eng        841            240                   8  Hands-On Machine Learning with Scikit-Learn an...
9781449369415      Andreas C. Müller, Sarah Guido            4.32           eng        549            238                  30       Introduction to Machine Learning with Python
9781492045113                    Emmanuel Ameisen            4.29           eng        359             24                   4     Building Machine Learning Powered Applications
9781787125933  Sebastian Raschka, Vahid Mirjalili            4.28           eng        794             35                   2                            Python Machine Learning
9781783555130                   Sebastian Raschka            4.28           eng        565            407                  26                            Python Machine Learning
9781491989388                         Chris Albon            4.27           eng        383             39                   6              Machine Learning with Python Cookbook
9781784393908                         Brett Lantz            4.24           eng        602             25                   0           Machine Learning with R - Second Edition
9781119482086               Marcos Lopez de Prado            4.23           eng        537             30                   4             Advances in Financial Machine Learning
9781782162148                         Brett Lantz            4.21           eng        537             18                   1                            Machine Learning with R
```

Example with aggregation:
```bash
./main.py -t machine_learning -r 3.5 -c 5 -s rating -a
       Average Rating    Num Pages  Ratings Count  Text Reviews Count
count       22.000000    22.000000      22.000000           22.000000
mean         4.046364   518.954545      73.500000            6.636364
std          0.314575   240.176617     104.517827            8.156478
min          3.560000   107.000000       6.000000            0.000000
25%          3.740000   388.750000      17.250000            1.000000
50%          4.090000   529.500000      30.000000            4.000000
75%          4.277500   584.500000      60.000000            8.750000
max          4.700000  1284.000000     407.000000           30.000000
```

## References
1. [*O'Reilly Platform Search API*](https://www.oreilly.com/online-learning/integration-docs/search.html)
2. [*Goodreads API*](https://www.goodreads.com/api)
3. [`requests`](https://requests.readthedocs.io/en/master/)
4. [`argparse`](https://docs.python.org/3/library/argparse.html)
