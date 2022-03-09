# COVID-Paper-Clustering
Clustering papers written about COVID 19 based on their impact. If you would like to see the project on Kaggle, click [here](https://www.kaggle.com/williamkaiser/covid-19-data-analysis/edit/run/89680063).

## Basis of the Project

This uses the [COVID-19 Open Research Dataset Challenge (CORD-19)](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge) for the paper dataset.

To textually analyze the dataset, SciSpaCy's large biomedical sciences [model](https://allenai.github.io/scispacy/) was used.

The majority of my code comes from [MasksimEkin]() with his [submission](https://www.kaggle.com/maksimeren/covid-19-literature-clustering) to this challenge. Including his beautiful Bokeh plot to visualize this data.

The one unique thing that this clustering incorporates is each paper's popularity in their respective fields. Alternative metrics were used via the [AltMetric API](https://altmetric.com) to measure each paper's impact. Each paper's impact vector (# of citations, # of news citations, # of blog posts, # of tweets, # of Facebook pages, # of Reddit posts, # of wikipedia mentions, and # of readers) was combined with 

## Why I Built This Project

This was part of my Senior-year AP Capstone project, where I used this analysis to analyze the spread of misinformation surrounding COVID19. The project soon shifted to clustering papers based on impact. From these clusters, I hope to generate new insights about how papers gain popularity, especially outside of scientific literature. 

**I will add a link to my paper when it is done here**
Imagine if someone reads this in 5 years... embarssing. 

## Running This Project

If anyone actually wants to run this for themselves, contact me at [wkaisertexas@gmail.com](mailto:wkaisertexas@gmail.com). 

This project was intially designed in Kaggle, but the RAM requirements proved insufficent for this use case.

## Final Thoughts
This project is horribly optimized, and I need to learn how to scale better across my CPU cores. The most intensive, single-threaded step was applying the Spacy Tokenizer to each paper. I made some half-hearted attempts and parallel processing with little success. This is really something to fix in the future.

Also, the notebook used started out fairly organized, but then degenerated into a mess by the end. This was done on kind of a time ***CRUNCH***, so please manage expectations if the inclination to analyze this arrises.
