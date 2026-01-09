#include "headers/parser.h"
#include "headers/utils.h"

// Parse command string into command structure
command_t* parse_command(char *cmd) {
    command_t *parsed_cmd = malloc(sizeof(command_t));
    if (!parsed_cmd) {
        print_error("Memory allocation failed");
        return NULL;
    }
    
    // Initialize command structure
    parsed_cmd->args = NULL;
    parsed_cmd->argc = 0;
    parsed_cmd->input_file = NULL;
    parsed_cmd->output_file = NULL;
    parsed_cmd->error_file = NULL;
    parsed_cmd->append_output = 0;
    parsed_cmd->background = 0;
    
    // Check for background execution
    char *cmd_copy = strdup(cmd);
    if (!cmd_copy) {
        free(parsed_cmd);
        return NULL;
    }
    
    trim_whitespace(cmd_copy);
    
    // Check for background execution
    if (cmd_copy[strlen(cmd_copy) - 1] == '&') {
        parsed_cmd->background = 1;
        cmd_copy[strlen(cmd_copy) - 1] = '\0';
        trim_whitespace(cmd_copy);
    }
    
    // Parse redirection
    char *input_redir = strstr(cmd_copy, " < ");
    char *output_redir = strstr(cmd_copy, " > ");
    char *append_redir = strstr(cmd_copy, " >> ");
    char *error_redir = strstr(cmd_copy, " 2> ");
    
    // Handle input redirection
    if (input_redir) {
        *input_redir = '\0';
        char *input_file = input_redir + 3;
        trim_whitespace(input_file);
        parsed_cmd->input_file = strdup(input_file);
        trim_whitespace(cmd_copy);
    }
    
    // Handle output redirection (check append first)
    if (append_redir) {
        *append_redir = '\0';
        char *output_file = append_redir + 4;
        trim_whitespace(output_file);
        parsed_cmd->output_file = strdup(output_file);
        parsed_cmd->append_output = 1;
        trim_whitespace(cmd_copy);
    } else if (output_redir) {
        *output_redir = '\0';
        char *output_file = output_redir + 3;
        trim_whitespace(output_file);
        parsed_cmd->output_file = strdup(output_file);
        parsed_cmd->append_output = 0;
        trim_whitespace(cmd_copy);
    }
    
    // Handle error redirection
    if (error_redir) {
        *error_redir = '\0';
        char *error_file = error_redir + 4;
        trim_whitespace(error_file);
        parsed_cmd->error_file = strdup(error_file);
        trim_whitespace(cmd_copy);
    }
    
    // Tokenize the remaining command
    parsed_cmd->args = tokenize(cmd_copy, &parsed_cmd->argc);
    
    free(cmd_copy);
    return parsed_cmd;
}

// Free command structure
void free_command(command_t *cmd) {
    if (!cmd) return;
    
    if (cmd->args) {
        free_string_array(cmd->args, cmd->argc);
    }
    if (cmd->input_file) {
        free(cmd->input_file);
    }
    if (cmd->output_file) {
        free(cmd->output_file);
    }
    if (cmd->error_file) {
        free(cmd->error_file);
    }
    free(cmd);
}

// Check if command is a built-in
int is_builtin(char *cmd) {
    if (!cmd) return 0;
    
    char *cmd_copy = strdup(cmd);
    if (!cmd_copy) return 0;
    
    char *first_token = strtok(cmd_copy, " \t");
    if (!first_token) {
        free(cmd_copy);
        return 0;
    }
    
    int result = (strcmp(first_token, "cd") == 0 ||
                  strcmp(first_token, "pwd") == 0 ||
                  strcmp(first_token, "echo") == 0 ||
                  strcmp(first_token, "exit") == 0 ||
                  strcmp(first_token, "history") == 0 ||
                  strcmp(first_token, "jobs") == 0 ||
                  strcmp(first_token, "fg") == 0 ||
                  strcmp(first_token, "bg") == 0);
    
    free(cmd_copy);
    return result;
}

// Check if command contains pipeline
int is_pipeline(char *cmd) {
    return strstr(cmd, "|") != NULL;
}

// Split pipeline into individual commands
char** split_pipeline(char *cmd, int *count) {
    *count = 0;
    char **commands = malloc(MAX_ARGS * sizeof(char*));
    if (!commands) {
        print_error("Memory allocation failed");
        return NULL;
    }
    
    char *token = strtok(cmd, "|");
    while (token != NULL && *count < MAX_ARGS) {
        trim_whitespace(token);
        if (strlen(token) > 0) {
            commands[*count] = strdup(token);
            (*count)++;
        }
        token = strtok(NULL, "|");
    }
    
    return commands;
}

// Tokenize string into array of tokens
char** tokenize(char *str, int *count) {
    *count = 0;
    char **tokens = malloc(MAX_ARGS * sizeof(char*));
    if (!tokens) {
        print_error("Memory allocation failed");
        return NULL;
    }
    
    // Make a copy since strtok modifies the original string
    char *str_copy = strdup(str);
    if (!str_copy) {
        free(tokens);
        return NULL;
    }
    
    char *token = strtok(str_copy, " \t");
    while (token != NULL && *count < MAX_ARGS) {
        tokens[*count] = strdup(token);
        (*count)++;
        token = strtok(NULL, " \t");
    }
    
    free(str_copy);
    return tokens;
}

// Remove leading and trailing whitespace
void trim_whitespace(char *str) {
    if (!str) return;
    
    // Remove leading whitespace
    char *start = str;
    while (*start && (*start == ' ' || *start == '\t' || *start == '\n' || *start == '\r')) {
        start++;
    }
    
    // Remove trailing whitespace
    char *end = start + strlen(start) - 1;
    while (end > start && (*end == ' ' || *end == '\t' || *end == '\n' || *end == '\r')) {
        end--;
    }
    
    // Move string to beginning and null terminate
    if (start != str) {
        memmove(str, start, end - start + 1);
    }
    str[end - start + 1] = '\0';
}
