OpenPath = "C:/Users/windo/Downloads/head_meshes (1)/GRAPPA/";
basePath = "C:/Users/windo/PycharmProjects/Registration1/folder2/";
for (i = 1; i < 1001; i++)
{
	a = OpenPath + "00" + i + "_rt_d.tif";
	open(a);
	run("Translate...", "x=0 y=75 interpolation=None stack");
	run("Window/Level...");
	setMinAndMax(131, 379);
	run("Apply LUT", "stack");
	b = OpenPath + "00" + i + "_rt_u.tif";
	open(b);
	run("Translate...", "x=0 y=-75 interpolation=None stack");
	run("Window/Level...");
	setMinAndMax(131, 379);
	run("Apply LUT", "stack");
	
	imageCalculator("Add create stack", "00" + i + "_rt_u.tif","00" + i + "_rt_d.tif");
	c = OpenPath + "00" + i + "_rt_n.tif";
	open(c);
	
	imageCalculator("Add create stack", "Result of 00" + i + "_rt_u.tif","00" + i + "_rt_n.tif");
	d = basePath + "00" + i + "_rt.tif";
	saveAs("Tiff", d);
	
	close("\\Others");
	
	close();
	///run("Close");
}