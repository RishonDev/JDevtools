#!/usr/bin/env python3
"""
jcompile-dispatch - Java compilation dispatcher with native image and packaging support.

This tool generates Maven POM files with GraalVM native-image support and
platform-specific packaging plugins (deb/rpm for Linux).
"""

import argparse
import os
import platform
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.dom import minidom


class PomGenerator:
    """Generates Maven POM files with native image and packaging support."""
    
    def __init__(self, existing_pom=None):
        """
        Initialize the POM generator.
        
        Args:
            existing_pom: Path to existing POM file to merge with (optional)
        """
        self.existing_pom = existing_pom
        self.namespace = "http://maven.apache.org/POM/4.0.0"
        
    def _get_os_type(self):
        """Determine the operating system type."""
        system = platform.system().lower()
        if system == "linux":
            return "linux"
        elif system == "darwin":
            return "mac"
        elif system == "windows":
            return "windows"
        else:
            return "unknown"
    
    def _create_base_pom(self):
        """Create a base POM structure."""
        ET.register_namespace('', self.namespace)
        
        root = ET.Element("{%s}project" % self.namespace)
        root.set("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation",
                "http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd")
        
        # Model version
        model_version = ET.SubElement(root, "{%s}modelVersion" % self.namespace)
        model_version.text = "4.0.0"
        
        # Basic project info
        group_id = ET.SubElement(root, "{%s}groupId" % self.namespace)
        group_id.text = "com.example"
        
        artifact_id = ET.SubElement(root, "{%s}artifactId" % self.namespace)
        artifact_id.text = "my-app"
        
        version = ET.SubElement(root, "{%s}version" % self.namespace)
        version.text = "1.0-SNAPSHOT"
        
        return root
    
    def _add_properties(self, root):
        """Add properties section to POM."""
        properties = ET.SubElement(root, "{%s}properties" % self.namespace)
        
        maven_compiler_source = ET.SubElement(properties, "{%s}maven.compiler.source" % self.namespace)
        maven_compiler_source.text = "11"
        
        maven_compiler_target = ET.SubElement(properties, "{%s}maven.compiler.target" % self.namespace)
        maven_compiler_target.text = "11"
        
        project_build_source = ET.SubElement(properties, "{%s}project.build.sourceEncoding" % self.namespace)
        project_build_source.text = "UTF-8"
        
        native_image_version = ET.SubElement(properties, "{%s}native.maven.plugin.version" % self.namespace)
        native_image_version.text = "0.9.28"
        
        return properties
    
    def _add_native_image_plugin(self, plugins):
        """Add GraalVM native-image plugin."""
        plugin = ET.SubElement(plugins, "{%s}plugin" % self.namespace)
        
        group_id = ET.SubElement(plugin, "{%s}groupId" % self.namespace)
        group_id.text = "org.graalvm.buildtools"
        
        artifact_id = ET.SubElement(plugin, "{%s}artifactId" % self.namespace)
        artifact_id.text = "native-maven-plugin"
        
        version = ET.SubElement(plugin, "{%s}version" % self.namespace)
        version.text = "${native.maven.plugin.version}"
        
        extensions = ET.SubElement(plugin, "{%s}extensions" % self.namespace)
        extensions.text = "true"
        
        configuration = ET.SubElement(plugin, "{%s}configuration" % self.namespace)
        
        image_name = ET.SubElement(configuration, "{%s}imageName" % self.namespace)
        image_name.text = "${project.artifactId}"
        
        main_class = ET.SubElement(configuration, "{%s}mainClass" % self.namespace)
        main_class.text = "${mainClass}"
        
        build_args = ET.SubElement(configuration, "{%s}buildArgs" % self.namespace)
        
        build_arg1 = ET.SubElement(build_args, "{%s}buildArg" % self.namespace)
        build_arg1.text = "--no-fallback"
        
        build_arg2 = ET.SubElement(build_args, "{%s}buildArg" % self.namespace)
        build_arg2.text = "--enable-url-protocols=http,https"
        
        return plugin
    
    def _add_rpm_plugin(self, plugins):
        """Add Maven RPM plugin for Linux."""
        plugin = ET.SubElement(plugins, "{%s}plugin" % self.namespace)
        
        group_id = ET.SubElement(plugin, "{%s}groupId" % self.namespace)
        group_id.text = "org.codehaus.mojo"
        
        artifact_id = ET.SubElement(plugin, "{%s}artifactId" % self.namespace)
        artifact_id.text = "rpm-maven-plugin"
        
        version = ET.SubElement(plugin, "{%s}version" % self.namespace)
        version.text = "2.2.0"
        
        configuration = ET.SubElement(plugin, "{%s}configuration" % self.namespace)
        
        name_elem = ET.SubElement(configuration, "{%s}name" % self.namespace)
        name_elem.text = "${project.artifactId}"
        
        version_elem = ET.SubElement(configuration, "{%s}version" % self.namespace)
        version_elem.text = "${project.version}"
        
        group_elem = ET.SubElement(configuration, "{%s}group" % self.namespace)
        group_elem.text = "Applications/Development"
        
        packager = ET.SubElement(configuration, "{%s}packager" % self.namespace)
        packager.text = "JDevtools"
        
        return plugin
    
    def _add_deb_plugin(self, plugins):
        """Add Maven DEB plugin for Linux."""
        plugin = ET.SubElement(plugins, "{%s}plugin" % self.namespace)
        
        group_id = ET.SubElement(plugin, "{%s}groupId" % self.namespace)
        group_id.text = "org.vafer"
        
        artifact_id = ET.SubElement(plugin, "{%s}artifactId" % self.namespace)
        artifact_id.text = "jdeb"
        
        version = ET.SubElement(plugin, "{%s}version" % self.namespace)
        version.text = "1.10"
        
        configuration = ET.SubElement(plugin, "{%s}configuration" % self.namespace)
        
        data_set = ET.SubElement(configuration, "{%s}dataSet" % self.namespace)
        
        data = ET.SubElement(data_set, "{%s}data" % self.namespace)
        
        src = ET.SubElement(data, "{%s}src" % self.namespace)
        src.text = "${project.build.directory}/${project.build.finalName}.jar"
        
        type_elem = ET.SubElement(data, "{%s}type" % self.namespace)
        type_elem.text = "file"
        
        mapper = ET.SubElement(data, "{%s}mapper" % self.namespace)
        
        mapper_type = ET.SubElement(mapper, "{%s}type" % self.namespace)
        mapper_type.text = "perm"
        
        prefix = ET.SubElement(mapper, "{%s}prefix" % self.namespace)
        prefix.text = "/usr/share/${project.artifactId}"
        
        return plugin
    
    def _merge_with_existing(self, new_root):
        """
        Merge new POM with existing POM file if provided.
        
        Args:
            new_root: The new POM root element
            
        Returns:
            Merged POM root element
        """
        if not self.existing_pom or not os.path.exists(self.existing_pom):
            return new_root
        
        try:
            tree = ET.parse(self.existing_pom)
            existing_root = tree.getroot()
            
            # Merge basic project info if exists
            for tag in ['groupId', 'artifactId', 'version', 'name', 'description']:
                existing_elem = existing_root.find("{%s}%s" % (self.namespace, tag))
                new_elem = new_root.find("{%s}%s" % (self.namespace, tag))
                
                if existing_elem is not None:
                    if new_elem is not None:
                        new_elem.text = existing_elem.text
                    else:
                        # Insert after modelVersion
                        model_version = new_root.find("{%s}modelVersion" % self.namespace)
                        idx = list(new_root).index(model_version) + 1
                        new_root.insert(idx, existing_elem)
            
            # Merge properties
            existing_props = existing_root.find("{%s}properties" % self.namespace)
            new_props = new_root.find("{%s}properties" % self.namespace)
            
            if existing_props is not None and new_props is not None:
                for prop in existing_props:
                    prop_name = prop.tag.replace("{%s}" % self.namespace, "")
                    existing_new_prop = new_props.find("{%s}%s" % (self.namespace, prop_name))
                    if existing_new_prop is None:
                        new_props.append(prop)
            
            # Merge dependencies if they exist
            existing_deps = existing_root.find("{%s}dependencies" % self.namespace)
            if existing_deps is not None:
                new_deps = new_root.find("{%s}dependencies" % self.namespace)
                if new_deps is None:
                    new_root.append(existing_deps)
                else:
                    # Merge dependencies
                    for dep in existing_deps:
                        new_deps.append(dep)
            
            return new_root
        except Exception as e:
            print(f"Warning: Could not merge with existing POM: {e}")
            return new_root
    
    def generate(self, output_path="pom.xml"):
        """
        Generate the POM file.
        
        Args:
            output_path: Path where to save the generated POM file
            
        Returns:
            Path to generated POM file
        """
        # Create base POM structure
        root = self._create_base_pom()
        
        # Add properties
        self._add_properties(root)
        
        # Add build section
        build = ET.SubElement(root, "{%s}build" % self.namespace)
        plugins = ET.SubElement(build, "{%s}plugins" % self.namespace)
        
        # Always add native image plugin
        self._add_native_image_plugin(plugins)
        
        # Add platform-specific plugins
        os_type = self._get_os_type()
        if os_type == "linux":
            self._add_rpm_plugin(plugins)
            self._add_deb_plugin(plugins)
            print("Added Linux-specific packaging plugins (RPM and DEB)")
        
        # Merge with existing POM if provided
        root = self._merge_with_existing(root)
        
        # Pretty print the XML
        xml_str = ET.tostring(root, encoding='unicode')
        dom = minidom.parseString(xml_str)
        pretty_xml = dom.toprettyxml(indent="  ")
        
        # Remove extra blank lines
        lines = [line for line in pretty_xml.split('\n') if line.strip()]
        pretty_xml = '\n'.join(lines)
        
        # Write to file
        with open(output_path, 'w') as f:
            f.write(pretty_xml)
        
        print(f"Generated POM file: {output_path}")
        print(f"Platform: {os_type}")
        print(f"Native image support: enabled")
        
        return output_path


def main():
    """Main entry point for jcompile-dispatch."""
    parser = argparse.ArgumentParser(
        description="Java compilation dispatcher with native image and packaging support",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate a new POM file
  jcompile-dispatch --output pom.xml
  
  # Merge with existing POM file
  jcompile-dispatch --existing pom.xml --output pom-new.xml
  
  # Generate POM in current directory
  jcompile-dispatch
        """
    )
    
    parser.add_argument(
        '--existing',
        help='Path to existing POM file to merge with',
        default=None
    )
    
    parser.add_argument(
        '--output',
        help='Output path for generated POM file (default: pom.xml)',
        default='pom.xml'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='jcompile-dispatch 0.1.0'
    )
    
    args = parser.parse_args()
    
    try:
        generator = PomGenerator(existing_pom=args.existing)
        output_file = generator.generate(output_path=args.output)
        
        print("\nNext steps:")
        print("1. Review and customize the generated POM file")
        print("2. Set the mainClass property for native image generation")
        print("3. Run 'mvn clean package native:compile' to build native image")
        if generator._get_os_type() == "linux":
            print("4. Run 'mvn rpm:rpm' to create RPM package")
            print("5. Run 'mvn jdeb:jdeb' to create DEB package")
        
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
