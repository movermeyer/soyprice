from application import app
from database import db
from models import Change, Variable
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


class ChangeView(ModelView):
    column_select_related_list = ('variable', )
    column_searchable_list = ('moment', 'value', 'variable.name')
    column_filters = ('moment', 'value', 'variable.name')


class VariableView(ModelView):
    column_searchable_list = ('name', 'description', 'reference')
    column_filters = ('name', )


admin = Admin(app, name='soyprice', template_mode='bootstrap3')
admin.add_view(ChangeView(Change, db.session))
admin.add_view(VariableView(Variable, db.session))
