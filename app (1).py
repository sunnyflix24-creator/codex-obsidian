import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash

app = Flask(__name__)
app.secret_key = "supersecretkey"  # required for flash messages

# Folder to store uploads
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ---------- Routes ---------- #

@app.route("/")
def home():
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    files = os.listdir(app.config["UPLOAD_FOLDER"])
    return render_template("dashboard.html", files=files)


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        flash("⚠️ No file part in request.", "warning")
        return redirect(url_for("dashboard"))

    file = request.files["file"]
    if file.filename == "":
        flash("⚠️ No file selected.", "warning")
        return redirect(url_for("dashboard"))

    if file:
        filename = file.filename
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        flash(f"✅ File '{filename}' uploaded successfully!", "success")
        return redirect(url_for("dashboard"))


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)


@app.route("/delete/<filename>", methods=["POST"])
def delete_file(filename):
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        flash(f"🗑️ File '{filename}' deleted successfully!", "success")
    else:
        flash("❌ File not found.", "error")
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
