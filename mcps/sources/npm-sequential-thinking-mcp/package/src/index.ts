#!/usr/bin/env node
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ErrorCode,
  ListToolsRequestSchema,
  McpError,
} from '@modelcontextprotocol/sdk/types.js';

interface SequentialThinkingArgs {
  problem: string;
  context?: string;
  constraints?: string[];
  goals?: string[];
}

interface BreakdownArgs {
  problem: string;
  levels?: number;
}

interface AnalyzeArgs {
  problem: string;
  approach?: 'swot' | 'pros-cons' | 'root-cause' | 'decision-tree';
}

interface StepByStepArgs {
  task: string;
  details?: boolean;
}

const isValidSequentialThinkingArgs = (args: any): args is SequentialThinkingArgs =>
  typeof args === 'object' &&
  args !== null &&
  typeof args.problem === 'string' &&
  (args.context === undefined || typeof args.context === 'string') &&
  (args.constraints === undefined || Array.isArray(args.constraints)) &&
  (args.goals === undefined || Array.isArray(args.goals));

const isValidBreakdownArgs = (args: any): args is BreakdownArgs =>
  typeof args === 'object' &&
  args !== null &&
  typeof args.problem === 'string' &&
  (args.levels === undefined || typeof args.levels === 'number');

const isValidAnalyzeArgs = (args: any): args is AnalyzeArgs =>
  typeof args === 'object' &&
  args !== null &&
  typeof args.problem === 'string' &&
  (args.approach === undefined || ['swot', 'pros-cons', 'root-cause', 'decision-tree'].includes(args.approach));

const isValidStepByStepArgs = (args: any): args is StepByStepArgs =>
  typeof args === 'object' &&
  args !== null &&
  typeof args.task === 'string' &&
  (args.details === undefined || typeof args.details === 'boolean');

class SequentialThinkingServer {
  private server: Server;

