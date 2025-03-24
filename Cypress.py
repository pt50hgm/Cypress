import pygame
import sys

from enum import Enum

"""
App (Mock functionality for app without GUI or function calls)
Page, notifications/popup
Login(), SetPage(newPage), SearchReports(), Subscribe(), FindSimilarReports(report)
"""
# class AppPagesEnum(Enum):
#     LOGIN, HOME, SEARCH, VIEW_REPORT = range(4)
class App:
    def __init__(self):
        self.usersDB = Database()
        self.reportsDB = Database()
        self.userId = None
        self.reportId = None
    
    def QueryUserIdFromLogin(self, username, password):
        users = self.usersDB.Read()
        for userId in users:
            user = users[userId]
            if user.username == username and user.password == password:
                return userId
        return None
    
    def CreateAccount(self, username, password):
        userId = self.QueryUserIdFromLogin(username, password)
        if userId != None:
            return False
        newUser = User(username, password)
        self.usersDB.Create(newUser.id, newUser)
        self.userId = newUser.id
        return True
    
    def Login(self, username, password):
        userId = self.QueryUserIdFromLogin(username, password)
        if userId == None:
            return False
        self.userId = userId
        return True
    def SearchReports(self):
        return list(self.reportsDB.Read().values())
    def FilterReports(self):
        return list(self.reportsDB.Read().values())
    def QuerySimilarReports(self, report):
        reports = self.reportsDB.Read()
        for reportId in reports:
            report = reports[reportId]


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
    def Read(self, id=None):
        if id == None:
            return self.data
        return self.data[id]
    def Delete(self, id):
        del self.data[id]
    def QueryEquals(self, equalFunc, value):
        pass


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
    nextId = 0
    def __init__(self, username, password):
        self.id = User.nextId
        User.nextId += 1
        
        self.username = username
        self.password = password

        self.status = UserStatusEnum.ACTIVE
        self.default_location = ()
        self.is_subscribed = False
    def ViewReport(self, report):
        pass
    def SetSubscribe(self, is_subscribed):
        self.is_subscribed = is_subscribed
    

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
    nextId = 0
    def __init__(self, location, type, description, user, time_submitted, department):
        self.id = Report.nextId
        Report.nextId += 1

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
    def IsSimilar(self, otherReport):
        # Add location and time proximity
        return (self.type == otherReport.type
            and self.department == otherReport.department)

"""
Resolution Action
date, description
"""
class ResolutionAction:
    def __init__(self, date, description):
        self.date = date
        self.description = description


# ---------- Utility Function for Drawing Text with a Box ----------
def DrawTextBox(surface, text, font, pos, text_color=pygame.Color('black'), box_color=pygame.Color('white'), padding=5):
    """Render text with a background box for better legibility."""
    if not text:
        return
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(topleft=pos)
    box_rect = pygame.Rect(text_rect.left - padding, text_rect.top - padding,
                           text_rect.width + 2 * padding, text_rect.height + 2 * padding)
    pygame.draw.rect(surface, box_color, box_rect)
    surface.blit(text_surface, text_rect)

