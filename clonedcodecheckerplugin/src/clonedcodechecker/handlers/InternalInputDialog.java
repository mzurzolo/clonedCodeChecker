package clonedcodechecker.handlers;
import org.junit.*;

import java.io.IOException;

import org.eclipse.jface.dialogs.IInputValidator;
import org.eclipse.jface.dialogs.InputDialog;
import org.eclipse.swt.widgets.Shell;
import clonedcodechecker.handlers.RunHandler;

public class InternalInputDialog extends InputDialog {
	
	public InternalInputDialog(Shell s, String d, String d2, String i, IInputValidator n) {
		super(s, d, d2, i, n);
	}
	
	public boolean close() {
		return super.close();
	}
	
	public int open() {
		return super.open();
	}
	
	public String getValuet() {
		return super.getValue();
	}
}
