#include "headers/shell.h"
#include "headers/parser.h"
#include "headers/executor.h"
#include "headers/builtin.h"
#include "headers/history.h"
#include "headers/jobs.h"
#include "headers/utils.h"

// Global variables
job_t jobs[MAX_JOBS];
int job_count = 0;
int current_job_id = 0;
char *history_file = ".history";

// Signal handler for Ctrl+C and Ctrl+Z
void signal_handler(int sig) {
    if (sig == SIGINT) {
        printf("\n");
        print_prompt();
        fflush(stdout);
    } else if (sig == SIGTSTP) {
        printf("\n");
        print_prompt();
        fflush(stdout);
    }
}

// Initialize shell
void init_shell(void) {
    // Set up signal handlers
    signal(SIGINT, signal_handler);
    signal(SIGTSTP, signal_handler);
    signal(SIGCHLD, SIG_IGN); // Ignore child termination signals
    
    // Initialize history
    init_history();
    
    // Clear job array
    for (int i = 0; i < MAX_JOBS; i++) {
        jobs[i].pid = 0;
        jobs[i].job_id = 0;
        jobs[i].command = NULL;
        jobs[i].status = 0;
        jobs[i].start_time = 0;
    }
    
    printf("Advanced Mini Bash Shell v2.0\n");
    printf("Type 'exit' to quit, 'help' for built-in commands\n");
}

// Cleanup shell resources
void cleanup_shell(void) {
    // Clean up completed jobs
    cleanup_completed_jobs();
    
    // Save history
    save_history();
    
    // Free job memory
    for (int i = 0; i < MAX_JOBS; i++) {
        if (jobs[i].command) {
            free(jobs[i].command);
            jobs[i].command = NULL;
        }
    }
}

// Print shell prompt
void print_prompt(void) {
    char cwd[1024];
    if (getcwd(cwd, sizeof(cwd)) != NULL) {
        printf("mini-bash:%s$ ", cwd);
    } else {
        printf("mini-bash$ ");
    }
    fflush(stdout);
}

// Read command from user
int read_command(char *cmd) {
    if (fgets(cmd, MAX_CMD_LEN, stdin) == NULL) {
        return 0; // EOF
    }
    
    // Remove newline
    cmd[strcspn(cmd, "\n")] = 0;
    
    // Skip empty commands
    if (strlen(cmd) == 0) {
        return 1;
    }
    
    return 1;
}

// Execute command
void execute_command(char *cmd) {
    // Add to history (skip if it's the same as last command)
    add_to_history(cmd);
    
    // Check if it's a pipeline
    if (is_pipeline(cmd)) {
        int count;
        char **commands = split_pipeline(cmd, &count);
        if (commands) {
            execute_pipeline(commands, count);
            free_string_array(commands, count);
        }
        return;
    }
    
    // Parse single command
    command_t *parsed_cmd = parse_command(cmd);
    if (parsed_cmd) {
        execute_single_command(parsed_cmd);
        free_command(parsed_cmd);
    }
}

// Main shell loop
int main(int argc, char *argv[]) {
    (void)argc;  // Suppress unused parameter warning
    (void)argv;   // Suppress unused parameter warning
    char cmd[MAX_CMD_LEN];
    
    // Initialize shell
    init_shell();
    
    // Main command loop
    while (1) {
        print_prompt();
        
        if (!read_command(cmd)) {
            printf("\n");
            break; // EOF
        }
        
        // Skip empty commands
        if (strlen(cmd) == 0) {
            continue;
        }
        
        // Execute command
        execute_command(cmd);
        
        // Clean up completed background jobs
        cleanup_completed_jobs();
    }
    
    // Cleanup and exit
    cleanup_shell();
    return 0;
}
