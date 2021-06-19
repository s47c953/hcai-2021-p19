# Classification into classes by aggregation functions of mixed behaviour

## AK HCAI Mini Projects (Class of 2021) - Mini Project 19 
A project for the course [AK HCAI Mini Projects (Class of 2021)](https://human-centered.ai/lv-706-046-ak-hci-2021-hcai/).

## Related Publications


## Introduction
This project implements the theoretical approaches described in [Related Publications](#related-publications) section and provides a set of example data sets.

## Quickstart Guide

<img src="images/app_layout.png" width="50%">

### File Structure
This application uses CSV files as data describtor. The separator used is a comma (",").
Additional, the file must have the following structure:
* **Row 1**: list of all attributes of the data points.<br/>
_Note: for easier node identification in plots the first attribute can be used as label by naming it "label"_
* **Row 2**: list of  the following structure "D<sub>L<sub>1</sub></sub>|D<sub>H<sub>1</sub></sub>, ... , D<sub>L<sub>n</sub></sub>|D<sub>H<sub>n</sub></sub>" where D<sub>L<sub>i</sub></sub> describes the value which should be rated most negatively and D<sub>H<sub>i</sub></sub> rated most positively for the corresponding attribute.<br/>
_Note: if D<sub>L<sub>i</sub></sub> > D<sub>H<sub>i</sub></sub> the application uses the inverse values the corresponding attribute._
* **Row 3-n**: list of numeric values. <br/>
_Note: if row 1 contains the label option the first element does not have to be a numeric value._

Example files can be found in the "examples" folder.

### Plot
The plot is segmented into 4 sections. In the lower left there is the left section and is further split into 2 parts. Values below the curve will strictly be marked as no (0) whereas values above the curve will have a value greater than 0.
In the upper right is the yes section. This is again split into 2 parts where above the curve the values will be strict yes (1) and values below the curve are smaller than 1.
The maybe fields in the upper left and lower right show data points which are calculated by the maybe functions.
The exact result of the plot depends on the used aggregation and quantifier function.


### Loading Data
Files structured as described in [File Structure](#file-structure) section can be loaded using the "Load File" Button. After loading the raw data a transformation to the space of aggregation functions is performed using D<sub>L</sub> and D<sub>H</sub>.

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

For more information about quantifier functions please refer to the [Related Publications](#related-publications) section.

### Aggregation functions
In the dropdown menu "Aggregation Function" the user can select a desired aggregation function. Currently there are 4 functions implemented and labeled as follows:
* **Lukasiewicz**: implements the Lukasiewicz t–norm and t–conorm
* **MinMax**: implements the MIN and MAX functions
* **TnormTconormGeometric**: implements the product t–norm, probabilistic sum t–conorm and geometric mean
* **TnormTconormArithmetic** implements the  product t–norm, probabilistic sum t–conorm and arithmetic mean

_Please note that currently only the Lukasiewicz t–norm and t–conorm make use of the parameters lambda and r_

### Parameter
#### lambda
The value of lambda influences the boundaries of the yes and no sections using the Lukasiewicz t–norm and t–conorm and can be any value greater than 0. Adjusting this paramater can be used to make the classifier more or less strict depending on the desired outcome. The following images show the results of changing lambda:

<img src="images/lukasiewicz_lr_1.png" width="33%" alt>
<img src="images/lukasiewicz_l_2.png" width="33%" alt>
<img src="images/lukasiewicz_l_0_5.png" width="33%" alt>

#### r
The value of r influences the resulting values of the maybe sections. Adjusting this paramater can be used to make the maybe sections more or less strict. The following images show the result of changing r:

<img src="images/lukasiewicz_lr_1.png" width="33%" alt>
<img src="images/lukasiewicz_r_n2.png" width="33%" alt>
<img src="images/lukasiewicz_r_2.png" width="33%" alt>

### Node Information
Each node represents a datapoint from the loaded file. The position is defined by the applied quantifier function for both axis and the value of the node is defined by the used aggregation function and its parameters.
Hoovering over a node will show an annotation including:
* The exact position of the node.
* If define, a target value for this node.
* The value of the node calculated with the selected aggregation function.
* The label of the node.

A node can be selected by clicking on it. This will show all the attributes of the datapoint in the lower left field of the application. Additionaly the user can set a desired target value for the node in order to calculated parameters lambda and r. More information in the section [Calculate Lambda and r](#calculate-lambda-and-r).

### Calculate Lambda and r

Using the "calc l r" button will let the application calculate best matching lambda and r values for the dataset. Therefore there must be a target value set for at least 1 datapoint. The application will then find the best matching values for lambda in range 0 < lambda <= 5 and r in range -2 <= r <= 4. After that the application shows the mean error for lambda and r.

## Examples
### Empty Plot
Using the plot function without providing any data will result in an empty plot. This can be used to see how the distribution of the values change when adjusting the aggregation functions or their parameters.

<img src="images/empty_plot.png" width="50%">

### Flats Dataset
This dataset consists of fictional appartments and contains the following attributes:
* Distance to schools
* Distance to grocery shops
* Distance to motorway
* Distance to public transport
* Size of the flat
* Size of the garden
* Number of rooms
* Price of the flat

The following example plot can be reproduced using following parameters:
* Apply most-of quantifier (m=0.4 and n=0.9) for x axis using distance-attributes
* Apply most-of quantifier (m=0.4 and n=0.9) for y axis using remaining attributes
* Draw plot by using Lukasiewicz t–norm and t–conorm

<img src="images/flat_plot.png" width="50%">

### Revenue Dataset
This dataset consists of fictional sales values and contains the following attributes:
* The sales of a given period
* The average time used per sale

Plotting this data using the Lukasiewicz t–norm and t–conorm results in the following plot:

<img src="images/sales.png" width="50%">

### Medical Dataset
