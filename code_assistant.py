import streamlit as st
import subprocess
import tempfile
import ast
import os
import shutil

st.set_page_config(page_title="AI Code Assistant", layout="wide")

# ---------------- BACKGROUND IMAGE ----------------

def set_bg():

    st.markdown(
        """
        <style>
        .stApp {
        background-image: url("https://images.hdqwalls.com/download/graph-web-abstract-4k-hn-1920x1080.jpg");
        background-size: cover;
        background-attachment: fixed;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg()

# ---------------- UI STYLE CUSTOMIZATION ----------------

st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Orbitron', sans-serif;
    }

    /* TEXT AREA */

    textarea {
        border-radius: 12px !important;
        border: 2px solid white !important;
        outline: none !important;
        box-shadow: none !important;
    }

    /* ADD THIS BLOCK HERE */

.stTextArea textarea {
    outline: none !important;
    box-shadow: none !important;
}

.stTextArea div[data-baseweb="textarea"] {
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
}

.stTextArea div[data-baseweb="textarea"]:focus-within {
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
}

    textarea:hover {
        border: 2px solid white !important;
        outline: none !important;
        box-shadow: 0 0 8px white !important;
    }

    textarea:focus {
        border: 2px solid white !important;
        outline: none !important;
        box-shadow: 0 0 10px white !important;
    }

    textarea:focus-visible {
        outline: none !important;
    }

    /* BUTTON STYLE */

    div.stButton > button {
        background-color: rgba(255,255,255,0.15);
        color: white;
        border-radius: 10px;
        border: 2px solid white;
        padding: 10px 24px;
        font-size: 16px;
        transition: 0.3s;
        outline: none !important;
    }

    div.stButton > button:hover {
        background-color: white;
        color: black;
        border: 2px solid white;
        transform: scale(1.05);
        outline: none !important;
    }

    /* LANGUAGE SELECT BOX */

    div[data-baseweb="select"] > div {
        background-color: white !important;
        color: black !important;
        border-radius: 10px !important;
        border: 2px solid white !important;
    }

    div[data-baseweb="select"]:hover {
        outline: none !important;
        box-shadow: none !important;
    }

    div[data-baseweb="select"]:focus {
        outline: none !important;
        box-shadow: none !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- UI ----------------

st.title("🤖 AI Code Assistant")
st.write("Here you can Analyze code, detect errors, and execute programs.")

language = st.selectbox(
    "Select Programming Language",
    ["-- NONE --", "Python", "C", "C++", "Java", "JavaScript"]
)

code = st.text_area("Enter your code in this text box ", height=350)

col1, col2, col3 = st.columns(3)

analyze_btn = col1.button("Analyze Code")
error_btn = col2.button("Check Errors")
run_btn = col3.button("Run Program")

analysis_output = st.empty()
error_output = st.empty()
execution_output = st.empty()

# ---------------- SMART CODE ANALYSIS ----------------

def smart_code_analysis(code, language):

    lines = code.split("\n")
    report = []

    report.append("🔎 AI Code Analysis\n")

    for i, line in enumerate(lines, start=1):

        line = line.strip()

        if line == "":
            continue

        # ---------- PYTHON ----------
        if language == "Python":

            if line.startswith("import"):
                report.append(f"Line {i}: Library import detected")

            elif "input(" in line:
                report.append(f"Line {i}: User input detected")

            elif "print(" in line:
                report.append(f"Line {i}: Output statement detected")

            elif line.startswith("def"):
                report.append(f"Line {i}: Function definition detected")

            elif "for " in line:
                report.append(f"Line {i}: For loop detected")

            elif "while " in line:
                report.append(f"Line {i}: While loop detected")

            elif "if " in line:
                report.append(f"Line {i}: Conditional statement detected")

            elif "=" in line and "==" not in line:
                report.append(f"Line {i}: Variable assignment detected")

        # ---------- C / C++ ----------
        elif language in ["C", "C++"]:

            if "#include" in line:
                report.append(f"Line {i}: Header file included")

            elif "int main" in line:
                report.append(f"Line {i}: Main function detected")

            elif "printf" in line or "cout" in line:
                report.append(f"Line {i}: Output statement detected")

            elif "scanf" in line or "cin" in line:
                report.append(f"Line {i}: Input statement detected")

            elif "for(" in line or "for (" in line:
                report.append(f"Line {i}: Loop detected")

            elif "if(" in line or "if (" in line:
                report.append(f"Line {i}: Conditional statement detected")

        # ---------- JAVASCRIPT ----------
        elif language == "JavaScript":

            if "console.log" in line:
                report.append(f"Line {i}: Output command detected")

            elif "function" in line:
                report.append(f"Line {i}: Function declaration detected")

            elif "let " in line or "const " in line:
                report.append(f"Line {i}: Variable declaration detected")

            elif "for(" in line or "while(" in line:
                report.append(f"Line {i}: Loop detected")

            elif "if(" in line:
                report.append(f"Line {i}: Conditional statement detected")

        # ---------- JAVA ----------
        elif language == "Java":

            if "class" in line:
                report.append(f"Line {i}: Class declaration detected")

            elif "public static void main" in line:
                report.append(f"Line {i}: Main method detected")

            elif "System.out.println" in line:
                report.append(f"Line {i}: Output statement detected")

            elif "Scanner" in line:
                report.append(f"Line {i}: Input system detected")

            elif "if(" in line:
                report.append(f"Line {i}: Conditional statement detected")

            elif "for(" in line or "while(" in line:
                report.append(f"Line {i}: Loop detected")

    report.append("\n💡 Suggestions:")

    if "print" not in code and language == "Python":
        report.append("Add print() to display results.")

    if language in ["C","C++"] and "main" not in code:
        report.append("Program should contain main() function.")

    if language == "JavaScript" and "console.log" not in code:
        report.append("Add console.log() to display output.")

    if language == "Java" and "System.out.println" not in code:
        report.append("Use System.out.println() to display output.")

    return "\n".join(report)

# ---------------- ERROR CHECK SYSTEM ----------------

def check_errors(code):

    if language == "Python":

        try:
            ast.parse(code)
            return "✅ No syntax errors detected"

        except SyntaxError as e:
            return f"❌ Python Syntax Error:\n{e}"

    elif language == "C":

        with tempfile.NamedTemporaryFile(delete=False, suffix=".c", mode="w") as f:
            f.write(code)
            filename = f.name

        compile_process = subprocess.run(
            ["gcc", filename],
            capture_output=True,
            text=True
        )

        if compile_process.stderr:
            return "❌ Compile Error:\n" + compile_process.stderr

        return "✅ No compile errors"

    elif language == "C++":

        with tempfile.NamedTemporaryFile(delete=False, suffix=".cpp", mode="w") as f:
            f.write(code)
            filename = f.name

        compile_process = subprocess.run(
            ["g++", filename],
            capture_output=True,
            text=True
        )

        if compile_process.stderr:
            return "❌ Compile Error:\n" + compile_process.stderr

        return "✅ No compile errors"

    elif language == "JavaScript":

        if "var " in code:
            return "⚠ Warning: Use 'let' or 'const' instead of var"

        if "==" in code:
            return "⚠ Warning: Consider using '==='"

        return "✅ No major errors detected"

    elif language == "Java":

        if shutil.which("javac") is None:
            return "❌ Java JDK not installed"

        folder = tempfile.mkdtemp()
        javafile = os.path.join(folder, "Main.java")

        with open(javafile, "w") as f:
            f.write(code)

        compile_process = subprocess.run(
            ["javac", javafile],
            capture_output=True,
            text=True
        )

        if compile_process.stderr:
            return "❌ Compile Error:\n" + compile_process.stderr

        return "✅ No compile errors detected"

# ---------------- RUN PROGRAM ----------------

def run_python(code):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w") as f:
        f.write(code)
        filename = f.name

    result = subprocess.run(
        ["python", filename],
        capture_output=True,
        text=True
    )

    return result.stdout + result.stderr


def run_c(code):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".c", mode="w") as f:
        f.write(code)
        cfile = f.name

    exe = cfile.replace(".c", ".exe")

    compile_process = subprocess.run(
        ["gcc", cfile, "-o", exe],
        capture_output=True,
        text=True
    )

    if compile_process.stderr:
        return "❌ Compile Error:\n" + compile_process.stderr

    run_process = subprocess.run(
        [exe],
        capture_output=True,
        text=True
    )

    return run_process.stdout + run_process.stderr


def run_cpp(code):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".cpp", mode="w") as f:
        f.write(code)
        cppfile = f.name

    exe = cppfile.replace(".cpp", ".exe")

    compile_process = subprocess.run(
        ["g++", cppfile, "-o", exe],
        capture_output=True,
        text=True
    )

    if compile_process.stderr:
        return "❌ Compile Error:\n" + compile_process.stderr

    run_process = subprocess.run(
        [exe],
        capture_output=True,
        text=True
    )

    return run_process.stdout + run_process.stderr


def run_js(code):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".js", mode="w") as f:
        f.write(code)
        jsfile = f.name

    result = subprocess.run(
        ["node", jsfile],
        capture_output=True,
        text=True
    )

    return result.stdout + result.stderr


def run_java(code):

    folder = tempfile.mkdtemp()
    javafile = os.path.join(folder, "Main.java")

    with open(javafile, "w") as f:
        f.write(code)

    compile_process = subprocess.run(
        ["javac", javafile],
        capture_output=True,
        text=True
    )

    if compile_process.stderr:
        return "❌ Compile Error:\n" + compile_process.stderr

    run_process = subprocess.run(
        ["java", "-cp", folder, "Main"],
        capture_output=True,
        text=True
    )

    return run_process.stdout + run_process.stderr


# ---------------- BUTTON ACTIONS ----------------

if language == "-- SELECT LANGUAGE --":
    st.warning("⚠ Please select a programming language first.")

elif analyze_btn:

    result = smart_code_analysis(code, language)

    analysis_output.code(result)

elif error_btn:

    errors = check_errors(code)

    error_output.code(errors)

elif run_btn:

    if language == "Python":
        output = run_python(code)

    elif language == "C":
        output = run_c(code)

    elif language == "C++":
        output = run_cpp(code)

    elif language == "JavaScript":
        output = run_js(code)

    elif language == "Java":
        output = run_java(code)

    execution_output.code(output)