---

description: "Task list for creating a Streamlit app to display the Physical AI & Humanoid Robotics book"
---

# Tasks: Streamlit Book Display Application

**Input**: Design documents from `/specs/001-create-robotics-textbook/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: No explicit tests requested in feature specification, but following best practices with pytest for backend and streamlit components.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file path in description

## Path Conventions

- **Streamlit app**: `streamlit_app/` directory
- **Backend (FastAPI)**: `backend/src/`
- **Docusaurus site**: `my-website/`

## Phase 1: Setup (Streamlit Project Structure)

**Purpose**: Set up Streamlit project structure and dependencies for book display

- [ ] T001 Create streamlit_app directory for the Streamlit application
- [ ] T002 Create requirements.txt for Streamlit app with necessary dependencies in streamlit_app/requirements.txt
- [ ] T003 Set up basic Streamlit app structure in streamlit_app/main.py
- [ ] T004 Configure API connection to backend in streamlit_app/config.py

---

## Phase 2: Foundational (Streamlit Core Infrastructure)

**Purpose**: Core Streamlit infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 Create base Streamlit layout and navigation in streamlit_app/main.py
- [ ] T006 Implement API client to connect with backend in streamlit_app/api_client.py
- [ ] T007 Create utility functions for content retrieval in streamlit_app/utils.py
- [ ] T008 Design base UI components for book display in streamlit_app/components.py
- [ ] T009 Implement authentication handling in streamlit_app/auth.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Foundation Robotics Education (Priority: P1) 🎯 MVP

**Goal**: Create the foundational content display in Streamlit to show the first chapters about embodied intelligence.

**Independent Test**: Streamlit app successfully displays foundational robotics education content allowing students to understand core principles.

### Implementation for User Story 1

- [ ] T010 [P] [US1] Create chapter listing view in streamlit_app/pages/chapter_list.py
- [ ] T011 [P] [US1] Create individual chapter display view in streamlit_app/pages/chapter_view.py
- [ ] T012 [US1] Implement GET chapters functionality from backend API in streamlit_app/api_client.py
- [ ] T013 [US1] Create navigation controls within chapters in streamlit_app/components.py
- [ ] T014 [US1] Design textbook styling for Streamlit in streamlit_app/style.css
- [ ] T015 [US1] Implement chapter progress tracking in streamlit_app/progress.py
- [ ] T016 [US1] Create table of contents sidebar in streamlit_app/components.py
- [ ] T017 [US1] Add basic search functionality in streamlit_app/search.py
- [ ] T018 [US1] Test foundational content display in Streamlit app

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Simulation-Based Learning (Priority: P2)

**Goal**: Integrate simulation content and controls into the Streamlit app to allow practitioners to learn about simulation workflows.

**Independent Test**: Streamlit app successfully displays simulation tutorials with integrated simulation controls and visualizations.

### Implementation for User Story 2

- [ ] T019 [P] [US2] Create simulation environment listing in streamlit_app/pages/sim_envs.py
- [ ] T020 [P] [US2] Create simulation instance creation UI in streamlit_app/pages/create_sim.py
- [ ] T021 [US2] Implement simulation API integration in streamlit_app/api_client.py
- [ ] T022 [US2] Create simulation control interface in streamlit_app/components.py
- [ ] T023 [US2] Add simulation visualization components in streamlit_app/viz.py
- [ ] T024 [US2] Design simulation parameter controls in streamlit_app/components.py
- [ ] T025 [US2] Create simulation results display in streamlit_app/pages/sim_results.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Advanced Humanoid Control (Priority: P3)

**Goal**: Display advanced control systems content with integrated AI assistance in Streamlit for experienced robotics engineers.

**Independent Test**: Streamlit app successfully presents advanced humanoid control content with interactive examples and AI-based explanations.

### Implementation for User Story 3

- [ ] T026 [P] [US3] Create AI assistant interface in streamlit_app/pages/ai_assistant.py
- [ ] T027 [P] [US3] Implement AI chat functionality from backend in streamlit_app/api_client.py
- [ ] T028 [US3] Create code example viewer in streamlit_app/components.py
- [ ] T029 [US3] Add syntax highlighting for code examples in streamlit_app/viz.py
- [ ] T030 [US3] Implement interactive code components in streamlit_app/components.py
- [ ] T031 [US3] Create ROS2 control system visualization in streamlit_app/viz.py
- [ ] T032 [US3] Add vision-language-action examples display in streamlit_app/pages/vla_examples.py

**Checkpoint**: User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Integrated Practical Application (Priority: P4)

**Goal**: Provide comprehensive course materials display in Streamlit for instructors to build complete courses.

**Independent Test**: Streamlit app successfully serves as the foundation for complete university courses with integrated assessment and progress tracking.

### Implementation for User Story 4

- [ ] T033 [US4] Create assessment display in streamlit_app/pages/assessments.py
- [ ] T034 [US4] Create course curriculum view in streamlit_app/pages/curriculum.py
- [ ] T035 [US4] Add instructor dashboard in streamlit_app/pages/instructor_dash.py
- [ ] T036 [US4] Create exercise and project display in streamlit_app/pages/exercises.py
- [ ] T037 [US4] Implement syllabus and lesson plan templates in streamlit_app/pages/syllabus.py
- [ ] T038 [US4] Add course progress visualization in streamlit_app/viz.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T039 [P] Add responsive design improvements for Streamlit app
- [ ] T040 [P] Implement dark/light theme toggle in streamlit_app/main.py
- [ ] T041 [P] Add accessibility features for textbook content
- [ ] T042 [P] Create comprehensive error handling for content loading
- [ ] T043 [P] Add performance optimization for content rendering
- [ ] T044 [P] Implement bookmark/favorite functionality
- [ ] T045 [P] Add content rating and feedback system
- [ ] T046 [P] Create print/export functionality for chapters
- [ ] T047 [P] Add search functionality across all content
- [ ] T048 Run end-to-end tests to validate complete Streamlit book display functionality

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Integrates with US1/US2/US3 components but should be independently testable

### Within Each User Story

- UI components before API integration
- Core display functionality before advanced features
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Different user stories can be worked on in parallel by different team members

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test Streamlit book display for foundational content only
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence