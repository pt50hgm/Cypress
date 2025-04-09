import pygame
import sys
import datetime

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
            otherReport = reports[reportId]
            if report.IsSimilar(otherReport):
                return report
        return None
    def QueryDuplicateReports(self, report):
        reports = self.reportsDB.Read()
        for reportId in reports:
            otherReport = reports[reportId]
            if report.IsDuplicate(otherReport):
                return report
        return None
    def SubmitReport(self, report):
        self.reportsDB.Create(report.id, report)
        return True



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
        return (
            self.type == otherReport.type and
            (self.location[0] - otherReport.location[0])**2 + (self.location[1] - otherReport.location[1])**2 < 30**2 and
            self.department == otherReport.department
        )
    def IsDuplicate(self, otherReport):
        return (
            self.IsSimilar(otherReport) and
            self.user.id == otherReport.user.id
        )
"""
Resolution Action
date, description
"""
class ResolutionAction:
    def __init__(self, date, description):
        self.date = date
        self.description = description


# ---------- Utility Function for Drawing Text with a Box ----------
def DrawTextBox(surface, text, font, pos, centered=False, text_color=pygame.Color('black'), box_color=pygame.Color('white'), padding=5):
    """Render text with a background box for better legibility."""
    if not text:
        return
    text_surface = font.render(text, True, text_color)
    if centered:
        text_rect = text_surface.get_rect(center=pos)
    else:
        text_rect = text_surface.get_rect(topleft=pos)
    box_rect = pygame.Rect(text_rect.left - padding, text_rect.top - padding,
                           text_rect.width + 2 * padding, text_rect.height + 2 * padding)
    # pygame.draw.rect(surface, box_color, box_rect)
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
        self.colorVal = 225

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
        if self.active or self.rect.collidepoint(pygame.mouse.get_pos()):
            self.colorVal += (255 - self.colorVal) / 6
        else:
            self.colorVal += (225 - self.colorVal) / 6
        colorVal = round(self.colorVal)
        pygame.draw.rect(screen, pygame.Color(colorVal, colorVal, colorVal), self.rect)
        self.txt_surface = FONT.render(self.GetDisplayText(), True, pygame.Color('black'))
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

