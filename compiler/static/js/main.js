var editor = ace.edit("editor");
editor.setTheme("ace/theme/chaos");
editor.session.setMode("ace/mode/python");

const syntexHighlighter = {
  java: "ace/mode/java",
  py: "ace/mode/python",
  js: "ace/mode/javascript",
  c: "ace/mode/c_cpp",
  cpp: "ace/mode/c_cpp",
}; // syntax highlighter

folder = false;
file = false;

let fileEditing = ["", -1]; // information about file being editing

let parent = -1; // id of the parent folder if the file are being created for the child.

isparent = false; // if the file being created is a child of some folder

let workspace = document.URL.split("/")[4]; // workspace id

// Ajax code for functioning

async function create_File_Folder(name, url, parent = -1) {
  const xhr = new XMLHttpRequest();
  xhr.open("POST", "/" + url);
  xhr.setRequestHeader(
    "X-CSRFToken",
    document.getElementsByName("csrfmiddlewaretoken")[0].value
  );
  xhr.send(
    JSON.stringify({ name: name, workspace: workspace, parent: parent })
  );
  console.log(xhr.status);
  xhr.onload = () => {
    if (xhr.status != 200) {
      alert("Error occured, can't create " + name);
    }
    const FID = JSON.parse(xhr.responseText)["id"];
    console.log(FID);
    create(FID, name);
  };
}
// AJAX codes End

// Function to view the child files of a folder
const viewFiles = (fNo) => {
  const folder1 = document.getElementById("folder" + fNo);
  if (folder1.style.display === "none") {
    folder1.style.display = "block";
  } else {
    folder1.style.display = "none";
  }
};

// To close askName modal
const closeoverlay = () => {
  document.getElementsByClassName("File_Folder_Modal")[0].style.display =
    "none";
  file = false;
  folder = false;
};

// Functon to ask for name of file or folder by popping up the modals
const askForName = (types, id = -1) => {
  let inputTag = document.getElementById("File_Folder_Name");
  document.getElementById("modalTitle").innerHTML = "Enter " + types + " Name";
  parent = id;
  if (id != -1) {
    isparent = true;
  }
  if (types === "folder") {
    folder = true;
    file = false;
    inputTag.placeholder = "Enter Folder Name";
  } else {
    folder = false;
    file = true;
    inputTag.placeholder = "Enter File Name";
  }
  document.getElementsByClassName("File_Folder_Modal")[0].style.display =
    "flex";
};

// Function to create folder or file
function creating_File_Folder() {
  const name = document.getElementById("File_Folder_Name").value;
  if (folder) {
    create_File_Folder(name, "createFolder");
  }
  if (file) {
    create_File_Folder(name, "createFile", parent);
    console.log(fileNo);
  }
}

const create = (ffno, name) => {
  document.getElementById("File_Folder_Name").value = ""; // to clear the input tag

  if (folder) {
    const folder1 = document.createElement("div"); // to create a new folder
    folder1.className = "FolderWrap";
    folder1.innerHTML = `<span><img height="20px" style="float: left; margin-right: 4px;" src="/static/folder2.png" alt=""></span> ${name}
                <span onclick="viewFiles(${ffno})">
                    <img height="14px" style="margin-left: 4px;" src="/static/arrow.png" alt="">
                </span>
                <div class="NewFile_forFolder" style="float: right;">
                        <img src="/static/new_file.png" alt="" title="New File" onclick="askForName('file',${ffno})">
                    </div>
                <ul id="folder${ffno}">
                </ul>`;
    document.getElementsByClassName("sideNav")[0].appendChild(folder1);
    folder = false;
  }

  if (file) {
    if (isparent) {
      // if the file is a child of some folder

      const file1 = document.createElement("li");
      file1.setAttribute("onclick", `fetchFile(${ffno})`);
      file1.className = "file";
      file1.innerHTML = `<span><img src="/static/file.png" height="15px" alt=""></span> ${name}`;
      document.getElementById("folder" + parent).appendChild(file1);
      parent = 0;
    } else {
      const file1 = document.createElement("p"); // to create a new file
      file1.className = "file";
      file1.setAttribute("onclick", "fetchFile(" + ffno + ")");
      file1.setAttribute("id", ffno);
      file1.innerHTML = `<span><img src="/static/file.png" height="15px" alt=""></span> ${name}`;
      document.getElementsByClassName("sideNav")[0].appendChild(file1);
    }

    file = false;
    isparent = false;
  }

  closeoverlay(); // to close the modal
};

// Function to fetch the file

const askUpload = () => {
  if (fileEditing[1] == -1) {
    alert("No file selected");
    return;
  }
  document.getElementById("fileId").setAttribute("value", fileEditing[1]);
  document.getElementById("inputtingFile").click();
  document.getElementById("uploadbutton").style.display = "block";
};

// Function to fetch file from backend

const fetchFile = (id) => {
  fileEditing[1] = id;
  const xhr = new XMLHttpRequest();
  xhr.open("POST", "/fetchFile");
  xhr.setRequestHeader(
    "X-CSRFToken",
    document.getElementsByName("csrfmiddlewaretoken")[0].value
  );
  xhr.send(JSON.stringify({ id: id }));
  xhr.onload = () => {
    const file = JSON.parse(xhr.responseText);
    editor.setValue(file["content"].replaceAll("\\n", "\n"));
    fileEditing[0] = file["name"];
    document.getElementsByClassName("currentFile")[0].innerHTML = file["name"];
    let extension = file["name"].split(".")[1];
    editor.session.setMode(syntexHighlighter[extension.toLowerCase()]);
  };
};

// Function to show output of the code
const showOutput = (result) => {
  let terminal = document.getElementsByClassName("terminal")[0];
  output = result["result"].replaceAll("\n", "<br>");
  terminal.innerHTML = `
            ${output}
            <br>
            -------------------
            Exit Code : ${result["exit_code"]}
            <br>
            Error: ${result["error"]}
            `;
};
// Function to save and execute the file
const submitCode = () => {
  const xhr = new XMLHttpRequest();
  xhr.open("POST", "/submitCode");
  xhr.setRequestHeader(
    "X-CSRFToken",
    document.getElementsByName("csrfmiddlewaretoken")[0].value
  );
  xhr.send(
    JSON.stringify({
      content: editor.getValue(),
      name: fileEditing[0],
      id: fileEditing[1],
    })
  );

  xhr.onload = () => {
    if (xhr.status != 200) {
      alert("Error occured, can't save and execute the file");
    }
    result = xhr.responseText;
    showOutput(JSON.parse(result)["output"]);
  };
};


const NewAccess = () => {
    document.getElementsByTagName('overlay')[0].style.display = 'flex';
}

const AddNewGrant = () =>{
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/addNewGrant");
    xhr.setRequestHeader(
        "X-CSRFToken",
        document.getElementsByName("csrfmiddlewaretoken")[0].value
    );
    xhr.send(
        JSON.stringify({
            workspace: workspace,
            grantee: document.getElementById('NewGrant').value,
        })
    );
    xhr.onload = () => {
        if (xhr.status != 200) {
            alert("Error occured, can't add new grant");
            return;
        }
        result = xhr.responseText;
        alert(result);
        document.getElementsByTagName('overlay')[0].style.display = 'none';
        let wrap = documen.getElementById('grantees');
        let newGrantee = document.createElement('li');
        newGrantee.innerHTML = document.getElementById('NewGrant').value;
        wrap.appendChild(newGrantee);
        document.getElementById('NewGrant').value = '';
    }
}

const closeoverlay_new = () => {
    document.getElementsByTagName("overlay")[0].style.display = "none";
    }
