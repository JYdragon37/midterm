from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, joinedload
from sqlalchemy.types import JSON, TypeDecorator
from sqlalchemy.dialects.postgresql import JSONB
import os
import json

app = Flask(__name__)

# Database configuration
DATABASE_URL = "postgresql://postgres.qfuqvxueqojaivzgtiwj:vdGS4.CLEg2.AyY@aws-0-ap-northeast-2.pooler.supabase.com:6543/postgres"

# SSL 설정 추가
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "sslmode": "require"
    }
)
Base = declarative_base()
Session = sessionmaker(bind=engine)

# JSON 타입을 위한 커스텀 타입 정의
class JSONDict(TypeDecorator):
    impl = JSON
    
    def process_bind_param(self, value, dialect):
        if value is None:
            return {}
        return value
    
    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        return value

# Database Models
class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    tasks = relationship('Task', back_populates='project', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'startDate': self.start_date.isoformat(),
            'endDate': self.end_date.isoformat(),
            'tasks': [task.to_dict() for task in self.tasks]
        }

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    name = Column(String, nullable=False)
    goal = Column(Integer, nullable=False)
    completions = Column(JSONB, nullable=False, default={})
    project = relationship('Project', back_populates='tasks')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'goal': self.goal,
            'completions': self.completions if isinstance(self.completions, dict) else {}
        }

# Create tables
Base.metadata.create_all(engine)

@app.route("/")
def home():
    return render_template("base.html", title="Home")

@app.route("/to_do_list")
def to_do_list():
    try:
        session = Session()
        projects = [project.to_dict() for project in session.query(Project).all()]
        return render_template("to_do_list.html", title="To-Do List", initial_projects=projects)
    except Exception as e:
        print(f"Error loading projects: {str(e)}")
        return render_template("to_do_list.html", title="To-Do List", initial_projects=[])
    finally:
        session.close()

@app.route("/tracking_dashboard")
def tracking_dashboard():
    return render_template("tracking_dashboard.html", title="Tracking Dashboard")

@app.route("/my_page")
def my_page():
    return render_template("my_page.html", title="My Page")

@app.route("/create_project", methods=["POST"])
def create_project():
    try:
        project_data = request.get_json()
        if not all(key in project_data for key in ['name', 'startDate', 'endDate']):
            return jsonify({"status": "error", "message": "Missing required fields"}), 400
        
        session = Session()
        new_project = Project(
            name=project_data['name'],
            start_date=datetime.fromisoformat(project_data['startDate']).date(),
            end_date=datetime.fromisoformat(project_data['endDate']).date()
        )
        session.add(new_project)
        session.commit()
        
        # Get all projects to return updated list
        projects = [project.to_dict() for project in session.query(Project).all()]
        session.close()
        
        return jsonify({
            "status": "success",
            "message": "Project created successfully",
            "projects": projects
        })
    except Exception as e:
        session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        session.close()

@app.route("/add_task", methods=["POST"])
def add_task():
    try:
        data = request.get_json()
        project_name = data.get('projectName')
        task_name = data.get('taskName')
        goal = int(data.get('goal'))

        if not all([project_name, task_name, goal]):
            return jsonify({"status": "error", "message": "Missing required fields"}), 400

        # Get date range (today ± 2 days)
        today = datetime.now().date()
        date_range = [(today + timedelta(days=i)).isoformat() 
                     for i in range(-2, 3)]

        session = Session()
        project = session.query(Project).filter_by(name=project_name).first()
        
        if project:
            new_task = Task(
                project_id=project.id,
                name=task_name,
                goal=goal,
                completions={date: False for date in date_range}
            )
            session.add(new_task)
            session.commit()
            
            # Refresh project data
            project = session.query(Project).filter_by(id=project.id).first()
            project_dict = project.to_dict()
            session.close()
            
            return jsonify({
                "status": "success",
                "message": "Task added successfully",
                "tasks": project_dict['tasks'],
                "dateRange": date_range,
                "today": today.isoformat()
            })
        
        return jsonify({"status": "error", "message": "Project not found"}), 404
    except Exception as e:
        session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        session.close()

