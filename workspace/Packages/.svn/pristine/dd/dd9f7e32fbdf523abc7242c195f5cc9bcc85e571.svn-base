'''
Created on Jul 28, 2014

@author: Rishi.Patel
'''

import shutil
import pandas as pd
import seaborn as sns
import webgen.html
import os


class WebReport(object):
    '''
    classdocs
    '''

    def __init__(self, param={}):
        '''
        Constructor
        '''

        self._load_defaults(param)
        self.oHtml = webgen.html.ToHtml({'class': 'maxim_one'})
        
        # TODO: Clean up below
        if 'save_path' not in param.keys():
            self.save_path = ''         # Current Directory
        else:
            self.save_path = param['save_path']

    def _load_defaults(self, param):
        'Place holder command in case class is called directly'

        self.TEMPLATE_PATH = param['path']
        self.TEMPLATE_NAME = param['name']
        self.TEMPLATE_DIR = param['dir']
        self.header = param['header']

    def _make_project_dir(self, name='default'):
        'Make Project Directory'

        path = self.save_path + name + '/'

        # Check and Create HTML Folder
        if os.path.exists(path):
            print 'WARNING OVER-WRITING FILES IN DIRECTORY:\n', path
            shutil.rmtree(path)
        else:
            print 'Creating new directory:\n', path

        self.copy_content(path)

        return path

    def generate_report(self, pages, name=''):
        'Merge data into page dict, open template, write, and save'

        TEMPLATE = self._get_template()
        proj_path = self._make_project_dir(name)

        # update toc here
        self.header['SBAR1_BODY'] = self.gen_toc_links(pages)
        for page in pages:
            print 'Creaing Page: {name} of {TOTAL}'.format(name=page.NAME, TOTAL=len(pages))
            if page.TYPE == 'CONTENT':
                page.save_page(TEMPLATE, self.header, self.oHtml, proj_path)

        print 'Report Complete: '+ proj_path

    def gen_toc_links(self, pages):
        'Convert list of list/series to url'

        toc = []
        for page in pages:
            save_page_as = page.NAME
            for item in [' ', '#', '-']:
                save_page_as = save_page_as.replace(item, '_')
            if page.TYPE == 'TOC':
                toc.append('<em><b>' + save_page_as + '</b></em>')
            elif page.TYPE == 'CONTENT':
                toc.append(self.oHtml.LINK_FMT(url=save_page_as + '.html', name=page.NAME))

        toc_html = self.oHtml._to_html_list(toc)
        return toc_html

    def _get_template(self):
        'Get HTML raw header'
        print self.TEMPLATE_PATH
        try:
            TEMPLATE = open(self.TEMPLATE_PATH + self.TEMPLATE_NAME, 'r')
        except IOError:
            print 'Check that the following file+path does exist:\n' + \
            self.TEMPLATE_PATH + self.TEMPLATE_NAME + '\n'
            print 'If not correct try manually passing in the path to the HTML Template'
            raise IOError
        
        html = TEMPLATE.read()
        TEMPLATE.close()

        return html

    def copy_content(self, path):
        'Copy webpage files - images, css, etc'

        shutil.copytree(self.TEMPLATE_PATH + self.TEMPLATE_DIR, path)

class MaximIntegrated(WebReport):

    def _load_defaults(self, param):
        'Set Page Dependencies'

        self.DEBUG = False
        
        #self.TEMPLATE_PATH = r'C:\Users\Rishi.Patel\Dropbox\Software\Python\HtmlTemplates\Maxim/'
        self.TEMPLATE_PATH = webgen.__path__[0] + '\HtmlTemplates\Maxim/'
        
        if 'TEMPLATE_PATH' in param.keys():
            print 'Overwrite default template path'
            self.TEMPLATE_PATH = param['TEMPLATE_PATH']
            
        self.TEMPLATE_NAME = 'standard.html'
        self.TEMPLATE_DIR = 'standard'

        self.header = {
                       'TITLE': 'SC2200 Regression Report',
                       'SLOGAN': '',
                       'NAME': '',
                       'MAIN_BODY': 'Fill in per page',
                       'SBAR1_TITLE': 'Main Menu',
                       'SBAR1_BODY': 'Fill in with page links',
                       'SBAR2_TITLE': 'Summary',
                       'SBAR2_BODY': 'General Info',
                       'HOME': '#',
                       'DATABASE': '#',
                       'SETUP': '#',
                       'CONTACT': '#',
                       'RESOURCES': '#',
                       'ABOUT': '#',
                       }

class Page(object):

    def __init__(self, name, content=False, TYPE='CONTENT'):

        self.NAME = name
        self.TYPE = TYPE

        if not content:
            content = {}

        self.content = pd.DataFrame(index=['title', 'data', 'text'])
        self.PLOT_DIR = 'plots/'
        self.add_mulitple(content)

    def save_page(self, TEMPLATE, header, oHtml, save_path):

        tmp = self.NAME.replace(' ', '_')
        name = tmp.replace('-', '_')
        header['MAIN_BODY'] = self.convert_to_html(oHtml, save_path)
        PAGE = open(save_path + name + '.html', 'w')
        PAGE.write(TEMPLATE % header)
        PAGE.close()

    def add_mulitple(self, content):

        for key in content.keys():
            self.add(**content[key])

    def add(self, data=False, title='', text=''):

        self.content[self.content.columns.size] = [title, data, text]

    def convert_to_html(self, oHtml, save_path):

        body_html = ''
        for col in self.content.columns:
            row = self.content[col]

            if type(row['text']) == pd.DataFrame:
                html = oHtml.df_to_html(row['text'])
            elif str(row['text']) == 'embed':
                html = ''
            else:
                html = oHtml.PRGH_FMT % row['text'] + '<br>'
            
            if type(row['data']) == sns.plt.Figure:
                fig_path = self._save_figure(row, save_path)
                html += oHtml.IMAGE_FMT(w='100%', url=fig_path, h='100%')
            elif type(row['data']) == pd.DataFrame:
                html += oHtml.df_to_html(row['data'])
            elif str(row['text']) == 'embed':
                html += oHtml.embed_image(row['data'])
            elif type(row['data']) == str():
                html += oHtml.PRGH_FMT % row['data'] + '<br>'
            else:
                pass
            
            body_html += oHtml.HEAD_TP1(title=row['title'], body=html)

        return body_html

    def _save_figure(self, info, path):

        title = info['title'].replace(' ', '_')
        title = title.replace('.', '_')
        title = title.replace(':', '')
        title = title.replace('-', 'm')

        save_path = self.PLOT_DIR + title + '.png'
        info['data'].savefig(path + save_path)

        return save_path
