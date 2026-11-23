# AGENTS.md
# FACEBOT — Project Instructions & Team Workflow

## 1. PROJECT IDENTITY

Project name: FACEBOT

Project type: University software engineering project.

Description:
FACEBOT is an intelligent assistant that uses a camera and facial recognition to identify previously registered participants who have explicitly consented to participate.

After a successful identification, the system retrieves the participant's profile from a JSON database and displays personalized information, interests, and recommended university projects.

The system must work on a local Wi-Fi network without requiring an Internet connection during normal operation.

The project is developed collaboratively by three students:

- Ashly: Frontend Design
- Rafael: Frontend Logic and API Integration
- Yamil: Backend, Computer Vision and Integration

The goal is to build one integrated software product, not three independent applications.

---

## 2. PRIMARY DEVELOPMENT OBJECTIVES

The system must:

1. Start a Python backend server.
2. Connect to a camera.
3. Detect a person in the camera feed.
4. Process facial recognition only for enrolled participants who have given consent.
5. Identify a registered participant when confidence requirements are satisfied.
6. Retrieve the participant's profile from the database.
7. Retrieve recommendations based on participant interests.
8. Send the information through a REST API.
9. Display personalized information in the frontend.
10. Return to the welcome screen after the interaction.

When identification is unsuccessful, the system must display a general welcome screen and offer an alternative manual interaction.

The system must never assume that an unknown visitor is a registered participant.

---

## 3. REQUIRED TECHNOLOGIES

Use the following technologies:

### Backend
- Python 3.11+
- FastAPI
- Uvicorn
- OpenCV
- Pydantic

### Frontend
- Python
- Flet

### Data
- JSON for the initial participant database.
- Separate protected storage for biometric templates, if needed.

### Development
- Git
- GitHub
- Pytest
- Python virtual environments
- HTTPX for API testing

Do not introduce React, Angular, Vue, Node.js or an independent JavaScript frontend.

The frontend must be implemented in Python using Flet.

Prefer stable, compatible package versions. Pin working dependencies in requirements.txt.

---

## 4. SYSTEM ARCHITECTURE

Use a modular client-server architecture.

### Backend responsibilities

The backend owns:

- Camera management.
- Image processing.
- Facial recognition.
- Participant verification.
- Profile retrieval.
- Recommendation logic.
- Session management.
- REST API.
- Error handling.

### Frontend responsibilities

The frontend owns:

- Visual presentation.
- Screen navigation.
- Welcome screen.
- Waiting screen.
- Processing screen.
- Recognized participant screen.
- Unknown visitor screen.
- Recommendation cards.
- API communication.
- Connection and error states.

### Communication

The frontend must communicate with the backend through HTTP REST endpoints.

The frontend must never access profiles.json directly.

The backend is the only component responsible for accessing the participant database.

Do not duplicate business logic between frontend and backend.

---

## 5. OFFICIAL PROJECT STRUCTURE

Maintain the following structure:

FACEBOT/
│
├── AGENTS.md
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
│
├── backend/
│   ├── main.py
│   ├── api/
│   │   ├── routes.py
│   │   └── schemas.py
│   │
│   ├── camera/
│   │   └── camera_service.py
│   │
│   ├── recognition/
│   │   └── face_service.py
│   │
│   ├── database/
│   │   ├── repository.py
│   │   └── profiles.json
│   │
│   └── services/
│       ├── recommendation.py
│       └── session_service.py
│
├── frontend/
│   ├── main.py
│   │
│   ├── screens/
│   │   ├── welcome.py
│   │   ├── waiting.py
│   │   ├── processing.py
│   │   ├── recognized.py
│   │   └── unknown.py
│   │
│   ├── components/
│   │   ├── profile_card.py
│   │   ├── interest_card.py
│   │   └── recommendation_card.py
│   │
│   └── services/
│       └── api_client.py
│
├── tests/
│   ├── test_api.py
│   ├── test_database.py
│   └── test_recommendations.py
│
└── docs/
    ├── architecture.md
    ├── api_contract.md
    ├── installation.md
    └── team_workflow.md

