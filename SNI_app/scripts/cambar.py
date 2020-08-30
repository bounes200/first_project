import pandas as pd
import numpy as np

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, FactorRange, HoverTool, Select, Panel
from bokeh.layouts import WidgetBox, row, column
from bokeh.palettes import YlGn
from bokeh.transform import factor_cmap


def bar_cam(sni_gsub):
    def make_plot(src):
        nvf = list(sni_gsub['NVF'].unique())
        color_map = factor_cmap(field_name='NVF',
                                palette=YlGn[8], factors=nvf)
        pm = figure(title = 'Repartition des clients notes de la CAMR CORPORATE', plot_width=600, plot_height=500,
                    x_axis_label='Rating Class', y_axis_label='Number of rated clients', x_range=nvf)
        pm.vbar(x='NVF', top='NB', source=src, width=0.5, color=color_map)
        pm.line('NVF', 'NB', source=src, color='red')

        hover = HoverTool(tooltips=[('NVF', '@NVF'), ('NB Rated', '@NB')])
        pm.add_tools(hover)

        pm.title.vertical_align = 'top'

        return pm

    def update_plot(attr, old, new):
        # read the current value of the dropdown
        cmr = camr_select.value
        # set new_data
        new_data = {
            'NVF': sni_gsub[sni_gsub['CAMR'] == cmr]['NVF'],
            'NB': sni_gsub[sni_gsub['CAMR'] == cmr]['Count']
        }

        # Assign new_data to the original source
        src.data = new_data

        # add the title
        p.title.text = 'Repartition des clients notes de la %s' % cmr



    camr_select = Select(options=list(sni_gsub['CAMR'].unique()), value='CAM CORPORATE', title='CAM Region')
    # attach the update to the value
    camr_select.on_change('value', update_plot)

    # Data
    data = {'NVF': sni_gsub[sni_gsub['CAMR'] == 'DOMAINE GRC']['NVF'],
            'NB': sni_gsub[sni_gsub['CAMR'] == 'DOMAINE GRC']['Count']
            }
    src = ColumnDataSource(data=data)
    # Plot
    p = make_plot(src)

    layout = column(WidgetBox(camr_select), p)

    tab = Panel(child=layout, title='Rating class distribution')

    return tab
