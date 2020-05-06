# LINFO1002A_projet2
python project in UCLouvain LINFO1002A course<br/>
group E6 <br/>
Members : <br/>
  <span class="marge">Allegaert Hadrien</span><br/>
  <span class="marge">Dourov Maxime</span><br/>
  <span class="marge">Lechat Jerome</span><br/>
  
## Run the server
To run the server it's simple as you use CLI or pycharm.
#### Command Line Interface
First you have to go on the main directory (LINFO1002_projet2) with the "cd" command the main server is named app.py as flask ask for <br/>
then you simply have to type "flask run" (for this version a warning message tell you it's a development server, don't care it's just a constant to setup because we used development mode to refresh easier). <br/>
#### Pycharm
With pycharm terminal you are directly in the good directory so you only have to type "flask run" to run the server

## Navigation tree
Once the server launch you can click on the link in blue "http://127.0.0.1:5000/" it's a local address open on the port 5000 (this port is used to be free),
a window with your default browser opening if you prefer to use another browser you can copy paste the link before in the browser you want to open the site.

When you're on the main page of the site a little representation of INGInious bar theme is done and recall you where you're in the site. <br/>

Some Graph in the main page give you info on all courses in db.<br/>
On the right you have the menu which is dynamically created from the db data. 
One point per course (with one page linked) and one per task affiliated (linked to its own page too) to display the task list simply Hover with your pointer the affiliated course. <br/>

There is at least two graph per pages.<br/>

## Specifications
The server run on a single template which is properly simple: at first a head which contain the chart.js import and the signature of the tab and it's followed by 3 types of container filled by flaks function "render_template"<br/>
These three functions are PATH, GRAPH (1 to  5) and MENU: they wait to get the html string code and fill the container with
These functions are maintain in container to easily CSS them.
MENU is filled from the courseList module which compute the list of course and fill a matrix with course and list of appropriated task.<br/>
PATH is only filled with the variable passed on the dynamical server to know where you are in the site.<br/>
GRAPH are the containers which can, or not, contains a graph( and only one)<br/>
GRAPH1 & GRAPH2 are CSS stylized on the same line, displayed with 50% of (width screen - menu width (200px)) -> 50% (widthScreen - 200px)<br/>
The other graphs are displayed under with 100% of the width screen - 200px.



  
