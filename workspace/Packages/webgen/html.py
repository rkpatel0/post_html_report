'''
Created on Jul 28, 2014

@author: Rishi.Patel
'''


class ToHtml(object):
    '''
    Methods to convert data types to html code.
    '''

    def __init__(self, param=False):
        'Generic Text to HTML converter with most the bells and whistles'

        self._load_formats(param)

    def _load_formats(self, param):
        'Create HTML Formats'

        # Type 1 HTML Formats:
        self.TYP1_FMT = '<{name}>%s</{name}>\n'.format
        self.TBLE_IDX = self.TYP1_FMT(name='th')
        self.TBLE_ITM = self.TYP1_FMT(name='td')
        self.TBLE_ROW = self.TYP1_FMT(name='tr')
        self.TBLE_NME = self.TYP1_FMT(name='table')
        self.LIST_FMT = self.TYP1_FMT(name='li')
        self.PRGH_FMT = self.TYP1_FMT(name='p')
        self.HEAD_END = self.PRGH_FMT % '&nbsp;'

        # Type 2 HTML Formats (don't change order!):
        self.TYP2_FMT = '\n<{name} {head}>{body}</{name}>\n'.format
        self.TITL_CSS = self.TYP2_FMT(name='h1',
                                      head='class="title"',
                                      body='{title}').format
        self.LINK_FMT = self.TYP2_FMT(name='a',
                                      head='href={url}',
                                      body='{name}').format
        self.STYL_CSS = self.TYP2_FMT(name='div',
                                      head='class="{cls}" style="{style}"',
                                      body='{data}').format
        HEAD_BODY = self.TITL_CSS(title='{title}') + '{body}\n' + self.HEAD_END
        self.HEAD_TP1 = self.TYP2_FMT(name='div',
                                      head='class="row1"',
                                      body=HEAD_BODY).format

        # Unique HTML Formats:
        self.BREAK_FMT = '<br>'
        self.IMAGE_FMT = "<img width={w} src={url} height={h}/>".format
        self.TBL_STYLESIZE_FMT = 'width:{width}px;height:{height}px;'.format

        # Constants Based on Default Webpage template
        self.TBL_DEFAULT = {
                            'class': 'tableone',
                            'row_width': 120,
                            'row_height': 35,
                            'MAX_WIDTH': 600,
                            }
        
        # Overwrite default settings with custom if passed in
        if param == False:
            param = {}
        for key in self.TBL_DEFAULT.keys():
            if key in param:
                self.TBL_DEFAULT[key] = param[key]

    def df_to_html(self, df, tbl_fmt={}):
        'Convert DataFrame to HTML Table'

        # Table Header (first row)
        index_name = df.index.name
        if not index_name:
            index_name = 'Index'
        df_html = self.list_to_tablerow([index_name] + df.columns.tolist())

        # Table Content (other rows)
        for i in range(df.index.size):
            row = [df.index[i]] + df.iloc[i].tolist()
            df_html += self.list_to_tablerow(row)
            #df_html += self.list_to_tablerow(df.iloc[i].tolist(), i)

        # Load Table Settings
        for key in self.TBL_DEFAULT.keys():
            if not key in tbl_fmt:
                tbl_fmt[key] = self.TBL_DEFAULT[key]

        # Set Table Size
        tbl_fmt['height'] = tbl_fmt['row_height'] * (df.index.size + 1)
        tbl_fmt['width'] = tbl_fmt['row_width'] * (df.columns.size + 2)

        if tbl_fmt['width'] > tbl_fmt['MAX_WIDTH']:
            tbl_fmt['width'] = tbl_fmt['MAX_WIDTH']

        # CSS Style
        css_html = self._to_html_table(df_html, tbl_fmt)

        return(css_html)

    def _to_html_table(self, raw_html, tbl_fmt):
        'Convert raw_html to standard table html'

        css_html = self.STYL_CSS(cls=tbl_fmt['class'],
                                 style=self.TBL_STYLESIZE_FMT(**tbl_fmt),
                                 data=self.TBLE_NME % (raw_html))

        return(css_html + self.BREAK_FMT)

    def list_to_tablerow(self, my_list, idx=''):
        'Convert list to a row for html table - in any convert_to_html_table'

        #html_str = self.TBLE_ITM % idx
        html_str = ''
        for name in my_list:
            html_str += self.TBLE_ITM % name

        return(self.TBLE_ROW % html_str)

    def _to_html_list(self, items):
        'Convert dictionary of pages to a list of links'

        list_html = ''
        for name in items:
            list_html += self.LIST_FMT % name

        return(self.TYP1_FMT(name='ul') % list_html)

    def embed_image(self, path):
        'Embed image'

        encoded = open(path, 'rb').read().encode('base64').replace('\n', '')

        return '<img src="data:image/png;base64,{0}">'.format(encoded)