This structure may be extended when technically necessary, but existing modules must not be reorganized without documenting the reason.

---

## 6. TEAM RESPONSIBILITIES

### ASHLY — FRONTEND DESIGN

Primary role:
Visual design and user experience.

Assigned directory ownership:

- frontend/screens/
- frontend/components/

Responsibilities:

1. Design the visual identity of FACEBOT.
2. Implement the welcome screen.
3. Implement the waiting screen.
4. Implement the processing screen.
5. Design the recognized participant screen.
6. Design the unknown visitor screen.
7. Create reusable visual components.
8. Design profile cards.
9. Design interest cards.
10. Design recommendation cards.
11. Ensure visual consistency.
12. Make the interface appropriate for a university exhibition.

Requirements:

- Use Python and Flet.
- Follow the API response contract.
- Use fictional data during visual development.
- Do not implement direct database access.
- Do not implement facial recognition.
- Do not modify backend business logic.

Expected deliverables:

- Functional visual screens.
- Reusable components.
- Consistent design system.
- Frontend visual documentation.

### RAFAEL — FRONTEND LOGIC AND API INTEGRATION

Primary role:
Frontend functionality and communication.

Assigned directory ownership:

- frontend/main.py
- frontend/services/

Responsibilities:

1. Implement frontend application initialization.
2. Implement screen navigation.
3. Connect the frontend to FastAPI.
4. Implement HTTP requests.
5. Process backend responses.
6. Manage application states.
7. Handle loading states.
8. Handle API connection errors.
9. Refresh the displayed session state.
10. Implement session reset behavior.
11. Integrate Ashly's visual components.
12. Test frontend behavior with the backend.

Requirements:

- Use Python and Flet.
- Use HTTPX or another appropriate HTTP client.
- Use the documented API contract.
- Never read profiles.json directly.
- Never implement facial recognition in the frontend.
- Coordinate component interfaces with Ashly.

Expected deliverables:

- Working frontend application.
- Functional API client.
- State management.
- Navigation.
- Backend integration.

### YAMIL — BACKEND, COMPUTER VISION AND INTEGRATION

Primary role:
Backend architecture and system integration.

Assigned directory ownership:

- backend/
- tests/
- docs/

Responsibilities:

1. Initialize the Python project.
2. Configure FastAPI.
3. Configure Uvicorn.
4. Implement the REST API.
5. Implement camera management with OpenCV.
6. Implement face detection and recognition.
7. Implement consent verification.
8. Implement the JSON repository.
9. Implement participant profile retrieval.
10. Implement recommendation logic.
11. Implement session management.
12. Implement API schemas.
13. Implement backend tests.
14. Document the API contract.
15. Integrate the frontend and backend.
16. Prepare local network deployment.

Requirements:

- Keep the backend modular.
- Use dependency injection when appropriate.
- Validate API inputs and outputs.
- Handle camera disconnections.
- Never expose biometric templates through public API responses.
- Never return raw facial images to the frontend.
- Never identify people who have not enrolled and consented.

Expected deliverables:

- Working backend.
- REST API.
- Camera service.
- Recognition service.
- JSON repository.
- Recommendation service.
- Automated tests.
- Technical documentation.

---

## 7. API CONTRACT

Implement the following endpoints.

### GET /api/status

Returns backend availability.

Example:

{
  "status": "online",
  "application": "FACEBOT"
}

### GET /api/camera/status

Returns camera availability.

Example:

{
  "status": "connected",
  "camera_available": true
}

### GET /api/session

Returns the current session state.

Possible states:

- waiting
- processing
- recognized
- unknown
- error

Example waiting:

{
  "status": "waiting",
  "person": null
}

Example recognized:

