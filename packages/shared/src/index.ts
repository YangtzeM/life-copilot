export type TaskPriority = "urgent" | "important" | "optional" | "low_value";

export interface ParsedTask {
  title: string;
  description: string;
  dueAt?: string | null;
  reminderAt?: string | null;
  priority: TaskPriority;
  needsReview: boolean;
}

export interface PlanStep {
  order: number;
  title: string;
  description: string;
}

export interface GeneratedPlan {
  taskId: string;
  summary: string;
  steps: PlanStep[];
}
