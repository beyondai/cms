#!/usr/bin/python
# -*- coding: utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.escape
import CouchObject
import Contest
import WebConfig
from StringIO import StringIO
from FileStorageLib import FileStorageLib

def get_task(taskname):
    for t in c.tasks:
        if t.name == taskname:
            return t
    else:
        raise KeyError("Task not found");

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class MainHandler(BaseHandler):
    def get(self):
        self.render("welcome.html",title="Titolo",header="Header",description="Descrizione",contest=c )

class LoginHandler(BaseHandler):
    def post(self):
        username = self.get_argument("username","")
        password = self.get_argument("password","")
        for u in c.users:
            if u.username == username and u.password == password:
                self.set_secure_cookie("user",self.get_argument("username"))
                break
        self.redirect("/?login_error=true")

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect("/")

class SubmissionViewHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,taskname):
        try:
            task = get_task(taskname)
        except:
            self.write("Task not found: "+taskname)
            return
        subm=[]
        for s in c.submissions:
            if s.user.username == self.current_user and s.task.name == task.name:
                subm.append(s)
        self.render("submission.html",submissions=subm, task = task)
class TaskViewHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,taskname):
        try:
            task = get_task(taskname)
        except:
            self.write("Task not found: "+taskname)
            return
            #raise tornado.web.HTTPError(404)
        self.render("task.html",task=task);

class TaskStatementViewHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, taskname):
        try:
            task = get_task(taskname)
        except:
            self.write("Task not found: "+taskname)
        statementFile = StringIO()
        FSL = FileStorageLib()
        FSL.get_file(task.statement, statementFile)
        self.set_header("Content-Type", "application/pdf")
        self.write(statementFile.getvalue())
        statementFile.close()

handlers = [
            (r"/",MainHandler),
            (r"/login",LoginHandler),
            (r"/logout",LogoutHandler),
            (r"/submissions/([a-zA-Z0-9-]+)",SubmissionViewHandler),
            (r"/tasks/([a-zA-Z0-9-]+)",TaskViewHandler),
            (r"/task_statement/([a-zA-Z0-9-]+)",TaskStatementViewHandler)
           ]
                                       
application = tornado.web.Application( handlers, **WebConfig.parameters)

c = CouchObject.from_couch("sample_contest")

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888);
    tornado.ioloop.IOLoop.instance().start()