{
  "status": "recognized",
  "person": {
    "id": "USR001",
    "name": "Carlos",
    "career": "Ingenieria de Sistemas",
    "interests": [
      "Inteligencia Artificial",
      "Robotica"
    ],
    "recommendations": []
  }
}

Example unknown:

{
  "status": "unknown",
  "person": null
}

### GET /api/person/{id}

Retrieves an enrolled participant's permitted public profile.

### POST /api/session/reset

Resets the current interaction and returns the application to waiting.

All responses must use consistent Pydantic schemas.

Do not expose internal recognition data, facial embeddings, image paths, or sensitive participant information.

Document any additional endpoints before implementing them.

---

## 8. DATABASE CONTRACT

Use profiles.json for the initial database.

Example:

{
  "profiles": [
    {
      "id": "USR001",
      "name": "Carlos",
      "career": "Ingenieria de Sistemas",
      "consent": true,
      "interests": [
        "Inteligencia Artificial",
        "Robotica",
        "Videojuegos"
      ],
      "recommendations": [
        {
          "title": "Proyecto de IA",
          "description": "Proyecto universitario de inteligencia artificial",
          "category": "Inteligencia Artificial"
        }
      ]
    }
  ]
}

Rules:

- Use fictional development profiles.
- Validate the consent field.
- Do not expose profiles without authorization.
- Keep biometric data separate from profile data.
- Use a repository abstraction for database access.
- Do not make the frontend read the JSON file.
- Do not store passwords or secrets in JSON.

---

## 9. NETWORK REQUIREMENTS

The system must support local Wi-Fi operation.

The backend should be configurable through environment variables.

Example:

HOST=0.0.0.0
PORT=8000
API_BASE_URL=http://192.168.1.100:8000
CAMERA_SOURCE=0

Do not hardcode the example IP address.

The server must listen on an appropriate local network interface.

The frontend must use a configurable backend URL.

The application must work without external Internet access after dependencies and necessary recognition models have been installed.

Handle firewall restrictions and local network connection errors.

A USB webcam connected to the server is the initial development target. IP camera support can be implemented as an additional camera source.

---

## 10. PRIVACY AND SECURITY

This project uses biometric technology and must prioritize participant privacy.

Mandatory rules:

1. Only process participants who explicitly consent.
2. Offer manual interaction as an alternative.
3. Do not identify random visitors.
4. Do not claim a match when confidence is insufficient.
5. Do not store raw camera footage by default.
6. Keep biometric templates separate from profile data.
7. Restrict access to biometric storage.
8. Provide a mechanism to remove enrolled participants and their associated data.
9. Avoid exposing sensitive data through API responses.
10. Reset the visible participant session after the interaction.

Do not implement facial recognition using scraped photographs, social media pictures, or publicly collected face databases.

Use synthetic data for initial tests.

---

## 11. GITHUB WORKFLOW

The main branch is:

main

Each member must work on a separate branch.

Branch naming:

feature/ashly-*
feature/rafael-*
feature/yamil-*

Examples:

feature/ashly-welcome-screen
feature/rafael-api-client
feature/yamil-fastapi-backend

Rules:

1. Never commit directly to main.
2. Every task must have a GitHub Issue.
3. Every Issue must have one responsible assignee.
4. Use Pull Requests to integrate work.
5. Reference the Issue in the Pull Request.
6. Run relevant tests before merging.
7. Avoid modifying another member's assigned files without coordination.
8. Use descriptive commit messages.
9. Keep branches synchronized with main.
10. Require review before merging.

Suggested commit format:

feat(frontend): add welcome screen

feat(api): implement session endpoint

fix(camera): handle camera disconnection

test(backend): add profile repository tests

docs(project): update architecture

---

## 12. GITHUB ISSUE MANAGEMENT

When asked to initialize GitHub project tasks:

