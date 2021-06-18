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
Files structured as described in **File Structure** section can be loaded using the "Load File" Button. After loading the raw data a transformation to the space of aggregation functions is performed using D<sub>L</sub> and D<sub>H</sub>.

### Defining Quantifier functions
Clicking the "Query" button opens a new window that allows the user to define the quantifier function for each axis. 

<img src="images/query.png" width="50%">

The steps to define quantifier functions are:
1. Select target axis
2. Select quantifier function
    * conjunctive
    * disjunctive
    * most-of
3. In case of "most-of" define m and n
4. Define the keys (attributes) used for the target axis
5. Apply for axis
6. Repeat steps 1-5 for other axis
7. Click "'Save and Close" to apply settings

For more information about quantifier functions please refer to the related publications section.


### Aggregation functions
In the dropdown menu "Aggregation Function" the user can select a desired aggregation function. Currently there are 4 functions implemented and labeled as follows:
* **Lukasiewicz**: implements the Lukasiewicz t–norm and t–conorm
* **MinMax**: implements the MIN and MAX functions
* **TnormTconormGeometric**: implements the product t–norm, probabilistic sum t–conorm and geometric mean
* **TnormTconormArithmetic** implements the  product t–norm, probabilistic sum t–conorm and arithmetic mean

_Please note that currently only the Lukasiewicz t–norm and t–conorm make use the parameters lambda and r_

### Parameter
#### lambda

#### r

### Plot

### Modifying Nodes

## Examples
### Empty Plot
<img src="images/empty_plot.png" width="50%">

### Appartment Dataset
<img src="images/flat_plot.png" width="50%">

### Medical Dataset
