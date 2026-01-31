#include "headers/utils.h"
#include <limits.h>
#include <stdlib.h>
#include <string.h>

// Expand tilde in path
char *expand_tilde(char *path) {
  if (!path)
    return NULL;

  if (path[0] == '~') {
    char *home = getenv("HOME");
    if (!home) {
      return strdup(path); // Return original if HOME not set
    }

    int home_len = strlen(home);
    int path_len = strlen(path);
    char *expanded = malloc(home_len + path_len);

    if (!expanded) {
      return NULL;
    }

    strcpy(expanded, home);
    strcat(expanded, path + 1); // Skip the '~'

    return expanded;
  }

  return strdup(path);
}

// Get absolute path
char *get_absolute_path(char *path) {
  if (!path)
    return NULL;

  char *abs_path = malloc(PATH_MAX);
  if (!abs_path)
    return NULL;

  if (realpath(path, abs_path) == NULL) {
    free(abs_path);
    return strdup(path); // Return original if realpath fails
  }

  return abs_path;
}

// Check if file is executable
int is_executable(char *path) {
  if (!path)
    return 0;

  struct stat st;
  if (stat(path, &st) == 0) {
    return (st.st_mode & S_IXUSR) || (st.st_mode & S_IXGRP) ||
           (st.st_mode & S_IXOTH);
  }

  return 0;
}

// Print error message
void print_error(char *msg) { fprintf(stderr, "mini-bash: %s\n", msg); }

// Print error message with errno
void print_error_with_errno(char *msg) {
  fprintf(stderr, "mini-bash: %s: %s\n", msg, strerror(errno));
}

// String duplicate (for compatibility with older systems)
#ifndef _POSIX_C_SOURCE
char *strdup(const char *s) {
  if (!s)
    return NULL;

  size_t len = strlen(s) + 1;
  char *dup = malloc(len);
  if (dup) {
    memcpy(dup, s, len);
  }
  return dup;
}
#endif

// Free string array
void free_string_array(char **arr, int count) {
  if (!arr)
    return;

  for (int i = 0; i < count; i++) {
    if (arr[i]) {
      free(arr[i]);
    }
  }
  free(arr);
}
