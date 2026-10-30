import type { Result } from "./types";

export function sortResults(results: Result[]): Result[] {
  return [...results].sort((left, right) => right.score - left.score);
}
