from dataclasses import dataclass

@dataclass
class PlotDataSet:
    """
    Object class to describe plot line
    plottype options: 'dash', 'dot', 'solid', 'dashdot'
    plotcolor options:
    """
    name: str
    timelist: list
    datalist: list
    plottype: str
    plotcolor: str

    def __init__(self, name, timelist, datalist, plottype, plotcolor) -> None:
        self.name = name
        self.timelist = timelist
        self.datalist = datalist
        self.plottype = plottype
        self.plotcolor = plotcolor
