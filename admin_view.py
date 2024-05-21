from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin import AdminIndexView, expose
from flask_ckeditor import CKEditorField
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask import Flask, request, redirect, render_template, url_for, flash, abort
from database import User, db


login_manager = LoginManager()
# user = db.session.execute(db.select(User).where(User.email == 'lawrence.nno@gmail.com')).scalar()


@login_manager.user_loader
def user_loader(user_id):
    return db.session.execute(db.select(User).where(User.id == user_id)).scalar()


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        if not current_user.is_admin and current_user.email != 'lawrence.nno@gmail.com':
            return redirect(url_for('index'))
        return super(MyAdminIndexView, self).index()


class ProductView(ModelView):
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'desc': CKEditorField
    }
    column_searchable_list = ['name', 'price', 'desc', 'image']
    column_filters = ['price']
    column_editable_list = ['price', 'name']

    def is_accessible(self):
        return current_user.is_authenticated and (
                    current_user.is_admin or current_user.email == 'lawrence.nno@gmail.com')

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


class OrderView(ModelView):
    column_searchable_list = ['reference', 'status']
    column_editable_list = ['status']

    def is_accessible(self):
        return current_user.is_authenticated and (current_user.is_admin or current_user.email == 'lawrence.nno@gmail.com')

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


class UserView(ModelView):
    column_searchable_list = ['email', 'country']
    column_filters = ['country']
    column_exclude_list = ['password']

    def is_accessible(self):
        return current_user.is_authenticated and (
                    current_user.is_admin or current_user.email == 'lawrence.nno@gmail.com')

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


class RestrictedFileAdmin(FileAdmin):
    def is_accessible(self):
        return current_user.is_authenticated and (current_user.is_admin or current_user.email == 'lawrence.nno@gmail.com')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))