basePath = "C:/Users/windo/Downloads/head_meshes (1)/2Dgrap/";
for (i = 1; i < 101; i++)
{
	mySavePath = basePath + "test/00" + i + "_augments.txt";
	
	a = (5)*random + (-5)*random;
	b = (5)*random + (-5)*random;
	c = (7)*random + (-7)*random;

	List.clear();

	List.set("y translation", a)
	List.set("x translation", b)
	List.set("rotation", c)

	m = List.getList;

	File.saveString(m, mySavePath);
	
	mySavePath1 = basePath + "grappa/00" + i + "_rt_n";
	mySavePath2 = basePath + "grappa/00" + i + "_rt_d";
	mySavePath3 = basePath + "grappa/00" + i + "_rt_u";
	
	open("C:/Users/windo/Downloads/head_meshes (1)/fixed_image0.png");
	
	run("Rotate... ", "angle=c grid=1 interpolation=Bilinear");
	run("Translate...", "x=a y=b interpolation=None stack");

	saveAs("PNG", mySavePath1);
	saveAs("PNG", mySavePath2);
	saveAs("PNG", mySavePath3);

	close("\\Others");

	close();
	}