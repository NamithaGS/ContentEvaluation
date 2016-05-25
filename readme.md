# Content Evaluation

# Synopsis
Evaluating Content Analysis of Text Retrieval Conference (TREC) Polar Dynamic Domain Dataset

## Motivation
Evaluating the content detection done for Big Data for TREC dataset

## Description
The content object units that are evaluated are:<br>
a. The enriched JSON extracted from Content Extraction project and inserted into either
Apache Solr or ElasticSearch <br>
b. The upstream CCA TREC-DD-Polar data that is used for the project

The overall content detection evaluation process can be divided into several steps:<br>
1. Selection of Content – accquiring data, and what process do you follow?<br>
2. Units for Content –  what are the default content objects that are getting evaluated.<br>
3. Preparing Content for Coding (Text Processing) – making text and metadata uniformly processed for enrichment.<br>
4. Coding the Content (Enrichment) – Performing annotation and extraction from the uniform text and metadata.<br>
5. Counting and Weighting – Evaluating and assessing results.<br>
6. Drawing Conclusions – Deriving meaning and insights from results.<br>

##Tasks
D3 visualizations to visualize:<br>
-> Identify the classification path from request to content.<br>
-> File size diversity of CCA dataset by MIME type.<br>
-> Parser call chain and how much text and metadata was actually obtained.<br>
-> Language identification and diversity across the dataset.<br>
-> Word Cloud D3 visualization of the text, metadatea, and language to find maximal occurring topics in the dataset.<br>
-> Algorithm to compute maximal joint agreement between the 4 algorithms of Named entity recognition tools (NLTK Rest, Core NLP,OpenNLP, Grobid).<br>
-> Identify the Spectrum (range, min/max) of measurements.<br>



## Contributors
Charan Shampur </br>
Manisha Kampasi

## License
Apache Tika
https://tika.apache.org/license.html
