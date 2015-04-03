from jinja2 import Environment, FileSystemLoader, FileSystemBytecodeCache

#----------------------------------------------------------
# http://jinja.pocoo.org/docs/api/
#----------------------------------------------------------
def guess_autoescape(template_name):
    if template_name is None or '.' not in template_name:
        return False
    ext = template_name.rsplit('.', 1)[1]
    return ext in ('html', 'htm', 'xml', 'tmpl')


#----------------------------------------------------------
# DAYS AGO
#----------------------------------------------------------
def days_ago(closing_date):

    from datetime import datetime

    try :
        date_now = datetime.now().date()
        date_end = datetime.strptime(closing_date, '%Y-%m-%d').date()

        last = date_end - date_now

        return last.days

    except :

        return closing_date

#----------------------------------------------------------
# from flask import render_template
# https://flask-docs-ja.readthedocs.org/en/latest/unicode/#id1
#----------------------------------------------------------
class jinja2_render(object):

    #----------------------------------------------------------
    # INIT
    #----------------------------------------------------------
    def __init__(self):

        self.file_encoding  = 'utf-8'
        self.template_dir   = '/tmp'
        self.template_c_dir = '/tmp/cache'

    #----------------------------------------------------------
    # SET FILE ENCODING
    #----------------------------------------------------------
    def set_file_encoding(encoding):

        self.file_encoding = encoding

    #----------------------------------------------------------
    # SET TEMPLATE DIR
    #----------------------------------------------------------
    def set_template_dir(template_dir):

        self.template_dir = template_dir

    #----------------------------------------------------------
    # SET TEMPLATE CACHE DIR
    #----------------------------------------------------------
    def set_template_c_dir(template_c_dir):

        self.template_c_dir = template_c_dir

    #----------------------------------------------------------
    # RENDER TEMPLATE
    #----------------------------------------------------------
    def render_template(self, template_file, **kwargs):

        #--- set template dir
        _loder = FileSystemLoader(self.template_dir, encoding=self.file_encoding)

        if self.template_c_dir:
            #--- set template and cache
            _cache = FileSystemBytecodeCache(directory=self.template_c_dir, pattern='%s.cache')
            env    = Environment(loader=_loder,
                                 bytecode_cache=_cache,
                                 autoescape=guess_autoescape,
                                 extensions=['jinja2.ext.autoescape'])
        else :
            #--- set template not cache
            env    = Environment(loader=_loder,
                                 autoescape=guess_autoescape,
                                 extensions=['jinja2.ext.autoescape'])



        #--- jinja2 add custom function
        # http://stackoverflow.com/questions/6036082/call-a-python-function-from-jinja2
        from flask import url_for
        env.globals.update(url_for=url_for)
        env.globals.update(url_for=url_for, days_ago=days_ago)

        tmpl   = env.get_template(template_file)

        return tmpl.render(kwargs)
