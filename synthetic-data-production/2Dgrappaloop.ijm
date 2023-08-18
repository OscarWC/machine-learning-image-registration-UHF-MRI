basePath = "C:/Users/windo/Downloads/head_meshes (1)/2Dgrap/";
for (i = 1; i < 2; i++)
{
	a = basePath + "grappa/00" + i + "_rt_d.png";
	open(a);
	run("Translate...", "x=0 y=75 interpolation=None stack");
	run("Window/Level...");
	setMinAndMax(131, 379);
	run("Apply LUT", "stack");
	b = basePath + "grappa/00" + i + "_rt_u.png";
	open(b);
	run("Translate...", "x=0 y=-75 interpolation=None stack");
	run("Window/Level...");
	setMinAndMax(131, 379);
	run("Apply LUT", "stack");
	
	imageCalculator("Add create stack", "00" + i + "_rt_u.png","00" + i + "_rt_d.png");
	c = basePath + "grappa/00" + i + "_rt_n.png";
	open(c);
	
	imageCalculator("Add create stack", "Result of 00" + i + "_rt_u.png","00" + i + "_rt_n.png");
	run("Add Specified Noise...", "standard=30");
	
	d = basePath + "train/00" + i + "_rt.png";
	saveAs("PNG", d);
	close("\\Others");
	
	close();
	///run("Close");
}