from flask               import Blueprint, request, redirect, url_for 
from app_sample.database import db_session
from app_sample.models   import SampleTable

blueprint = Blueprint("sample", __name__, static_folder='static', static_url_path='/static')

#----------------------------------------------------------
# USE jinja2 (original wrapper)
#----------------------------------------------------------
import config
from libs.jinja2_wrapper import jinja2_render
jinja2 = jinja2_render()
jinja2.file_encoding  = config.app_sample.CHARSET
jinja2.template_dir   = config.app_sample.TEMPLATE_D
jinja2.template_c_dir = config.app_sample.TEMPLATE_C

#----------------------------------------------------------
# remove database sessions at the end of the request
#----------------------------------------------------------
@blueprint.teardown_app_request
def shutdown_session(exception=None):

    db_session.remove()

#----------------------------------------------------------
# 404 ERROR
#----------------------------------------------------------
@blueprint.app_errorhandler(404)
def not_found(error):
    return jinja2.render_template('404.html'), 404

#----------------------------------------------------------
# 500 ERROR
#----------------------------------------------------------
@blueprint.app_errorhandler(500)
def handle_500(error):
    return jinja2.render_template('500.html'), 500

#----------------------------------------------------------
# SELECT
#----------------------------------------------------------
@blueprint.route('/', methods=['GET'])
def sample_top():

    template_file = 'index.html'
    data          = SampleTable.query.all()
    static        = {"url_for('.static', filename='css/sample.css')":url_for('.static', filename='css/sample.css'),
                     "url_for('.static', filename='js/sample.js')"  :url_for('.static', filename='js/sample.js'),
                     "url_for('.static', filename='img/sample.png')":url_for('.static', filename='img/sample.png'),
                     "url_for('static', filename='js/sample.js')"   :url_for('.static', filename='js/sample.js'),
                     'blueprint.static_folder'                      : blueprint.static_folder,
                     'blueprint.static_url_path'                    : blueprint.static_url_path,
                     'blueprint.url_prefix'                         : blueprint.url_prefix,
                     }
    return jinja2.render_template(template_file, data=data, static=static)

#----------------------------------------------------------
# INSERT
#----------------------------------------------------------
@blueprint.route('/new', methods=['POST'])
def sample_new():

    if request.method == 'POST':

        from datetime import datetime

        tbl_obj         = SampleTable()
        tbl_obj.title   = request.form.get('title',  '-- no data --')
        tbl_obj.message = request.form.get('message','-- no data --')
        tbl_obj.date    = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db_session.add(tbl_obj)
        db_session.commit()

    return redirect(url_for('.sample_top'))

#----------------------------------------------------------
# UPDATE
#----------------------------------------------------------
@blueprint.route('/update/<int:update_id>', methods=['POST'])
def sample_update(update_id):

    if request.method == 'POST':

        from datetime import datetime

        tbl_obj         = db_session.query(SampleTable).get(update_id)
        tbl_obj.title   = request.form.get('title',   '-- no data--')
        tbl_obj.message = request.form.get('message', '-- no data--')
        tbl_obj.date    = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db_session.commit()

    return redirect(url_for('.sample_top'))

#----------------------------------------------------------
# DELETE
#----------------------------------------------------------
@blueprint.route('/del/<int:delete_id>', methods=['GET'])
def sample_del(delete_id):

    tbl_obj = db_session.query(SampleTable).get(delete_id)

    db_session.delete(tbl_obj)
    db_session.commit()

    return redirect(url_for('.sample_top'))

#----------------------------------------------------------
# TEST
#----------------------------------------------------------
@blueprint.route('/test')
def sample_test():

    return 'Hello World!'
