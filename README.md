# COVID-Paper-Clustering
Clustering papers written about COVID 19 based on their impact. If you would like to see the project on Kaggle, click [here](https://www.kaggle.com/williamkaiser/covid-19-data-analysis/edit/run/89680063).

##### Insert a photo of the data-vizualization here... I would look 


## Basis of the Project

This uses the [COVID-19 Open Research Dataset Challenge (CORD-19)](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge) for the paper dataset.

To textually analyze the dataset, SciSpaCy's large biomedical sciences [model](https://allenai.github.io/scispacy/) was used.

The majority of my code comes from [MasksimEkin]() with his [submission](https://www.kaggle.com/maksimeren/covid-19-literature-clustering) to this challenge. Including his beautiful Bokeh plot to visualize this data.

The one unique thing that this clustering incorporates is each paper's popularity in their respective fields. Alternative metrics were used via the [AltMetric API](https://altmetric.com) to measure each paper's impact. Each paper's impact vector (# of citations, # of news citations, # of blog posts, # of tweets, # of Facebook pages, # of Reddit posts, # of wikipedia mentions, and # of readers) was combined with the PCA-reduced textual analysis vector upon which K-means clustering was run.

###### The final plot can be shown here ***Include a link to the raw data visualization***.

## Why I Built This Project

This was part of my Senior-year AP Capstone project, where I used this analysis to analyze the spread of misinformation surrounding COVID19. The project soon shifted to clustering papers based on impact. From these clusters, I hope to generate new insights about how papers gain popularity, especially outside of scientific literature. 

**I will add a link to my paper when it is done here**
Imagine if someone reads this in 5 years... embarssing. 

## Running This Project

If anyone actually wants to run this for themselves, contact me at [wkaisertexas@gmail.com](mailto:wkaisertexas@gmail.com). 

This project was intially designed in Kaggle, but the RAM requirements proved insufficent for this use case.

## Noteable Data Science Choices

Data science decisions can be a little fuzzy, so I will explain some of the statistically significant choices that I made to determine the parameters to use.

Pretty common, but an Elbow plot was use to analyze the number of K-means clusters to use. After reading the elbow plot, it was decided that 20 clusters was a good number. This elbow plot was flatter than ideal. To wit, it is likely that similar number would have faired well also.

#### TODO: INSERT ELBOW Plot

Perhaps the most important decision was what weight to assing each paper's impact. Given the skew of each paper's impact, the sigmoid function was applied to linearize the dataset, and impact was normalized. 

This normalized vector was then combined with the paper vector after going through a round of PCA to reduce dimesions. Therefore, the final paper vector can be expressed as:

```math
V_{paper} = (1-p)T_{paper} +p\sigma(I_{paper})$$
```

Where:
- `V_{paper}` is the final vector of the paper for K-means clustering
- `T_{paper}` is the tokenized paper vector after PCA reduction
- `I_{paper}` is the impact vector of each paper
- `p` is the weight of the paper's impact vector \[0, 1].

A plot of the K-means error was made for p between 0 and 1 with intervals of 0.05, and it was found that a p-value of ____ was optimal.

#### TODO: Insert the graph here.

## Final Thoughts
This project is horribly optimized, and I need to learn how to scale better across my CPU cores. The most intensive, single-threaded step was applying the Spacy Tokenizer to each paper. I made some half-hearted attempts and parallel processing with little success. This is really something to fix in the future.

Also, the notebook used started out fairly organized, but then degenerated into a mess by the end. This was done on kind of a time ***CRUNCH***, so please manage expectations if the inclination to analyze this arrises.

