package dev.rishon.jdevtools;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit test for App class
 */
public class AppTest {
    
    @Test
    public void testGetVersion() {
        App app = new App();
        assertEquals("1.0.0", app.getVersion());
    }
    
    @Test
    public void testAppNotNull() {
        App app = new App();
        assertNotNull(app);
    }
}
