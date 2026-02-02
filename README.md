# JDevtools
Curated Dev tools for creating native apps in Core Java and Java

## Overview

JDevtools provides a set of Maven wrapper-based tools for instant Java compilation and testing. These tools simplify and accelerate Java development workflows.

## Available Tools

### 1. jcompile-dispatch
A Maven wrapper dispatcher that intelligently compiles Java code using parallel processing.

**Usage:**
```bash
./jcompile-dispatch [OPTIONS]
```

**Options:**
- `--parallel [N]` - Use parallel compilation (default: 1 thread per core)
- `--threads N` - Use exactly N threads for compilation
- `--goals GOALS` - Custom Maven goals (default: clean compile)
- `-h, --help` - Display help message

**Examples:**
```bash
# Compile with parallel processing
./jcompile-dispatch --parallel

# Compile with 4 threads
./jcompile-dispatch --threads 4

# Custom goals
./jcompile-dispatch --goals "clean package"
```

### 2. jcompile
Fast Java compilation using the Maven wrapper with optimized settings.

**Usage:**
```bash
./jcompile [OPTIONS]
```

**Options:**
- `--clean` - Clean before compiling
- `--skip-tests` - Skip test compilation
- `--offline` - Work offline
- `--debug` - Enable debug output
- `--quiet` - Quiet output
- `-h, --help` - Display help message

**Examples:**
```bash
# Basic compilation
./jcompile

# Clean and compile
./jcompile --clean

# Compile in offline mode
./jcompile --offline
```

### 3. jtest
Fast Java testing tool with support for parallel execution and selective testing.

**Usage:**
```bash
./jtest [OPTIONS]
```

**Options:**
- `--compile` - Compile before testing
- `--integration` - Run integration tests (verify phase)
- `--single CLASS` - Run a single test class
- `--method CLASS` - Run specific test method
- `--parallel [N]` - Run tests in parallel (default 4 threads)
- `--offline` - Work offline
- `--debug` - Enable debug output
- `--quiet` - Quiet output
- `-h, --help` - Display help message

**Examples:**
```bash
# Run all tests
./jtest

# Run tests in parallel with 8 threads
./jtest --parallel 8

# Run a single test class
./jtest --single MyTestClass

# Compile and test
./jtest --compile
```

### 4. jconfigure
Configuration tool that verifies and displays the JDevtools setup.

**Usage:**
```bash
./jconfigure [COMMAND]
```

**Commands:**
- `check` - Check and verify configuration (default)
- `test` - Test Maven wrapper
- `show` - Show current configuration
- `help` - Display help message

**Examples:**
```bash
# Check configuration
./jconfigure

# Show configuration details
./jconfigure show

# Test Maven wrapper
./jconfigure test
```

## Windows Support

All tools are available for Windows with `.cmd` extensions:
- `jcompile-dispatch.cmd`
- `jcompile.cmd`
- `jtest.cmd`
- `jconfigure.cmd`

## Prerequisites

- Java 11 or higher
- Internet connection (for initial Maven wrapper download)

## Quick Start

1. Clone the repository
2. Run configuration check:
   ```bash
   ./jconfigure
   ```
3. Compile your Java project:
   ```bash
   ./jcompile
   ```
4. Run tests:
   ```bash
   ./jtest
   ```

## Maven Wrapper

JDevtools includes a Maven wrapper that automatically downloads and uses the correct Maven version, ensuring consistency across different development environments.

## License

This project is open source and available under standard licensing terms.
## Tools

### jcompile-dispatch

Java compilation dispatcher with native image and packaging support.

This tool generates Maven POM files with:
- **GraalVM native-image support** for creating platform-specific native executables (Mac, Linux, Windows)
- **Linux packaging plugins** (RPM and DEB) - automatically included when running on Linux
- **Merging with existing POM files** - preserves your project settings

#### Installation

```bash
pip install -e .
```

Or run directly:

```bash
python3 -m jdevtools.jcompile_dispatch
```

#### Usage

Generate a new POM file:
```bash
jcompile-dispatch --output pom.xml
```

Merge with existing POM file:
```bash
jcompile-dispatch --existing pom.xml --output pom-new.xml
```

#### Building Native Images

After generating the POM file:

1. Review and customize the generated POM file
2. Ensure the `mainClass` property is set correctly
3. Build native image:
   ```bash
   mvn clean package native:compile
   ```

#### Creating Linux Packages

On Linux systems, you can create distribution packages:

Create RPM package:
```bash
mvn rpm:rpm
```

Create DEB package:
```bash
mvn jdeb:jdeb
```

## Features

- ✅ Cross-platform native image generation (Mac, Linux, Windows)
- ✅ Automatic platform detection
- ✅ Linux-specific packaging (RPM/DEB) when on Linux
- ✅ Merges with existing Maven POM files
- ✅ Preserves user settings and dependencies
- ✅ Uses Codehaus Mojo plugins for RPM packaging
- ✅ Uses jdeb for DEB packaging
