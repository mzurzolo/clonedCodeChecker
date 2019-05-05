
import static org.eclipse.swtbot.swt.finder.waits.Conditions.shellCloses;

import org.eclipse.swtbot.eclipse.finder.*;
import org.eclipse.swtbot.swt.finder.junit.SWTBotJunit4ClassRunner;
import org.eclipse.swtbot.swt.finder.widgets.SWTBotShell;
import org.junit.AfterClass;
import org.junit.BeforeClass;
import org.junit.Test;
import org.junit.runner.RunWith;

@RunWith(SWTBotJunit4ClassRunner.class)
public class SWTTest {

    private static SWTWorkbenchBot bot;

    @BeforeClass
    public static void initBot() {
        bot = new SWTWorkbenchBot();
        bot.viewByTitle("Welcome").close();
    }

    @AfterClass
    public static void afterClass() {
        bot.resetWorkbench();
    }

    @Test
    public void testCancel() {
    	bot.toolbarButtonWithTooltip("Run Cloned Code Checker").click();
    	SWTBotShell dialog = bot.shell("Cloned Code Checker");
        dialog.activate();
        bot.label("Please enter a directory to check:");
        bot.button("Cancel").click();
        bot.waitUntil(shellCloses(dialog));
    }

    public void testOK() {
    	bot.toolbarButtonWithTooltip("Run Cloned Code Checker").click();
    	SWTBotShell dialog = bot.shell("Cloned Code Checker");
        dialog.activate();
        bot.textWithLabel(
    			"Please enter a directory to check:"
    			).setText("/home/mzurzolo/CODE/SWE1/opencv");
        bot.button("OK").click();
        bot.waitUntil(shellCloses(dialog));
    }
}
