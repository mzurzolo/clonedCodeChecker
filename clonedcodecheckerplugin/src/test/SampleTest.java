package test;

import org.junit.Test;
import org.osgi.framework.Bundle;
import org.osgi.framework.BundleContext;
import org.osgi.framework.BundleException;
import org.osgi.framework.FrameworkUtil;

import clonedcodechecker.Activator;

import org.osgi.framework.BundleActivator;

public class SampleTest implements BundleActivator
{
	private static Bundle bundle = FrameworkUtil.getBundle(Activator.class);
	private static BundleContext context = bundle.getBundleContext();

	static BundleContext getContext() {
		return context;
	}

	public void start(BundleContext bundleContext) throws Exception {
		this.context = bundleContext;
	}

	public void stop(BundleContext bundleContext) throws Exception {
		this.context = null;
	}

    @Test
    public void testActivator() throws BundleException {
				bundle.start();
        bundle.stop();

    }

}
