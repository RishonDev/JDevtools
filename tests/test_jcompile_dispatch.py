"""Tests for jcompile_dispatch module."""

import os
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from jdevtools.jcompile_dispatch import PomGenerator


def test_basic_pom_generation():
    """Test basic POM file generation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = os.path.join(tmpdir, 'pom.xml')
        generator = PomGenerator()
        result = generator.generate(output_path=output_file)
        
        assert os.path.exists(output_file), "POM file should be created"
        assert result == output_file, "Should return output file path"
        
        # Parse and verify structure
        tree = ET.parse(output_file)
        root = tree.getroot()
        
        # Check namespace
        assert 'maven.apache.org' in root.tag, "Should have Maven namespace"
        
        # Check basic elements
        ns = {'mvn': 'http://maven.apache.org/POM/4.0.0'}
        assert root.find('mvn:modelVersion', ns) is not None, "Should have modelVersion"
        assert root.find('mvn:groupId', ns) is not None, "Should have groupId"
        assert root.find('mvn:artifactId', ns) is not None, "Should have artifactId"
        assert root.find('mvn:version', ns) is not None, "Should have version"
        
        print("✓ Basic POM generation test passed")


def test_native_image_plugin():
    """Test that native image plugin is included."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = os.path.join(tmpdir, 'pom.xml')
        generator = PomGenerator()
        generator.generate(output_path=output_file)
        
        tree = ET.parse(output_file)
        root = tree.getroot()
        
        # Read file content
        with open(output_file, 'r') as f:
            content = f.read()
        
        assert 'org.graalvm.buildtools' in content, "Should include GraalVM plugin"
        assert 'native-maven-plugin' in content, "Should include native-maven-plugin"
        
        print("✓ Native image plugin test passed")


def test_linux_specific_plugins():
    """Test that Linux-specific plugins are included on Linux."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = os.path.join(tmpdir, 'pom.xml')
        generator = PomGenerator()
        os_type = generator._get_os_type()
        generator.generate(output_path=output_file)
        
        with open(output_file, 'r') as f:
            content = f.read()
        
        if os_type == 'linux':
            assert 'rpm-maven-plugin' in content, "Should include RPM plugin on Linux"
            assert 'org.codehaus.mojo' in content, "Should include Codehaus Mojo"
            assert 'jdeb' in content, "Should include jdeb plugin on Linux"
            print("✓ Linux-specific plugins test passed")
        else:
            print(f"⊘ Skipping Linux-specific test (running on {os_type})")


def test_merge_with_existing():
    """Test merging with existing POM file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        existing_file = os.path.join(tmpdir, 'existing.xml')
        output_file = os.path.join(tmpdir, 'merged.xml')
        
        # Create existing POM
        existing_content = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.test</groupId>
    <artifactId>test-app</artifactId>
    <version>3.0.0</version>
    <name>Test App</name>
    <properties>
        <mainClass>com.test.Main</mainClass>
    </properties>
</project>"""
        
        with open(existing_file, 'w') as f:
            f.write(existing_content)
        
        # Generate merged POM
        generator = PomGenerator(existing_pom=existing_file)
        generator.generate(output_path=output_file)
        
        # Verify merge
        with open(output_file, 'r') as f:
            content = f.read()
        
        assert 'com.test' in content, "Should preserve existing groupId"
        assert 'test-app' in content, "Should preserve existing artifactId"
        assert '3.0.0' in content, "Should preserve existing version"
        assert 'Test App' in content, "Should preserve existing name"
        assert 'com.test.Main' in content, "Should preserve existing mainClass"
        assert 'native-maven-plugin' in content, "Should add native-maven-plugin"
        
        print("✓ Merge with existing POM test passed")


def test_properties_preserved():
    """Test that properties from existing POM are preserved."""
    with tempfile.TemporaryDirectory() as tmpdir:
        existing_file = os.path.join(tmpdir, 'existing.xml')
        output_file = os.path.join(tmpdir, 'merged.xml')
        
        # Create existing POM with custom properties
        existing_content = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>my-app</artifactId>
    <version>1.0-SNAPSHOT</version>
    <properties>
        <custom.property>custom-value</custom.property>
        <another.property>another-value</another.property>
    </properties>
</project>"""
        
        with open(existing_file, 'w') as f:
            f.write(existing_content)
        
        # Generate merged POM
        generator = PomGenerator(existing_pom=existing_file)
        generator.generate(output_path=output_file)
        
        # Verify properties preserved
        with open(output_file, 'r') as f:
            content = f.read()
        
        assert 'custom.property' in content, "Should preserve custom property"
        assert 'custom-value' in content, "Should preserve custom property value"
        assert 'another.property' in content, "Should preserve another property"
        assert 'another-value' in content, "Should preserve another property value"
        
        print("✓ Properties preservation test passed")


if __name__ == '__main__':
    print("Running jcompile-dispatch tests...\n")
    
    try:
        test_basic_pom_generation()
        test_native_image_plugin()
        test_linux_specific_plugins()
        test_merge_with_existing()
        test_properties_preserved()
        
        print("\n✅ All tests passed!")
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error running tests: {e}")
        sys.exit(1)