@app.route("/update_task_status", methods=["POST"])
def update_task_status():
    session = Session()
    try:
        data = request.get_json()
        task_id = data.get('taskId')
        date = data.get('date')
        completed = data.get('completed')

        print(f"[1] Received request - Task ID: {task_id}, Date: {date}, Completed: {completed}")

        task = session.query(Task).filter_by(id=task_id).first()
        if not task:
            return jsonify({"status": "error", "message": "Task not found"}), 404

        print(f"[2] Found task: {task.name}, Current completions: {task.completions}")

        # completions를 새 딕셔너리로 복사
        current_completions = dict(task.completions) if task.completions else {}
        current_completions[date] = completed

        # 새로운 completions 상태를 할당
        task.completions = current_completions

        print(f"[3] Updated completions (before commit): {task.completions}")

        # 변경사항 커밋
        session.commit()
        session.refresh(task)

        print(f"[4] Final completions state: {task.completions}")

        return jsonify({
            "status": "success",
            "message": "Task status updated successfully",
            "completions": task.completions
        })

    except Exception as e:
        print(f"[ERROR] Exception occurred: {str(e)}")
        session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        session.close()

# 프로젝트 목록을 가져오는 새로운 API 엔드포인트 추가
@app.route("/get_projects", methods=["GET"])
def get_projects():
    try:
        session = Session()
        projects = [project.to_dict() for project in session.query(Project).all()]
        return jsonify({
            "status": "success",
            "projects": projects
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    finally:
        session.close()

@app.route("/update_project", methods=["POST"])
def update_project():
    try:
        data = request.get_json()
        project_id = data.get('projectId')
        new_name = data.get('name')
        new_start_date = datetime.fromisoformat(data.get('startDate')).date()
        new_end_date = datetime.fromisoformat(data.get('endDate')).date()

        session = Session()
        project = session.query(Project).filter_by(id=project_id).first()
        
        if project:
            project.name = new_name
            project.start_date = new_start_date
            project.end_date = new_end_date
            session.commit()
            
            projects = [p.to_dict() for p in session.query(Project).all()]
            return jsonify({
                "status": "success",
                "message": "Project updated successfully",
                "projects": projects
            })
        
        return jsonify({"status": "error", "message": "Project not found"}), 404
    except Exception as e:
        session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        session.close()

@app.route("/delete_project", methods=["POST"])
def delete_project():
    try:
        data = request.get_json()
        project_id = data.get('projectId')

        session = Session()
        project = session.query(Project).filter_by(id=project_id).first()
        
        if project:
            session.delete(project)
            session.commit()
            
            projects = [p.to_dict() for p in session.query(Project).all()]
            return jsonify({
                "status": "success",
                "message": "Project deleted successfully",
                "projects": projects
            })
        
        return jsonify({"status": "error", "message": "Project not found"}), 404
    except Exception as e:
        session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        session.close()

@app.route("/update_task", methods=["POST"])
def update_task():
    try:
        data = request.get_json()
        task_id = data.get('taskId')
        new_name = data.get('name')
        new_goal = data.get('goal')

        session = Session()
        task = session.query(Task).filter_by(id=task_id).first()
        
        if task:
            task.name = new_name
            task.goal = new_goal
            session.commit()
            
            project = session.query(Project).filter_by(id=task.project_id).first()
            return jsonify({
                "status": "success",
                "message": "Task updated successfully",
                "tasks": [t.to_dict() for t in project.tasks]
            })
        
        return jsonify({"status": "error", "message": "Task not found"}), 404
    except Exception as e:
        session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        session.close()

@app.route("/delete_task", methods=["POST"])
def delete_task():
    try:
        data = request.get_json()
        task_id = data.get('taskId')

        session = Session()
        task = session.query(Task).filter_by(id=task_id).first()
        
        if task:
            project_id = task.project_id
            session.delete(task)
            session.commit()
            
            project = session.query(Project).filter_by(id=project_id).first()
            return jsonify({
                "status": "success",
                "message": "Task deleted successfully",
                "tasks": [t.to_dict() for t in project.tasks]
            })
        
        return jsonify({"status": "error", "message": "Task not found"}), 404
    except Exception as e:
        session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        session.close()

@app.route("/get_project/<int:project_id>")
def get_project(project_id):
    session = Session()
    try:
        print(f"[1] Fetching project {project_id}")
        
        # 프로젝트와 관련 태스크들을 한 번에 가져옴
        project = session.query(Project).options(
            joinedload(Project.tasks)
        ).filter_by(id=project_id).first()
        
        if not project:
            print(f"[2] Project not found: {project_id}")
            return jsonify({"status": "error", "message": "Project not found"}), 404

        # 프로젝트 데이터 변환
        project_data = project.to_dict()
        
        print(f"[3] Project tasks data:")
        for task in project_data['tasks']:
            print(f"Task {task['id']}: {task['name']}")
            print(f"Completions: {task['completions']}")

        return jsonify({
            "status": "success",
            "project": project_data
        })

    except Exception as e:
        print(f"[ERROR] Exception in get_project:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        session.close()

if __name__ == "__main__":
    app.run(debug=True)