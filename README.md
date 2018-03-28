This project is to review drug poisoning mortality in the state of Kentucky 
by county, and to see if there is any obvious correlation between drug deaths 
and a county's dry/wet status. Or at least to see if the increase in the rate of
drug deaths increased faster in dry counties than wet counties. 

The idea for the project came from a study published by three professors at UofL
(https://ideas.repec.org/p/pra/mprapa/66274.html) showing that statistically, 
there are more meth labs in Kentucky's dry counties (in terms of arrests) than in 
wet counties. So, following that, I would assume that it would follow that the 
rate of drug deaths would be higher in dry counties as well.

The data that I used was 'Drug Poisoning Mortality by County: United States' from 
Data.gov. 
(https://catalog.data.gov/dataset/drug-poisoning-mortality-by-county-united-states)
The full data set contains information the age adjusted drug poisoning 
deaths (per 100,000 people) by every county in the United States (save for a few 
noted exceptions on the data source page) for the range of years of 1999-2016.
Since the comparison that I wanted to make relied on if a county was wet or dry, 
one issue is that distinction is not included in the initially data set. Searching 
online, I was unable to easily find a list of Kentucky counties and their wet/dry
status for a particular year. Doing research on it, over the last decade many 
counties have held votes on their alcohol status, so that does fuzzy up the end 
result a bit. Since the API consisted of a range, I was hoping to find a list of 
counties from somewhere in the middle. However, I ended up using a map published 
in 2012.
(http://www.kentucky.com/news/politics-government/article44371632.html)
I was able to copy and paste a list of Kentucky counties and their FIPS (Federal
Information Processing Standards) number, which was a column in my data set, into 
an excel sheet. I then just manually marked down if a county was wet/moist or 
Dry/Dry with special circumstances. This would be used later for a sql statement 
using FIPS to group wet counties for one chart and dry counties in another chart.

To run my project, with python it would require sqlite3, pandas, seaborn, and 
matplotlib. These should all be listed in the requirement.txt file. 

For the purposes of my project's question, I would only need the data from the 
state of Kentucky. First, the full data set would be placed into the sql database. 
A query was then written to parse down the information into wet Kentucky counties 
first using the FIPS number, then into dry Kentucky counties. To clean that data, 
I stripped off the tail end of the Death Rate column, as it presented the rate as 
a range in groupings of 2 (example: 2-3.9, 4,-5.9, etc). So that information was 
cleaned so that it was a single number for graphing, choosing the even and whole 
first number. The two exceptions were the first grouping '<2" which I changed to 
1 and the last group "30+" which I just left at 30. 

The other column that needed cleaning was the County column, as it was 
redundant initially, with every entry in the County column containing the word 
county, and then the appropriate state. So that was cleaned so that it only had the
name of the County. This was mainly done because I had initially envisioned the end
product figure have data points labeled by county (or at least able to hover over 
to see), but there ended up being so many points that the figure was already 
crowded enough. That might end up being more of a second version of this project
if I came back to improve it.

For plotting out the data, based on the type of data I had, I wanted to use a 
scatter plot (which each point having a faint hue, so that the more hits on that 
point, the darker it would be). Over the scatter plot, I wanted to show a 
regression line. The comparison between the two graphs would be seeing which of 
two had a steeper regression line. The data shown is the Age Adjusted Drug Related
Death Rate for the corresponding year, for each county based on its wet or dry status.

To display the scatter plot with a regression line, using seaborn was the method
that would be able to produce the output that I was looking for. The coding 
produces two separate figures; the comparison between the two is just visual.

For the scope of this project, I did not try to find anything more statistically 
accurate. But just by looking at the end result, the Dry County figure does have 
a steeper regression line, showing that drug deaths did increase more in those 
counties compared to wet counties. Though both charts show just how quickly drug 
related deaths have increased across the board for the state of Kentucky.
