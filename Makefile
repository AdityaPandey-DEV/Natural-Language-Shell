# Advanced Mini Bash Shell Makefile

CC = gcc
CFLAGS = -Wall -Wextra -std=c99 -g -O2
LDFLAGS = 
TARGET = mini-bash
HEADERS_DIR = headers

# Source files
SOURCES = main.c parser.c executor.c builtin.c redirection.c pipeline.c jobs.c history.c utils.c
OBJECTS = $(SOURCES:.c=.o)

# Default target
all: $(TARGET)

# Build the main executable
$(TARGET): $(OBJECTS)
	$(CC) $(OBJECTS) -o $(TARGET) $(LDFLAGS)
	@echo "Build complete! Run './$(TARGET)' to start the shell."

# Compile source files
%.o: %.c
	$(CC) $(CFLAGS) -I$(HEADERS_DIR) -c $< -o $@

# Clean build artifacts
clean:
	rm -f $(OBJECTS) $(TARGET) .history
	@echo "Clean complete!"

# Install (optional)
install: $(TARGET)
	cp $(TARGET) /usr/local/bin/
	@echo "Installed $(TARGET) to /usr/local/bin/"

# Uninstall (optional)
uninstall:
	rm -f /usr/local/bin/$(TARGET)
	@echo "Uninstalled $(TARGET) from /usr/local/bin/"

# Debug build
debug: CFLAGS += -DDEBUG -g3
debug: $(TARGET)

# Release build
release: CFLAGS += -DNDEBUG -O3
release: clean $(TARGET)

# Run the shell
run: $(TARGET)
	./$(TARGET)

# Test the shell with sample commands
test: $(TARGET)
	@echo "Testing basic commands..."
	@echo "ls" | ./$(TARGET)
	@echo "pwd" | ./$(TARGET)
	@echo "echo Hello World" | ./$(TARGET)

# Show help
help:
	@echo "Available targets:"
	@echo "  all      - Build the shell (default)"
	@echo "  clean    - Remove build artifacts"
	@echo "  debug    - Build with debug symbols"
	@echo "  release  - Build optimized release version"
	@echo "  run      - Build and run the shell"
	@echo "  test     - Run basic tests"
	@echo "  install  - Install to /usr/local/bin/"
	@echo "  uninstall- Remove from /usr/local/bin/"
	@echo ""
	@echo "Voice Control (Phase 3):"
	@echo "  voice-setup   - Setup voice control dependencies"
	@echo "  voice-install - Install Python voice dependencies"
	@echo "  voice-test    - Test voice control module"
	@echo "  voice-demo    - Run interactive voice demo"
	@echo "  voice-run     - Start voice-controlled shell"
	@echo ""
	@echo "  help     - Show this help message"

# Voice control targets
voice-setup: $(TARGET)
	@echo "Setting up voice control..."
	@chmod +x setup_voice.sh
	@./setup_voice.sh

voice-test: $(TARGET)
	@echo "Testing voice control..."
	@python3 test_voice.py

voice-demo: $(TARGET)
	@echo "Running voice control demo..."
	@python3 voice_demo.py

voice-run: $(TARGET)
	@echo "Starting voice-controlled shell..."
	@python3 voice_enhanced.py

# Install voice dependencies
voice-install:
	@echo "Installing voice control dependencies..."
	@pip3 install -r requirements.txt

# Phony targets
.PHONY: all clean install uninstall debug release run test help voice-setup voice-test voice-demo voice-run voice-install
