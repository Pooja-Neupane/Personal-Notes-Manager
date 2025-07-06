from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

# OOP Design: Note class to represent individual notes
class Note:
    def __init__(self, title, content):
        self.title = title
        self.content = content

# OOP Design: NoteManager to manage note operations
class NoteManager:
    def __init__(self):
        self.notes = []

    def add_note(self, title, content):
        self.notes.append(Note(title, content))

    def get_notes(self):
        return self.notes

    def delete_note(self, index):
        if 0 <= index < len(self.notes):
            del self.notes[index]

# Instantiate NoteManager
note_manager = NoteManager()

# UI Template (Embedded HTML with Bootstrap)
template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Personal Notes Manager</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
<div class="container mt-5">
    <h1 class="mb-4 text-center">📝 Personal Notes Manager</h1>
    <form method="POST" action="/add" class="card p-3 mb-4 shadow-sm">
        <div class="mb-3">
            <label class="form-label">Note Title</label>
            <input type="text" name="title" class="form-control" required>
        </div>
        <div class="mb-3">
            <label class="form-label">Note Content</label>
            <textarea name="content" class="form-control" rows="3" required></textarea>
        </div>
        <button type="submit" class="btn btn-primary">Add Note</button>
    </form>

    {% if notes %}
    <div class="row">
        {% for note in notes %}
        <div class="col-md-4">
            <div class="card mb-4 shadow-sm">
                <div class="card-body">
                    <h5 class="card-title">{{ note.title }}</h5>
                    <p class="card-text">{{ note.content }}</p>
                    <a href="/delete/{{ loop.index0 }}" class="btn btn-danger btn-sm">Delete</a>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
    {% else %}
    <p class="text-muted text-center">No notes yet. Add some!</p>
    {% endif %}
</div>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(template, notes=note_manager.get_notes())

@app.route("/add", methods=["POST"])
def add():
    title = request.form["title"]
    content = request.form["content"]
    note_manager.add_note(title, content)
    return redirect("/")

@app.route("/delete/<int:index>")
def delete(index):
    note_manager.delete_note(index)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
