# JDevtools
Curated Dev tools for creating native apps in Core Java and Java

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
