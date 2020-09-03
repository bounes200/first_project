import pandas as pd
import numpy as np

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Panel, HoverTool, Select, DataTable, TableColumn, LabelSet, Div
from bokeh.layouts import WidgetBox, row, column
from bokeh.palettes import Spectral8, YlGn, Accent, Category20, GnBu
from bokeh.transform import factor_cmap
from bokeh.models import Column


def bar_cam(sni_csub, sni_dsub):
    # make data sources
    def make_camr_src(cmr):
        data = {'NVF': sni_csub[sni_csub['CAMR'] == cmr]['NVF'],
                'NB': sni_csub[sni_csub['CAMR'] == cmr]['Count']
                }
        return data

    def make_dr_src(dr):
        data = {'NVF': sni_dsub[sni_dsub['DR'] == dr]['NVF'],
                'NB': sni_dsub[sni_dsub['DR'] == dr]['Count']
                }
        return data

    # make plots

    def make_plots(src1, src2):
        nvf = list(sni_csub['NVF'].unique())
        color_map = factor_cmap(field_name='NVF',
                                palette=GnBu[8], factors=nvf)

        # define figure and plot p1

        p1 = figure(title = 'Répartition du PTF de la CAM CORPORATE par classe de risque',plot_height = 450, plot_width = 600,x_axis_label='Rating Class', y_axis_label='Number of rated clients', x_range=nvf,
                    toolbar_location='below')
        p1.vbar(x='NVF', top='NB', source=src1, width=0.5, color='#2B7C75')
        #p1.line('NVF', 'NB', source=src1, color='red')
        p1.toolbar.active_drag = None
        hover1 = HoverTool(tooltips=[('NVF', '@NVF'), ('NB Rated', '@NB')])
        p1.add_tools(hover1)
        labels1 = LabelSet(x='NVF', y='NB', text='NB', level='glyph',
                          x_offset=0, y_offset=1, source=src1, render_mode='canvas', text_align = 'center',
                          text_font_style = 'bold', text_font_size = '10pt')
        p1.add_layout(labels1)

        # define figure and plot p2

        p2 = figure(title = 'Répartition du PTF de la CAM CORPORATE par classe de risque',plot_height = 450,
                    plot_width = 600,x_axis_label='Rating Class', y_axis_label='Number of rated clients',
                    x_range=nvf,toolbar_location='below')
        p2.vbar(x='NVF', top='NB', source=src2, width=0.5, color='#2D7D3E')
        #p2.line('NVF', 'NB', source=src2, color='black')
        p2.toolbar.active_drag = None
        hover2 = HoverTool(tooltips=[('NVF', '@NVF'), ('NB Rated', '@NB')])
        p2.add_tools(hover2)
        labels2 = LabelSet(x='NVF', y='NB', text='NB', level='glyph',
                           x_offset=0, y_offset=1, source=src2, render_mode='canvas', text_align='center',
                           text_font_style='bold', text_font_size='10pt')
        p2.add_layout(labels2)

        return p1, p2

    # plot style

    def style(p):
        p.xgrid.visible = False
        p.ygrid.visible = False
        p.yaxis.visible = False
        # title
        p.title.align = 'center'
        p.title.text_font_size = '12pt'
        p.title.text_font = 'times'

        # Axis titles
        p.xaxis.axis_label_text_font_size = '11pt'
        p.xaxis.axis_label_text_font_style = 'bold italic'
        p.yaxis.axis_label_text_font_size = '11pt'
        p.yaxis.axis_label_text_font_style = 'bold italic'

        # Tick labels
        p.xaxis.major_label_text_font_size = '9pt'
        p.yaxis.major_label_text_font_size = '9pt'
        p.border_fill_color = None
        p.outline_line_color = None

        return p

    # callback 1
    def update_plot1(attr, old, new):
        # read the current value of the dropdown
        cmr = camr_select.value
        # set new_data
        new_data = make_camr_src(cmr)

        # Assign new_data to the original source
        src1.data = new_data
        p1.title.text = 'Répartition du PTF de la %s par classe de risque' % cmr

    # callback 2
    def update_plot2(attr, old, new):
        # read the current value of the dropdown
        dr = dr_select.value
        # set new_data
        new_data = make_dr_src(dr)

        # Assign new_data to the original source
        src2.data = new_data
        p2.title.text = 'Répartition du PTF de la %s par classe de risque' % dr
    def table(src1, src2):
        col1 = [TableColumn(field='NVF', title='Rating Class'), TableColumn(field='NB', title='Clients Rated')]
        tbl1 = DataTable(source=src1, columns=col1, editable=True, width = 600)

        col2 = [TableColumn(field='NVF', title='Rating Class'), TableColumn(field='NB', title='Clients Rated')]
        tbl2 = DataTable(source=src2, columns=col2, editable=True, width = 600)

        return tbl1, tbl2

    camr_select = Select(options=list(sni_csub['CAMR'].unique()), value='CAM CORPORATE', title='Choisir une CAM Region')
    # attach the update to the value
    camr_select.on_change('value', update_plot1)

    dr_select = Select(options=list(sni_dsub['DR'].unique()), value='CAM CORPORATE', title='Choisir une DR')
    # attach the update to the value
    dr_select.on_change('value', update_plot2)
    camr_select.width = 600
    # Data

    data1 = make_camr_src(camr_select.value)
    data2 = make_dr_src(dr_select.value)

    src1 = ColumnDataSource(data=data1)
    src2 = ColumnDataSource(data=data2)

    p1, p2 = make_plots(src1, src2)
    p1 = style(p1)
    p2 = style(p2)
    tbl1, tbl2 = table(src1, src2)

    layout = row([column([Column(camr_select, width = 500), p1, tbl1]),
                  column([Column(dr_select, width = 500), p2, tbl2])])

    tab = Panel(child=layout, title='Rating class distribution')

    return tab
