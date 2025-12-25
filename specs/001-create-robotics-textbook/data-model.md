# Data Model: Physical AI & Humanoid Robotics Textbook Platform

## Overview

This document defines the data models for the Physical AI & Humanoid Robotics textbook platform, based on the entities identified in the feature specification and requirements from the Physical AI & Humanoid Robotics Course Constitution.

## Core Entities

### User

Represents a learner, instructor, or administrator using the platform.

**Fields**:
- `id` (UUID): Unique identifier
- `email` (String): User's email address
- `username` (String): Unique username
- `first_name` (String): User's first name
- `last_name` (String): User's last name
- `role` (Enum): USER, INSTRUCTOR, ADMIN
- `created_at` (DateTime): Account creation timestamp
- `updated_at` (DateTime): Last update timestamp
- `last_login` (DateTime): Last login timestamp
- `is_active` (Boolean): Whether the account is active

### Textbook Chapter

Represents a chapter in the Physical AI & Humanoid Robotics textbook.

**Fields**:
- `id` (UUID): Unique identifier
- `title` (String): Chapter title
- `slug` (String): URL-friendly identifier
- `content` (Text): Markdown content of the chapter
- `level` (Enum): FOUNDATION, INTERMEDIATE, ADVANCED
- `topic_area` (Enum): EMBODIED_INTELLIGENCE, SIMULATION, CONTROL_SYSTEMS, VISION_LANGUAGE_ACTION
- `estimated_reading_time` (Integer): In minutes
- `order_index` (Integer): Position in the textbook sequence
- `prerequisites` (JSON): List of prerequisite chapters or concepts
- `learning_objectives` (JSON): List of learning objectives
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp

### Simulation Environment

Represents a simulation environment available in the platform (Gazebo, Unity, NVIDIA Isaac).

**Fields**:
- `id` (UUID): Unique identifier
- `name` (String): Name of the simulation environment
- `type` (Enum): GAZEBO, UNITY, NVIDIA_ISAAC, CUSTOM
- `version` (String): Version of the simulation environment
- `description` (Text): Description of the environment
- `assets_path` (String): Path to simulation assets
- `config_template` (JSON): Configuration template for new instances
- `requirements` (JSON): System requirements
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp

### Simulation Instance

Represents a running instance of a simulation.

**Fields**:
- `id` (UUID): Unique identifier
- `user_id` (UUID): Reference to the user running the simulation
- `simulation_env_id` (UUID): Reference to the simulation environment
- `chapter_id` (UUID): Reference to the textbook chapter
- `name` (String): Name of the simulation instance
- `state` (Enum): PENDING, RUNNING, PAUSED, COMPLETED, ERROR
- `parameters` (JSON): Configuration parameters for this instance
- `results` (JSON): Simulation results and metrics
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp
- `started_at` (DateTime): When simulation started
- `completed_at` (DateTime): When simulation completed

### Learning Progress

Tracks a user's progress through the textbook and related activities.

**Fields**:
- `id` (UUID): Unique identifier
- `user_id` (UUID): Reference to the user
- `chapter_id` (UUID): Reference to the chapter
- `status` (Enum): NOT_STARTED, IN_PROGRESS, COMPLETED
- `completion_percentage` (Float): Percentage completed (0.0 to 1.0)
- `time_spent` (Integer): Time spent in seconds
- `last_accessed` (DateTime): Last time chapter was accessed
- `assessment_scores` (JSON): Scores for chapter assessments
- `simulation_attempts` (JSON): Summary of related simulation attempts
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp

### Question & Answer Session

Represents an interaction with the AI chatbot.

**Fields**:
- `id` (UUID): Unique identifier
- `user_id` (UUID): Reference to the user
- `session_id` (UUID): Grouping identifier for related questions
- `question` (Text): The question asked by the user
- `answer` (Text): The AI-generated response
- `context_used` (JSON): Vector store references used for the answer
- `confidence_score` (Float): Confidence level of the response
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp

### Assessment

Represents an assessment (quiz, exercise) associated with a chapter.

**Fields**:
- `id` (UUID): Unique identifier
- `chapter_id` (UUID): Reference to the chapter
- `title` (String): Assessment title
- `description` (Text): Description of the assessment
- `type` (Enum): QUIZ, EXERCISE, PROJECT, SIMULATION_TASK
- `questions` (JSON): List of questions with possible answers
- `max_score` (Integer): Maximum possible score
- `time_limit` (Integer): Time limit in seconds (null if no limit)
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp

### Assessment Submission

Represents a user's submission for an assessment.

**Fields**:
- `id` (UUID): Unique identifier
- `assessment_id` (UUID): Reference to the assessment
- `user_id` (UUID): Reference to the user
- `answers` (JSON): User's answers to the questions
- `score` (Integer): Score achieved
- `status` (Enum): SUBMITTED, GRADED
- `graded_at` (DateTime): When the assessment was graded
- `feedback` (Text): Feedback for the user
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp

### Vector Store Document

Represents a document in the vector store for RAG functionality.

**Fields**:
- `id` (String): Unique identifier from Qdrant
- `content_id` (UUID): Reference to the textbook content (chapter, section, etc.)
- `content_type` (Enum): CHAPTER, SECTION, CODE_EXAMPLE, GLOSSARY_TERM
- `text_content` (Text): The actual text content
- `embedding` (JSON): Vector embedding of the content
- `metadata` (JSON): Additional metadata for retrieval
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp

## Relationships

### User to Learning Progress
- One-to-Many: A user can have progress records for multiple chapters

### Chapter to Learning Progress
- One-to-Many: A chapter can have progress records for multiple users

### Chapter to Assessment
- One-to-Many: A chapter can have multiple related assessments

### User to Assessment Submission
- One-to-Many: A user can submit multiple assessments

### Assessment to Assessment Submission
- One-to-Many: An assessment can have multiple submissions

### Chapter to Simulation Instance
- One-to-Many: A chapter can have multiple related simulation instances

### User to Simulation Instance
- One-to-Many: A user can have multiple simulation instances

### User to Question & Answer Session
- One-to-Many: A user can have multiple Q&A sessions

## Indexes

### Performance Indexes
- `User.email`: For authentication lookups
- `LearningProgress.user_id`: For user progress queries
- `LearningProgress.chapter_id`: For chapter progress analytics
- `AssessmentSubmission.assessment_id`: For assessment result queries
- `SimulationInstance.user_id`: For user's simulation instances
- `VectorStoreDocument.content_id`: For content lookup in RAG

### Unique Constraints
- `User.email`: Must be unique
- `User.username`: Must be unique
- `TextbookChapter.slug`: Must be unique