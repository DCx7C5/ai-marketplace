# Sequential Thinking MCP

A Model Context Protocol (MCP) server that provides sequential thinking and problem-solving tools for systematic analysis and planning.

## Features

This MCP server provides four powerful tools for structured thinking:

### 🧠 Sequential Thinking
Apply a systematic methodology to solve complex problems step-by-step with structured analysis phases.

### 🔍 Problem Breakdown
Break down complex problems into smaller, manageable components across multiple levels of detail.

### 📊 Problem Analysis
Analyze problems using proven frameworks:
- **SWOT Analysis**: Strengths, Weaknesses, Opportunities, Threats
- **Pros/Cons Analysis**: Weighted decision making
- **Root Cause Analysis**: 5 Whys and Fishbone diagrams
- **Decision Tree Analysis**: Probabilistic decision making

### 📋 Step-by-Step Planning
Create detailed implementation plans with phases, milestones, and actionable tasks.

## Installation

```bash
npm install -g sequential-thinking-mcp
```

## Usage

### With MCP Clients

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "sequential-thinking": {
      "command": "sequential-thinking-mcp",
      "args": []
    }
  }
}
```

### Available Tools

#### 1. Sequential Thinking
```javascript
{
  "name": "sequential_thinking",
  "arguments": {
    "problem": "How to improve team productivity",
    "context": "Remote team of 10 developers",
    "constraints": ["Budget limited to $5000", "Must implement in 3 months"],
    "goals": ["Increase productivity by 20%", "Improve team satisfaction"]
  }
}
```

#### 2. Problem Breakdown
```javascript
{
  "name": "problem_breakdown",
  "arguments": {
    "problem": "Implement new customer onboarding system",
    "levels": 3
  }
}
```

#### 3. Problem Analysis
```javascript
{
  "name": "analyze_problem",
  "arguments": {
    "problem": "High customer churn rate",
    "approach": "root-cause"
  }
}
```

#### 4. Step-by-Step Planning
```javascript
{
  "name": "step_by_step_plan",
  "arguments": {
    "task": "Launch new product feature",
    "details": true
  }
}
```

## Analysis Frameworks

### SWOT Analysis
- **Strengths**: Internal positive factors
- **Weaknesses**: Internal negative factors
- **Opportunities**: External positive factors
- **Threats**: External negative factors

### Root Cause Analysis
- **5 Whys**: Drill down to root causes
- **Fishbone Diagram**: Categorize contributing factors

### Decision Tree Analysis
- **Probabilistic outcomes**: Assign probabilities to different scenarios
- **Expected value calculation**: Make data-driven decisions

## Example Output

The tools provide structured, actionable analysis in markdown format, including:

- 📋 Clear problem definitions
- 🎯 Specific action items
- 📊 Structured frameworks
- ✅ Checkboxes for tracking progress
- 💡 Recommendations for next steps

## Requirements

- Node.js 18.0.0 or higher
- MCP-compatible client (Claude Desktop, etc.)

## Development

```bash
# Clone the repository
git clone https://github.com/taybr99/sequential-thinking-mcp
cd sequential-thinking-mcp

# Install dependencies
npm install

# Build the project
npm run build

# Run in development mode
npm run dev
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Keywords

- MCP (Model Context Protocol)
- Sequential Thinking
- Problem Solving
- Analysis Framework
- Decision Making
- Planning
- SWOT Analysis
- Root Cause Analysis
- Project Management
- AI Tools
