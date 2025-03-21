# import Pygame
from enum import Enum

"""
App (Mock functionality for app without GUI or function calls)
Page, notifications/popup
Login(), SetPage(newPage), SearchReports(), Subscribe(), FindSimilarReports(report)
"""
class App:
    def __init__(self):
        self.page = ""
        self.notifs = []
    def Login(self):
        pass
    def SetPage(self, newPage):
        self.page = newPage
    def SearchReports(self):
        pass
    def Subscribe(self):
        pass
    def FindSimilarReports(self, report):
        pass


"""
Database Stub
Map of ID -> Data
Create(id, value), Read(), Read(id), Update(id, newValue), Delete(id)
"""
class Database:
    def __init__(self):
        self.data = {}
    def Create(self, id, value):
        self.data[id] = value
    def Update(self, id, value):
        self.data[id] = value
    def Read(self):
        return self.data
    def Read(self, id):
        return self.data[id]
    def Delete(self, id):
        del self.data[id]


"""
User
ID, Username, password
Account status (Active, suspended, banned)
home/default_location (map will be centered around this location)
is_subscribed (boolean)
ViewReport(reportId)
"""
class UserStatusEnum(Enum):
    ACTIVE, SUSPENDED, BANNED = range(3)
class User:
    def __init__(self, id):
        self.id = id
        self.status = UserStatusEnum.ACTIVE
        self.default_location = ()
        self.is_subscribed = False
        print("DSF")
    def ViewReport(self, report):
        pass

"""
Employee (User)
Department
SuspendUser(user), BanUser(user)
ForwardReport(), CloseReport()
"""
class Employee(User):
    def __init__(self, id, department):
        User.__init__(self, id)
        self.department = department
    def SuspendUser(user):
        user.SetStatus(UserStatusEnum.SUSPENDED)
    def BanUser(user):
        user.SetStatus(UserStatusEnum.BANNED)
    def ForwardReport(report, department):
        report.SetStatus(ReportStatusEnum.SUBMITTED)
        # Insert report forwarding
    def CloseReport(report):
        report.SetStatus(ReportStatusEnum.RESOLVED)


"""
Problem Report
ID, location, type (optional), description (text only, for now), user, time_submitted, department, and sequence of resolution actions taken so far
status
IsValid(), ViewReport(), FlagAsDuplicate()
Employee only: ForwardReport(), CloseReport(), FlagAsFalse(), AddResolutionAction(newAction)
"""
class ReportStatusEnum(Enum):
    DUPLICATE, FALSE, CREATED, SUBMITTED, REVIEWED, IN_PROGRESS, RESOLVED = range(7)
class Report:
    def __init__(self, id, location, type, description, user, time_submitted, department):
        self.id = id
        self.location = location
        self.type = type
        self.description = description
        self.user = user
        self.time_submitted = time_submitted
        self.department = department
        self.resolution_actions = []

        self.status = ReportStatusEnum.CREATED
    def SetStatus(self, newStatus):
        self.status = newStatus
    def IsValid(self):
        pass
    def FlagAsDuplicate(self):
        self.status = ReportStatusEnum.DUPLICATE
        # Insert actions on user
    def FlagAsFalse(self):
        self.status = ReportStatusEnum.FALSE
        # Insert actions on user
    def AddResolutionAction(self, newAction):
        self.resolution_actions.append(newAction)


"""
Resolution Action
date, description
"""
class ResolutionAction:
    def __init__(self, date, description):
        self.date = date
        self.description = description
