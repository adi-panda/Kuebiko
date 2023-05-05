/**
 * Exits immediately with the given `exitCode`.
 * @example
 * ```typescript
 * import { exit } from '@tauri-apps/api/process';
 * await exit(1);
 * ```
 *
 * @param exitCode The exit code to use.
 * @returns A promise indicating the success or failure of the operation.
 *
 * @since 1.0.0
 */
declare function exit(exitCode?: number): Promise<void>;
/**
 * Exits the current instance of the app then relaunches it.
 * @example
 * ```typescript
 * import { relaunch } from '@tauri-apps/api/process';
 * await relaunch();
 * ```
 *
 * @returns A promise indicating the success or failure of the operation.
 *
 * @since 1.0.0
 */
declare function relaunch(): Promise<void>;

declare const process_exit: typeof exit;
declare const process_relaunch: typeof relaunch;
declare namespace process {
  export {
    process_exit as exit,
    process_relaunch as relaunch,
  };
}

export { exit as e, process as p, relaunch as r };
