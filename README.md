# crossfit_open_2018
This repo contains Python-based data aggregation, visualization, and machine learning notebooks for the 2018 Crossfit Open, in addition to a CSV data sample (not yet added).

## repo structure
**data_collection** - database schema setup and automated web scraping for 2018 Open leaderboard and athlete profile data

**data_visualization** - data visualizations and statistical measurement for athletes using their 2018 Open leaderboard scores and profile benchmark lift/metcon stats

**scorer.py** - leaderboard scoring module used to rank athletes based on custom leaderboards. These leaderboards can be composed of all Open workouts, all athlete profile statistics, or any combination of any/all measurable GPP (general physical performance) metrics

**learning/** - folder containing data analysis and predictive modeling for 3 different performance-based learning tasks

## technology used
* Python 3.5
* PyMySQL
* Selenium
* Jupyter
* NumPy
* Pandas
* Matplotlib
* Seaborn
* scikit-learn

## sample data
A .csv sample of the data can be found in the sample_data/ directory. This dataset has been cleaned of problematic entries and incomplete data points.