1. Inspect the existing repository.
2. Check the available collaborators.
3. Verify the GitHub usernames of Ashly, Rafael and Yamil.
4. Never guess GitHub usernames.
5. Create labels:
   - frontend
   - backend
   - computer-vision
   - integration
   - documentation
   - testing
   - priority-high
   - priority-medium
6. Create milestone:
   FACEBOT - MVP
7. Divide the implementation into small, independent Issues.
8. Assign each Issue to the correct verified GitHub collaborator.
9. Include a clear title.
10. Include context and implementation requirements.
11. Include acceptance criteria.
12. Include dependencies when necessary.
13. Reference the relevant directories.
14. Avoid duplicate Issues.
15. Do not assign one Issue to multiple people unless genuinely shared.
16. Do not start implementation until the initial architecture and task assignments are established.

If a collaborator cannot be found, create the Issue without assigning it and report the missing account.

Do not claim an Issue was created unless GitHub confirms its creation.

---

## 13. INITIAL DEVELOPMENT MILESTONES

### Milestone 1 — Project Foundation

- Repository setup.
- Folder structure.
- Python environment.
- Dependencies.
- Documentation.
- JSON sample database.

### Milestone 2 — Backend Foundation

- FastAPI initialization.
- Pydantic schemas.
- Health endpoint.
- Profile repository.
- Session endpoint.
- Backend tests.

### Milestone 3 — Frontend Foundation

- Flet initialization.
- Welcome screen.
- Waiting screen.
- Recognized screen.
- Unknown screen.
- Reusable components.

### Milestone 4 — API Integration

- HTTP client.
- Session polling or equivalent update mechanism.
- Navigation.
- Error handling.
- Reset functionality.

### Milestone 5 — Computer Vision

- Camera initialization.
- Face detection.
- Consent-aware enrollment.
- Local recognition.
- Confidence validation.
- Unknown-person handling.

### Milestone 6 — Final Integration

- Full application integration.
- Local Wi-Fi configuration.
- End-to-end testing.
- Exhibition preparation.
- Documentation.

---

## 14. DEVELOPMENT RULES FOR AI AGENTS

When developing this project:

- Read AGENTS.md before making changes.
- Inspect existing files before creating new ones.
- Do not overwrite working code without justification.
- Do not generate unnecessary modules.
- Do not introduce unnecessary dependencies.
- Keep modules small and reusable.
- Add type hints to important functions.
- Handle exceptions properly.
- Write tests for important functionality.
- Update documentation when architecture changes.
- Respect team ownership.
- Follow the API contract.
- Use mock data when a dependent module is not ready.
- Do not create fake implementations and describe them as production-ready.
- Never commit secrets, private keys, biometric templates, or personal participant data.

If a task is outside your assigned responsibility, create an Issue or coordinate with the responsible member instead of modifying their module.

---

## 15. DEFINITION OF DONE

A task is considered complete only when:

- Its implementation exists.
- Its acceptance criteria are satisfied.
- Relevant tests pass.
- Documentation is updated if necessary.
- It does not break existing modules.
- Its changes are submitted through a Pull Request.
- The Pull Request references the corresponding Issue.

The MVP is complete when:

1. Backend starts successfully.
2. Frontend starts successfully.
3. Frontend communicates with backend.
4. JSON profiles can be retrieved.
5. Session states are displayed correctly.
6. Camera status is available.
7. A consenting enrolled participant can be recognized in the supported test environment.
8. Unknown visitors are not falsely identified.
9. Personalized recommendations are displayed.
10. The experience can reset for the next participant.
11. The application operates on the local Wi-Fi network.

---

## 16. FINAL INSTRUCTION

Build FACEBOT as a unified, modular and maintainable university project.

Prioritize a working MVP over unnecessary complexity.

First establish the repository, architecture, contracts, GitHub Issues and team responsibilities.

Then implement each module in dependency order.

Do not assume that Ashly, Rafael or Yamil have completed work until the corresponding implementation and tests are verified.

All project decisions must remain consistent with this document.
