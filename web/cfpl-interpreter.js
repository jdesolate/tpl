class CFPLInterpreter {
  constructor() {
    this.editor = null;
    this.examples = {
      input: {
        title: "Basic variable declaration and output example",
        code: `** Sample CFPL Program
VAR abc, b, c AS INT
VAR x='_', w_23='w' AS CHAR
VAR t=TRUE AS BOOL

START
    abc=b=10
    w_23='a' 
    ** this is a comment
    OUTPUT: abc & "hi" & b & # & w_23 & "#"
STOP`,
      },
      conditions: {
        title: "Conditional statements and decision making",
        code: `** Conditional Example 
VAR age AS INT 
VAR message AS CHAR

START
    INPUT: age
    IF (age < 18) 
    START 
        message = "Too young to vote"
    STOP
    ELSE 
    START 
        message = "You can vote!"
    STOP
    
    OUTPUT: "Age: " & age & # 
    OUTPUT: message
STOP`,
      },
      loops: {
        title: "Loop structures for repetitive operations",
        code: `** Loop Example 
VAR i, sum AS INT
VAR result AS CHAR

START
    sum = 0
    i = 1
    result = "The sum is now: "
    
    WHILE (i <= 5) START
        OUTPUT: "Sum:" & sum         
        sum = sum + i
        OUTPUT: "Adding " & i & # & result & sum & #
        i = i + 1
    STOP
    
    OUTPUT: "Final sum: " & sum & # 
STOP`,
      },
    };

    this.currentExample = "input";
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
    // Existing event bindings
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

    // Interactive examples event bindings
    document.querySelectorAll(".example-btn").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        const exampleType = e.target.getAttribute("data-example");
        this.switchExample(exampleType);
      });
    });

    // Load to editor button
    const loadToEditorBtn = document.getElementById("loadToEditor");
    if (loadToEditorBtn) {
      loadToEditorBtn.addEventListener("click", () => {
        this.loadCurrentExampleToEditor();
      });
    }

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

  switchExample(exampleType) {
    if (!this.examples[exampleType]) return;

    // Update current example
    this.currentExample = exampleType;

    // Update active button
    document.querySelectorAll(".example-btn").forEach((btn) => {
      btn.classList.remove("active");
    });
    document
      .querySelector(`[data-example="${exampleType}"]`)
      .classList.add("active");

    // Update example info
    const exampleInfo = document.getElementById("exampleInfo");
    if (exampleInfo) {
      exampleInfo.textContent = this.examples[exampleType].title;
    }

    // Update code display
    const exampleCode = document.getElementById("exampleCode");
    if (exampleCode) {
      exampleCode.textContent = this.examples[exampleType].code;
    }

    // Add a subtle animation effect
    const codeExample = document.querySelector(".code-example");
    if (codeExample) {
      codeExample.style.opacity = "0.7";
      setTimeout(() => {
        codeExample.style.opacity = "1";
      }, 150);
    }
  }

  loadCurrentExampleToEditor() {
    if (this.examples[this.currentExample]) {
      this.editor.setValue(this.examples[this.currentExample].code);
      this.editor.focus();
      this.setStatus(
        `${this.capitalizeFirst(this.currentExample)} example loaded to editor`,
      );

      // Scroll to top of editor
      this.editor.scrollTo(0, 0);

      // Add visual feedback
      const loadBtn = document.getElementById("loadToEditor");
      if (loadBtn) {
        const originalText = loadBtn.textContent;
        loadBtn.textContent = "Loaded!";
        loadBtn.style.background = "rgba(72, 187, 120, 0.3)";
        loadBtn.style.borderColor = "rgba(72, 187, 120, 0.6)";

        setTimeout(() => {
          loadBtn.textContent = originalText;
          loadBtn.style.background = "rgba(102, 126, 234, 0.2)";
          loadBtn.style.borderColor = "rgba(102, 126, 234, 0.4)";
        }, 1500);
      }
    }
  }

  capitalizeFirst(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
  }

  updateLineCount() {
    const lineCount = this.editor.lineCount();
    const lineCountElement = document.getElementById("lineCount");
    if (lineCountElement) {
      lineCountElement.textContent = lineCount;
    }
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
    if (!container) return;

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
    if (outputElement) {
      outputElement.textContent = output;
      outputElement.className = "output-content success";
    }
  }

  showError(error) {
    const outputElement = document.getElementById("output");
    if (outputElement) {
      outputElement.textContent = error;
      outputElement.className = "output-content error";
    }
  }

  clearOutput() {
    const outputElement = document.getElementById("output");
    if (outputElement) {
      outputElement.textContent = "Ready to execute CFPL code...";
      outputElement.className = "output-content";
    }
    this.setStatus("Ready");
  }

  clearCode() {
    this.editor.setValue("");
    this.editor.focus();
    this.setStatus("Code cleared");
  }

  loadExample() {
    // Load the current selected example (default is 'input')
    this.loadCurrentExampleToEditor();
  }

  setStatus(text) {
    const statusElement = document.getElementById("statusText");
    if (statusElement) {
      statusElement.textContent = text;
    }
  }

  showLoading(show) {
    const overlay = document.getElementById("loadingOverlay");
    if (overlay) {
      if (show) {
        overlay.classList.remove("hidden");
      } else {
        overlay.classList.add("hidden");
      }
    }
  }

  toggleReference() {
    const section = document.getElementById("referenceSection");
    const button = document.getElementById("toggleReference");
    if (!section || !button) return;

    const content = section.querySelector(".reference-content");
    if (!content) return;

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
