# Quickstart Guide: Physical AI & Humanoid Robotics Textbook Platform

## Overview

This guide will help you set up and run the Physical AI & Humanoid Robotics textbook platform locally. The platform consists of a Docusaurus documentation site, a FastAPI backend, and integration with simulation environments.

## Prerequisites

Before getting started, ensure you have the following installed:

- **Git** (v2.30+)
- **Node.js** (v18+)
- **Python** (v3.11+)
- **Docker** (v20+)
- **Docker Compose** (v2.0+)
- **ROS 2** (Humble Hawksbill) - for simulation features
- **Unity Hub** (2022.3 LTS) - for Unity simulation environments
- **NVIDIA Isaac Sim** (if available) - for Isaac simulation features

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/robotics-textbook-platform.git
cd robotics-textbook-platform
```

### 2. Set up Docusaurus Frontend

```bash
# Navigate to the Docusaurus directory
cd my-website

# Install dependencies
npm install

# Create a .env file with API configuration
cat > .env << EOF
REACT_APP_API_BASE_URL=http://localhost:8000
REACT_APP_QDRANT_URL=http://localhost:6333
EOF

# Start the development server
npm run start
```

The Docusaurus frontend will be available at `http://localhost:3000`.

### 3. Set up FastAPI Backend

Open a new terminal and navigate to the backend directory:

```bash
# Create and activate a Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Create a .env file with configuration
cat > .env << EOF
DATABASE_URL=postgresql://user:password@localhost:5432/robotics_textbook
QDRANT_URL=http://localhost:6333
OPENAI_API_KEY=your-openai-api-key
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
EOF

# Run database migrations (if using an ORM with migrations)
python -m alembic upgrade head

# Start the FastAPI server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The FastAPI backend will be available at `http://localhost:8000`, with automatic documentation at `http://localhost:8000/docs`.

### 4. Set up Vector Store (Qdrant)

```bash
# Run Qdrant using Docker
docker run -d --name qdrant -p 6333:6333 -p 6334:6334 \
  -v $(pwd)/qdrant_storage:/qdrant/storage:z \
  qdrant/qdrant
```

### 5. Set up Supporting Services

Use Docker Compose to start all supporting services:

```bash
# Create docker-compose.yml file
cat > docker-compose.yml << EOF
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: robotics_textbook
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - qdrant_storage:/qdrant/storage:z

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
  qdrant_storage:
EOF

# Start all services
docker-compose up -d
```

### 6. Initialize the Platform

Once all services are running, initialize the platform with essential data:

```bash
# Run the initialization script
cd backend
python -m src.scripts.initialize_db
```

This script will:
- Create default user roles
- Load textbook chapters
- Set up vector embeddings for RAG functionality
- Create default simulation configurations

## Running Simulations

### ROS 2 Simulation Environment

1. Source your ROS 2 installation:
```bash
source /opt/ros/humble/setup.bash
source ./simulations/ros2_ws/install/setup.bash
```

2. Launch a simulation:
```bash
ros2 launch humanoid_gazebo humanoid_world.launch.py
```

### Unity Simulation Environment

1. Open Unity Hub and load the simulation project from `./simulations/unity/`
2. Build the project for your target platform
3. Use the backend API to interface with the Unity simulation

### NVIDIA Isaac Simulation (if available)

1. Follow NVIDIA Isaac Sim setup instructions
2. Launch the simulation from your Isaac applications folder

## Project Structure

```
robotics-textbook-platform/
├── my-website/              # Docusaurus documentation site
│   ├── docs/                # Textbook content in markdown
│   ├── src/                 # Custom React components
│   ├── static/              # Static assets
│   └── docusaurus.config.js # Configuration
├── backend/                 # FastAPI backend
│   ├── src/
│   │   ├── main.py          # Application entry point
│   │   ├── models/          # Pydantic models
│   │   ├── schemas/         # Database schemas
│   │   ├── routes/          # API endpoints
│   │   ├── services/        # Business logic
│   │   └── utils/           # Utility functions
│   └── requirements.txt     # Python dependencies
├── simulations/             # Robotics simulation environments
│   ├── ros2_ws/             # ROS2 workspace with humanoid packages
│   ├── gazebo/              # Gazebo simulation worlds/models
│   ├── unity/               # Unity simulation environments
│   └── isaac/               # NVIDIA Isaac simulation configurations
├── vectorstore/             # Qdrant configurations
├── specs/                   # Specification documents
└── docker-compose.yml       # Docker services configuration
```

## Development Commands

### Frontend (Docusaurus)
```bash
cd my-website
npm run start          # Start development server
npm run build          # Build for production
npm run serve          # Serve built site locally
```

### Backend (FastAPI)
```bash
cd backend
pip install -r requirements.txt  # Install dependencies
uvicorn src.main:app --reload    # Start development server
pytest                           # Run tests
```

### Code Formatting
```bash
# Backend formatting
black src/
isort src/

# Frontend formatting
npm run format
```

## Testing

### Backend Tests
```bash
cd backend
pytest tests/  # Run all tests
pytest tests/unit/  # Run unit tests only
pytest tests/integration/  # Run integration tests only
```

### Frontend Tests
```bash
cd my-website
npm run test  # Run component tests
```

## Deployment

### Production Build

1. Build the frontend:
```bash
cd my-website
npm run build
```

2. Deploy the FastAPI backend using your preferred method (Docker, cloud platform, etc.)

### Environment Configuration

For production deployment, set these environment variables:

```bash
# Backend environment variables
DATABASE_URL=postgresql://user:password@prod-db:5432/robotics_textbook
QDRANT_URL=https://your-qdrant-instance.com
OPENAI_API_KEY=your-production-openai-key
SECRET_KEY=your-production-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENVIRONMENT=production
LOG_LEVEL=info
```

## Troubleshooting

### Common Issues

1. **Port Already in Use**: If you get "Address already in use" errors, ensure no other processes are using the required ports (3000, 8000, 5432, 6333, etc.).

2. **Python Dependencies**: If you encounter Python dependency issues, ensure you're using Python 3.11+ and create a fresh virtual environment.

3. **Docker Issues**: For Docker-related problems, make sure Docker and Docker Compose are properly installed and running.

### Development Tips

1. **API Documentation**: Visit `http://localhost:8000/docs` for interactive API documentation and testing.

2. **Frontend Components**: When creating new Docusaurus components for interactive textbook elements, place them in `my-website/src/components/`.

3. **Simulation Integration**: All simulation environments should expose REST APIs that the backend can interact with for consistent integration.

## Next Steps

1. Review the [Architecture Documentation](./architecture.md) for system design details
2. Check the [API Contracts](./contracts/api-contract.md) for integration specifications
3. Explore the [Data Models](./data-model.md) for database structure information
4. Look at the [Task List](../tasks.md) for implementation steps