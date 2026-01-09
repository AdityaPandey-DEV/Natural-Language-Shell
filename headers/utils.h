#ifndef UTILS_H
#define UTILS_H

#include "shell.h"

// Function prototypes
char* expand_tilde(char *path);
char* get_absolute_path(char *path);
int is_executable(char *path);
void print_error(char *msg);
void print_error_with_errno(char *msg);
char* strdup(const char *s);
void free_string_array(char **arr, int count);

#endif
