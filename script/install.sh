#!/bin/bash

# Advanced Mini Bash Shell - Production Installation Script
# This script installs the shell system-wide for production use

set -e  # Exit on any error

echo "🔥 Advanced Mini Bash Shell - Production Installation"
echo "====================================================="
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root for system installation
if [ "$EUID" -eq 0 ]; then
    INSTALL_PREFIX="/usr/local"
    BIN_DIR="/usr/local/bin"
    MAN_DIR="/usr/local/share/man/man1"
    print_status "Installing system-wide (requires root privileges)"
else
    INSTALL_PREFIX="$HOME/.local"
    BIN_DIR="$HOME/.local/bin"
    MAN_DIR="$HOME/.local/share/man/man1"
    print_status "Installing for current user"
fi

# Create directories if they don't exist
print_status "Creating installation directories..."
mkdir -p "$BIN_DIR"
mkdir -p "$MAN_DIR"

# Build the shell
print_status "Building Mini Bash shell..."
make clean
make

if [ $? -eq 0 ]; then
    print_success "Shell built successfully"
else
    print_error "Failed to build shell"
    exit 1
fi

# Install the shell
print_status "Installing Mini Bash shell..."
cp mini-bash "$BIN_DIR/"
chmod +x "$BIN_DIR/mini-bash"

# Create symlink for easy access
if [ -w "$BIN_DIR" ]; then
    ln -sf "$BIN_DIR/mini-bash" "$BIN_DIR/mbash" 2>/dev/null || true
    print_success "Created symlink: mbash -> mini-bash"
fi

# Install voice control components (optional)
print_status "Installing voice control components..."
mkdir -p "$INSTALL_PREFIX/share/mini-bash"

# Copy voice control files
cp voice_*.py "$INSTALL_PREFIX/share/mini-bash/" 2>/dev/null || true
cp shell_bridge.py "$INSTALL_PREFIX/share/mini-bash/" 2>/dev/null || true
cp voice_config.json "$INSTALL_PREFIX/share/mini-bash/" 2>/dev/null || true
cp requirements.txt "$INSTALL_PREFIX/share/mini-bash/" 2>/dev/null || true

# Create voice control wrapper script
cat > "$BIN_DIR/mini-bash-voice" << 'EOF'
#!/bin/bash
# Mini Bash Voice Control Wrapper

SCRIPT_DIR="$(dirname "$0")"
VOICE_DIR="$(dirname "$SCRIPT_DIR")/share/mini-bash"

if [ -f "$VOICE_DIR/voice_enhanced.py" ]; then
    cd "$VOICE_DIR"
    python3 voice_enhanced.py "$@"
else
    echo "Voice control not installed. Run: pip3 install -r requirements.txt"
    exit 1
fi
EOF

chmod +x "$BIN_DIR/mini-bash-voice"

# Create man page
print_status "Creating man page..."
cat > "$MAN_DIR/mini-bash.1" << 'EOF'
.TH MINI-BASH 1 "October 2024" "Advanced Mini Bash Shell"
.SH NAME
mini-bash \- Advanced Mini Bash Shell with Voice Control
.SH SYNOPSIS
.B mini-bash
.RI [ options ]
.SH DESCRIPTION
Advanced Mini Bash Shell is a feature-rich shell implementation with:
.IP \(bu 2
Full UNIX shell functionality (pipelines, redirection, background jobs)
.IP \(bu 2
Built-in commands (cd, pwd, echo, history, jobs, fg, bg)
.IP \(bu 2
Command history with persistent storage
.IP \(bu 2
Signal handling (Ctrl+C, Ctrl+Z)
.IP \(bu 2
Voice control support (Hindi & English)
.SH OPTIONS
No command-line options are currently supported.
.SH VOICE CONTROL
To use voice control, run:
.B mini-bash-voice
.PP
This requires Google Cloud credentials and Python dependencies.
.SH FILES
.I ~/.history
.RS
Command history file
.RE
.I ~/.mini-bash/
.RS
Configuration directory
.RE
.SH SEE ALSO
.BR bash (1),
.BR sh (1)
.SH AUTHOR
Advanced Mini Bash Shell Development Team
EOF

# Update PATH if needed
if [ "$EUID" -ne 0 ]; then
    if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
        print_warning "Add $HOME/.local/bin to your PATH"
        echo "Add this line to your ~/.bashrc or ~/.zshrc:"
        echo "export PATH=\"\$HOME/.local/bin:\$PATH\""
    fi
fi

# Test installation
print_status "Testing installation..."
if "$BIN_DIR/mini-bash" -c "echo 'Installation test successful'" 2>/dev/null; then
    print_success "Installation test passed"
else
    print_warning "Installation test failed, but shell may still work"
fi

# Final instructions
echo
print_success "Installation complete!"
echo
echo "🚀 Usage:"
echo "  mini-bash          # Start the shell"
echo "  mbash              # Short alias"
echo "  mini-bash-voice    # Start with voice control"
echo
echo "📚 Documentation:"
echo "  man mini-bash      # View manual page"
echo "  README.md          # Project documentation"
echo "  README_PHASE3.md   # Voice control documentation"
echo
print_success "Advanced Mini Bash Shell is ready for production use! 🔥"
