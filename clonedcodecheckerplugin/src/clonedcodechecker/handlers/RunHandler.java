package clonedcodechecker.handlers;

import java.io.IOException;

import javax.inject.Named;

import clonedcodechecker.handlers.InternalInputDialog;

import org.eclipse.e4.core.di.annotations.Execute;
import org.eclipse.e4.ui.services.IServiceConstants;
import org.eclipse.jface.dialogs.InputDialog;
import org.eclipse.swt.widgets.Shell;

/** <b>Warning</b> :
As explained in <a href="http://wiki.eclipse.org/Eclipse4/RCP/FAQ#Why_aren.27t_my_handler_fields_being_re-injected.3F">this wiki page</a>, it is not recommended to define @Inject fields in a handler. <br/><br/>
<b>Inject the values in the @Execute methods</b>
*/
public class RunHandler {
	private InternalInputDialog inputdialog;
	private String init_string = System.getProperty("user.home");

	@Execute
	public void execute(@Named(IServiceConstants.ACTIVE_SHELL) Shell s) {
		
		
		this.setInputDialog(s);
		this.openInputDialog();
		String inputstring = this.getInput();
		ProcessBuilder pBuilder = this.getprocessBuilder(inputstring);
		
		try {
			this.startProcess(pBuilder);
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	public void setInputDialog(Shell s) {
		this.inputdialog = new InternalInputDialog(s,
				"Run Cloned Code Checker",
				"Please enter a directory to check:",
				this.init_string, null);
	}
	
	public void openInputDialog() {
		this.inputdialog.open();
	}
		
	public void closeDialog() {
		this.inputdialog.close();
	}
	
	public String getInput() {
		return this.inputdialog.getValue();
	}
	
	public ProcessBuilder getprocessBuilder(String entered_directory) {
		ProcessBuilder processBuilder = new ProcessBuilder().inheritIO();
		String commandString = "ccc" + " -rjd " + entered_directory;
		processBuilder.command("bash", "-c", commandString);
		return processBuilder;
	}
	
	public void startProcess(ProcessBuilder processBuilder) throws IOException {
		processBuilder.start();
	}
	
	public void setInitString(String s) {
		this.init_string = s;
	}
	
	




}
