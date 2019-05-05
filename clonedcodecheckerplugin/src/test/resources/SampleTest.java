import org.junit.Test;
import org.osgi.framework.Bundle;
import org.osgi.framework.BundleContext;
import org.osgi.framework.BundleException;
import org.osgi.framework.FrameworkUtil;
import org.eclipse.swt.widgets.Shell;
import clonedcodechecker.handlers.RunHandler;
import clonedcodechecker.Activator;

import org.osgi.framework.BundleActivator;

public class SampleTest
{
	private static Bundle bundle = FrameworkUtil.getBundle(Activator.class);
	private static BundleContext testcontext = bundle.getBundleContext();
	private static BundleContext context;
	private RunHandler runHandler = new RunHandler();
	private Shell shell = new Shell();

	@Test
	public void testActivator() throws BundleException {
		this.bundle.start();
		this.bundle.stop();
	}

	@Test
	public void testHandlersetInitString() {
		this.runHandler.setInitString("/home");
	}

	@Test
	public void testHandlersetInputDialog() {
		this.runHandler.setInputDialog(shell);
		this.runHandler.openInputDialog();
		this.runHandler.okDialog();
	}

	public void testHandlergetInput() {
		this.runHandler.getInput();
	}

	@Test
	public void testHandlergetprocessBuilder() {
		this.runHandler.getprocessBuilder("/home");
	}

}
