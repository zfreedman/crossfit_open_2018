"""
The below code is responsible for implementing information retrieval
from a MySQL database into a Pandas DataFrame using PyMySQL/Pandas
for the 2018 CrossFit Open.
"""
import seaborn as sb

#styling settings
#https://matplotlib.org/users/customizing.html
font_color = "#ffffff"
bg_color = "#000000"
axes_label_size = "medium"
figure_size = [8, 6]
def stylize():
    sb.set(
        rc = {
            "axes.edgecolor": "green",
            "axes.facecolor": bg_color,
            "axes.labelcolor": font_color,
            #this link for these 2 parameters
            #https://stackoverflow.com/questions/28825594/why-doesnt-the-matplotlib-label-fontsize-work
            "axes.labelsize": 16,
            "axes.titlesize": 16,

            "grid.color": font_color,
            "grid.linewidth": .5,

            #this link is just for figure.facecolor
            #http://jonathansoma.com/lede/data-studio/matplotlib/changing-the-background-of-a-pandas-matplotlib-graph/
            "figure.facecolor": bg_color,
            "figure.figsize": ", ".join([str(i) for i in figure_size]),
            #"figure.titlesize": "large",

            "font.family": [u"sans-serif"],
            "font.sans-serif": [
                u"Arial",
                u"sans-serif"
            ],

            #"legend.fancybox": True,
            #"legend.facecolor": "red",
            "legend.framealpha": .95,
            "legend.fontsize": "medium",

            "lines.linewidth": 1.25,
            #"lines.marker": "x",
            #"lines.markersize": 60,

            "text.color": font_color,

            "xtick.color": font_color,
            #"xtick.labelsize": axes_label_size,
            #"xtick.direction": "out",

            "ytick.color": font_color
            #"ytick.labelsize": axes_label_size
        }
    )
