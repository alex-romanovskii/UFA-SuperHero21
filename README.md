# UFA-SuperHero21

### Publication of the solution to the [hakatanon](https://iqparkevents.com/hack) problem developed in 48 hours.

### About Hackaton  
- The online hackathon UFA_SUPERHERO is a project for IT professionals in Russia, the main task of which is to support promising teams within the framework of the launch of the new IQ park technology park. The best teams will have the opportunity to study at the Skolkovo startup school and become a resident of the new IQ park technology park.

### Our hakatanon task
- Creation of an algorithm for high-quality automatic interpretation of statistical data of industrial production in the Republic of Bashkortostan
- Development of a service for graphical visualization of statistical data on industrial production of the Republic of Bashkortostan (according to specified metrics) 

### Solution
#### Tab "О нас" (about us)
contains introductory information  
![Screenshot](pic/about_us.PNG)

#### Tab "Дашборд" (Dashboard)
Various data dependencies can be found here.
Additionally: statistics for other regions are uploaded to the server. The last two visualizations allow for a visual comparison of the production index by region.
is a dashboard consisting of interactive visualizations: 
- Sunburst plots (visualize hierarchical data spanning outwards radially from root to leaves)
![Screenshot](pic/Sunburst.PNG)
- Bar plots
![Screenshot](pic/Bar.PNG)
- Line plots
![Screenshot](pic/Line.PNG)
![Screenshot](pic/Line2.PNG)
- Choropleth Maps
![Screenshot](pic/Map.PNG)

#### Tab "Форма онлайн" (Online form)
form for submitting statistical data online. A check is automatically carried out for the correctness of filling in the data. After submitting the form, the data will be automatically added to the current data on the server, and the dashboard will update the visualizations
![Screenshot](pic/online_form.PNG)

#### Tab "Загрузить" (Upload)
Here you can download the previous form in csv format. The system will check not only the file extension, but also the names and number of columns in the form. Only with full compliance, the form will be uploaded to the server and automatically added to the previous data. The dashboard will also update all visualizations.  
Added on this tab, you can analyze the number of missing values for each participant who submitted the form.
![Screenshot](pic/upload.PNG.PNG)

### Technology (Python)
- Dash (Frontend)
- Plotly (Visualization)
- Pandas (Data Preprocessing)