class Button:
    def __init__(self, text, x, y, w, h, callback):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback
        self.txt_surface = FONT.render(text, True, pygame.Color('white'))
        self.colorVal = 100
        self.color = pygame.Color(0, 50, 100)

    def Draw(self, screen):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.colorVal += (200 - self.colorVal) / 6
        else:
            self.colorVal += (100 - self.colorVal) / 6
        self.color = pygame.Color(0, 50, round(self.colorVal))
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
            scene_manager.SetScene(ReportScene())
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
        bg_surface = pygame.Surface((WIDTH, HEIGHT))
        bg_surface.set_alpha(150)
        bg_surface.fill((255,255,255))
        screen.blit(bg_surface, (0, 0))
        title_text = "Cypress App"
        title_surface = BIG_FONT.render(title_text, True, pygame.Color('black'))
        title_rect = title_surface.get_rect(center=(WIDTH // 2, 100))
        DrawTextBox(screen, title_text, BIG_FONT, (title_rect.x, title_rect.y))
        self.username_box.Draw(screen)
        self.password_box.Draw(screen)
        self.login_button.Draw(screen)
        DrawTextBox(screen, "Username:", FONT, (120, 205))
        DrawTextBox(screen, "Password:", FONT, (120, 255))
        if self.message:
            DrawTextBox(screen, self.message, FONT, (WIDTH // 2, 360), centered=True, text_color=pygame.Color('red'))

class ReportScene(SceneBase):
    def __init__(self):
        super().__init__()
        try:
            self.map_surface = pygame.image.load("toronto_map.png").convert()
            self.map_surface = pygame.transform.scale(self.map_surface, (450, 300))
        except Exception as e:
            print("Error loading Toronto map:", e)
            self.map_surface = pygame.Surface((450, 300))
            self.map_surface.fill(pygame.Color('lightgray'))
        self.selected_location = None

        self.problem_box = InputBox(300, 420, 200, 32)
        self.desc_box = InputBox(300, 460, 300, 32)

        self.submit_button = Button("Submit", (WIDTH - 100) // 2, 500, 100, 40, self.SubmitReport)
        self.search_button = Button("Search", 30, 235, 100, 40, self.GoToSearch)
        self.sign_out_button = Button("Sign Out", 30, 285, 100, 40, self.GoToLogin)

        self.message = ""

    def SubmitReport(self):
        location = self.selected_location
        problem_type = self.problem_box.text.strip()
        description = self.desc_box.text.strip()
        if location is None:
            self.message = "Please select a location on the map."
            return
        if problem_type == "":
            self.message = "Please select a problem type."
            return
        if description == "":
            self.message = "Please provide a description."
            return

        user = app.usersDB.Read(app.userId)
        now = datetime.datetime.now()
        report = Report(location, problem_type, description, user, now, "TBD")
        duplicate = app.QueryDuplicateReports(report)
        similar = app.QuerySimilarReports(report)

        if duplicate != None:
            self.message = "A duplicate report already exists."
            return
        if similar != None:
            self.message = "A similar report exists."
            return

        app.SubmitReport(report)

        self.message = "Report submitted successfully!"
        self.problem_box.text = ""
        self.desc_box.text = ""
        self.problem_box.txt_surface = FONT.render("", True, pygame.Color('black'))
        self.desc_box.txt_surface = FONT.render("", True, pygame.Color('black'))
        self.selected_location = None

    def GoToSearch(self):
        scene_manager.SetScene(SearchScene())
    def GoToLogin(self):
        scene_manager.SetScene(LoginScene())

    def ProcessEvents(self, events):
        for event in events:
            self.problem_box.HandleEvent(event)
            self.desc_box.HandleEvent(event)
            self.submit_button.HandleEvent(event)
            self.search_button.HandleEvent(event)
            self.sign_out_button.HandleEvent(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                map_rect = self.map_surface.get_rect(center=(WIDTH // 2, 250))
                if map_rect.collidepoint(event.pos):
                    mapX, mapY = map_rect.topleft
                    x, y = event.pos[0] - mapX, event.pos[1] - mapY
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
        bg_surface = pygame.Surface((WIDTH, HEIGHT))
        bg_surface.set_alpha(150)
        bg_surface.fill((255,255,255))
        screen.blit(bg_surface, (0, 0))
        title_text = "Report a Problem"
        title_surface = BIG_FONT.render(title_text, True, pygame.Color('black'))
        title_rect = title_surface.get_rect(center=(WIDTH // 2, 50))
        DrawTextBox(screen, title_text, BIG_FONT, (title_rect.x, title_rect.y))
        map_rect = self.map_surface.get_rect(center=(WIDTH // 2, 250))
        map_border_rect = pygame.Surface((450+10, 300+10)).get_rect(center=(WIDTH // 2, 250))
        mapX, mapY = map_rect.topleft
        pygame.draw.rect(screen, pygame.Color(0, 50, 100), map_border_rect)
        screen.blit(self.map_surface, (mapX, mapY))
        if self.selected_location:
            marker_pos = (mapX + self.selected_location[0], mapY + self.selected_location[1])
            pygame.draw.circle(screen, pygame.Color('red'), marker_pos, 5)
        DrawTextBox(screen, "Problem Type:", FONT, (100, 420+5))
        DrawTextBox(screen, "Description:", FONT, (100, 460+5))
        self.problem_box.Draw(screen)
        self.desc_box.Draw(screen)
        self.submit_button.Draw(screen)
        self.search_button.Draw(screen)
        self.sign_out_button.Draw(screen)
        if self.message:
            DrawTextBox(screen, self.message, FONT, (100, 550), text_color=pygame.Color('blue'))

class SearchScene(SceneBase):
    def __init__(self):
        super().__init__()
        try:
            self.map_surface = pygame.image.load("toronto_map.png").convert()
            self.map_surface = pygame.transform.scale(self.map_surface, (450, 300))
        except Exception as e:
            print("Error loading Toronto map:", e)
            self.map_surface = pygame.Surface((450, 300))
            self.map_surface.fill(pygame.Color('lightgray'))

        self.reports = app.SearchReports()
        self.message = ""
        self.back_button = Button("Back", (WIDTH - 150) // 2, 420, 150, 40, self.GoBack)

    def GoBack(self):
        scene_manager.SetScene(ReportScene())

    def ProcessEvents(self, events):
        for event in events:
            self.back_button.HandleEvent(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the click was inside the map
                map_rect = self.map_surface.get_rect(center=(WIDTH // 2, 250))
                if map_rect.collidepoint(event.pos):
                    mapX, mapY = map_rect.topleft
                    map_click = (event.pos[0] - mapX, event.pos[1] - mapY)
                    
                    # Check if any report marker is close enough
                    for report in self.reports:
                        if report.location:
                            rx, ry = report.location
                            if (rx - map_click[0])**2 + (ry - map_click[1])**2 < 15**2:
                                scene_manager.SetScene(ViewReportScene(report))
                                return

                    self.message = "No report selected. Click closer to a marker."

    def Update(self):
        pass

    def Render(self, screen):
        if bg_image:
            screen.blit(bg_image, (0, 0))
        else:
            screen.fill(pygame.Color('white'))
        bg_surface = pygame.Surface((WIDTH, HEIGHT))
        bg_surface.set_alpha(150)
        bg_surface.fill((255,255,255))
        screen.blit(bg_surface, (0, 0))

        # Draw the title
        DrawTextBox(screen, "Search Reports", BIG_FONT, (WIDTH // 2 - 150, 20))

        map_rect = self.map_surface.get_rect(center=(WIDTH // 2, 250))
        map_border_rect = pygame.Surface((450+10, 300+10)).get_rect(center=(WIDTH // 2, 250))
        mapX, mapY = map_rect.topleft
        pygame.draw.rect(screen, pygame.Color(0, 50, 100), map_border_rect)
        screen.blit(self.map_surface, (mapX, mapY))

        # Draw markers on map
        for report in self.reports:
            if report.location:
                px, py = report.location
                pygame.draw.circle(screen, pygame.Color('red'), (mapX + px, mapY + py), 6)

        self.back_button.Draw(screen)

        if self.message:
            DrawTextBox(screen, self.message, FONT, (WIDTH // 2, 550), centered=True, text_color=pygame.Color('blue'))

class ViewReportScene(SceneBase):
    def __init__(self, report):
        super().__init__()
        self.report = report
        self.back_button = Button("Back", (WIDTH - 150) // 2, 550, 150, 40, self.GoBack)

        try:
            self.map_surface = pygame.image.load("toronto_map.png").convert()
            self.map_surface = pygame.transform.scale(self.map_surface, (450, 300))
        except Exception as e:
            print("Error loading Toronto map in ViewReportScene:", e)
            self.map_surface = pygame.Surface((450, 300))
            self.map_surface.fill(pygame.Color('lightgray'))

    def GoBack(self):
        scene_manager.SetScene(SearchScene())

    def ProcessEvents(self, events):
        for event in events:
            self.back_button.HandleEvent(event)

    def Update(self):
        pass

    def Render(self, screen):
        if bg_image:
            screen.blit(bg_image, (0, 0))
        else:
            screen.fill(pygame.Color('white'))
        bg_surface = pygame.Surface((WIDTH, HEIGHT))
        bg_surface.set_alpha(150)
        bg_surface.fill((255,255,255))
        screen.blit(bg_surface, (0, 0))

        DrawTextBox(screen, "View Report", BIG_FONT, (WIDTH // 2 - 150, 20))
        
        map_rect = self.map_surface.get_rect(center=(WIDTH // 2, 250))
        map_border_rect = pygame.Surface((450+10, 300+10)).get_rect(center=(WIDTH // 2, 250))
        mapX, mapY = map_rect.topleft
        pygame.draw.rect(screen, pygame.Color(0, 50, 100), map_border_rect)
        screen.blit(self.map_surface, (mapX, mapY))

        # Marker
        if self.report.location:
            marker_pos = (mapX + self.report.location[0], mapY + self.report.location[1])
            pygame.draw.circle(screen, pygame.Color('red'), marker_pos, 6)

        self.back_button.Draw(screen)

        base_x = WIDTH // 2 - 220
        base_y = 420

        # Each line on its own
        lines = []
        lines.append((f"Submitted: {self.report.time_submitted.strftime("%Y-%m-%d %H:%M:%S")}", f""))
        lines.append((f"Type: {self.report.type}", f"Description: {self.report.description}"))
        lines.append((f"Location: {self.report.location}", f"User: {self.report.user.username}    Status: {self.report.status.name}"))
        lines.append((f"Actions Taken: ", f""))

        text_y = base_y
        for left_text, right_text in lines:
            DrawTextBox(screen, left_text, SMALL_FONT, (base_x, text_y))
            DrawTextBox(screen, right_text, SMALL_FONT, (base_x + 200, text_y))
            text_y += 28

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
SMALL_FONT = pygame.font.SysFont("Times", 18)
FONT = pygame.font.SysFont("Times", 24)
BIG_FONT = pygame.font.SysFont("Times", 48, bold=True)

app = App()
# ---------- Dummy USERS Dictionary for Login ----------
app.CreateAccount("admin", "admin")
app.CreateAccount("user", "password")

start_scene = LoginScene()
# start_scene = ReportScene()
scene_manager = SceneManager()

# ---------- Load Background Image ----------
try:
    bg_image = pygame.image.load("background.png").convert()
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
except Exception as e:
    print("Error loading background image:", e)
    bg_image = None


if __name__ == '__main__':
    main()