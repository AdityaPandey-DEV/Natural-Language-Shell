#include "headers/history.h"

// Global history array
static char *history[MAX_HISTORY];
static int history_count = 0;

// Initialize history
void init_history(void) {
    for (int i = 0; i < MAX_HISTORY; i++) {
        history[i] = NULL;
    }
    load_history();
}

// Add command to history
void add_to_history(char *command) {
    if (!command || strlen(command) == 0) {
        return;
    }
    
    // Skip if same as last command
    if (history_count > 0 && strcmp(history[history_count - 1], command) == 0) {
        return;
    }
    
    // Free old history if at capacity
    if (history_count >= MAX_HISTORY) {
        free(history[0]);
        // Shift all entries left
        for (int i = 0; i < MAX_HISTORY - 1; i++) {
            history[i] = history[i + 1];
        }
        history_count--;
    }
    
    // Add new command
    history[history_count] = strdup(command);
    if (history[history_count]) {
        history_count++;
    }
}

// Save history to file
void save_history(void) {
    FILE *file = fopen(history_file, "w");
    if (!file) {
        return; // Silently fail if can't save
    }
    
    for (int i = 0; i < history_count; i++) {
        if (history[i]) {
            fprintf(file, "%s\n", history[i]);
        }
    }
    
    fclose(file);
}

// Load history from file
void load_history(void) {
    FILE *file = fopen(history_file, "r");
    if (!file) {
        return; // No history file exists yet
    }
    
    char line[MAX_CMD_LEN];
    while (fgets(line, sizeof(line), file) && history_count < MAX_HISTORY) {
        // Remove newline
        line[strcspn(line, "\n")] = 0;
        
        if (strlen(line) > 0) {
            history[history_count] = strdup(line);
            if (history[history_count]) {
                history_count++;
            }
        }
    }
    
    fclose(file);
}

// Print history
void print_history(int count) {
    int start = (count > history_count) ? 0 : history_count - count;
    
    for (int i = start; i < history_count; i++) {
        if (history[i]) {
            printf("%d\t%s\n", i + 1, history[i]);
        }
    }
}

// Get history command by index
char* get_history_command(int index) {
    if (index < 1 || index > history_count) {
        return NULL;
    }
    
    return history[index - 1];
}
