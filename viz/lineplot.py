"""
import library
"""
from pathlib import Path
import sys

import plotly.graph_objects as go

if __name__ == "__main__":
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from lineplot_data import PlotDataSet
else: 
    from .lineplot_data import PlotDataSet

class LinePlot:
    """
    Class to draw a lineplot
    """
    def __init__(self, data_list: list[PlotDataSet] = None) -> None:
        if data_list is not None:
            self.data = data_list

    def update_data(self, data_list: list[PlotDataSet]):
        """
        Update data of the class
        """
        self.data = data_list

    def draw_plot(self):
        """
        Draw line plot
        """
        fig = go.Figure()
        if self.data is not None:
            for line_data in self.data:
                plotdata = line_data.datalist
                timelist = line_data.timelist
                plotname = line_data.name
                plottype = line_data.plottype
                plotcolor = line_data.plotcolor

                fig.add_trace(go.Scatter(x=timelist, y=plotdata, name=plotname, line=dict(color=plotcolor, width=4, dash=plottype)))

        fig.update_layout(title='FInancial Overview',
                   xaxis_title='Month',
                   yaxis_title='SGD')
        fig.show()

if __name__ == "__main__":
    # Test data
    month = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
         'August', 'September', 'October', 'November', 'December']
    inc = [28.8, 28.5, 37.0, 56.8, 69.7, 79.7, 78.5, 77.8, 74.1, 62.6, 45.3, 39.9]
    exp = [12.7, 14.3, 18.6, 35.5, 49.9, 58.0, 60.0, 58.6, 51.7, 45.2, 32.2, 29.1]

    actualm = ['April', 'May', 'June', 'July']
    actual = [30.8, 28.5, 37.0, 56.8]

    p1 = PlotDataSet("Income", month, inc, 'dot', 'mediumblue')
    p2 = PlotDataSet("Expense", month, exp, 'dot', 'firebrick')
    p3 = PlotDataSet("Actual", actualm, actual, 'solid', 'darkgreen')
    data = [p1, p2, p3]
    plot = LinePlot(data)
    plot.draw_plot()
