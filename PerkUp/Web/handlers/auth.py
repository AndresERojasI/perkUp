from . import base
import tornado
import web_core
import os, uuid
import simplejson as json
from web_core import models
import pprint
from sqlalchemy import inspect

session_opts = {
    'session.cookie_expires': True
}

__UPLOADS__ = "static/uploads/"
class AuthHandler(base.BaseHandler):
    def get(self):
        self.clear_cookie('user')
        return self.render("auth/login.html", errors=False)

    def post(self):
        session = self.get_session()
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)

        try:
            user = session.query(web_core.models.User) \
                .filter(web_core.models.User.username == username, web_core.models.User.password == password) \
                .first()

            if user == None:
                return self.render("auth/login.html", errors="Login failed, please check your credentials andd try again")
            else:
                self.set_secure_cookie('user', json.dumps({
                    'name' : user.name,
                    'last_name' : user.last_name,
                    'email' : user.email,
                    'username' : user.username,
                    'avatar' : user.avatar,
                    'organization': {
                        'id' : user.organization_user.id,
                        'name' : user.organization_user.name,
                        'logo' : user.organization_user.logo,
                        'address' : user.organization_user.address,
                        'unique_domain' : user.organization_user.unique_domain,
                        'lat_lang' : user.organization_user.lat_lang
                    }
                }))
                self.redirect("/")
        except ValueError:
            return self.render("auth/login.html", errors="Login failed, there was an unexpected error, please try again in a moment")

class OrganizationCreationHandler(base.BaseHandler):
    def get(self):
        self.clear_cookie('company_data')
        return self.render("auth/org_create.html", errors=False)

    def post(self):
        #validates the basic required fields
        organization_name = self.get_argument('org_name', None)
        org_subdomain = self.get_argument('org_subdomain', None)
        org_logo = self.request.files['org_logo']
        org_address = self.get_argument('org_address', None)
        lat_lang = self.get_argument('lat_lang', None)

        if lat_lang != None:
            lat_lang = lat_lang.split('|')

        #self.finish(json.dumps(lat_lang))
        if organization_name == None or org_subdomain == None:
            return self.render("auth/org_create.html",
                               errors="There are errors in this fom please check them and try again")

        if org_logo != None:
            fileinfo = org_logo[0]
            fname = fileinfo['filename']
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            org_logo = cname
            fh = open(__UPLOADS__ + 'company_logos/' + cname, 'w')
            fh.write(fileinfo['body'])

        self.set_secure_cookie('company_data', json.dumps({
            'org_name': organization_name,
            'org_subdomain': org_subdomain,
            'org_logo': org_logo,
            'org_address': org_address,
            'latittude_long': lat_lang,
        }))

        self.redirect('/')



class CreateAdminHandler(base.BaseHandler):
    def get(self):
        return self.render("auth/admin_create.html", errors=False)

    def post(self):
        #create an organization and assign the user as an administrator
        org_data = self.get_secure_cookie('company_data')

        if not org_data:
            self.redirect('/organization/create')

        org_data = json.loads(org_data)

        admin_email = self.get_argument('admin_email', None)
        admin_email_confirm = self.get_argument('admin_email_confirm', None)

        if admin_email != admin_email_confirm:
            return self.render("auth/admin_create.html",
                               errors="The email and the confirmation does not match, please fix it.")

        admin_avatar = self.request.files['admin_avatar']
        if admin_avatar != None:
            fileinfo = admin_avatar[0]
            fname = fileinfo['filename']
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            admin_avatar = cname
            fh = open(__UPLOADS__ + 'user_avatars/' + cname, 'w')
            fh.write(fileinfo['body'])

        admin_name = self.get_argument('admin_name', None)
        admin_last_name = self.get_argument('admin_last_name', None)
        admin_user = self.get_argument('admin_user', None)
        admin_password = self.get_argument('admin_password', None)

        try:
            #we have gathered all the data needed, so now we create everything.
            org = models.Organization(
                name=org_data['org_name'],
                address=org_data['org_address'],
                unique_domain=org_data['org_subdomain'],
                lat_lang=','.join(org_data['latittude_long']),
                logo=org_data['org_logo']
            )

            session = self.get_session()
            session.add(org)

            usr = models.User(
                name=admin_name,
                last_name = admin_last_name,
                email = admin_email,
                password = admin_password,
                username = admin_user,
                avatar=admin_avatar,
                organization_user=org
            )

            session.add(usr)
            session.commit()
        except ValueError:
            return self.render("auth/org_create.html",
                               errors="There was an error when trying to create this organization, please try again in a moment")



class ValidateSubdomain(base.BaseHandler):
    def get(self):
        org_subdomain = self.get_argument('org_subdomain', None)
        if org_subdomain != None:
            session = self.get_session()
            count = session.query(web_core.models.Organization)\
                .filter(web_core.models.Organization.unique_domain == org_subdomain)\
                .count()
            if count == 0:
                self.set_status(200)
                self.write('valid')
            else:
                self.set_status(404)
                self.write('taken')
        else:
            self.set_status(404)
            self.write('wrong call')