  constructor() {
    this.server = new Server(
      {
        name: 'sequential-thinking-server',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.setupToolHandlers();
    
    // Error handling
    this.server.onerror = (error) => console.error('[MCP Error]', error);
    process.on('SIGINT', async () => {
      await this.server.close();
      process.exit(0);
    });
  }

  private setupToolHandlers() {
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [
        {
          name: 'sequential_thinking',
          description: 'Apply sequential thinking methodology to solve complex problems step-by-step',
          inputSchema: {
            type: 'object',
            properties: {
              problem: {
                type: 'string',
                description: 'The problem or challenge to analyze',
              },
              context: {
                type: 'string',
                description: 'Additional context about the problem',
              },
              constraints: {
                type: 'array',
                items: { type: 'string' },
                description: 'Known constraints or limitations',
              },
              goals: {
                type: 'array',
                items: { type: 'string' },
                description: 'Desired outcomes or goals',
              },
            },
            required: ['problem'],
          },
        },
        {
          name: 'problem_breakdown',
          description: 'Break down complex problems into smaller, manageable components',
          inputSchema: {
            type: 'object',
            properties: {
              problem: {
                type: 'string',
                description: 'The complex problem to break down',
              },
              levels: {
                type: 'number',
                description: 'Number of breakdown levels (default: 3)',
              },
            },
            required: ['problem'],
          },
        },
        {
          name: 'analyze_problem',
          description: 'Analyze problems using structured frameworks (SWOT, pros/cons, root cause, decision tree)',
          inputSchema: {
            type: 'object',
            properties: {
              problem: {
                type: 'string',
                description: 'The problem to analyze',
              },
              approach: {
                type: 'string',
                enum: ['swot', 'pros-cons', 'root-cause', 'decision-tree'],
                description: 'Analysis framework to use',
              },
            },
            required: ['problem'],
          },
        },
        {
          name: 'step_by_step_plan',
          description: 'Create a detailed step-by-step plan for executing a task or solving a problem',
          inputSchema: {
            type: 'object',
            properties: {
              task: {
                type: 'string',
                description: 'The task or problem to create a plan for',
              },
              details: {
                type: 'boolean',
                description: 'Include detailed sub-steps and considerations',
              },
            },
            required: ['task'],
          },
        },
      ],
    }));

    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      try {
        switch (request.params.name) {
          case 'sequential_thinking':
            if (!isValidSequentialThinkingArgs(request.params.arguments)) {
              throw new McpError(
                ErrorCode.InvalidParams,
                'Invalid sequential thinking arguments'
              );
            }
            return await this.sequentialThinking(request.params.arguments);

          case 'problem_breakdown':
            if (!isValidBreakdownArgs(request.params.arguments)) {
              throw new McpError(
                ErrorCode.InvalidParams,
                'Invalid problem breakdown arguments'
              );
            }
            return await this.problemBreakdown(request.params.arguments);

          case 'analyze_problem':
            if (!isValidAnalyzeArgs(request.params.arguments)) {
              throw new McpError(
                ErrorCode.InvalidParams,
                'Invalid analyze problem arguments'
              );
            }
            return await this.analyzeProblem(request.params.arguments);

          case 'step_by_step_plan':
            if (!isValidStepByStepArgs(request.params.arguments)) {
              throw new McpError(
                ErrorCode.InvalidParams,
                'Invalid step by step plan arguments'
              );
            }
            return await this.stepByStepPlan(request.params.arguments);

          default:
            throw new McpError(
              ErrorCode.MethodNotFound,
              `Unknown tool: ${request.params.name}`
            );
        }
      } catch (error) {
        console.error('Tool execution error:', error);
        return {
          content: [
            {
              type: 'text',
              text: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`,
            },
          ],
          isError: true,
        };
      }
    });
  }

  private async sequentialThinking(args: SequentialThinkingArgs) {
    const { problem, context, constraints, goals } = args;
    
    const sections = [
      '# Sequential Thinking Analysis',
      '',
      '## Problem Definition',
      `**Problem**: ${problem}`,
    ];

    if (context) {
      sections.push(`**Context**: ${context}`);
    }

    if (constraints && constraints.length > 0) {
      sections.push('**Constraints**:');
      constraints.forEach(constraint => sections.push(`- ${constraint}`));
    }

    if (goals && goals.length > 0) {
      sections.push('**Goals**:');
      goals.forEach(goal => sections.push(`- ${goal}`));
    }

    sections.push(
      '',
      '## Step-by-Step Analysis',
      '',
      '### Step 1: Information Gathering',
      '- What information do we have?',
      '- What information do we need?',
      '- What assumptions are we making?',
      '',
      '### Step 2: Problem Decomposition',
      '- Break the problem into smaller parts',
      '- Identify dependencies between parts',
      '- Prioritize components by importance/urgency',
      '',
      '### Step 3: Solution Generation',
      '- Brainstorm potential approaches',
      '- Consider multiple perspectives',
      '- Evaluate feasibility of each approach',
      '',
      '### Step 4: Solution Evaluation',
      '- Compare solutions against goals',
      '- Assess risks and benefits',
      '- Consider resource requirements',
      '',
      '### Step 5: Implementation Planning',
      '- Define clear next steps',
      '- Identify required resources',
      '- Set milestones and checkpoints',
      '',
      '### Step 6: Monitoring and Adjustment',
      '- Define success metrics',
      '- Plan for regular reviews',
      '- Prepare contingency plans',
      '',
      '## Recommended Next Actions',
      '1. **Immediate**: Gather additional information if needed',
      '2. **Short-term**: Break down the problem further using problem_breakdown tool',
      '3. **Medium-term**: Analyze specific aspects using analyze_problem tool',
      '4. **Long-term**: Create detailed implementation plan using step_by_step_plan tool'
    );

    return {
      content: [
        {
          type: 'text',
          text: sections.join('\n'),
        },
      ],
    };
  }

  private async problemBreakdown(args: BreakdownArgs) {
    const { problem, levels = 3 } = args;
    
    const sections = [
      '# Problem Breakdown Analysis',
      '',
      `**Main Problem**: ${problem}`,
      ''
    ];

    for (let level = 1; level <= levels; level++) {
      sections.push(`## Level ${level} Breakdown`);
      
      switch (level) {
        case 1:
          sections.push(
            '### Primary Components',
            '- **Technical aspects**: What technical challenges need to be addressed?',
            '- **Human factors**: What people-related issues are involved?',
            '- **Process elements**: What processes need to be considered?',
            '- **Resource requirements**: What resources are needed?',
            '- **External dependencies**: What external factors affect this problem?',
            ''
          );
          break;
        case 2:
          sections.push(
            '### Secondary Components',
            '**Technical Aspects**:',
            '- System requirements and constraints',
            '- Integration challenges',
            '- Performance considerations',
            '',
            '**Human Factors**:',
            '- Stakeholder needs and expectations',
            '- Skills and training requirements',
            '- Communication needs',
            '',
            '**Process Elements**:',
            '- Workflow design',
            '- Quality assurance',
            '- Risk management',
            '',
            '**Resource Requirements**:',
            '- Budget and financial considerations',
            '- Time constraints',
            '- Equipment and tools',
            '',
            '**External Dependencies**:',
            '- Third-party services',
            '- Regulatory requirements',
            '- Market conditions',
            ''
          );
          break;
        case 3:
          sections.push(
            '### Detailed Components',
            '**Immediate Actions Required**:',
            '- Research and analysis tasks',
            '- Stakeholder consultations',
            '- Resource allocation decisions',
            '',
            '**Short-term Objectives**:',
            '- Proof of concept development',
            '- Team formation and training',
            '- Initial implementation steps',
            '',
            '**Long-term Goals**:',
            '- Full solution deployment',
            '- Performance optimization',
            '- Maintenance and support',
            ''
          );
          break;
      }
    }

    sections.push(
      '## Summary',
      'Use this breakdown to:',
      '- Focus on one component at a time',
      '- Identify critical path dependencies',
      '- Assign responsibilities to team members',
      '- Create detailed project timelines',
      '- Monitor progress systematically'
    );

    return {
      content: [
        {
          type: 'text',
          text: sections.join('\n'),
        },
      ],
    };
  }

  private async analyzeProblem(args: AnalyzeArgs) {
    const { problem, approach = 'swot' } = args;
    
    const sections = [
      '# Problem Analysis',
      '',
      `**Problem**: ${problem}`,
      `**Analysis Method**: ${approach.toUpperCase()}`,
      ''
    ];

    switch (approach) {
      case 'swot':
        sections.push(
          '## SWOT Analysis',
          '',
          '### Strengths',
          '- What advantages do we have?',
          '- What do we do well?',
          '- What resources do we have access to?',
          '- What others see as our strengths?',
          '',
          '### Weaknesses',
          '- What could we improve?',
          '- What do we do poorly?',
          '- What should we avoid?',
          '- What factors lose us opportunities?',
          '',
          '### Opportunities',
          '- What opportunities are available?',
          '- What trends could we take advantage of?',
          '- How can we turn strengths into opportunities?',
          '- What changes in environment could benefit us?',
          '',
          '### Threats',
          '- What threats could harm us?',
          '- What is our competition doing?',
          '- What obstacles do we face?',
          '- What changes in environment could threaten us?'
        );
        break;

      case 'pros-cons':
        sections.push(
          '## Pros and Cons Analysis',
          '',
          '### Pros (Advantages)',
          '- **Benefit 1**: [Describe specific advantage]',
          '- **Benefit 2**: [Describe specific advantage]',
          '- **Benefit 3**: [Describe specific advantage]',
          '',
          '### Cons (Disadvantages)',
          '- **Risk 1**: [Describe specific disadvantage]',
          '- **Risk 2**: [Describe specific disadvantage]',
          '- **Risk 3**: [Describe specific disadvantage]',
          '',
          '### Neutral Factors',
          '- **Factor 1**: [Neither advantage nor disadvantage]',
          '- **Factor 2**: [Depends on implementation]',
          '',
          '### Decision Matrix',
          '- Weight each pro and con by importance (1-10)',
          '- Calculate total weighted score',
          '- Compare with alternatives'
        );
        break;

      case 'root-cause':
        sections.push(
          '## Root Cause Analysis',
          '',
          '### Problem Symptoms',
          '- What are the visible effects?',
          '- When do these symptoms occur?',
          '- Who is affected by these symptoms?',
          '',
          '### 5 Whys Analysis',
          '1. **Why** does this problem occur?',
          '   - [First level cause]',
          '2. **Why** does that cause occur?',
          '   - [Second level cause]',
          '3. **Why** does that cause occur?',
          '   - [Third level cause]',
          '4. **Why** does that cause occur?',
          '   - [Fourth level cause]',
          '5. **Why** does that cause occur?',
          '   - [Root cause]',
          '',
          '### Fishbone Diagram Categories',
          '**People**: Human factors contributing to the problem',
          '**Process**: Procedural issues',
          '**Technology**: Technical or equipment issues',
          '**Environment**: External factors',
          '**Materials**: Resource-related issues',
          '**Measurement**: Data or metric issues'
        );
        break;

      case 'decision-tree':
        sections.push(
          '## Decision Tree Analysis',
          '',
          '### Decision Points',
          '```',
          'Problem: [Main Problem]',
          '├── Option A: [First major choice]',
          '│   ├── Outcome A1: [Possible result]',
          '│   │   ├── Probability: [%]',
          '│   │   └── Impact: [High/Medium/Low]',
          '│   └── Outcome A2: [Possible result]',
          '│       ├── Probability: [%]',
          '│       └── Impact: [High/Medium/Low]',
          '├── Option B: [Second major choice]',
          '│   ├── Outcome B1: [Possible result]',
          '│   │   ├── Probability: [%]',
          '│   │   └── Impact: [High/Medium/Low]',
          '│   └── Outcome B2: [Possible result]',
          '│       ├── Probability: [%]',
          '│       └── Impact: [High/Medium/Low]',
          '└── Option C: [Third major choice]',
          '    └── [Continue pattern...]',
          '```',
          '',
          '### Expected Value Calculation',
          '- **Option A**: (Probability A1 × Impact A1) + (Probability A2 × Impact A2)',
          '- **Option B**: (Probability B1 × Impact B1) + (Probability B2 × Impact B2)',
          '- **Option C**: [Continue calculation...]',
          '',
          '### Recommended Decision',
          '- Compare expected values',
          '- Consider risk tolerance',
          '- Account for qualitative factors'
        );
        break;
    }

    return {
      content: [
        {
          type: 'text',
          text: sections.join('\n'),
        },
      ],
    };
  }

  private async stepByStepPlan(args: StepByStepArgs) {
    const { task, details = false } = args;
    
    const sections = [
      '# Step-by-Step Implementation Plan',
      '',
      `**Task**: ${task}`,
      ''
    ];

    if (details) {
      sections.push(
        '## Phase 1: Planning and Preparation',
        '### Step 1: Define Objectives',
        '- [ ] Clarify the end goal',
        '- [ ] Identify success criteria',
        '- [ ] Set measurable milestones',
        '- [ ] Determine timeline',
        '',
        '### Step 2: Gather Resources',
        '- [ ] Identify required skills',
        '- [ ] Allocate team members',
        '- [ ] Secure necessary tools',
        '- [ ] Confirm budget availability',
        '',
        '### Step 3: Risk Assessment',
        '- [ ] Identify potential obstacles',
        '- [ ] Develop mitigation strategies',
        '- [ ] Create contingency plans',
        '- [ ] Establish communication protocols',
        '',
        '## Phase 2: Execution',
        '### Step 4: Initial Implementation',
        '- [ ] Begin with pilot or prototype',
        '- [ ] Test core functionality',
        '- [ ] Gather initial feedback',
        '- [ ] Make necessary adjustments',
        '',
        '### Step 5: Full Deployment',
        '- [ ] Roll out complete solution',
        '- [ ] Monitor performance metrics',
        '- [ ] Address issues promptly',
        '- [ ] Document lessons learned',
        '',
        '### Step 6: Optimization',
        '- [ ] Analyze performance data',
        '- [ ] Identify improvement opportunities',
        '- [ ] Implement optimizations',
        '- [ ] Validate improvements',
        '',
        '## Phase 3: Maintenance and Review',
        '### Step 7: Ongoing Maintenance',
        '- [ ] Establish maintenance schedule',
        '- [ ] Train support team',
        '- [ ] Create documentation',
        '- [ ] Set up monitoring systems',
        '',
        '### Step 8: Performance Review',
        '- [ ] Measure against objectives',
        '- [ ] Gather stakeholder feedback',
        '- [ ] Identify areas for improvement',
        '- [ ] Plan future enhancements'
      );
    } else {
      sections.push(
        '## High-Level Steps',
        '1. **Plan**: Define objectives and gather resources',
        '2. **Prepare**: Set up environment and tools',
        '3. **Execute**: Implement the solution step by step',
        '4. **Test**: Validate functionality and performance',
        '5. **Deploy**: Roll out to production or final environment',
        '6. **Monitor**: Track performance and gather feedback',
        '7. **Optimize**: Make improvements based on data',
        '8. **Maintain**: Provide ongoing support and updates',
        '',
        '## Next Steps',
        '- Break down each high-level step into specific tasks',
        '- Assign owners and deadlines to each task',
        '- Create a project timeline with dependencies',
        '- Set up regular check-ins and progress reviews'
      );
    }

    sections.push(
      '',
      '## Success Metrics',
      '- **Quality**: Define what "done" looks like',
      '- **Timeline**: Track progress against milestones',
      '- **Budget**: Monitor resource utilization',
      '- **Stakeholder Satisfaction**: Gather feedback regularly',
      '',
      '## Tips for Success',
      '- Start small and iterate',
      '- Communicate progress regularly',
      '- Be prepared to adapt the plan',
      '- Document decisions and lessons learned',
      '- Celebrate milestones and achievements'
    );

    return {
      content: [
        {
          type: 'text',
          text: sections.join('\n'),
        },
      ],
    };
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('Sequential Thinking MCP server running on stdio');
  }
}

const server = new SequentialThinkingServer();
server.run().catch(console.error);
