
import org.junit.*;

import java.io.IOException;

import org.eclipse.jface.dialogs.InputDialog;
import org.eclipse.swt.widgets.Shell;
import clonedcodechecker.handlers.RunHandler;

public class MockTest {
	private Shell shell = new Shell();
    private RunHandler runHandler = new RunHandler();

    public void testsetInputDialog() {
    	this.runHandler.setInputDialog(this.shell);
    }

    public void testopencloseDialog() {
    	this.runHandler.openInputDialog();
    	this.runHandler.closeDialog();
    }


    public void testgetInput() {
		this.runHandler.getInput();
    }

    public void testProcess() {
    	ProcessBuilder pb = this.runHandler.getprocessBuilder("/tmp");
			try {
				this.runHandler.startProcess(pb);
			} catch (IOException e) {
				e.printStackTrace();
			}
    }

    public void testsetInitString() {
    	this.runHandler.setInitString("/tmp");
	}

    public void execute() {
    	this.runHandler.setInitString("/tmp");
        runHandler.execute(shell);
        this.runHandler.closeDialog();
    }
}
