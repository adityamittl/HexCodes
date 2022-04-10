# TeamElite

## 💡 Inspiration

- make a Web Based IDE that empower user to collaborate with others their workspace 
- Creating an OCR based model which perfectly recognise the text written and convert into the code to compile it for you.
- Providing user multiple programming languages support.
  
## ⚙ Tech Stack Used
- Front end: HTML5, CSS3, Javascript
- Backend: Django, Python
- Database: SQLite3
- Encryption: Python cryptography library
- Image Recognisation: pytesseract

## 💻 How it works
- When the user hit the web address, they first asked to login or signup into the system.
- Then user asked to create a workspace or use some exixting workspace.
  - They can saperately see if the workspace is created by them or if it is shared by their team.
- Upon selecting the workspace, then user enters into the IDE section where they can-
  - Create folders
  - Create Files
  - Create Files in folder
  - i.e They can easily organise their files
- IDE dynamically adapts according to the file type and highlights their codes respectively.
- upon writing code, user can execute, and their output is reflected into the terminal section
- Files are automatically saved once use hit run button
- Secondly user can create/select a file and feed the hand written code into the system , OCR model recognise characters and push all those code into respective file, where user can see or make some changes into the file.
- All those sensitive data that are flowing between front end and backend are completely encrypted to endure user security.
- This web based IDE is a completely Secure as no files are stored in the media folder this ensures that only the authorized user can see the corrosponding programs.

- Available programming language support:
  - C
  - C++
  - Python
  - Java
  - Javascript
  - And can add more languages

## 🧠 Challenges we ran into:
- Creating the project in this time limit is a huge success with all the constraints
- Managing workspaces
- Integrating the OCR model that recognise hand written code.

## Installing and Running
- Installing and integrating guide of Tesseract is [Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)

- TO execute code locally, go to compiler directory and do
  ```
  python manage.py makemigrations
  python manage.py migrate
  python manage.py runserver
  ```

## What we have learned
- Mentoring session with Kundan Nigan was awesome
- Learned managing workspaces
- Integration of OCR 

## Steps taken to ensure security
- We used VMWare virtual environment to endure disk security and stability 
- Used encryption for handling of sensitive data
- No files are left in media folder, this make sure that only authorized person can access the files

## What next for this project
Since we had a time constraint, we can't make this a complete but those are the point which we'll cover 
- Integration of voice recognisation model
- Making UI more beautiful
- making interactive terminal
- Adding AI to detect some suspecious activity in the terminal.
- 

## Use of vmware in this project
- vmware helps in debugging of applications in multiple environments, without changing development machines.
- It also allows us to rigorously test programs in different runtime environments before release to production.

![image](https://user-images.githubusercontent.com/76921082/162639983-dd0343e0-93e4-4643-9757-61b9f57736c7.png)

![image](https://user-images.githubusercontent.com/76921082/162639995-3851e942-b4c6-4cea-9bd8-ac8261fd6d13.png)

![image](https://user-images.githubusercontent.com/76921082/162640002-e8964760-0775-4db2-ae4d-1d5cfde426b4.png)

![image](https://user-images.githubusercontent.com/76921082/162640018-db7bc91a-c272-4c3a-8210-0a9ae1506992.png)

![image](https://user-images.githubusercontent.com/76921082/162640036-b64c445a-5f78-453b-8423-62dae6648f8b.png)

