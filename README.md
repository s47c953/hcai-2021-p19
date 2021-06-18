# Classification into classes by aggregation functions of mixed behaviour

## AK HCAI Mini Projects (Class of 2021) - Mini Project 19 
A project for the course https://human-centered.ai/lv-706-046-ak-hci-2021-hcai/


## Introduction
This project implements the theoretical approaches discussed in 

> Extension of the work of Classification by ordinal sumsof conjunctive and disjunctive functions for explainableAI and interpretable machine learning solutions

in a practical way

## Quickstart Guide

### File Structure
This application uses .csv files as data describtor. The separator used is a comma (",").
Additional, the file must have following structure:
* **Row 1**: comma separated list of all attributes of the data points.<br/>
_Note: for easier node identification in plots the first attribute can be used as label by naming it "label"_
* **Row 2**: comma seperated list of following structure "D<sub>L<sub>1</sub></sub>|D<sub>H<sub>1</sub></sub>, ... , D<sub>L<sub>n</sub></sub>|D<sub>H<sub>n</sub></sub>" where D<sub>L<sub>i</sub></sub> describes the value which should be rated most negativ and D<sub>H<sub>i</sub></sub> rated most positiv for the corresponding attribute.<br/>
_Note: if D<sub>L<sub>i</sub></sub> > D<sub>H<sub>i</sub></sub> the application uses the inverse values the corresponding attribute._
* **Row 3-n**: comma separated list of numeric values. <br/>
_Note: if row 1 contains the label option the first element does not have to be a numeric value._

Examples files can be found in "demo_files"

### Loading Data

### Defining Quantifier functions

### Aggregation functions

### Parameter
#### lambda

#### r

### Plot

### Modifying Nodes

## Examples
### Empty Plot

### Appartment Dataset

### Medical Dataset
