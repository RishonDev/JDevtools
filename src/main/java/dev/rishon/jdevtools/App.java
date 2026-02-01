package dev.rishon.jdevtools;

/**
 * Main class for JDevtools
 */
public class App {
    public static void main(String[] args) {
        System.out.println("JDevtools - Maven Wrapper Tools");
        System.out.println("Available tools: jcompile, jcompile-dispatch, jtest, jconfigure");
    }
    
    public String getVersion() {
        return "1.0.0";
    }
}
