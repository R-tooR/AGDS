# AGDS
Implementation of AGDS associative data structure with GUI (branch: gui)

Application converts relational data set into AGDS graph structure, which enables very easy and fast sorting (e.g. by overall similarity).
Also, such a structure is "lighter" because of removing duplicates of same value, which is represented by node.

![Slider](/images/slider.gif)

How to use application:
1. Clone repository
2. Run shell, go to repo directory and type `python gui.py`
3. Select file to load (file should be `.csv` or `.xls`) ![Load](/images/calculate.PNG)
4. Graph will be drawn automatically (instances nodes are on the upper part of plot, while values on lower part).
5. Default instance, which is selected, is instance of index `0` (first row of dataset)
6. Use slider to adjust graph to contain only instances, which similarity parameter is bigger than selected.
7. To change instance, to which others will be compared, in spin select instance with different id, and click `Calculate`
![Calculate](/images/calculate.PNG)
8. Graph should be redrawn for similarity threshold equal to `0`
