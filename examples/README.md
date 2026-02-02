# Examples

## Example 1: Generate a Basic POM

```bash
cd examples
python3 -m jdevtools.jcompile_dispatch --output example-pom.xml
```

This generates a basic POM file with:
- GraalVM native-image plugin configured
- Platform-specific packaging plugins (RPM and DEB on Linux)
- Default project structure

## Example 2: Merge with Existing POM

If you have an existing POM file:

```bash
# Create a sample existing POM
cat > my-existing-pom.xml << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    
    <groupId>com.mycompany</groupId>
    <artifactId>my-java-app</artifactId>
    <version>2.0.0</version>
    <name>My Java Application</name>
    <description>A sample Java application</description>
    
    <properties>
        <mainClass>com.mycompany.Main</mainClass>
        <java.version>17</java.version>
    </properties>
    
    <dependencies>
        <dependency>
            <groupId>org.slf4j</groupId>
            <artifactId>slf4j-api</artifactId>
            <version>2.0.0</version>
        </dependency>
    </dependencies>
</project>
EOF

# Merge with native image and packaging support
python3 -m jdevtools.jcompile_dispatch --existing my-existing-pom.xml --output enhanced-pom.xml
```

The enhanced POM will:
- Preserve your groupId, artifactId, version
- Keep your existing dependencies
- Preserve your custom properties (like mainClass)
- Add GraalVM native-image plugin
- Add Linux packaging plugins (if on Linux)

## Example 3: Build a Native Image

After generating the POM:

```bash
# Install the dependencies and compile
mvn clean package

# Build native image (requires GraalVM)
mvn native:compile

# The native executable will be in target/
ls -lh target/
```

## Example 4: Create Linux Packages

On Linux systems:

```bash
# Create RPM package
mvn rpm:rpm

# Create DEB package
mvn jdeb:jdeb

# Packages will be in target/
ls -lh target/*.rpm target/*.deb
```

## Platform Support

The tool automatically detects your platform:
- **Linux**: Adds RPM and DEB packaging plugins
- **Mac**: Only adds native-image plugin (no packaging plugins)
- **Windows**: Only adds native-image plugin (no packaging plugins)

This ensures the generated POM works on all platforms.
