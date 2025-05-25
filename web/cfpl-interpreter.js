class CFPLInterpreter {
  constructor() {
    this.editor = null;
    this.initializeEditor();
    this.bindEvents();
    this.updateLineCount();
  }

  initializeEditor() {
    this.editor = CodeMirror.fromTextArea(
      document.getElementById("codeEditor"),
      {
        mode: "text/x-csrc",
        theme: "monokai",
        lineNumbers: true,
        indentUnit: 4,
        lineWrapping: true,
        matchBrackets: true,
        autoCloseBrackets: true,
        foldGutter: true,
        gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter"],
      },
    );

    this.editor.on("change", () => {
      this.updateLineCount();
    });

    // Set initial content
    this.loadExample();
  }

  bindEvents() {
    document
      .getElementById("runCode")
      .addEventListener("click", () => this.runCode());
    document
      .getElementById("clearCode")
      .addEventListener("click", () => this.clearCode());
    document
      .getElementById("loadExample")
      .addEventListener("click", () => this.loadExample());
    document
      .getElementById("clearOutput")
      .addEventListener("click", () => this.clearOutput());
    document
      .getElementById("refreshVars")
      .addEventListener("click", () => this.refreshVariables());
    document
      .getElementById("toggleReference")
      .addEventListener("click", () => this.toggleReference());

    // Keyboard shortcuts
    document.addEventListener("keydown", (e) => {
      if (e.ctrlKey || e.metaKey) {
        if (e.key === "Enter") {
          e.preventDefault();
          this.runCode();
        } else if (e.key === "k") {
          e.preventDefault();
          this.clearOutput();
        }
      }
    });
  }

  updateLineCount() {
    const lineCount = this.editor.lineCount();
    document.getElementById("lineCount").textContent = lineCount;
  }

  async runCode() {
    const code = this.editor.getValue();
    const inputData = document.getElementById("inputData").value;

    if (!code.trim()) {
      this.showError("Please enter some CFPL code to execute.");
      return;
    }

    this.showLoading(true);
    this.setStatus("Executing...");

    try {
      const result = await eel.run_cfpl_code(code, inputData)();

      if (result.success) {
        this.showOutput(result.output || "(No output)");
        this.setStatus("Execution completed successfully");
        await this.refreshVariables();
      } else {
        this.showError(result.error);
        this.setStatus("Execution failed");
      }
    } catch (error) {
      this.showError("Connection error: " + error.message);
      this.setStatus("Connection error");
    } finally {
      this.showLoading(false);
    }
  }

  async refreshVariables() {
    try {
      const variables = await eel.get_variables()();
      this.displayVariables(variables);
    } catch (error) {
      console.error("Error refreshing variables:", error);
    }
  }

  displayVariables(variables) {
    const container = document.getElementById("variables");

    if (Object.keys(variables).length === 0) {
      container.innerHTML = '<p class="no-vars">No variables declared</p>';
      return;
    }

    let html = '<div class="var-table">';
    for (const [name, value] of Object.entries(variables)) {
      const type = this.getVariableType(value);
      const displayValue = this.formatValue(value);

      html += `
                <div class="var-row">
                    <span class="var-name">${name}</span>
                    <span class="var-type">${type}</span>
                    <span class="var-value">${displayValue}</span>
                </div>
            `;
    }
    html += "</div>";

    container.innerHTML = html;
  }

  getVariableType(value) {
    if (typeof value === "number") {
      return Number.isInteger(value) ? "INT" : "FLOAT";
    } else if (typeof value === "string") {
      return value.length === 1 ? "CHAR" : "STRING";
    } else if (typeof value === "boolean") {
      return "BOOL";
    }
    return "UNKNOWN";
  }

  formatValue(value) {
    if (typeof value === "string") {
      return `'${value}'`;
    } else if (typeof value === "boolean") {
      return value ? "TRUE" : "FALSE";
    }
    return String(value);
  }

  showOutput(output) {
    const outputElement = document.getElementById("output");
    outputElement.textContent = output;
    outputElement.className = "output-content success";
  }

  showError(error) {
    const outputElement = document.getElementById("output");
    outputElement.textContent = error;
    outputElement.className = "output-content error";
  }

  clearOutput() {
    const outputElement = document.getElementById("output");
    outputElement.textContent = "Ready to execute CFPL code...";
    outputElement.className = "output-content";
    this.setStatus("Ready");
  }

  clearCode() {
    this.editor.setValue("");
    this.editor.focus();
    this.setStatus("Code cleared");
  }

  loadExample() {
    const exampleCode = `* Sample CFPL Program
VAR abc, b, c AS INT
VAR x, w_23='w' AS CHAR
VAR t="TRUE" AS BOOL

START
    abc=b=10
    w_23='a'
    * this is a comment
    OUTPUT: abc & "hi" & b & "#" & w_23 & "[#]"
STOP`;
    this.editor.setValue(exampleCode);
    this.setStatus("Example loaded");
  }

  setStatus(text) {
    document.getElementById("statusText").textContent = text;
  }

  showLoading(show) {
    const overlay = document.getElementById("loadingOverlay");
    if (show) {
      overlay.classList.remove("hidden");
    } else {
      overlay.classList.add("hidden");
    }
  }

  toggleReference() {
    const section = document.getElementById("referenceSection");
    const button = document.getElementById("toggleReference");
    const content = section.querySelector(".reference-content");

    if (content.style.display === "none") {
      content.style.display = "block";
      button.textContent = "Hide";
    } else {
      content.style.display = "none";
      button.textContent = "Show";
    }
  }
}

// Initialize the interpreter when the page loads
document.addEventListener("DOMContentLoaded", () => {
  new CFPLInterpreter();
});
