# Physical AI & Humanoid Robotics Textbook Platform API Contract

## Base URL: `https://api.robotics-textbook.example.com`

## Authentication
All endpoints require authentication via Bearer token in the Authorization header:
`Authorization: Bearer {jwt_token}`

---

## User Management

### GET /api/v1/users/profile
**Description**: Get current user's profile information.

**Response**:
- 200: User profile data
  ```json
  {
    "id": "uuid",
    "email": "user@example.com",
    "username": "username",
    "first_name": "John",
    "last_name": "Doe",
    "role": "USER|INSTRUCTOR|ADMIN",
    "created_at": "2023-01-01T00:00:00Z"
  }
  ```

### PUT /api/v1/users/profile
**Description**: Update current user's profile information.

**Request Body**:
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "username": "johndoe"
}
```

**Response**:
- 200: Updated profile data

---

## Textbook Content

### GET /api/v1/chapters
**Description**: List all textbook chapters with pagination.

**Query Parameters**:
- `page` (integer, optional): Page number (default: 1)
- `limit` (integer, optional): Items per page (default: 10, max: 50)
- `level` (string, optional): Filter by level (FOUNDATION|INTERMEDIATE|ADVANCED)
- `topic_area` (string, optional): Filter by topic area

**Response**:
- 200: List of chapters
  ```json
  {
    "items": [
      {
        "id": "uuid",
        "title": "Introduction to Embodied Intelligence",
        "slug": "intro-embodied-intelligence",
        "level": "FOUNDATION",
        "topic_area": "EMBODIED_INTELLIGENCE",
        "estimated_reading_time": 25,
        "order_index": 1,
        "created_at": "2023-01-01T00:00:00Z"
      }
    ],
    "total": 20,
    "page": 1,
    "limit": 10
  }
  ```

### GET /api/v1/chapters/{slug}
**Description**: Get a specific chapter by slug.

**Response**:
- 200: Chapter details
  ```json
  {
    "id": "uuid",
    "title": "Introduction to Embodied Intelligence",
    "slug": "intro-embodied-intelligence",
    "content": "# Markdown content here...",
    "level": "FOUNDATION",
    "topic_area": "EMBODIED_INTELLIGENCE",
    "estimated_reading_time": 25,
    "learning_objectives": [
      "Understand the concept of embodied intelligence",
      "Explain perception-cognition-action loops"
    ],
    "prerequisites": [
      "math-foundations",
      "programming-basics"
    ],
    "order_index": 1,
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
  }
  ```

---

## Learning Progress

### GET /api/v1/progress
**Description**: Get user's learning progress across all chapters.

**Response**:
- 200: Learning progress summary
  ```json
  {
    "total_chapters": 20,
    "completed_chapters": 5,
    "in_progress_chapters": 2,
    "progress_percent": 35.0,
    "time_spent_total": 7200,  // in seconds
    "chapters": [
      {
        "chapter_id": "uuid",
        "chapter_title": "Introduction to Embodied Intelligence",
        "status": "COMPLETED|IN_PROGRESS|NOT_STARTED",
        "completion_percentage": 1.0,
        "time_spent": 1800,
        "last_accessed": "2023-01-01T00:00:00Z",
        "assessment_scores": [85, 92]
      }
    ]
  }
  ```

### POST /api/v1/progress/{chapter_id}
**Description**: Update progress for a specific chapter.

**Request Body**:
```json
{
  "status": "IN_PROGRESS|COMPLETED",
  "completion_percentage": 0.5,
  "time_spent": 1800  // seconds spent since last update
}
```

**Response**:
- 200: Updated progress

---

## Assessments

### GET /api/v1/chapters/{chapter_id}/assessments
**Description**: Get assessments for a specific chapter.

**Response**:
- 200: List of assessments
  ```json
  {
    "assessments": [
      {
        "id": "uuid",
        "title": "Quiz: Embodied Intelligence Concepts",
        "description": "Test your understanding of embodied intelligence",
        "type": "QUIZ|EXERCISE|PROJECT|SIMULATION_TASK",
        "max_score": 100,
        "time_limit": 1800,
        "created_at": "2023-01-01T00:00:00Z"
      }
    ]
  }
  ```

### GET /api/v1/assessments/{assessment_id}
**Description**: Get details of a specific assessment.

**Response**:
- 200: Assessment details
  ```json
  {
    "id": "uuid",
    "chapter_id": "uuid",
    "title": "Quiz: Embodied Intelligence Concepts",
    "description": "Test your understanding of embodied intelligence",
    "type": "QUIZ",
    "questions": [
      {
        "id": "q1",
        "type": "MULTIPLE_CHOICE|TRUE_FALSE|SHORT_ANSWER",
        "question": "What is embodied intelligence?",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "correct_answer_index": 2
      }
    ],
    "max_score": 100,
    "time_limit": 1800
  }
  ```

### POST /api/v1/assessments/{assessment_id}/submit
**Description**: Submit answers for an assessment.

**Request Body**:
```json
{
  "answers": [
    {
      "question_id": "q1",
      "answer": "Option B"
    }
  ]
}
```

**Response**:
- 200: Submission result
  ```json
  {
    "id": "uuid",
    "assessment_id": "uuid",
    "user_id": "uuid",
    "answers": [
      {
        "question_id": "q1",
        "provided_answer": "Option B",
        "is_correct": true
      }
    ],
    "score": 85,
    "max_score": 100,
    "percentage": 85.0,
    "status": "GRADED",
    "graded_at": "2023-01-01T00:00:00Z",
    "feedback": "Good understanding of basic concepts, review advanced applications"
  }
  ```

---

## Simulation Management

### GET /api/v1/simulations
**Description**: List available simulation environments.

**Response**:
- 200: List of simulation environments
  ```json
  {
    "simulations": [
      {
        "id": "uuid",
        "name": "Gazebo Humanoid Simulator",
        "type": "GAZEBO",
        "version": "Harmonic",
        "description": "Simulation environment for humanoid robot control",
        "requirements": {
          "cpu": "4 cores",
          "memory": "8GB",
          "gpu": "Required"
        }
      }
    ]
  }
  ```

### POST /api/v1/simulations/{simulation_id}/instances
**Description**: Create a new simulation instance.

**Request Body**:
```json
{
  "name": "My Control Algorithm",
  "chapter_id": "uuid",
  "parameters": {
    "robot_model": "atlas",
    "environment": "simple_maze",
    "physics_rate": 1000
  }
}
```

**Response**:
- 201: New simulation instance
  ```json
  {
    "id": "uuid",
    "name": "My Control Algorithm",
    "user_id": "uuid",
    "simulation_env_id": "uuid",
    "chapter_id": "uuid",
    "state": "PENDING",
    "parameters": {
      "robot_model": "atlas",
      "environment": "simple_maze",
      "physics_rate": 1000
    },
    "created_at": "2023-01-01T00:00:00Z",
    "started_at": null,
    "completed_at": null
  }
  ```

### GET /api/v1/simulations/instances/{instance_id}
**Description**: Get details of a specific simulation instance.

**Response**:
- 200: Simulation instance details
  ```json
  {
    "id": "uuid",
    "name": "My Control Algorithm",
    "user_id": "uuid",
    "simulation_env_id": "uuid",
    "chapter_id": "uuid",
    "state": "RUNNING",
    "parameters": {
      "robot_model": "atlas",
      "environment": "simple_maze",
      "physics_rate": 1000
    },
    "results": {
      "duration": 180,  // seconds
      "distance_traveled": 5.2,  // meters
      "energy_consumed": 45.6  // units
    },
    "created_at": "2023-01-01T00:00:00Z",
    "started_at": "2023-01-01T00:00:00Z",
    "completed_at": null
  }
  ```

### POST /api/v1/simulations/instances/{instance_id}/control
**Description**: Send control commands to a running simulation.

**Request Body**:
```json
{
  "command": "move_forward|turn_left|turn_right|jump|stop",
  "parameters": {
    "velocity": 0.5,
    "duration": 2.0
  }
}
```

**Response**:
- 200: Command accepted
  ```json
  {
    "status": "accepted",
    "command": "move_forward",
    "timestamp": "2023-01-01T00:00:00Z"
  }
  ```

---

## AI Chat Interface

### POST /api/v1/ai/chat
**Description**: Send a message to the AI assistant for textbook-related help.

**Request Body**:
```json
{
  "message": "Explain how the perception-cognition-action loop works in humanoid robots",
  "context": {
    "chapter_slug": "embodied-intelligence",
    "section": "perception-cognition-action-loop"
  },
  "session_id": "uuid"  // optional, for conversation continuity
}
```

**Response**:
- 200: AI response
  ```json
  {
    "response": "The perception-cognition-action loop is fundamental to embodied intelligence...",
    "session_id": "uuid",
    "references": [
      {
        "type": "CHAPTER",
        "id": "uuid",
        "title": "Embodied Intelligence Fundamentals",
        "section": "perception-cognition-action-loop"
      }
    ],
    "confidence_score": 0.87
  }
  ```

### POST /api/v1/ai/search
**Description**: Semantic search in the textbook content using the vector store.

**Request Body**:
```json
{
  "query": "How do I implement stable locomotion in humanoid robots?",
  "max_results": 5,
  "filters": {
    "topic_area": "CONTROL_SYSTEMS",
    "level": "ADVANCED"
  }
}
```

**Response**:
- 200: Search results
  ```json
  {
    "results": [
      {
        "content_id": "uuid",
        "content_type": "CHAPTER|SECTION|CODE_EXAMPLE",
        "title": "Advanced Humanoid Locomotion",
        "excerpt": "Stable locomotion in humanoid robots requires...",
        "relevance_score": 0.92,
        "url": "/docs/advanced-locomotion"
      }
    ]
  }
  ```