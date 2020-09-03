import pandas as pd
import numpy as np
import datetime

from bokeh.plotting import figure
from bokeh.io import show, output_notebook, push_notebook, curdoc
from bokeh.models import ColumnDataSource, FactorRange, HoverTool, Select, Panel
from bokeh.layouts import WidgetBox, row, column
from bokeh.models import Column
from bokeh.palettes import YlGn

# function time_series

def time_series(grouper):
    def make_plot(src):
        pp = figure(title='Rating Time Series: CAM CORPORATE', title_location='above', plot_width=500, plot_height=500,
                    x_axis_label='Date',
                    y_axis_label='Number Rated', x_axis_type='datetime')

        pp.line('time', 'NVF', line_color='purple', line_width=3, source=src)
        hover = HoverTool(tooltips=[('Date', '@time{%Y-%m}'), ('NB Rated', '@NVF')],
                          formatters={'@time': 'datetime', '@NVF': 'numeral'})
        pp.add_tools(hover)
        pp.title.align = "center"
        pp.title.text_font_size = "12px"
        pp.axis.axis_label_text_font_style = 'bold'
        pp.axis.axis_label_text_font_size = '20pt'
        pp.axis.major_label_text_font_size = '10pt'

        return pp

    def update_plot(attr, old, new):
        # read the current value of the dropdown
        cmr = camr_select.value
        # set new_data
        new_data = {
            'time': grouper[grouper['CAMR'] == cmr]['date'],
            'NVF': grouper[grouper['CAMR'] == cmr]['NVF']
        }

        # Assign new_data to the original source
        src.data = new_data

        # add the title
        p.title.text = 'Rating Time Series: %s' % cmr

    camr_select = Select(options=sorted(list(grouper['CAMR'].unique())), value='CAM CORPORATE', title='CAM Region')
    # attach the update to the value
    camr_select.on_change('value', update_plot)

    # Data
    data = {'time': grouper[grouper['CAMR'] == 'DOMAINE GRC']['date'],
            'NVF': grouper[grouper['CAMR'] == 'DOMAINE GRC']['NVF']}
    src = ColumnDataSource(data=data)

    # Plot
    p = make_plot(src)

    layout = column([Column(camr_select, width = 500), p])

    tab = Panel(child=layout, title='Rating Times series per CAMR')

    return tab


