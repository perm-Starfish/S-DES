## **Programming Assignment Submission Protocol**

Hi, Everyone.

To maintain a professional development environment and ensure academic fairness, we are implementing a mandatory submission protocol for all programming assignments. Please follow these guidelines strictly.

### **1. Plagiarism Detection: The MOSS System**
We utilize **MOSS (Measure Of Software Similarity)** from Stanford University to verify the originality of your work.
* **How it works:** MOSS does not simply look for "copy-paste." It analyzes the **structural logic** of your code. Changing variable names, swapping loops (e.g., `for` to `while`), or modifying comments **will not** bypass MOSS.
* **Trust & Reliability:** MOSS is the global gold standard for computer science integrity. It effectively distinguishes between common algorithmic patterns and intentional logic duplication.
* **Manual Review:** Any submission flagged with a high similarity index will undergo a manual review by the teaching staff.

### **2. Required Folder Structure**
Your submission must be organized as follows. The introduction of the **`src`** folder is mandatory to separate logic from documentation.

**Directory Example (for Problems 3-1 and 3-4):**
```text
[Your_Student_ID]
├── 3-1/
│   ├── src/                 <-- All source code files (.cpp, .h, .py, etc.)
│   ├── design_doc.pdf       <-- Technical design & logic explanation
│   ├── readme.md            <-- Environment setup & run instructions
│   └── request.txt          <-- Feature checklist & requirement fulfillment
└── 3-4/
    ├── src/
    ├── design_doc.pdf
    ├── readme.md
    └── request.txt
```

### **3. Mandatory Documentation & Execution Policy**
* **README & Request:** These files serve as the "Manual" for the TAs. They must specify how to set up your environment and run your code. 
    * **The "Zero-Tolerance" Rule:** If your code **fails to compile or run** according to your README instructions, you will receive a **score of 0** for the programming portion. No exceptions.
* **Request (Requirement Checklist):** This file should list which specific assignment requirements you have fulfilled and any special test cases you have passed.

* **Source Code Header (Mandatory)**
Every source file in your src/ folder must begin with a standardized header comment for identification and copyright purposes. Failure to include this may result in a score deduction.
``` c
/*
 * Student ID: [Your ID, e.g., 112550001]
 * Name: [Your Full Name]
 * Assignment: [e.g., Assignment 3-1]
 * Copyright (c) 2026 [Your Name]. All rights reserved.
 */
```

### **4. Grading Breakdown**
Please note that your grade is split into two independent components:
1.  **Code Functionality (X%):** Based on correctness, efficiency, and passing automated test cases.
2.  **Design Document (Y%):** This is graded **separately**. You will be evaluated on your ability to explain your algorithms, data structures, and the rationale behind your implementation. A working program with a poor Design Doc will still result in a lower overall grade.

### 5. Additional Technical Requirements (Lessons from Previous Submissions)
Ensure your submission does not contain the following common errors:

- No Hardcoded Paths: Your code must use relative paths to access data files. If your code contains paths like C:\Users\Name\Desktop\..., it will fail on our machines, resulting in 0 points.

- Clean Submissions: Do NOT include unnecessary files such as:

  - Compiled executables (.exe, .out).

  - IDE-specific folders (.vscode/, .idea/, __pycache__/).

  - System junk (.DS_Store, Thumbs.db).

- Library Dependencies: If your code requires specific libraries (e.g., numpy, pandas), you must list the exact versions in your readme.md.

- Input Interface (No "Guessing Games"): **Your program must provide a clear I/O interface.**

  - DO NOT use interactive "guessing game" style prompts (e.g., "Please click a button" or "Guess a number").

  - The program should accept inputs via Command Line Arguments or Standard Input (stdin) as specified in the problem description to allow for automated testing.

- Build System (Makefile/Scripts): **Ensure your Makefile or build scripts use correct filenames and relative paths.**

  - The TA will run make from the problem root directory; if it fails due to incorrect paths or case-sensitivity issues, it will not be fixed for you.

- Dependency Management: **DO NOT** include entire library folders (e.g., node_modules/, venv/).

  - List all required libraries and their exact versions in your readme.md.

- Valid Imports/Includes: **All #include or import statements must refer to files actually present in your src folder or standard libraries. Broken dependencies = 0 points.**

### 6. Packaging & Submission

Root Directory: When unzipping your file, it should immediately show your [Student_ID] folder. Do not create redundant nested folders (e.g., Assignment_3.zip -> Assignment_3 -> Student_ID -> ...).

