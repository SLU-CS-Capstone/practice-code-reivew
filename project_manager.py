import datetime
import smtplib

class ProjectManager:
    def __init__(self):
        self.projects = []
        self.team_members = []
        self.tasks = []
        self.db_connection = None
    
    def add_project(self, name, description, deadline, budget, client_email, client_phone, project_type, priority):
        project = {
            'name': name,
            'description': description,
            'deadline': deadline,
            'budget': budget,
            'client_email': client_email,
            'client_phone': client_phone,
            'type': project_type,
            'priority': priority,
            'created_at': datetime.datetime.now(),
            'status': 'New'
        }
        self.projects.append(project)
        self.notify_team(f"New project added: {name}")
        self.update_database()
        return True

    def add_task(self, project_name, task_name, assignee, due_date, estimated_hours, actual_hours, status):
        for project in self.projects:
            if project['name'] == project_name:
                task = {
                    'name': task_name,
                    'assignee': assignee,
                    'due_date': due_date,
                    'estimated_hours': estimated_hours,
                    'actual_hours': actual_hours,
                    'status': status
                }
                self.tasks.append(task)
                self.notify_team(f"New task added: {task_name} for project {project_name}")
                self.update_database()
                return True
        return False

    def update_task_status(self, task_name, new_status):
        for task in self.tasks:
            if task['name'] == task_name:
                task['status'] = new_status
                self.notify_team(f"Task status updated: {task_name} is now {new_status}")
                self.update_database()
                return True
        return False

    def generate_project_report(self, project_name):
        for project in self.projects:
            if project['name'] == project_name:
                report = f"Project Report for {project_name}\n"
                report += f"Description: {project['description']}\n"
                report += f"Deadline: {project['deadline']}\n"
                report += f"Budget: ${project['budget']}\n"
                report += f"Status: {project['status']}\n"
                report += "Tasks:\n"
                for task in self.tasks:
                    if task['name'].startswith(project_name):
                        report += f"  - {task['name']}: {task['status']} (Assigned to: {task['assignee']})\n"
                return report
        return "Project not found"

    def notify_team(self, message):
        for member in self.team_members:
            self.send_email(member['email'], "Project Update", message)

    def send_email(self, to_email, subject, body):
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("projectmanager@company.com", "password123")
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail("projectmanager@company.com", to_email, message)
            server.quit()
        except Exception as e:
            print(f"Failed to send email: {str(e)}")

    def update_database(self):
        # Assume this method updates a database with the latest project and task information
        if self.db_connection is None:
            self.db_connection = self.connect_to_database()
        # ... database update logic here ...
        pass

    def connect_to_database(self):
        # Assume this method establishes a database connection
        pass

    def calculate_project_cost(self, project_name):
        total_cost = 0
        for project in self.projects:
            if project['name'] == project_name:
                for task in self.tasks:
                    if task['name'].startswith(project_name):
                        total_cost += task['actual_hours'] * 100  # Assume $100 per hour
                return total_cost
        return 0

    def get_overdue_tasks(self):
        today = datetime.datetime.now().date()
        overdue_tasks = []
        for task in self.tasks:
            if task['due_date'] < today and task['status'] != 'Completed':
                overdue_tasks.append(task)
        return overdue_tasks
