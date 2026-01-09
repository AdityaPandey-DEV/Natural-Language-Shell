#ifndef PARSER_H
#define PARSER_H

#include "shell.h"

// Function prototypes
command_t* parse_command(char *cmd);
void free_command(command_t *cmd);
int is_builtin(char *cmd);
int is_pipeline(char *cmd);
char** split_pipeline(char *cmd, int *count);
char** tokenize(char *str, int *count);
void trim_whitespace(char *str);

#endif
