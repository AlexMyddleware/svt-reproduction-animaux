# Export Feature Analysis: SVT Reproduction Animaux → Next.js Migration

## Overview
This document lists all features from the current Flask-based learning game that you haven't mentioned in your migration plan, as well as features you described that work differently in the actual project.

---

## PART 1: Features NOT Mentioned in Your Migration Plan

### 1. Anki Desktop Integration (Complete System)
**This is a major feature that wasn't mentioned at all.**

- **Anki Connection Page** (`anki.html`)
  - Connection status indicator
  - Deck listing and selection
  - Authentication status display
  - Error diagnosis with helpful suggestions
  - Connection testing functionality

- **Anki Training Interface** (`anki_training.html`)
  - Card display with formatted question/answer
  - Four response buttons for spaced repetition:
    - "Again" (ease 1) - Mark as difficult
    - "Hard" (ease 2) - Mark as moderately hard
    - "Good" (ease 3) - Mark as correctly answered
    - "Easy" (ease 4) - Mark as very easy
  - Progress indicator
  - Real-time sync with Anki desktop application via AnkiConnect API

- **Anki Backend Services**
  - `anki_service.py`: API communication with Anki
  - `anki_config.py`: Configuration for Anki endpoint (http://127.0.0.1:8765)
  - `anki_error_handler.py`: Detailed error diagnosis and user-friendly suggestions
  - `anki_training_service.py`: Card retrieval and answer submission
  - `anki_card_formatter.py`: HTML parsing and content extraction

### 2. Second Game Type: Image Matching (Relier les Images)
**You only mentioned the multiple-choice quiz. This is a completely different game type.**

- **Image Matching Game** (`relier_images.html`)
  - Central image display as the "question"
  - Multiple word options arranged around the screen
  - Draw-line connection mechanism:
    - Click and hold on central image
    - Drag to word to create connection line
    - Line turns green if correct match
    - Line turns red and disappears if incorrect match
  - SVG-based line drawing for connection visualization
  - Touch-enabled for mobile devices
  - Real-time line following mouse cursor
  - Automatic answer validation on connection completion

- **Data Structure for Image Matching:**
```json
{
    "id": 1,
    "image_path": "path/to/image.jpg",
    "correct_word": "correct answer",
    "incorrect_words": ["wrong1", "wrong2", "wrong3", "wrong4"]
}
```

### 3. Folder Hierarchy and Organization System
**You mentioned a list of decks, but didn't describe the full folder organization system.**

- **Hierarchical Folder Structure**
  - Nested folders and subfolders
  - Expandable/collapsible tree view
  - Folder operations:
    - Create new folders
    - Rename folders
    - Delete folders (with confirmation)
    - Move folders between locations
    - Drag-and-drop reorganization

- **Questions Management Tree Interface** (`questions_tree.html`)
  - Visual tree representation of all content
  - Game type selector (switch between Fill-in-blank and Image Matching)
  - Folder-specific action buttons
  - Fold all / Unfold all buttons
  - Per-folder statistics display

### 4. Focus Mode System
**You mentioned a "focus" button but didn't describe how it actually works.**

- **How Focus Mode Works:**
  1. User selects "Focus" on a folder in the management tree
  2. All sibling folders are automatically moved to a `.focused_backup_[folder_name]` directory
  3. Only the focused folder remains visible in the game
  4. URL includes `focus=folder_name` parameter
  5. Game only loads and shows questions from the focused folder
  6. Focus indicator banner displays during gameplay (purple border)
  7. Quick unfocus button in game UI
  8. Unfocus restores all backup folders from hidden directory
  9. Backup directory is automatically cleaned up

- **Technical Implementation:**
  - Physical file system manipulation (moves actual folders)
  - Hidden backup directories (prefixed with `.`)
  - URL parameter tracking
  - Automatic detection on page load
  - Survives app restart

### 5. Complete Settings System
**You mentioned font and color, but there's more.**

- **Font Family Selection** (7 options):
  1. Atkinson Hyperlegible (default, accessibility-focused)
  2. Orbitron (retro sci-fi style)
  3. Serif (Georgia)
  4. Sans-serif (Segoe UI)
  5. Monospace (Courier New)
  6. Cursive (Comic Sans MS)
  7. Fantasy (Impact)

- **Auto-validate Setting:**
  - Checkbox to automatically mark questions as completed when answered correctly
  - Persistent across sessions
  - Affects game behavior globally

- **Live Preview Areas:**
  - Real-time font preview
  - Real-time color preview
  - Immediate visual feedback on changes

### 6. Advanced Physics System
**You mentioned random movement but not the physics engine.**

- **Physics Engine Features:**
  - Gravity-based word floating
  - Velocity and acceleration calculations
  - Time-delta based updates for smooth animation
  - Pausable during drag operations
  - Elasticity on boundary collision

- **Collision System:**
  - Bounding box collision detection (AABB)
  - Continuous collision response
  - Directional bounce calculations
  - Multiple simultaneous collision handling
  - Collision spark effects with particles
  - Colored glow effects (neon colors)
  - Flash effects at collision point

- **Boundary Handling:**
  - Container boundary enforcement
  - Position clamping
  - Velocity reflection on boundary hit
  - Words never go off-screen

- **Modular JavaScript Architecture:**
  - `physics_calculations.js`: Velocity and acceleration
  - `collision_system.js`: Collision detection and response
  - `boundary_handling.js`: Container enforcement
  - `physics_manager.js`: Coordinates all physics operations
  - `option_physics.js`: Individual option physics

### 7. Retro 80s Disco Theme
**You mentioned no visual theme.**

- **Complete Neon/Retro Visual Design:**
  - Neon color palette (pink, cyan, purple, green, yellow)
  - Glowing text effects with drop shadows
  - CRT scanline overlay effect
  - Chrome gradient text effect with 5s pulse animation
  - Dark background with subtle grid pattern
  - Glow animations on hover
  - Scale transforms on button interactions
  - Message slide down animation
  - Bounce effects (multiple directions)
  - Collision sparks animation (500ms)
  - Fade effects on state changes

### 8. Detailed Statistics System
**You mentioned statistics but not the full implementation.**

- **Game-Level Statistics:**
  - Separate scores for each game type (Fill-in-blank and Image Matching)
  - Persistent storage in `assets/Data/scores.json`
  - Session-based tracking synchronized with file
  - Display on main menu
  - Display in game interface
  - Manual reset option from main menu

- **Question-Level Statistics:**
  - Correct answer count per question
  - Wrong answer count per question
  - Completion status (boolean flag)
  - Statistics visible in management tree
  - Stored in individual question JSON files
  - Automatic increment on answer validation

### 9. Create Question Interface
**You mentioned upload for new decks, but there's a detailed creation form.**

- **Question Creation Form** (`create_question.html`)
  - Game type selector (Fill-in-blank vs Image Matching)
  - For Fill-in-blank questions:
    - Question text input
    - Multiple answer option input fields (4 options)
    - Correct answer selection dropdown
    - Validation to ensure correct answer matches an option
  - For Image Matching questions:
    - Question text input
    - Image path/selection with file browser
    - Correct word input
    - Multiple incorrect word inputs (array of 4)
  - Form validation with error messaging
  - Success/error notification system
  - Return to menu button

### 10. Desktop Application Features
**The current app is a bundled desktop app, not a web app.**

- **PyInstaller Bundled Executable:**
  - Standalone desktop application
  - No web server required for end users
  - Runs locally with Flask backend
  - File system access for question management
  - Quit button to close application
  - Unsaved changes tracking
  - Window close handling

- **Local File System Integration:**
  - Direct folder and file manipulation
  - File browser for image selection
  - JSON file editing
  - Folder tree management
  - Physical file movement for focus mode

### 11. Navigation and UI Controls
**More detailed than mentioned.**

- **In-Game Navigation:**
  - "Valider" (Validate) button - Submit answer
  - "Réinitialiser" (Reset) button - Clear answer and restart word movement
  - "Précédent" (Previous) button - Go to previous question (when available)
  - "Suivant" (Next) button - Go to next question (when available)
  - "Retour au menu" (Return to menu) button
  - Question counter display (e.g., "Question 1 / 20")
  - Real-time score display

- **Main Menu Options (8 buttons):**
  1. Texte à trous (Fill-in-the-blank game)
  2. Relier les images (Image matching game)
  3. Créer une question (Create new questions)
  4. Gérer les questions (Manage/organize questions)
  5. Page Anki (Anki integration)
  6. Réinitialiser les scores (Reset scores)
  7. Paramètres (Settings)
  8. Quitter (Quit application)

- **Score Display on Main Menu:**
  - Texte à trous score
  - Relier les images score
  - Both scores shown simultaneously

### 12. Visual Feedback Systems
**More detailed than the simple animations you mentioned.**

- **Answer Validation Feedback:**
  - Green border on blank when correct answer is placed
  - Red border and bounce-back animation when incorrect
  - Text color changes on blank area
  - Option highlighting during drag
  - Animated transitions between states

- **Interactive Element Feedback:**
  - Hover effects on buttons (scale + glow)
  - Active states on forms
  - Focus states on inputs
  - Drag-over highlighting
  - Button press feedback with transform
  - Drop zone visual indication

- **Status Indicators:**
  - Question counter (e.g., "5/20")
  - Progress indication
  - Focus mode banner with purple border
  - Score display in game header
  - Statistics in management tree
  - Connection status for Anki

### 13. Drag-and-Drop for Tree Management
**Different from question answering drag-drop.**

- **Tree Reorganization:**
  - Drag questions between folders
  - Drag folders to new locations
  - Visual drag indicator
  - Drop zone highlighting
  - Confirmation on drop
  - Multi-level hierarchy support

### 14. Keyboard and Touch Support
**Not mentioned.**

- **Keyboard Support:**
  - Form submission with Enter key
  - Menu navigation via Tab key
  - Escape key handling for dialogs

- **Touch Support:**
  - Touch-enabled line drawing for image matching
  - Mobile-friendly drag-and-drop
  - Touch event handlers

### 15. Error Handling and Diagnostics
**Not mentioned.**

- **Anki Error Diagnosis:**
  - Detailed error analysis
  - Suggests possible causes
  - Provides user-friendly suggestions
  - Handles network errors, authentication issues, API errors
  - Connection testing with feedback

- **Form Validation:**
  - Required field checking
  - Option validation (correct answer must match an option)
  - Error messaging system
  - Success notifications

### 16. Session Management
**Different from user authentication.**

- **Flask Session System:**
  - Session per browser instance
  - Unique secret key per application instance
  - Session data for debugging (when enabled)
  - Scores stored per session + persistent file backup
  - No traditional user login/logout
  - Single-user local application

### 17. Logging and Debug System
**Not mentioned.**

- **Conditional Logging:**
  - Debug logging based on environment variable
  - `conditional_log()` utility function
  - `log_if_enabled()` decorator for function logging
  - Contextual debug information
  - Performance monitoring points
  - Error reporting helpers

### 18. Question Navigation System
**More complex than simple next/previous.**

- **Advanced Navigation:**
  - Sequential navigation (Next/Previous buttons)
  - Direct question ID access via URL parameters
  - Auto-redirect to first question if current doesn't exist
  - Question counting system
  - Active (non-completed) question filtering
  - Focus-aware navigation (only shows focused folder questions)

### 19. Data Persistence Architecture
**Not mentioned.**

- **Dual Persistence System:**
  - Session-based state tracking (in-memory)
  - File-based persistent storage (JSON files)
  - Synchronization between session and files
  - Automatic file creation with defaults if missing
  - Recovery from JSON files on restart

- **File Locations:**
  - Questions: `assets/Data/fill_the_blanks/` and `assets/Data/image_matching/`
  - Scores: `assets/Data/scores.json`
  - Settings: `assets/settings.json`

### 20. Completion Status System
**Different from simple progress tracking.**

- **Question Completion:**
  - Boolean "completed" flag per question
  - Stored in question JSON file
  - Can be toggled manually in management tree
  - Auto-set on correct answer (if auto_validate enabled)
  - Affects which questions appear in game
  - Used for progress tracking

- **Active Question Filtering:**
  - Game only shows non-completed questions
  - Loop back to first active question when reaching end
  - Manual completion toggle available

---

## PART 2: Features You Mentioned That Work DIFFERENTLY

### 1. User Management System
**What you said:**
> "here are the components for the user management system:
> 1. User Authentication Component
> 2. Database Connection Component
> 3. Login Form Component
> 4. Registration Form Component
> 5. User Dashboard Component
> 6. Logout Functionality Component"

**How it actually works:**
- **NO user authentication system exists**
- **NO login/registration forms**
- **NO user accounts or profiles**
- **NO logout functionality**
- It's a single-user desktop application
- Uses Flask sessions for temporary state only
- No database connection for users
- Settings are global (not per-user)

**Migration Note:** You'll need to build the entire user authentication system from scratch if you want multi-user support.

---

### 2. "List of Decks" Interface
**What you said:**
> "There is a list of the decks of questions, if the user clicks on the deck, it starts playing the deck"

**How it actually works:**
- There is **NO simple list of decks**
- Instead, there's a **hierarchical folder tree** with nested folders
- The interface is a management tree (`questions_tree.html`) with:
  - Expandable/collapsible folders
  - Multiple action buttons per folder (focus, rename, delete, create subfolder)
  - Questions nested under folders
  - Drag-and-drop reorganization
  - Separate view for Fill-in-blank and Image Matching questions
- To play a deck, users go to main menu and select game type
- The game shows ALL active (non-completed) questions by default
- Users can "focus" a folder to play only those questions

**Migration Note:** You'll need to decide:
- Do you want the simple "list of decks" approach you described?
- Or do you want the current complex hierarchical folder system?
- The current system is much more complex to implement

---

### 3. "Upload Components for New Decks"
**What you said:**
> "There is an upload components for new decks"

**How it actually works:**
- **NO deck upload feature exists**
- **NO bulk question import**
- Instead, there's a **single question creation form**
- Users create questions ONE AT A TIME via form
- Form inputs:
  - Question text
  - Answer options (manual entry)
  - Correct answer selection
  - Image selection (for image matching type)
- Questions are saved as individual JSON files
- File naming: `question001.json`, `question002.json`, etc.
- No CSV import, no JSON upload, no bulk operations

**Migration Note:** You should add bulk upload if you want users to import multiple questions at once.

---

### 4. Question Schema
**What you said:**
```json
{
    "text": "The question text goes here",
    "options": ["Answer choice 1", "Answer choice 2", "Answer choice 3", "Answer choice 4"],
    "correct_answer": "Answer choice 2",
    "completed": false,
    "statistics": {
        "correct_answers": 0,
        "wrong_answers": 0
    }
}
```

**How it actually works:**
This is **ONLY for Fill-in-the-Blank questions**. But there are **TWO question types**:

**Fill-in-the-Blank Schema:**
```json
{
    "text": "Question text with blank: ____",
    "options": ["option1", "option2", "option3", "option4"],
    "correct_answer": "option1",
    "completed": false,
    "statistics": {
        "correct_answers": 0,
        "wrong_answers": 0
    }
}
```

**Image Matching Schema:**
```json
{
    "id": 1,
    "image_path": "path/to/image.jpg",
    "correct_word": "correct answer",
    "incorrect_words": ["wrong1", "wrong2", "wrong3", "wrong4"]
}
```

**Migration Note:** You need to handle BOTH question types, not just multiple-choice.

---

### 5. Answer Movement Behavior
**What you said:**
> "when inside the questions interface, the possible answers move around randomly"

**How it actually works:**
- **NOT random movement**
- It's a **physics-based simulation** with:
  - Gravity and velocity
  - Acceleration calculations
  - Collision detection between answers
  - Boundary enforcement (answers bounce off walls)
  - Elasticity on collisions
  - Time-delta based smooth animation
  - Configurable speed (20-500ms update frequency)
  - Pause when dragging

**Migration Note:** "Random movement" is much simpler to implement than the current physics engine. Decide if you want:
- Simple random position changes (easier)
- Full physics simulation (more engaging but complex)

---

### 6. Speed Slider
**What you said:**
> "the user has a slider that can adjust the speed of the movement from very slow (left side of the slider) to very fast (right side of the slider)"

**How it actually works:**
- Speed slider exists, but it works **INVERSELY**
- Range: 20ms to 500ms (update interval)
- LEFT side (20ms) = **TRÈS RAPIDE** (very fast, more frequent updates)
- RIGHT side (500ms) = **TRÈS LENT** (very slow, less frequent updates)
- Display shows percentage: 25% to 250%
- Lower milliseconds = faster movement
- Higher milliseconds = slower movement

**Migration Note:** The logic is reversed from typical slider expectations. Decide if you want:
- Left = slow, Right = fast (typical)
- Current system where lower interval = faster

---

### 7. Collision Behavior
**What you said:**
> "When moving, the answers should not collide with each other, they should adjust their trajectory to avoid overlapping."

**How it actually works:**
- Answers **DO collide with each other**
- Collisions are a **feature**, not avoided
- When answers collide:
  - They bounce off each other
  - Collision spark effects appear
  - Colored glow effects
  - Flash at collision point
  - Directional bounce calculations
- Collision effects can be toggled on/off

**Migration Note:** You described collision avoidance. The current app has collision detection and visual effects. Decide which approach you prefer.

---

### 8. Wrong Answer Behavior
**What you said:**
> "If the user answers wrongly, the selected answer goes back to moving but it is now highlighted in red for 2 seconds before resuming movement."

**How it actually works:**
- Wrong answers show **red border on the blank area** (not on the option itself)
- The option **bounces back to original position** (animated)
- It **immediately resumes normal movement** (no 2-second delay)
- No red highlighting of the option itself
- No timed color change
- Visual feedback is on the drop target, not the dragged element

**Migration Note:** Your description is different. Decide if you want:
- Red highlight on the option for 2 seconds (your description)
- Red border on blank + bounce back (current behavior)

---

### 9. Success Animation
**What you said:**
> "if the user answers correctly, there is a success animation and the game moves on to the next question."

**How it actually works:**
- Green border on blank area (not a full animation)
- **Does NOT automatically move to next question**
- User must click "Suivant" (Next) button
- OR user must click "Valider" button again
- No confetti, no celebration animation, no auto-advance

**Migration Note:** You described auto-advance. Current app requires manual navigation.

---

### 10. User Dashboard Features
**What you said:**
> "In the User Dashboard, there is a play button that immediately starts the last played deck."

**How it actually works:**
- **NO "User Dashboard" exists**
- The **Main Menu** is the landing page
- **NO "last played deck" tracking**
- **NO quick-play button for last deck**
- Users must:
  1. Choose game type (Fill-in-blank OR Image Matching)
  2. Game loads ALL active questions
  3. Or use focus mode to filter to specific folder

**Migration Note:** You'll need to add:
- Last played deck tracking
- Quick resume functionality
- Actual user dashboard

---

### 11. Deck Actions
**What you said:**
> "each deck has a button to focus the deck or reset the progress (will set all the 'completed': true / false flags to false for the questions in that deck)"

**How it actually works:**
- Focus button exists ✓
- **NO "reset progress" button per deck**
- Only a **global "Reset Scores"** button on main menu
- Resets ALL scores for BOTH game types
- No per-deck or per-folder reset
- Completion flags are not easily bulk-reset
- Individual questions can be toggled in management tree

**Migration Note:** Add per-deck reset if you want granular control.

---

### 12. Statistics Reset
**What you said:**
> "each deck also has a button to reset the statistics (sets correct_answers and wrong_answers to 0 for the questions in that deck)"

**How it actually works:**
- **NO per-deck statistics reset button**
- Only global score reset from main menu
- No way to reset per-question statistics in UI
- Would require manual JSON file editing
- Statistics are stored in individual question files

**Migration Note:** Add per-deck or per-question statistics reset functionality.

---

### 13. Mobile Optimization
**What you said:**
> "it is a learning game website optimized for mobile, assuming the user holds the phone in landscape mode with both hands and uses their thumbs to interact with the interface."

**How it actually works:**
- It's a **desktop application** (PyInstaller bundled)
- **NOT optimized for mobile**
- Designed for desktop browser window
- Some touch support exists (for image matching line drawing)
- No specific landscape orientation handling
- No thumb-zone optimization
- No mobile-specific UI adjustments

**Migration Note:** You'll need to add mobile optimization from scratch, including:
- Landscape orientation lock/preference
- Thumb-zone button placement
- Touch-optimized drag-and-drop
- Responsive design for mobile screens

---

### 14. No Scrolling Requirement
**What you said:**
> "During the quiz, there should be no scrolling horizontally or vertically, the entire interface should fit within the screen."

**How it actually works:**
- This is **mostly true** for the game interface
- Fill-in-blank game fits in viewport
- Image matching game fits in viewport
- BUT:
  - Management tree DOES scroll (vertical)
  - Settings page DOES scroll (vertical)
  - Main menu fits without scrolling
  - Create question form DOES scroll

**Migration Note:** Current game screens honor this, but management interfaces don't.

---

### 15. Font Specification
**What you said:**
> "The font for the questions and answer should be Atkinson Hyperlegible."

**How it actually works:**
- Atkinson Hyperlegible is the **default** font
- But users can **change it** in settings to 6 other fonts:
  - Orbitron
  - Serif (Georgia)
  - Sans-serif (Segoe UI)
  - Monospace (Courier New)
  - Cursive (Comic Sans MS)
  - Fantasy (Impact)
- Global font setting applies to entire app

**Migration Note:** Decide if you want:
- Fixed Atkinson Hyperlegible font (your description)
- User-selectable fonts (current implementation)

---

### 16. Database System
**What you said:**
> "using the database system neon"

**How it actually works:**
- **NO database**
- **NO Neon**
- **NO PostgreSQL, MySQL, MongoDB, or any DB**
- Everything is **JSON files** on the file system:
  - Questions: Individual JSON files
  - Scores: Single JSON file
  - Settings: Single JSON file
- File-based persistence only

**Migration Note:** You'll need to:
- Set up Neon database
- Design SQL schemas
- Migrate all JSON data to database tables
- Implement database queries instead of file operations

---

### 17. Deployment Platform
**What you said:**
> "we are making a website that will be deployed on vercel, it is a learning game website using vercel and next.js"

**How it actually works:**
- **NOT a website**
- It's a **desktop application** (PyInstaller executable)
- Uses Flask backend (Python)
- Runs locally on user's computer
- No Vercel deployment
- No Next.js
- No web hosting needed

**Migration Note:** This is a complete rebuild:
- From Flask to Next.js
- From desktop to web
- From local files to database
- From Python to JavaScript/TypeScript
- Complete architecture change

---

## PART 3: Additional Considerations for Migration

### Technology Stack Differences

**Current Stack:**
- Backend: Flask (Python)
- Frontend: HTML5, CSS3, vanilla JavaScript
- Storage: JSON files
- Deployment: Desktop executable (PyInstaller)
- Server: Waitress (WSGI)

**Target Stack (Based on your description):**
- Backend: Next.js API routes (Node.js)
- Frontend: React (Next.js)
- Storage: Neon (PostgreSQL)
- Deployment: Vercel
- Server: Vercel serverless functions

**What needs to be rebuilt:**
- Entire backend in JavaScript/TypeScript
- Frontend components in React
- Database migrations and queries
- Authentication system (doesn't exist currently)
- File upload system (doesn't exist currently)

### Features That Are Desktop-Specific

These will need alternative implementations:
1. Quit button → Not applicable for web
2. File system folder manipulation → Database folder relationships
3. Physical file movement for focus mode → Database queries with filters
4. PyInstaller executable → Vercel web deployment
5. Local file storage → Remote database storage
6. Window close handling → Browser tab close handling

### Missing Features You'll Need to Build

1. **User authentication** (login, registration, logout)
2. **User profiles** and per-user data isolation
3. **Deck upload** system (CSV, JSON, or form-based)
4. **Last played deck** tracking
5. **Quick resume** functionality
6. **Per-deck progress reset**
7. **Per-deck statistics reset**
8. **Mobile optimization** (landscape, thumb zones)
9. **Database schema** design and migrations
10. **Multi-user support** (deck sharing, privacy settings)

### Features You May Want to Simplify

1. **Physics engine** → Simple random movement
2. **Collision system** → Collision avoidance
3. **Hierarchical folders** → Flat deck list
4. **Two game types** → Focus on one initially
5. **Anki integration** → Skip unless needed
6. **Desktop-style file management** → Web-based deck management

---

## Summary

**Major features you didn't mention:**
- Anki integration (complete system)
- Image matching game (second game type)
- Hierarchical folder organization
- Advanced physics engine
- Retro 80s visual theme
- Complete settings system
- Question creation form
- Desktop application architecture

**Features that work differently:**
- No user authentication (you described full user system)
- Hierarchical folders (you described simple deck list)
- No deck upload (you described upload component)
- Physics simulation (you described random movement)
- Collisions are a feature (you described collision avoidance)
- Manual navigation (you described auto-advance)
- Desktop app (you described web app)
- JSON files (you described Neon database)

**Recommendation:**
Before starting migration, decide:
1. Do you want to replicate ALL features or simplify?
2. Which game type(s) to implement first?
3. Simple deck list or hierarchical folders?
4. Physics engine or simple movement?
5. Which visual theme (retro or modern)?
6. Anki integration or skip it?

This will significantly affect development time and complexity.