# ---------- Utility Classes ----------
class InputBox:
    def __init__(self, x, y, w, h, text='', masked=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.text = text
        self.masked = masked
        self.txt_surface = FONT.render(self.GetDisplayText(), True, pygame.Color('black'))
        self.active = False

    def GetDisplayText(self):
        return '*' * len(self.text) if self.masked else self.text

    def HandleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                pass
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            self.txt_surface = FONT.render(self.GetDisplayText(), True, pygame.Color('black'))

    def Update(self):
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def Draw(self, screen):
        pygame.draw.rect(screen, pygame.Color('white'), self.rect)
        self.txt_surface = FONT.render(self.GetDisplayText(), True, pygame.Color('black'))
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

class Button:
    def __init__(self, text, x, y, w, h, callback):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback
        self.txt_surface = FONT.render(text, True, pygame.Color('white'))
        self.color = pygame.Color('gray')

    def Draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_rect = self.txt_surface.get_rect(center=self.rect.center)
        screen.blit(self.txt_surface, text_rect)

    def HandleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()

# ---------- Scene Management ----------
class SceneBase:
    global app, scene_manager

    def __init__(self):
        pass

    def ProcessEvents(self, events):
        pass

    def Update(self):
        pass

    def Render(self, screen):
        pass
    

class SceneManager:
    def __init__(self):
        pass

    def SetScene(self, next_scene):
        self.active_scene = next_scene
    
    def Run(self):
        while self.active_scene is not None:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.active_scene.ProcessEvents(events)
            self.active_scene.Update()
            self.active_scene.Render(screen)

            pygame.display.flip()
            clock.tick(30)

# ---------- Scenes ----------
class LoginScene(SceneBase):
    def __init__(self):
        super().__init__()
        self.username_box = InputBox(300, 200, 200, 32)
        self.password_box = InputBox(300, 250, 200, 32, masked=True)
        self.message = ""
        self.failed_attempts = 0

        self.login_button = Button("Login", 350, 300, 100, 40, self.TryLogin)

    def TryLogin(self):
        username = self.username_box.text.strip()
        password = self.password_box.text.strip()
        valid_login = app.Login(username, password)
        if valid_login:
            self.message = "Login successful!"
            scene_manager.SetScene(ReportScene(username))
        else:
            self.failed_attempts += 1
            self.message = "Invalid username or password."
            if self.failed_attempts >= 3:
                self.message = "Too many failed attempts. Account locked for 15 minutes."
                self.username_box.text = ""
                self.password_box.text = ""
        self.username_box.txt_surface = FONT.render(self.username_box.GetDisplayText(), True, pygame.Color('black'))
        self.password_box.txt_surface = FONT.render(self.password_box.GetDisplayText(), True, pygame.Color('black'))

    def ProcessEvents(self, events):
        for event in events:
            self.username_box.HandleEvent(event)
            self.password_box.HandleEvent(event)
            self.login_button.HandleEvent(event)

    def Update(self):
        self.username_box.Update()
        self.password_box.Update()

    def Render(self, screen):
        if bg_image:
            screen.blit(bg_image, (0, 0))
        else:
            screen.fill(pygame.Color('white'))
        title_text = "Login"
        title_surface = BIG_FONT.render(title_text, True, pygame.Color('black'))
        title_rect = title_surface.get_rect(center=(WIDTH // 2, 100))
        DrawTextBox(screen, title_text, BIG_FONT, (title_rect.x, title_rect.y))
        self.username_box.Draw(screen)
        self.password_box.Draw(screen)
        self.login_button.Draw(screen)
        DrawTextBox(screen, "Username:", FONT, (120, 205))
        DrawTextBox(screen, "Password:", FONT, (120, 255))
        if self.message:
            DrawTextBox(screen, self.message, FONT, (300, 350), text_color=pygame.Color('red'))

class ReportScene(SceneBase):
    def __init__(self, username):
        super().__init__()
        self.username = username
        try:
            self.map_surface = pygame.image.load("toronto_map.png").convert()
            self.map_surface = pygame.transform.scale(self.map_surface, (600, 400))
        except Exception as e:
                print("Error loading Toronto map:", e)
                self.map_surface = pygame.Surface((600, 400))
                self.map_surface.fill(pygame.Color('lightgray'))
        self.report_info = ""
        self.selected_location = None

        self.problem_box = InputBox(100, 450, 200, 32)
        self.desc_box = InputBox(350, 450, 300, 32)

        self.submit_button = Button("Submit Report", 350, 500, 150, 40, self.SubmitReport)
        self.message = ""

    def SubmitReport(self):
        if self.selected_location is None:
            self.message = "Please select a location on the map."
            return
        if self.problem_box.text.strip() == "":
            self.message = "Please select a problem type."
            return
        if self.desc_box.text.strip() == "":
            self.message = "Please provide a description."
            return

        self.report_info = f"Report by {self.username}: {self.problem_box.text}, {self.desc_box.text} at {self.selected_location}"
        self.message = "Report submitted successfully!"
        self.problem_box.text = ""
        self.desc_box.text = ""
        self.problem_box.txt_surface = FONT.render("", True, pygame.Color('black'))
        self.desc_box.txt_surface = FONT.render("", True, pygame.Color('black'))
        self.selected_location = None

    def ProcessEvents(self, events):
        for event in events:
            self.problem_box.HandleEvent(event)
            self.desc_box.HandleEvent(event)
            self.submit_button.HandleEvent(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                map_rect = pygame.Rect(100, 30, 600, 400)
                if map_rect.collidepoint(event.pos):
                    x, y = event.pos[0] - 100, event.pos[1] - 30
                    self.selected_location = (x, y)
                    self.message = f"Location selected: {self.selected_location}"

    def Update(self):
        self.problem_box.Update()
        self.desc_box.Update()

    def Render(self, screen):
        if bg_image:
            screen.blit(bg_image, (0, 0))
        else:
            screen.fill(pygame.Color('white'))
        title_text = "Report a Problem"
        title_surface = BIG_FONT.render(title_text, True, pygame.Color('black'))
        title_rect = title_surface.get_rect(center=(WIDTH // 2, 20))
        DrawTextBox(screen, title_text, BIG_FONT, (title_rect.x, title_rect.y))
        map_rect = self.map_surface.get_rect(center=(WIDTH // 2, 270))  # or try 280 if still tight
        screen.blit(self.map_surface, map_rect.topleft)
        if self.selected_location:
            marker_pos = (100 + self.selected_location[0], 30 + self.selected_location[1])
            pygame.draw.circle(screen, pygame.Color('red'), marker_pos, 5)
        DrawTextBox(screen, "Problem Type:", FONT, (100, 410))
        DrawTextBox(screen, "Description:", FONT, (350, 410))
        self.problem_box.Draw(screen)
        self.desc_box.Draw(screen)
        self.submit_button.Draw(screen)
        if self.message:
            DrawTextBox(screen, self.message, FONT, (100, 550), text_color=pygame.Color('blue'))
        if self.report_info:
            DrawTextBox(screen, self.report_info, FONT, (100, 580), text_color=pygame.Color('green'))

# ---------- Main ----------
def main():
    global scene_manager
    scene_manager.SetScene(start_scene)
    scene_manager.Run()


pygame.init()

# ---------- Global Settings ----------
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cypress System Prototype")
clock = pygame.time.Clock()

# ---------- Fonts ----------
FONT = pygame.font.SysFont("Arial", 24)
BIG_FONT = pygame.font.SysFont("Arial", 48)


app = App()
# ---------- Dummy USERS Dictionary for Login ----------
app.CreateAccount("admin", "admin")
app.CreateAccount("user", "password")

start_scene = LoginScene()
# start_scene = ReportScene("user")
scene_manager = SceneManager()

# ---------- Load Background Image ----------
try:
    bg_image = pygame.image.load("background.png").convert()
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
except Exception as e:
    print("Error loading background image:", e)
    bg_image = None

# user1 = User("Username1", "Password1")
# user2 = User("Username2", "Password2")
# report1 = Report("Location1", "Type1", "Description1", user1, "insert time", "Department1")
# report2 = Report("Location2", "Type2", "Description2", user2, "insert time", "Department2")
# users = Database()
# users.Create(user1.id, user1)
# users.Create(user2.id, user2)
# print(user1.id, report1.id, user2.id, report2.id)

if __name__ == '__main__':
    main()