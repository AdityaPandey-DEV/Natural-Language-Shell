#include "headers/jobs.h"
#include "headers/utils.h"

// Add a new job
int add_job(pid_t pid, char *command) {
    if (job_count >= MAX_JOBS) {
        print_error("Maximum number of jobs reached");
        return -1;
    }
    
    // Find empty slot
    for (int i = 0; i < MAX_JOBS; i++) {
        if (jobs[i].pid == 0) {
            jobs[i].pid = pid;
            jobs[i].job_id = ++current_job_id;
            jobs[i].command = strdup(command);
            jobs[i].status = 0; // Running
            jobs[i].start_time = time(NULL);
            job_count++;
            return jobs[i].job_id;
        }
    }
    
    return -1;
}

// Remove a job
int remove_job(pid_t pid) {
    for (int i = 0; i < MAX_JOBS; i++) {
        if (jobs[i].pid == pid) {
            if (jobs[i].command) {
                free(jobs[i].command);
            }
            jobs[i].pid = 0;
            jobs[i].job_id = 0;
            jobs[i].command = NULL;
            jobs[i].status = 0;
            jobs[i].start_time = 0;
            job_count--;
            return 0;
        }
    }
    return -1;
}

// Find job by job ID
job_t* find_job(int job_id) {
    for (int i = 0; i < MAX_JOBS; i++) {
        if (jobs[i].job_id == job_id && jobs[i].pid != 0) {
            return &jobs[i];
        }
    }
    return NULL;
}

// Find job by process ID
job_t* find_job_by_pid(pid_t pid) {
    for (int i = 0; i < MAX_JOBS; i++) {
        if (jobs[i].pid == pid) {
            return &jobs[i];
        }
    }
    return NULL;
}

// Update job status
void update_job_status(pid_t pid, int status) {
    job_t *job = find_job_by_pid(pid);
    if (job) {
        job->status = status;
    }
}

// Print all jobs
void print_jobs(void) {
    printf("Job ID\tPID\tStatus\tCommand\n");
    printf("------\t---\t------\t-------\n");
    
    for (int i = 0; i < MAX_JOBS; i++) {
        if (jobs[i].pid != 0) {
            const char *status_str = "Unknown";
            switch (jobs[i].status) {
                case 0: status_str = "Running"; break;
                case 1: status_str = "Stopped"; break;
                case 2: status_str = "Completed"; break;
            }
            printf("[%d]\t%d\t%s\t%s\n", 
                   jobs[i].job_id, jobs[i].pid, status_str, jobs[i].command);
        }
    }
}

// Wait for a specific job
int wait_for_job(int job_id) {
    job_t *job = find_job(job_id);
    if (!job) {
        print_error("No such job");
        return -1;
    }
    
    int status;
    pid_t result = waitpid(job->pid, &status, 0);
    
    if (result == -1) {
        print_error_with_errno("waitpid failed");
        return -1;
    }
    
    // Remove completed job
    remove_job(job->pid);
    
    return WEXITSTATUS(status);
}

// Resume a job (foreground or background)
int resume_job(int job_id, int foreground) {
    job_t *job = find_job(job_id);
    if (!job) {
        print_error("No such job");
        return -1;
    }
    
    if (job->status == 1) { // Stopped
        if (kill(job->pid, SIGCONT) == -1) {
            print_error_with_errno("Cannot resume job");
            return -1;
        }
        job->status = 0; // Running
    }
    
    if (foreground) {
        // Bring to foreground
        if (tcsetpgrp(STDIN_FILENO, getpgid(job->pid)) == -1) {
            print_error_with_errno("Cannot bring job to foreground");
            return -1;
        }
        
        // Wait for job to complete
        int status;
        waitpid(job->pid, &status, WUNTRACED);
        
        if (WIFSTOPPED(status)) {
            job->status = 1; // Stopped
            printf("\n[%d] Stopped\t%s\n", job->job_id, job->command);
        } else {
            remove_job(job->pid);
        }
        
        // Restore terminal control
        tcsetpgrp(STDIN_FILENO, getpgrp());
    }
    
    return 0;
}

// Clean up completed jobs
void cleanup_completed_jobs(void) {
    for (int i = 0; i < MAX_JOBS; i++) {
        if (jobs[i].pid != 0) {
            int status;
            pid_t result = waitpid(jobs[i].pid, &status, WNOHANG);
            
            if (result > 0) {
                // Process has terminated
                printf("\n[%d] Done\t%s\n", jobs[i].job_id, jobs[i].command);
                remove_job(jobs[i].pid);
            }
        }
    }
}
