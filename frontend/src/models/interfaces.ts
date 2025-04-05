// filepath: c:\Users\Ivan\csu-python\project-ai\frontend\src\models\interfaces.ts

export interface Task {
    id?: number; // Optional for new tasks
    name: string;
    project_id: number;
    description: string;
    acceptance_criteria: string;
    priority: "LOW" | "NORMAL" | "HIGH" | "CRITICAL"; // Matches FastAPI Enum
}

export interface Resource {
    id?: number; // Optional for new resources
    name: string;
    project_id: number;
    description: string;
}

export interface Project {
    id: number;
    name: string;
    description: string;
    tasks: Task[];
    resources: Resource[];
}

export interface ChatQuery<T = Project | Task | Resource> {
    query: string;
    attached: T | null;
}

export interface ChatResponse {
    answer: string;
    projects: Project[];
    tasks: Task[];
    resources: Resource[];
}